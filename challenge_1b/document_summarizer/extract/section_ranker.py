from sklearn.feature_extraction.text import TfidfVectorizer

def rank_sections(sections, persona, task):
    scored = []
    context = f"{persona} tasked with: {task}"
    texts = [s['text'] for s in sections]
    
    tfidf = TfidfVectorizer().fit_transform([context] + texts)
    scores = (tfidf[0] @ tfidf[1:].T).toarray()[0]  # similarity of context vs each section

    for i, s in enumerate(sections):
        s['score'] = float(scores[i])
        scored.append(s)
    scored = sorted(scored, key=lambda x: x['score'], reverse=True)
    for idx, s in enumerate(scored):
        s['importance_rank'] = idx + 1
    
    return scored

