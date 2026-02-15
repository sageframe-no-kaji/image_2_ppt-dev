#!/usr/bin/env python3
"""
Gradio Web UI for PPTX Builder
Simple interface for converting PDFs and images to PowerPoint
"""

import gradio as gr
import tempfile
import shutil
from pathlib import Path
from typing import Optional, List
import time

from make_ppt import (
    build_presentation,
    convert_pdf_to_images,
    pdf_first_page_size_inches,
    SLIDE_SIZES,
)


# Slide size options for dropdown
SLIDE_SIZE_OPTIONS = {
    "16:9 (Widescreen)": (13.3333333333, 7.5),
    "4:3 (Standard)": (10.0, 7.5),
    "Letter (11\" x 8.5\")": (11.0, 8.5),
    "A4 (11.69\" x 8.27\")": (11.69, 8.27),
    "Legal (14\" x 8.5\")": (14.0, 8.5),
    "Tabloid (17\" x 11\")": (17.0, 11.0),
}


def process_files(
    files: List[gr.File],
    slide_size: str,
    fit_mode: str,
    dpi: int = 300
) -> Optional[str]:
    """
    Process uploaded files and create PowerPoint presentation.

    Args:
        files: List of uploaded files (PDFs or images)
        slide_size: Selected slide size preset
        fit_mode: "Fit whole image" or "Crop to fill"
        dpi: DPI for PDF conversion

    Returns:
        Path to generated PPTX file or None on error
    """
    if not files:
        return None

    # Create temp directory for processing
    temp_dir = Path(tempfile.mkdtemp(prefix="pptx_builder_"))

    try:
        # Get slide dimensions
        width_in, height_in = SLIDE_SIZE_OPTIONS[slide_size]
        mode = "fit" if fit_mode == "Fit whole image" else "fill"

        image_files = []

        # Process each uploaded file
        for file in files:
            file_path = Path(file.name)

            # Handle PDFs
            if file_path.suffix.lower() == ".pdf":
                # Convert PDF to images
                pdf_images = convert_pdf_to_images(file_path, dpi=dpi)
                image_files.extend(pdf_images)
            else:
                # Direct image files
                image_files.append(file_path)

        if not image_files:
            return None

        # Sort images
        image_files.sort(key=lambda p: p.name.lower())

        # Create output PPTX
        output_path = temp_dir / "presentation.pptx"

        build_presentation(
            images=image_files,
            output_path=output_path,
            slide_width_in=width_in,
            slide_height_in=height_in,
            mode=mode
        )

        return str(output_path)

    except Exception as e:
        print(f"Error processing files: {e}")
        # Cleanup on error
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
        return None


# Create Gradio interface
with gr.Blocks(title="PPTX Builder") as app:
    gr.Markdown(
        """
        # PPTX Builder

        Convert PDFs and images to PowerPoint presentations at 300 DPI.

        **Supported formats:** PDF, PNG, JPG, JPEG, TIFF, WebP, BMP, GIF, ICO, HEIC, HEIF
        """
    )

    with gr.Row():
        with gr.Column():
            files = gr.File(
                label="Upload PDF or Images",
                file_count="multiple",
                file_types=[
                    ".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff",
                    ".webp", ".bmp", ".gif", ".ico", ".heic", ".heif"
                ]
            )

            slide_size = gr.Dropdown(
                choices=list(SLIDE_SIZE_OPTIONS.keys()),
                value="16:9 (Widescreen)",
                label="Slide Size"
            )

            fit_mode = gr.Radio(
                choices=["Fit whole image", "Crop to fill"],
                value="Fit whole image",
                label="Image Placement"
            )

            dpi = gr.Slider(
                minimum=150,
                maximum=600,
                value=300,
                step=50,
                label="PDF Conversion DPI"
            )

            submit_btn = gr.Button("Create Presentation", variant="primary")

        with gr.Column():
            output = gr.File(label="Download PPTX")

            gr.Markdown(
                """
                ### How it works:
                1. Upload one or more PDFs or images
                2. Choose slide size and placement mode
                3. Click "Create Presentation"
                4. Download your PPTX file

                **Note:** Files are automatically deleted after 30 days.
                """
            )

    # Connect interface
    submit_btn.click(
        fn=process_files,
        inputs=[files, slide_size, fit_mode, dpi],
        outputs=output
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
