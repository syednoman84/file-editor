"""
Script to remove lines starting with "Correct Answer:" from PDF files.
Reads all PDFs from an 'input' directory and saves processed files to an 'output' directory.
Uses PyMuPDF (fitz) to redact matching text from each page.
"""

import fitz  # PyMuPDF
import sys
import os
import glob


INPUT_DIR = "input"
OUTPUT_DIR = "output"


def remove_correct_answers(input_pdf, output_pdf):
    """
    Remove all text lines starting with 'Correct Answer:' from the PDF.

    Args:
        input_pdf: Path to the input PDF file.
        output_pdf: Path for the output PDF.
    """
    doc = fitz.open(input_pdf)
    redaction_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block.get("type") != 0:  # Skip non-text blocks (images, etc.)
                continue

            for line in block.get("lines", []):
                line_text = "".join(span["text"] for span in line["spans"]).strip()

                if line_text.startswith("Correct Answer:") or line_text.startswith("Answer:"):
                    rect = fitz.Rect(line["bbox"])
                    page.add_redact_annot(rect, fill=(1, 1, 1))  # White fill
                    redaction_count += 1

        page.apply_redactions()

    doc.save(output_pdf)
    doc.close()

    return redaction_count


def process_all_pdfs():
    """Process all PDF files from the input directory and save to output directory."""
    # Create directories if they don't exist
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Find all PDF files in the input directory
    pdf_files = glob.glob(os.path.join(INPUT_DIR, "*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in '{INPUT_DIR}/' directory.")
        print(f"Place your PDF files in the '{INPUT_DIR}/' folder and run again.")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF file(s) in '{INPUT_DIR}/'")
    print("-" * 50)

    total_redactions = 0

    for pdf_path in sorted(pdf_files):
        filename = os.path.basename(pdf_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(OUTPUT_DIR, f"{name}_no_answers{ext}")

        print(f"Processing: {filename}...", end=" ")
        redactions = remove_correct_answers(pdf_path, output_path)
        total_redactions += redactions
        print(f"removed {redactions} answer(s)")

    print("-" * 50)
    print(f"All done! Processed {len(pdf_files)} file(s), removed {total_redactions} total answer(s).")
    print(f"Output saved to '{OUTPUT_DIR}/' directory.")


if __name__ == "__main__":
    process_all_pdfs()
