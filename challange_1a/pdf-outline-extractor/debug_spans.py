import json
from outline.pdf_reader import extract_spans

# Path to the PDF file
pdf_path = 'input/file03.pdf'  # Change this to your actual file name

# Extract spans
spans = extract_spans(pdf_path)

# Output file path
output_path = 'output/spans_debug.json'

# Write spans to a JSON file
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(spans, f, indent=2, ensure_ascii=False)

print(f"✅ Spans written to {output_path}")
