import os, json, sys
from outline.pdf_reader import extract_spans
from outline.line_builder import build_lines
from outline.line_builder import build_paragraphs
from outline.features_copy import compute_stats, detect_candidates, score_and_filter
from outline.heading_detector import assign_levels
from outline.title import select_title
from outline.exporter import export_json

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'


def process_pdf(pdf_path):
    doc_id = os.path.splitext(os.path.basename(pdf_path))[0]
    try:
        spans = extract_spans(pdf_path)
        lines = build_lines(spans)
        paras = build_paragraphs(lines)
        
        stats = compute_stats(paras)
        candidates = detect_candidates(paras, stats)
        scored = score_and_filter(candidates, stats)
        assigned = assign_levels(scored)
        title = select_title(assigned, lines)
        export_json(title, assigned, os.path.join(OUTPUT_DIR, doc_id + '.json'))
        print(f"Processed {pdf_path}")
    except Exception as e:
        print(f"ERROR processing {pdf_path}: {e}", file=sys.stderr)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("No PDFs found in /app/input")
    for name in pdf_files:
        process_pdf(os.path.join(INPUT_DIR, name))

if __name__ == '__main__':
    main()