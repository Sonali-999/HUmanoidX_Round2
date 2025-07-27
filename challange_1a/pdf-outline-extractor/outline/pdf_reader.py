import fitz

def extract_spans(pdf_path):
    doc = fitz.open(pdf_path)
    spans = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict").get("blocks", [])
        for b in blocks:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text = s.get("text", "").strip()
                    if not text:
                        continue
                    spans.append({
                        'text': text,
                        'font': s.get('font', ''),
                        'size': float(s.get('size', 0)),
                        'bold': any(tag in s.get('font','').lower() for tag in ['bold','black','semibold','medium']) ,
                        'x': s.get('bbox', [0,0,0,0])[0],
                        'y': s.get('bbox', [0,0,0,0])[1],
                        'page': page_num,
                        'bbox': s.get('bbox', [0,0,0,0])
                    })
                    
    doc.close()
    return spans