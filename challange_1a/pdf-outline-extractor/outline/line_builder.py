import math
from collections import Counter

LINE_Y_TOL = 2.0  # merge spans with y difference < tolerance
MIN_X_SPACING = 2.5  # minimum distance between spans to avoid overlap

MAX_PARAGRAPH_SPACING = 5.0  # vertical spacing threshold between lines in a paragraph
STYLE_TOLERANCE = 1.0  # allowable difference in font size

def build_paragraphs(lines):
    paragraphs = []
    current = []
    last_line = None

    for line in sorted(lines, key=lambda l: (l['page'], l['y'])):
        if not current:
            current.append(line)
            last_line = line
            continue

        # Core comparison logic
        same_page = line['page'] == last_line['page']

        line_gap = abs(line['y'] - last_line['y'])
        avg_font_size = (line['font_size'] + last_line['font_size']) / 2
        dynamic_spacing_threshold = avg_font_size * 1.5  # more flexible than a fixed value

        close_y = line_gap <= dynamic_spacing_threshold
        similar_font = line['font'] == last_line['font']
        similar_size = abs(line['font_size'] - last_line['font_size']) <= STYLE_TOLERANCE

        # ✅ More tolerant bold compatibility check
        bold_compatible = (
            line['bold'] == last_line['bold'] or
            (similar_font and similar_size)
        )

        if same_page and close_y and similar_font and similar_size and bold_compatible:
            current.append(line)
        else:
            paragraphs.append(_finalize_paragraph(current))
            current = [line]
        last_line = line

    if current:
        paragraphs.append(_finalize_paragraph(current))

    return paragraphs



def _finalize_paragraph(lines):
    # Join line texts with newline or space based on preference
    text = ' '.join(l['text'] for l in lines)
    return {
        'text': text.strip(),
        'page': lines[0]['page'],
        'font_size': lines[0]['font_size'],
        'font': lines[0]['font'],
        'bold': any(l['bold'] for l in lines),
        'line_count': len(lines),
        'y_top': min(l['y'] for l in lines),
        'y_bottom': max(l['y'] for l in lines),
    }


def build_lines(spans):
    # Group spans per page, then by approximate y
    pages = {}
    for sp in spans:
        pages.setdefault(sp['page'], []).append(sp)
    all_lines = []
    for page, pspans in pages.items():
        pspans.sort(key=lambda s: (round(s['y'], 1), s['x']))
        current = []
        last_y = None
        for s in pspans:
            if last_y is None or abs(s['y'] - last_y) <= LINE_Y_TOL:
                current.append(s)
                last_y = s['y'] if last_y is None else (last_y + s['y']) / 2
            else:
                all_lines.append(_finalize_line(current, page))
                current = [s]
                last_y = s['y']
        if current:
            all_lines.append(_finalize_line(current, page))
    return all_lines


def _finalize_line(spans, page):
    spans_sorted = sorted(spans, key=lambda s: s['x'])

    # Deduplicate
    seen = set()
    unique_spans = []
    for s in spans_sorted:
        key = (round(s['x'], 1), round(s['y'], 1), s['text'])
        if key not in seen:
            seen.add(key)
            unique_spans.append(s)

    # Filter overlapping
    filtered_spans = []
    last_x = -float('inf')
    for s in unique_spans:
        if s['x'] - last_x > MIN_X_SPACING:
            filtered_spans.append(s)
            last_x = s['x']

    # Smart spacing
    text_parts = []
    last_x = None
    for s in filtered_spans:
        starts_with_lower = s['text'][:1].islower()

        if last_x is not None:
            estimated_char_width = s['size'] * 0.5
            if s['x'] - last_x > estimated_char_width and not starts_with_lower:
                text_parts.append(" ")
        text_parts.append(s['text'])
        last_x = s['x'] + s['size'] * 0.6  # estimate span end
    text = ''.join(text_parts)

    avg_size = sum(s['size'] for s in filtered_spans) / len(filtered_spans)
    bold = any(s['bold'] for s in filtered_spans)
    y = min(s['y'] for s in filtered_spans)

    font_counts = Counter(s['font'] for s in filtered_spans)
    most_common_font = font_counts.most_common(1)[0][0] if font_counts else None

    return {
        'text': text.strip(),
        'page': page,
        'font_size': avg_size,
        'bold': bold,
        'y': y,
        'font': most_common_font
    }
# This function builds lines from spans extracted from a PDF.