"""
Budget PDF Parser (Template)
Extracts scheme allocation data from Union Budget PDF documents.

This is a template script showing the approach for parsing budget documents.
Actual PDF parsing requires downloading budget documents from indiabudget.gov.in.

Usage:
    python budget_pdf_parser.py --input budget_2024.pdf --output allocations.csv
"""

import argparse
import csv
import re
from pathlib import Path


def extract_tables_from_text(text):
    """
    Extract budget table rows from raw PDF text.
    Budget tables typically follow this pattern:
    Scheme Name | BE 2023-24 | RE 2023-24 | BE 2024-25
    """
    rows = []
    # Pattern: words followed by numbers (crores)
    pattern = re.compile(
        r"^(.+?)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s*$",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        scheme = match.group(1).strip()
        be_current = float(match.group(2).replace(",", ""))
        re_current = float(match.group(3).replace(",", ""))
        be_next = float(match.group(4).replace(",", ""))
        rows.append({
            "scheme_name": scheme,
            "budget_estimate_cr": be_current,
            "revised_estimate_cr": re_current,
            "next_year_estimate_cr": be_next,
        })
    return rows


def parse_budget_pdf(pdf_path):
    """
    Parse a Union Budget PDF and extract allocation data.
    Requires: pip install pdfplumber
    """
    try:
        import pdfplumber
    except ImportError:
        print("Install pdfplumber: pip install pdfplumber")
        print("This is a template -- see docs/methodology.md for manual data collection.")
        return []

    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return extract_tables_from_text(text)


def save_to_csv(rows, output_path):
    if not rows:
        print("No data extracted.")
        return
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Union Budget PDF for scheme allocations")
    parser.add_argument("--input", required=True, help="Path to budget PDF")
    parser.add_argument("--output", default="allocations.csv", help="Output CSV path")
    args = parser.parse_args()

    rows = parse_budget_pdf(args.input)
    save_to_csv(rows, args.output)
