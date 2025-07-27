KEYWORDS = {
    "college_group": [
        "nightlife", "beach", "adventure", "water sports", "bars", "outdoor", "clubs", "hiking", "fun",
        "interactive", "events", "celebrations", "scenic views", "historic sites", "affordable", "group activity"
    ]
}

def filter_relevant_sections(sections, group_type="college", trip_length=4):
    relevant = []
    for section in sections:
        text = section['text'].lower()
        if any(kw in text for kw in KEYWORDS.get("college_group", [])):
            if len(relevant) < 20:  # limit for conciseness
                relevant.append({
                    'document': section['document'],
                    'page_number': section['page'],
                    'section_title': section['text'][:50].strip() + '...',
                    'importance_rank': section['importance_rank'],
                    'refined_text': section['text']
                })
    return relevant


