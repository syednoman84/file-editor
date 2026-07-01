# Remove Answers from PDFs

## Overview

Redacts lines containing answers from PDF files, useful for creating practice exam versions without visible solutions.

## Script

`remove_answers.py`

## How It Works

1. Reads all PDF files from the `input/` directory
2. Scans each page for text lines starting with "Correct Answer:" or "Answer:"
3. Applies a white redaction over matching lines to hide them
4. Saves processed files to the `output/` directory with `_no_answers` appended to the filename

## Usage

```bash
# 1. Place PDF files in the input/ directory
# 2. Run the script
python remove_answers.py
```

## Input / Output

| Location | Description |
|----------|-------------|
| `input/` | Place source PDF files here |
| `output/` | Processed files appear here as `<filename>_no_answers.pdf` |

## Dependencies

- Python 3
- PyMuPDF (`pip install PyMuPDF`)

## Limitations

- Only removes text-based answer lines. Answers embedded as images (e.g., scanned PDFs) are not detected or redacted.
- Matching is prefix-based — a line must start with "Correct Answer:" or "Answer:" to be redacted.
