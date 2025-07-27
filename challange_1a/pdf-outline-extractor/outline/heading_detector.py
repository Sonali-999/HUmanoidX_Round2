from collections import defaultdict
import re
from difflib import SequenceMatcher

def normalize_text(text):
    # Remove trailing digits or page-like numbers
    return re.sub(r'\s*\d{1,3}$', '', text).strip().lower()

def deduplicate_headings(headings, similarity_threshold=0.92):
    seen = []
    unique = []

    for h in headings:
        norm = normalize_text(h['text'])

        is_duplicate = False
        for s in seen:
            similarity = SequenceMatcher(None, norm, s).ratio()
            if similarity >= similarity_threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            seen.append(norm)
            unique.append(h)

    return unique

def assign_levels(scored):
    scored = deduplicate_headings(scored)
    if not scored:
        return []
    # Group by size_rank
    groups = defaultdict(list)
    for c in scored:
        groups[c['size_rank']].append(c)
    # Order groups by average font_size desc then average score desc
    group_list = list(groups.items())
    group_list.sort(key=lambda kv: (-avg([x['font_size'] for x in kv[1]]), -avg([x['score'] for x in kv[1]])))

    mapping = {}
    for idx,(rank, items) in enumerate(group_list):
        if idx == 0:
            mapping[rank] = 'H1'
        elif idx == 1:
            mapping[rank] = 'H2'
        else:
            mapping[rank] = 'H3'

    assigned = []
    for c in scored:
        level = mapping.get(c['size_rank'], 'H3')
        # Adjust using numbering depth
        if c['numbering_depth'] >= 2 and level == 'H1':
            level = 'H2'
        if c['numbering_depth'] >= 3 and level == 'H2':
            level = 'H3'
        assigned.append({
            'level': level,
            'text': c['text'].strip(),
            'page': c['page'],
            'score': c['score']
        })

    # Sort by page then original y (not stored? we can keep y) – preserve order
    assigned.sort(key=lambda x: (x['page']))
    return assigned

def avg(vals):
    return sum(vals)/len(vals) if vals else 0