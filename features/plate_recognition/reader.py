import re
from functools import lru_cache

import cv2
import numpy as np


VALID_PLATE_LETTERS = [
    "\u0628", "\u062c", "\u062f", "\u0633", "\u0635", "\u0637", "\u0642",
    "\u0644", "\u0645", "\u0646", "\u0648", "\u0647", "\u06cc", "\u0627\u0644\u0641",
    "\u067e", "\u062a", "\u062b", "\u062d", "\u062e", "\u0630", "\u0631",
    "\u0632", "\u0698", "\u0634", "\u0636", "\u0639", "\u063a", "\u0641",
    "\u06a9",
]

PERSIAN_DIGITS = "\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9"
ARABIC_DIGITS = "\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669"
ENGLISH_DIGITS = "0123456789"
DIGIT_ALLOWLIST = ENGLISH_DIGITS + PERSIAN_DIGITS + ARABIC_DIGITS
LETTER_ALLOWLIST = "".join(VALID_PLATE_LETTERS)


@lru_cache(maxsize=1)
def get_reader():
    import easyocr

    return easyocr.Reader(["fa", "en"], gpu=False)


def read_plate_from_upload(file_storage, max_candidates=6, zone_candidates=6):
    file_bytes = file_storage.read()
    image_array = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return {
            "success": False,
            "message": "Could not read image",
            "needs_manual_review": True,
        }

    return read_plate_from_image(image, max_candidates=max_candidates, zone_candidates=zone_candidates)


def read_plate_from_image(image, max_candidates=6, zone_candidates=6):
    reader = get_reader()
    candidates = find_plate_candidates(image, max_candidates=max_candidates)

    best = None
    best_invalid = None

    for index, candidate in enumerate(candidates, start=1):
        crop = candidate["padded_crop"]
        variant_ocr = {}

        for variant_name, variant_image in build_ocr_variants(crop).items():
            variant_ocr[variant_name] = read_with_easyocr(reader, variant_image)

        if index <= zone_candidates:
            zoned_ocr = read_zoned_plate(reader, crop)
            zoned_ocr["hybrid"] = build_hybrid_plate(zoned_ocr, variant_ocr)

            hybrid = zoned_ocr["hybrid"]
            if hybrid["success"]:
                candidate_best = {
                    "candidate": index,
                    "source": "hybrid_zoned_ocr",
                    "confidence": hybrid["confidence"],
                    "plate": hybrid["plate"],
                    "parts": hybrid["parts"],
                    "inferred": hybrid["inferred"],
                }
                if best is None or candidate_best["confidence"] > best["confidence"]:
                    best = candidate_best

        for group_name, group_items in variant_ocr.items():
            for item in group_items:
                if best_invalid is None or item["confidence"] > best_invalid["confidence"]:
                    best_invalid = {
                        "candidate": index,
                        "source": group_name,
                        "raw_text": item["raw_text"],
                        "normalized_text": item["normalized_text"],
                        "confidence": item["confidence"],
                        "failure": item["failure"],
                    }

                if item["extracted"]:
                    candidate_best = {
                        "candidate": index,
                        "source": group_name,
                        "raw_text": item["raw_text"],
                        "normalized_text": item["normalized_text"],
                        "confidence": item["confidence"],
                        "plate": item["extracted"]["plate"],
                        "parts": item["extracted"]["parts"],
                        "inferred": {},
                    }
                    if best is None or candidate_best["confidence"] > best["confidence"]:
                        best = candidate_best

    if not best:
        return {
            "success": False,
            "message": "Plate was not detected",
            "best_invalid": best_invalid,
            "needs_manual_review": True,
        }

    return {
        "success": True,
        "plate": best["plate"],
        "parts": best["parts"],
        "confidence": best["confidence"],
        "source": best["source"],
        "inferred": best["inferred"],
        "needs_manual_review": bool(best["inferred"]) or best["confidence"] < 0.85,
    }


def convert_digits_to_english(text):
    for fa, en in zip(PERSIAN_DIGITS, ENGLISH_DIGITS):
        text = text.replace(fa, en)

    for ar, en in zip(ARABIC_DIGITS, ENGLISH_DIGITS):
        text = text.replace(ar, en)

    return text


def normalize_ocr_text(text):
    text = convert_digits_to_english(text)
    text = text.replace(" ", "")
    text = text.replace("-", "")
    text = text.replace("_", "")
    text = text.replace(".", "")
    text = text.replace("I", "1")
    text = text.replace("l", "1")
    text = text.replace("O", "0")
    text = text.replace("o", "0")
    text = text.replace("\u0643", "\u06a9")
    text = text.replace("\u064a", "\u06cc")
    return text


def extract_plate(text):
    cleaned = normalize_ocr_text(text)

    for letter in VALID_PLATE_LETTERS:
        pattern = rf"(\d{{2}}){re.escape(letter)}(\d{{3}})(\d{{2}})"
        match = re.search(pattern, cleaned)

        if match:
            p1, p3, p4 = match.groups()
            return {
                "plate": f"{p1}{letter}{p3}{p4}",
                "parts": {"p1": p1, "p2": letter, "p3": p3, "p4": p4},
            }

    return None


