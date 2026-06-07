# 🅿️ Smart Parking System with Python

A modern, full-featured web-based parking management system built with Python and Flask.


## ✨ Features

- **Large Capacity**: 8 floors with 50 parking spots each (Total 400 spots)
- **Modern Web Interface**: Beautiful dark theme with full RTL (Persian) support
- **Interactive Parking Map**: Real-time visual grid showing occupied and free spots
- **Smart Entry/Exit**: Automatic cost calculation when vehicles exit
- **Vehicle Management**: Store car details (plate number, model, phone number)
- **Live Dashboard**: Real-time statistics (free spots, occupied, total)
- **Persistent Storage**: Data saved in local files (`car.dat`, `parking_session.dat`)
- **Professional Logging**: All operations logged in `loglist.log`

## 🛠️ Technologies

- **Backend**: Python + Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vazirmatn + Bebas Neue fonts)
- **Architecture**: MVC (Model-View-Controller)
- **Data Storage**: File-based (Pickle serialization)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mahdiyazdi83/Parking-system-with-python.git
   cd Parking-system-with-python

Install dependencies:Bashpip install flask
Run the application:Bashpython app.py
[Open your browser and go to:texthttp://127.0.0.1:5000](http://127.0.0.1:5000)

📁 Project Structure
Parking-system-with-python/
├── app.py                    # Main Flask application
├── controller/               # Business logic controllers
├── model/                    # Data models (Car, ParkingSpot, ...)
├── templates/                # HTML templates
├── tools/                    # Helper utilities
├── car.dat                   # Vehicle database
├── parking_session.dat       # Active parking sessions
└── loglist.log               # Application logs
🎯 How to Use

Park a Vehicle: Enter plate number, car model, phone number, and select a spot
Exit Vehicle: Enter plate number → cost is calculated automatically
Live Map: Visually monitor all parking spots in real-time

📌 Notes

This project is under active development
Data is stored locally in files (not suitable for production environments yet)
Fully responsive and optimized for desktop use

👨‍💻 Author
Mahdi Yazdi
Published: June 2026

⭐ If you found this project useful, please give it a star!
