import json
from outline.pdf_reader import extract_spans
from outline.line_builder import build_lines  # assuming your build_lines function is here
from outline.line_builder import build_paragraphs  # import paragraph function

pdf_path = 'input/file03.pdf'  # change to your real PDF name
output_path = 'output/lines_debug.json'
output_path1 = 'output/para_debug.json'

# Step 1: Extract spans
spans = extract_spans(pdf_path)

# Step 2: Build lines from spans
lines = build_lines(spans)

# Step 3: Build paragraphs from lines
paragraphs = build_paragraphs(lines)

# # Step 4: Save lines to a JSON file
# with open(output_path, 'w', encoding='utf-8') as f:
#     json.dump(lines, f, indent=2, ensure_ascii=False)
# print(f"✅ Lines written to {output_path}")

# Step 5: Save paragraphs to a JSON file
with open(output_path1, 'w', encoding='utf-8') as f:
    json.dump(paragraphs, f, indent=2, ensure_ascii=False)
print(f"✅ Paragraphs written to {output_path1}")
