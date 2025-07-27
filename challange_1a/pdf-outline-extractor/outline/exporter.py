import json

def export_json(title, headings, out_path):
    outline = []
    for h in headings:
        outline.append({
            'level': h['level'],
            'text': h['text'],
            'page': int(h['page'])
        })
    data = {'title': title, 'outline': outline}
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)