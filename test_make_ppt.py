"""
Tests for make_ppt.py

Run with: pytest test_make_ppt.py
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from make_ppt import (
    list_images,
    detect_input_type,
    ALLOWED_EXTS,
    SLIDE_SIZES
)


class TestImageListing:
    """Test image file detection and listing"""

    def test_list_images_filters_correctly(self, tmp_path):
        """Should only return supported image formats"""
        # Create test files
        (tmp_path / "image.png").touch()
        (tmp_path / "photo.jpg").touch()
        (tmp_path / "document.txt").touch()  # Should be ignored
        (tmp_path / "data.json").touch()  # Should be ignored

        images = list_images(tmp_path)

        assert len(images) == 2
        assert all(img.suffix.lower() in ALLOWED_EXTS for img in images)

    def test_list_images_case_insensitive(self, tmp_path):
        """Should handle uppercase extensions"""
        (tmp_path / "IMAGE.PNG").touch()
        (tmp_path / "PHOTO.JPG").touch()

        images = list_images(tmp_path)

        assert len(images) == 2

    def test_list_images_sorted_alphabetically(self, tmp_path):
        """Should sort filenames case-insensitively"""
        (tmp_path / "zebra.png").touch()
        (tmp_path / "Apple.jpg").touch()
        (tmp_path / "banana.png").touch()

        images = list_images(tmp_path)

        names = [img.name.lower() for img in images]
        assert names == sorted(names)


class TestInputDetection:
    """Test input type detection (PDF vs folder vs unknown)"""

    def test_detect_pdf(self, tmp_path):
        """Should detect PDF files"""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.touch()

        assert detect_input_type(pdf_file) == "pdf"

    def test_detect_folder_with_images(self, tmp_path):
        """Should detect folder with images"""
        (tmp_path / "image.png").touch()

        assert detect_input_type(tmp_path) == "folder"

    def test_detect_empty_folder(self, tmp_path):
        """Should return unknown for empty folder"""
        assert detect_input_type(tmp_path) == "unknown"

    def test_detect_unknown_file(self, tmp_path):
        """Should return unknown for non-PDF files"""
        txt_file = tmp_path / "test.txt"
        txt_file.touch()

        assert detect_input_type(txt_file) == "unknown"


class TestSlidePresets:
    """Test slide size presets"""

    def test_all_presets_valid(self):
        """All slide presets should have valid dimensions"""
        for key, (label, width, height) in SLIDE_SIZES.items():
            assert isinstance(width, (int, float))
            assert isinstance(height, (int, float))
            assert width > 0
            assert height > 0
            assert len(label) > 0

    def test_standard_sizes_included(self):
        """Common sizes should be available"""
        labels = [label for label, _, _ in SLIDE_SIZES.values()]

        assert any("16:9" in label for label in labels)
        assert any("4:3" in label for label in labels)
        assert any("Letter" in label for label in labels)
        assert any("A4" in label for label in labels)


class TestAllowedExtensions:
    """Test allowed file extensions"""

    def test_common_formats_supported(self):
        """Common image formats should be supported"""
        required = {".png", ".jpg", ".jpeg"}
        assert required.issubset(ALLOWED_EXTS)

    def test_heic_supported(self):
        """HEIC format should be supported"""
        assert ".heic" in ALLOWED_EXTS or ".heif" in ALLOWED_EXTS

    def test_extensions_lowercase(self):
        """All extensions should be lowercase for comparison"""
        assert all(ext.islower() for ext in ALLOWED_EXTS)


# Integration test (requires PIL)
class TestIntegration:
    """Integration tests requiring actual image processing"""

    @pytest.mark.integration
    def test_create_simple_presentation(self, tmp_path):
        """End-to-end test creating a simple presentation"""
        from PIL import Image
        from make_ppt import build_presentation

        # Create test image
        img_path = tmp_path / "test.png"
        img = Image.new('RGB', (100, 100), color='red')
        img.save(img_path)

        # Create presentation
        output = tmp_path / "output.pptx"
        build_presentation(
            images=[img_path],
            output_path=output,
            slide_width_in=10.0,
            slide_height_in=7.5,
            mode="fit"
        )

        assert output.exists()
        assert output.stat().st_size > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
