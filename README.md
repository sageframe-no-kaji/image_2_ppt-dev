# PPTX Builder — Images & PDFs → PowerPoint (300 DPI)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A single-purpose command-line tool that takes **either** a folder of images **or** a PDF file, then builds a `.pptx` with one slide per page/image at 300 DPI. No PowerPoint app is needed to create presentations — only to open the result.

## 📥 Installation

### From GitHub

```bash
git clone https://github.com/sageframe-no-kaji/pptx-builder.git
cd pptx-builder
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ✅ Features

### 🔹 Input Options
- **PDF file**
  → Automatically converted to PNGs at **300 DPI** (via PyMuPDF)
- **Folder of images**
  → Non-image files are ignored

### 🔹 Supported Image Formats
.png · .jpg · .jpeg · .tif · .tiff
.webp · .bmp · .gif · .ico · .heic · .heif
(Animated GIFs use only the first frame.)

### 🔹 Slide Size Presets
You can choose at runtime:
1. 16:9 (13.33" × 7.5")
2. 4:3 (10" × 7.5")
3. Letter (11" × 8.5")
4. A4 (11.69" × 8.27")
5. Legal (14" × 8.5")
6. Tabloid (17" × 11")

### 🔹 Image Placement Modes
Choose one per run:
1. **Fit whole image**
   - No cropping
   - No stretching
   - Letterboxing/pillarboxing if needed
2. **Crop to fill**
   - Full coverage
   - Proportional scaling
   - Edges may be trimmed

### 🔹 Output
- One slide per image or PDF page
- Images are centered and never stretched
- Sorted alphabetically (case-insensitive)
- Exports `.pptx` to your chosen location
- Temporary PNGs from PDF conversion are auto-deleted

---

## ✅ Requirements

**Python 3.8 or higher**

Create and activate a virtual environment (recommended), then install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Dependencies:**
- `python-pptx` — PowerPoint file creation
- `Pillow` — Image processing
- `PyMuPDF` — PDF rendering
- `pdf2image` — PDF to image conversion
- `pillow-heif` — HEIC/HEIF support

---

## ✅ Usage
### Interactive Mode

Run the script without arguments for interactive prompts:

```bash
```
python3 make_ppt.py
```

You’ll be prompted for:
1. Path to a PDF or a folder with images
2. Output filename
3. Slide size
4. Placement mode (fit or fill)

When finished, you’ll see something like:

```
### CLI Mode

For batch processing or automation:

```bash
**Interactive:**
```bash
python3 make_ppt.py
Enter a path to a PDF file or a folder of images: /Users/me/Desktop/images
Enter output filename (without extension) [slides]: MyDeck
Choose slide size:
  1) 16:9 (13.33" x 7.5")
  2) 4:3  (10" x 7.5")
  3) Letter  (11" x 8.5")
  4) A4      (11.69" x 8.27")
  5) Legal   (14" x 8.5")
  6) Tabloid (17" x 11")
# Process folder recursively
python3 make_ppt.py -i images/ --recursive

# High DPI conversion
python3 make_ppt.py -i document.pdf --dpi 600
 (configurable via `--dpi`)
- HEIC/HEIF support provided by `pillow-heif`
- Non-image files in folders are silently ignored
- No stretching — images are always scaled proportionally
- Temporary PDF conversions are cleaned up automatically
- `Ctrl+C` exits cleanly

---

## 📦 Packaging (Optional)

Create a standalone binary (Mac/Linux/Windows) with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile make_ppt.py
```

Output will appear in the `dist/` folder.

---

## � Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=make_ppt --cov-report=html

# Run only unit tests (skip integration)
pytest -m "not integration"
```

### Code Quality

```bash
# Format code with Black
black make_ppt.py test_make_ppt.py

# Lint with flake8
flake8 make_ppt.py

# Type check with mypy
mypy make_ppt.py

# Or use pre-commit hooks (auto-formats on commit)
pre-commit install
pre-commit run --all-files
```

---

## �🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

- **Issues:** https://github.com/sageframe-no-kaji/pptx-builder/issues
- **Pull Requests:** https://github.com/sageframe-no-kaji/pptx-builder/pulls

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💡 Why This Tool?

There is **no existing free or open-source tool** that:
- Converts PDF → editable PPTX (page-per-slide, high DPI)
- Handles folders of mixed-format images (including HEIC, TIFF, WebP)
- Lets users pick slide size & scaling mode
- Works offline without requiring PowerPoint or Acrobat
- Supports both interactive and CLI batch modes
```
python3 make_ppt.py
Enter a path to a PDF file or a folder of images: /Users/me/Desktop/images
Enter output filename (without extension) [slides]: MyDeck
Choose slide size:
  1) 16:9 ...
Enter number (1-6): 1
How should images be placed?
  1) Fit whole image ...
  2) Crop to fill ...
Enter 1 or 2: 1
✅ Presentation saved to: /Users/me/Desktop/images/MyDeck.pptx
```

---

## ✅ Notes
- PDFs are rasterized at 300 DPI using PyMuPDF
- HEIC/HEIF support provided by `pillow-heif`
- Non-image files in folders are silently ignored
- No stretching — images are always scaled proportionally
- Temporary PDF conversions are cleaned up automatically
- `Ctrl+C` exits cleanly

---

## ✅ Packaging (Optional)
Create a standalone binary (Mac/Linux/Windows) with:

```
pyinstaller --onefile make_ppt.py
```

Output will appear in the `dist/` folder.

---

## ✅ Summary
Use this script when you want fast, clean conversion of images or PDFs into PPTX slides — with correct sizing, scaling, and zero manual setup. Just run it, follow prompts, and you're done.
