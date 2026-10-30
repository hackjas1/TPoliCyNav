"""
=============================================================================
TPoliCynav — PDF Text Extraction Script
Checkpoint 1, Deliverable 2: Data Collection
=============================================================================
Extracts raw text from PDF documents in the project and saves them as
plain text files in data/raw/ for preprocessing.

Usage:
    python scripts/extract_pdf.py
=============================================================================
"""

import os
import sys
import pdfplumber

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# PDF sources to extract
PDF_SOURCES = {
    "TPC Student Handbook.pdf": "tpc_student_handbook.txt",
}

# Also check for the Municipal Ordinance PDF if downloaded
ORDINANCE_PDF = os.path.join(
    os.path.expanduser("~"),
    ".gemini", "antigravity-ide", "brain",
    "9f09278d-15a5-4549-85ca-d3ae17ecaaa3",
    ".tempmediaStorage", "0ffcce10647fe03c.pdf"
)


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract all text from a PDF file using pdfplumber.
    Returns the concatenated text from all pages.
    """
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"  📄 Found {total_pages} pages")
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_text.append(f"\n--- Page {i + 1} ---\n{text}")
            if (i + 1) % 20 == 0:
                print(f"  ⏳ Processed {i + 1}/{total_pages} pages...")
    return "\n".join(all_text)


def main():
    print("=" * 60)
    print("TPoliCynav — PDF Text Extraction")
    print("=" * 60)

    # 1. Extract TPC Student Handbook
    for pdf_name, output_name in PDF_SOURCES.items():
        pdf_path = os.path.join(PROJECT_ROOT, pdf_name)
        if os.path.exists(pdf_path):
            print(f"\n📖 Extracting: {pdf_name}")
            text = extract_pdf_text(pdf_path)
            output_path = os.path.join(RAW_DATA_DIR, output_name)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  ✅ Saved to {output_path}")
            print(f"  📊 Extracted {len(text):,} characters")
        else:
            print(f"  ⚠️  PDF not found: {pdf_path}")

    # 2. Extract Municipal Ordinance 127 (if available)
    if os.path.exists(ORDINANCE_PDF):
        print(f"\n📖 Extracting: Municipal Ordinance No. 127")
        text = extract_pdf_text(ORDINANCE_PDF)
        output_path = os.path.join(RAW_DATA_DIR, "municipal_ordinance_127.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  ✅ Saved to {output_path}")
        print(f"  📊 Extracted {len(text):,} characters")
    else:
        print(f"\n⚠️  Municipal Ordinance PDF not found at expected path.")
        print(f"    Expected: {ORDINANCE_PDF}")

    # 3. Summary
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    for fname in os.listdir(RAW_DATA_DIR):
        fpath = os.path.join(RAW_DATA_DIR, fname)
        size = os.path.getsize(fpath)
        print(f"  📄 {fname} — {size:,} bytes")
    print("=" * 60)


if __name__ == "__main__":
    main()