def extract_ocr_order_plate(text):
    cleaned = normalize_ocr_text(text)

    for letter in VALID_PLATE_LETTERS:
        pattern = rf"(\d{{3,5}}){re.escape(letter)}(\d{{2}})"
        match = re.search(pattern, cleaned)

        if match:
            before_letter, after_letter = match.groups()
            return {
                "parts": {
                    "p1": after_letter,
                    "p2": letter,
                    "p3": before_letter[:3],
                    "p4": before_letter[3:5],
                },
                "normalized_text": cleaned,
            }

    return None


def explain_plate_failure(text):
    cleaned = normalize_ocr_text(text)
    digits = re.findall(r"\d", cleaned)
    letters = [letter for letter in VALID_PLATE_LETTERS if letter in cleaned]

    if not cleaned:
        reason = "empty OCR output"
    elif not letters:
        reason = "no valid Persian plate letter found"
    elif len(digits) < 7:
        reason = f"not enough digits: expected 7, got {len(digits)}"
    elif len(digits) > 7:
        reason = f"too many digits: expected 7, got {len(digits)}"
    else:
        reason = "digits and letter found, but order does not match plate format"

    return {
        "normalized_text": cleaned,
        "digits": "".join(digits),
        "letters": letters,
        "reason": reason,
    }


def preprocess_for_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    edges = cv2.Canny(blur, 30, 200)
    return edges


def build_ocr_variants(crop):
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    scaled = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    denoised = cv2.bilateralFilter(scaled, 9, 75, 75)

    adaptive = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )

    _, otsu = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(scaled)

    return {
        "raw": crop,
        "gray_scaled": scaled,
        "denoised": denoised,
        "adaptive": adaptive,
        "otsu": otsu,
        "contrast": contrast,
    }


