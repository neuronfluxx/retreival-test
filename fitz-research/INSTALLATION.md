# Installation Guide for PaddleOCR

## Issue: Python 3.14 Compatibility

PaddlePaddle doesn't have pre-built wheels for Python 3.14 yet. Here are your options:

## Option 1: Install PaddleOCR (Recommended - Easiest)

PaddleOCR can work without PaddlePaddle installed, using a lighter backend:

```bash
# Install just PaddleOCR (will use ONNX backend automatically)
pip install paddleocr

# Install other dependencies
pip install -r requirements.txt
```

PaddleOCR will automatically download and use the ONNX runtime instead of PaddlePaddle.

## Option 2: Use Python 3.11 or 3.12 (Most Compatible)

The most reliable option is to use a compatible Python version:

```bash
# Create a new virtual environment with Python 3.11 or 3.12
python3.11 -m venv venv311
source venv311/bin/activate

# Install dependencies
pip install paddlepaddle paddleocr PyMuPDF Pillow
```

If you don't have Python 3.11/3.12 installed:

```bash
# Using Homebrew
brew install python@3.11

# Or download from python.org
# https://www.python.org/downloads/
```

## Option 3: Install PaddlePaddle from Source (Advanced)

If you need the full PaddlePaddle functionality:

```bash
# Clone PaddlePaddle repository
git clone https://github.com/PaddlePaddle/Paddle.git
cd Paddle

# Build from source (takes time)
pip install -r python/requirements.txt
python setup.py install
```

## Option 4: Try Alternative OCR - Tesseract + pytesseract

If PaddleOCR installation is problematic, I can create an alternative script using Tesseract:

```bash
# Install Tesseract on macOS
brew install tesseract

# Install Python wrapper
pip install pytesseract PyMuPDF Pillow
```

## Recommended Installation Steps (Try in Order)

### Step 1: Try direct PaddleOCR installation
```bash
pip install paddleocr
```

### Step 2: If that works, install other dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Test the installation
```bash
python3 -c "from paddleocr import PaddleOCR; print('PaddleOCR installed successfully!')"
```

## Verification

After installation, verify it works:

```bash
python3 extract_text_paddle_ocr.py --help
```

If you see the help message, you're ready to go!

## Still Having Issues?

Let me know which option you prefer, or if you'd like me to:
1. Create a Tesseract-based alternative script
2. Create a Docker setup for consistent environment
3. Modify the script to work with a different OCR engine
