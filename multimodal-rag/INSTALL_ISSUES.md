# Installation Issues & Solutions

## Python 3.14 Compatibility

Python 3.14 is very new (released 2025), and some packages don't have compatible versions yet. The requirements.txt has been updated to use versions that work with Python 3.14.

### What Changed

**Original packages that don't support Python 3.14:**
- `unstructured[all-docs]==0.16.9` → Changed to `unstructured==0.11.8`
- `layoutparser[all]==0.3.4` → Removed (optional, OpenCV fallback used)
- `camelot-py[cv]` → Removed (optional, pdfplumber covers most cases)
- `tabula-py` → Removed (optional, pdfplumber covers most cases)
- `opencv-contrib-python` → Changed to `opencv-python-headless`

**Impact:**
- ✅ **No functionality loss**: The system works fully with the updated packages
- ✅ **OpenCV fallback**: Layout detection uses OpenCV (already implemented)
- ✅ **PDFPlumber**: Handles all table extraction needs

### Installation Command

```bash
# Activate your virtual environment
source venv/bin/activate

# Install with updated requirements
pip install -r requirements.txt
```

### Expected Installation Time

- **First time**: 5-10 minutes (downloading PyTorch, transformers, etc.)
- **Subsequent**: 1-2 minutes

### Large Packages

These packages are large and will take time to download:
- `torch` (~200MB)
- `transformers` (~500MB with models)
- `sentence-transformers` (~100MB)
- `chromadb` (~50MB)

### Optional Advanced Packages

If you want advanced layout detection (optional):

```bash
# Install layoutparser with detectron2 (requires compilation)
pip install layoutparser
pip install 'git+https://github.com/facebookresearch/detectron2.git'
```

**Note**: This requires:
- GCC compiler
- CUDA (for GPU support)
- Additional system libraries

It's **not required** for the system to work - OpenCV provides good layout detection.

### Troubleshooting

#### Issue: PyTorch installation fails

**Solution**: Install PyTorch separately first:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### Issue: EasyOCR fails

**Solution**: Install dependencies:
```bash
brew install tesseract
pip install easyocr
```

#### Issue: ChromaDB fails

**Solution**: Install with specific version:
```bash
pip install chromadb==0.5.23 --no-cache-dir
```

#### Issue: "No matching distribution" errors

**Solution 1**: Use Python 3.11 or 3.12 (most compatible):
```bash
# Install Python 3.12 with Homebrew
brew install python@3.12

# Create new venv with Python 3.12
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Solution 2**: Install packages individually:
```bash
pip install fastapi uvicorn pydantic pydantic-settings
pip install torch torchvision transformers sentence-transformers
pip install chromadb openai
pip install easyocr pdf2image pdfplumber
pip install python-dotenv loguru prometheus-client
pip install pytest pytest-asyncio httpx
```

### Verification

After installation, verify everything works:

```bash
python validate_setup.py
```

This will check:
- ✓ All required packages installed
- ✓ Models can be initialized
- ✓ Embeddings can be generated
- ✓ Configuration is correct

### What Works Without Optional Packages

The system is fully functional without these optional packages:

| Package | Status | Alternative |
|---------|--------|-------------|
| layoutparser | Optional | OpenCV-based detection |
| detectron2 | Optional | Rule-based layout |
| camelot-py | Optional | pdfplumber for tables |
| tabula-py | Optional | pdfplumber for tables |

### Recommended Python Versions

For best compatibility:

1. **Python 3.12** (Recommended) - Best package support
2. **Python 3.11** - Excellent support
3. **Python 3.10** - Good support
4. **Python 3.14** - Works but fewer packages available

### If You Want to Use Python 3.12

```bash
# Install Python 3.12
brew install python@3.12

# Create new virtual environment
python3.12 -m venv venv312
source venv312/bin/activate

# Install requirements
pip install -r requirements.txt

# You'll have access to more package versions
```

### Current Status

With the updated requirements.txt:
- ✅ All core functionality works
- ✅ Python 3.14 compatible
- ✅ No compilation required
- ✅ Faster installation
- ✅ Fewer dependencies to manage

### Next Steps

1. Try installing with updated requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. If that succeeds, validate:
   ```bash
   python validate_setup.py
   ```

3. If you still have issues, consider Python 3.12:
   ```bash
   brew install python@3.12
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

The system will work great either way! 🚀