def build_zone_variants(zone):
    if len(zone.shape) == 3:
        gray = cv2.cvtColor(zone, cv2.COLOR_BGR2GRAY)
    else:
        gray = zone

    scaled = cv2.resize(gray, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(scaled)

    adaptive = cv2.adaptiveThreshold(
        contrast,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        9,
    )

    return {"scaled": scaled, "contrast": contrast, "adaptive": adaptive}


def crop_with_padding(image, x, y, w, h):
    padding_x = int(w * 0.18)
    padding_y = int(h * 0.40)

    x1 = max(x - padding_x, 0)
    y1 = max(y - padding_y, 0)
    x2 = min(x + w + padding_x, image.shape[1])
    y2 = min(y + h + padding_y, image.shape[0])

    return {"crop": image[y1:y2, x1:x2]}


def find_plate_candidates(image, max_candidates=6):
    edges = preprocess_for_edges(image)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image_area = image.shape[0] * image.shape[1]
    candidates = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if h == 0:
            continue

        ratio = w / h
        area = w * h
        area_ratio = area / image_area

        if 2.0 <= ratio <= 6.5 and area_ratio >= 0.001 and w >= 80 and h >= 20:
            padded = crop_with_padding(image, x, y, w, h)
            candidates.append({
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "ratio": ratio,
                "area": area,
                "padded_crop": padded["crop"],
            })

    candidates = sorted(candidates, key=lambda item: item["area"], reverse=True)
    return candidates[:max_candidates]


def estimate_plate_body_start(crop):
    height, width = crop.shape[:2]

    if len(crop.shape) != 3:
        return int(width * 0.18)

    search_width = max(int(width * 0.40), 1)
    left_area = crop[:, :search_width]
    blue = left_area[:, :, 0].astype("int16")
    green = left_area[:, :, 1].astype("int16")
    red = left_area[:, :, 2].astype("int16")

    blue_mask = (blue > red + 25) & (blue > green + 10) & (blue > 80)
    column_scores = blue_mask.mean(axis=0)
    blue_columns = [index for index, score in enumerate(column_scores) if score > 0.18]

    if not blue_columns:
        return int(width * 0.18)

    strip_end = max(blue_columns)
    return min(strip_end + int(width * 0.04), int(width * 0.35))


def split_plate_zones(crop):
    height, width = crop.shape[:2]
    body_x1 = estimate_plate_body_start(crop)
    body_x2 = int(width * 0.97)
    y1 = int(height * 0.10)
    y2 = int(height * 0.90)
    body_width = body_x2 - body_x1

    zones = {
        "p1": (0.00, 0.25),
        "p2": (0.25, 0.43),
        "p3": (0.43, 0.80),
        "p4": (0.84, 1.00),
    }

    output = {}
    for name, (start, end) in zones.items():
        x1 = body_x1 + int(body_width * start)
        x2 = body_x1 + int(body_width * end)
        output[name] = crop[y1:y2, x1:x2]

    return output


def read_easyocr_items(reader, image, allowlist=None):
    kwargs = {}

    if allowlist:
        kwargs["allowlist"] = allowlist

    return reader.readtext(image, **kwargs)


def read_with_easyocr(reader, image):
    output = []

    for box, text, confidence in read_easyocr_items(reader, image):
        extracted = extract_plate(text)
        output.append({
            "raw_text": text,
            "normalized_text": normalize_ocr_text(text),
            "confidence": float(confidence),
            "extracted": extracted,
            "failure": None if extracted else explain_plate_failure(text),
        })

    return output


def read_digit_zone(reader, zone, expected_length):
    best = None
    all_results = []

    for variant_name, variant_image in build_zone_variants(zone).items():
        results = read_easyocr_items(reader, variant_image, allowlist=DIGIT_ALLOWLIST)

        for box, text, confidence in results:
            normalized = normalize_ocr_text(text)
            digits = "".join(re.findall(r"\d", normalized))
            item = {
                "variant": variant_name,
                "raw_text": text,
                "normalized_text": normalized,
                "digits": digits,
                "confidence": float(confidence),
                "valid": len(digits) == expected_length,
            }
            all_results.append(item)

            if item["valid"] and (best is None or item["confidence"] > best["confidence"]):
                best = item

    if best is None and all_results:
        best = max(all_results, key=lambda item: item["confidence"])

    return {"best": best, "all": all_results}


def read_letter_zone(reader, zone):
    best = None
    all_results = []

    for variant_name, variant_image in build_zone_variants(zone).items():
        results = read_easyocr_items(reader, variant_image, allowlist=LETTER_ALLOWLIST)

        for box, text, confidence in results:
            normalized = normalize_ocr_text(text)
            letters = [letter for letter in VALID_PLATE_LETTERS if letter in normalized]
            letter = letters[0] if letters else ""
            item = {
                "variant": variant_name,
                "raw_text": text,
                "normalized_text": normalized,
                "letter": letter,
                "confidence": float(confidence),
                "valid": bool(letter),
            }
            all_results.append(item)

            if item["valid"] and (best is None or item["confidence"] > best["confidence"]):
                best = item

    if best is None and all_results:
        best = max(all_results, key=lambda item: item["confidence"])

    return {"best": best, "all": all_results}


def read_zoned_plate(reader, crop):
    zones = split_plate_zones(crop)
    p1 = read_digit_zone(reader, zones["p1"], expected_length=2)
    p2 = read_letter_zone(reader, zones["p2"])
    p3 = read_digit_zone(reader, zones["p3"], expected_length=3)
    p4 = read_digit_zone(reader, zones["p4"], expected_length=2)

    parts = {
        "p1": p1["best"]["digits"] if p1["best"] else "",
        "p2": p2["best"]["letter"] if p2["best"] else "",
        "p3": p3["best"]["digits"] if p3["best"] else "",
        "p4": p4["best"]["digits"] if p4["best"] else "",
    }

    valid = (
        len(parts["p1"]) == 2 and
        bool(parts["p2"]) and
        len(parts["p3"]) == 3 and
        len(parts["p4"]) == 2
    )

    confidence_values = [
        result["best"]["confidence"]
        for result in [p1, p2, p3, p4]
        if result["best"]
    ]
    confidence = sum(confidence_values) / len(confidence_values) if confidence_values else 0.0

    return {
        "success": valid,
        "plate": f"{parts['p1']}{parts['p2']}{parts['p3']}{parts['p4']}" if valid else None,
        "parts": parts,
        "confidence": confidence,
        "zones": {"p1": p1, "p2": p2, "p3": p3, "p4": p4},
    }


def build_hybrid_plate(zoned_ocr, variant_ocr):
    parts = dict(zoned_ocr["parts"])
    best_source = None
    best_confidence = 0.0

    for group_name, group_items in variant_ocr.items():
        for item in group_items:
            extracted = extract_ocr_order_plate(item["raw_text"])

            if not extracted:
                continue

            confidence = item["confidence"]
            if confidence < best_confidence:
                continue

            candidate_parts = dict(parts)

            for key, value in extracted["parts"].items():
                if value:
                    candidate_parts[key] = value

            parts = candidate_parts
            best_source = {
                "source": group_name,
                "raw_text": item["raw_text"],
                "normalized_text": item["normalized_text"],
                "confidence": confidence,
            }
            best_confidence = confidence

    valid = (
        len(parts["p1"]) == 2 and
        bool(parts["p2"]) and
        len(parts["p3"]) == 3 and
        len(parts["p4"]) == 2
    )

    inferred = {}

    if (
        not valid and
        len(parts["p1"]) == 2 and
        bool(parts["p2"]) and
        len(parts["p3"]) == 3 and
        len(parts["p4"]) == 1
    ):
        parts["p4"] = parts["p4"] * 2
        inferred["p4"] = "duplicated single province digit"
        valid = True

    return {
        "success": valid,
        "plate": f"{parts['p1']}{parts['p2']}{parts['p3']}{parts['p4']}" if valid else None,
        "parts": parts,
        "confidence": max(zoned_ocr["confidence"], best_confidence),
        "source": best_source,
        "inferred": inferred,
    }
