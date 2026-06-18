# Smart Parking System with Python

A web-based parking management system built with Python and Flask. It provides an
RTL Persian dashboard for parking cars, exiting cars, viewing live parking spot
status, and optionally filling the plate fields from a car image using local OCR.

## Features

- Large capacity parking map: 8 floors with 50 parking spots each
- RTL Persian web interface
- Interactive live parking spot grid
- Vehicle entry and exit workflow
- Automatic parking cost calculation on exit
- Local file-based storage with `car.dat` and `parking_session.dat`
- Operation logs in `loglist.log`
- Optional plate OCR helper using OpenCV and EasyOCR

## Plate OCR Helper

The OCR feature is intentionally designed as a manual-review helper:

1. The user uploads a car image from the plate input area.
2. The backend analyzes the image locally with OpenCV and EasyOCR.
3. The detected plate parts are inserted into the UI fields.
4. The user reviews/corrects the fields manually.
5. The user clicks the normal park button.

The OCR endpoint does not save cars, park cars, or modify data files directly.
It only returns detected plate text to the frontend.

## Technologies

- Python
- Flask
- HTML, CSS, JavaScript
- OpenCV
- EasyOCR
- PyTorch
- File-based persistence

## Installation

### Windows

Run:

```bat
install.bat
```

### Linux/macOS

Run:

```bash
chmod +x install.sh
./install.sh
```

The installer scripts install the required Python packages one by one.

## Running The App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## GPU Notes

The OCR module currently loads EasyOCR in CPU mode for compatibility:

```python
easyocr.Reader(["fa", "en"], gpu=False)
```

To use GPU, install a CUDA-enabled PyTorch build, then change `gpu=False` to
`gpu=True` in `features/plate_recognition/reader.py`.

You can check CUDA availability with:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

## Project Structure

```text
Parking-system-with-python/
├── app.py
├── controller/
├── features/
│   └── plate_recognition/
├── model/
├── templates/
├── tools/
├── install.bat
├── install.sh
├── car.dat
├── parking_session.dat
└── loglist.log
```

## Usage

- Park a vehicle: enter plate, model, mobile number, floor, and parking spot.
- Read plate from image: click the upload icon beside the plate field, then
  review the detected result before submitting.
- Exit a vehicle: choose an active car and calculate the exit cost.
- Monitor spots: use the live parking grid to see occupied and free locations.

## Notes

- This project is for learning and demonstration.
- Data is stored locally in files, so it is not production-grade storage.
- OCR accuracy depends on image quality, plate angle, lighting, and crop quality.

## Author

Mahdi Yazdi

Published: June 2026
