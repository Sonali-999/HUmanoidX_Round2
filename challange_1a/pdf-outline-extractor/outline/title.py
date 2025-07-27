def select_title(assigned, lines):
    # Check for multiple H1s on page 1 and merge
    page1_h1 = [a for a in assigned if a['level'] == 'H1' and a['page'] == 1]
    if page1_h1:
        page1_h1.sort(key=lambda a: a.get('y', 0))
        return ' '.join(a['text'] for a in page1_h1).strip()

    # Fallback: largest + boldest + topmost
    top_lines = [l for l in lines if l['page'] in (1, 2)]
    if not top_lines:
        return "Untitled"

    # Prefer big, bold, high-up text
    top_lines.sort(key=lambda l: (-l['font_size'], not l['bold'], l['y']))
    return top_lines[0]['text'][:120]
