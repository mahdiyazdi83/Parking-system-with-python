#!/bin/bash

# Update pip
python3 -m pip install --upgrade pip

# Web framework
pip3 install flask

# Computer vision and OCR
pip3 install opencv-python
pip3 install easyocr

# PyTorch runtime
pip3 install torch
pip3 install torchvision

# Persian plate validation helpers
pip3 install persian-tools

echo "All packages installed successfully!"
