# PPTX Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/sageframe-no-kaji/pptx-builder/actions/workflows/test.yml/badge.svg)](https://github.com/sageframe-no-kaji/pptx-builder/actions/workflows/test.yml)

Convert PDFs and images to PowerPoint presentations. Each page or image becomes a slide at configurable DPI.

## Installation

### Docker (Web UI)

```bash
git clone https://github.com/sageframe-no-kaji/pptx-builder.git
cd pptx-builder
docker compose up -d
```

Access web interface at http://localhost:7860

See [DOCKER.md](DOCKER.md) for details.

### Python CLI

```bash
git clone https://github.com/sageframe-no-kaji/pptx-builder.git
cd pptx-builder
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**System dependencies:**
- Python 3.8+
- `poppler-utils` (for PDF conversion)
  - Debian/Ubuntu: `apt install poppler-utils`
  - macOS: `brew install poppler`

## Usage

### Web UI

```bash
docker compose up -d
# Open http://localhost:7860
```

Upload files, select options, download presentation.

### Command Line

**Interactive mode:**
```bash
python make_ppt.py
```

**CLI examples:**
```bash
# Convert PDF
python make_ppt.py -i document.pdf

# Custom output name
python make_ppt.py -i document.pdf -o slides.pptx

# Higher DPI (slower, sharper)
python make_ppt.py -i document.pdf --dpi 600

# Process folder of images
python make_ppt.py -i photos/

# Batch process
python make_ppt.py -i file1.pdf file2.pdf --quiet --force

# Process folder recursively
python make_ppt.py -i images/ --recursive
```

**Common options:**
- `-i, --input PATH` - Input file(s) or folder
- `-o, --output NAME` - Output filename (single input only)
- `--dpi DPI` - PDF rendering quality (default: 300)
- `-r, --recursive` - Process subfolders
- `--quiet` - No prompts
- `--force` - Overwrite existing files
- `-h, --help` - Show all options

## Features

**Supported formats:**
- PDF (multi-page supported)
- Images: PNG, JPG, JPEG, TIFF, WebP, BMP, GIF, ICO, HEIC, HEIF

**Slide sizes:**
- 16:9 Widescreen (13.33" × 7.5") - default
- 4:3 Standard (10" × 7.5")
- Letter (11" × 8.5")
- A4 (11.69" × 8.27")
- Legal (14" × 8.5")
- Tabloid (17" × 11")

**Image placement:**
- **Fit** - No cropping, entire image visible (default)
- **Fill** - No whitespace, may crop edges

**Output:**
- One slide per image/page
- Images sorted alphabetically
- Centered, never stretched
- Compatible with PowerPoint, LibreOffice, Google Slides

## Documentation

**Man page:**
```bash
man docs/make_ppt.1
```

**Additional documentation:**
- [DOCKER.md](DOCKER.md) - Docker deployment
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- [docs/GRADIO_TUTORIAL.md](docs/GRADIO_TUTORIAL.md) - Web UI technical guide
- [docs/MAN_PAGE_USAGE.md](docs/MAN_PAGE_USAGE.md) - Man page instructions

## Development

**Run tests:**
```bash
pip install -r requirements-dev.txt
pytest
pytest --cov=make_ppt --cov-report=html
```

**Code quality:**
```bash
black make_ppt.py test_make_ppt.py  # Format
flake8 make_ppt.py                   # Lint
mypy make_ppt.py                     # Type check
```

**Pre-commit hooks:**
```bash
pre-commit install
pre-commit run --all-files
```

## Notes

- PDF rendering: 150-300 DPI recommended (600 DPI is slow)
- Large PDFs (30+ pages) at 300 DPI may take 30-60 seconds
- Temporary files cleaned up automatically
- HEIC/HEIF require `pillow-heif` package (included)

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

Issues and pull requests welcome at https://github.com/sageframe-no-kaji/pptx-builder
