# Smart Parking System with Python 🚗

A Flask-based parking management system with a Persian RTL dashboard. The app
manages parking entries, exits, live spot status, local data storage, and includes
an optional image-based plate OCR helper.

## ✨ Main Features

- 400 parking spots: 8 floors × 50 spots
- Persian RTL web dashboard
- Interactive live parking map
- Vehicle entry and exit workflow
- Automatic cost calculation when a car exits
- Local file storage with `car.dat` and `parking_session.dat`
- Operation logging in `loglist.log`
- Optional plate OCR helper powered by OpenCV + EasyOCR

## 🔎 Plate OCR Helper

The OCR feature is a helper, not an automatic final decision maker.

Flow:

1. User clicks the upload icon beside the plate field.
2. User selects a car image.
3. Flask sends the image to the local OCR module.
4. OpenCV finds plate-like areas.
5. EasyOCR reads the possible plate text.
6. The UI fills the plate fields.
7. User reviews and edits the plate if needed.
8. User manually clicks the normal park button.

This keeps the workflow safer: OCR speeds up typing, but the user still confirms
the final plate before saving anything.

## 🧪 Test Images

Sample car images are included in:

```text
image_for_test/
```

These images are useful for testing the OCR behavior with different angles,
lighting, and plate visibility. OCR accuracy depends heavily on image quality,
so manual review is still expected.

## 🛠️ Technologies

- Python
- Flask
- HTML, CSS, JavaScript
- OpenCV
- EasyOCR
- PyTorch
- File-based persistence

## 🚀 Installation

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

The install scripts upgrade pip and install the required packages one by one.

## ▶️ Run The App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## ⚡ GPU Note

By default, OCR runs in CPU mode for compatibility:

```python
easyocr.Reader(["fa", "en"], gpu=False)
```

To use GPU, install a CUDA-enabled PyTorch build, then change `gpu=False` to
`gpu=True` in:

```text
features/plate_recognition/reader.py
```

Quick CUDA check:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

## 📁 Project Structure

```text
Parking-system-with-python/
├── app.py
├── controller/
├── features/
│   └── plate_recognition/
├── image_for_test/
├── model/
├── templates/
├── tools/
├── install.bat
├── install.sh
├── car.dat
├── parking_session.dat
└── loglist.log
```

## 🎯 How To Use

- Park a car: enter plate, car model, mobile number, floor, and spot.
- Read plate from image: upload a car image, review the detected plate, then save.
- Exit a car: choose an active vehicle and calculate the parking cost.
- Monitor parking: use the live grid to see free and occupied spots.

## 📌 Notes

- This project is built for learning and demonstration.
- Data is stored locally in files, not in a production database.
- The OCR result should always be checked by the user before parking.
- The included images are test cases, not production training data.

## Author

Mahdi Yazdi  
Published: June 2026
