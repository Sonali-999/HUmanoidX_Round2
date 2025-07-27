import re, statistics
from collections import Counter

CJK_RANGE = [('\u4e00','\u9fff'), ('\u3040','\u30ff'), ('\u3400','\u4dbf')]  # Basic CJK + Hiragana/Katakana

numbering_regex = re.compile(r"^(?:[0-9]{1,3}(?:\.[0-9]{1,3}){0,3}|[IVXLC]+)\.?\s+")

END_PUNCT = set('.?!;:')

def compute_stats(lines):
    sizes = [round(l['font_size'],2) for l in lines if l['text']]
    size_counts = Counter(sizes)
    sorted_sizes = [s for s,_ in size_counts.most_common()]
    if not sorted_sizes:
        sorted_sizes=[0]
    body_size = statistics.median(sizes) if sizes else 0
    return {
        'sorted_sizes': sorted_sizes,  # descending by frequency
        'body_size': body_size,
        'max_size': max(sizes) if sizes else 0
    }

def is_cjk(text):
    for ch in text:
        code = ord(ch)
        for start,end in CJK_RANGE:
            if ord(start) <= code <= ord(end):
                return True
    return False

def detect_candidates(lines, stats):
    cands = []
    for line in lines:
        t = line['text']
        if not t or len(t) < 2:
            continue
        words = t.split()
        wc = len(words)
        cjk = is_cjk(t)
        charlen = len(t)
        # Quick length heuristic
        if (not cjk and wc > 20) or (cjk and charlen > 60):
            continue
        ends_punct = t.strip()[-1] in END_PUNCT and not numbering_regex.match(t + ' ')
        font_size = line['font_size']
        size_rank = size_rank_of(font_size, stats['sorted_sizes'])
        numbering_depth = depth_numbering(t)
        letters = [ch for ch in t if ch.isalpha()]
        caps = sum(1 for ch in letters if ch.isupper())
        capital_ratio = (caps/len(letters)) if letters else 0
        cands.append({
            **line,
            'word_count': wc,
            'char_count': charlen,
            'ends_punct': ends_punct,
            'size_rank': size_rank,
            'numbering_depth': numbering_depth,
            'capital_ratio': capital_ratio,
            'is_cjk': cjk
        })
    return cands

def size_rank_of(size, sorted_sizes):
    # Rank by descending numeric size (not frequency) for clarity
    unique_sizes = sorted(set(sorted_sizes), reverse=True)
    for i,s in enumerate(unique_sizes, start=1):
        if abs(size - s) < 0.01:
            return i
    return len(unique_sizes) + 1

def depth_numbering(text):
    # Count numeric dot depth e.g. 1.2.3 => 3 ; Roman numerals => 1
    m = numbering_regex.match(text + ' ')
    if not m:
        return 0
    core = m.group(0).strip()
    if re.match(r'^[IVXLC]+\.?$', core, re.I):
        return 1
    nums = core.split('.')
    return len([n for n in nums if n.strip() and n.strip('.').isdigit()])

def score_and_filter(cands, stats):
    out = []
    for c in cands:
        score = 0.0
        if c['size_rank'] <= 4:
            score += (4 - c['size_rank']) * 2.0
        if c['bold']:
            score += 1.5
        if c['numbering_depth'] > 0:
            score += 1.2
        if not c['is_cjk'] and c['capital_ratio'] > 0.6:
            score += 1.0
        if c['word_count'] <= 20:
            score += 0.8
        if not c['ends_punct']:
            score += 0.5
        # Title/top bias
        # page position not available here (need page height for exact). Skip or add optional.
        # Penalties
        if c['ends_punct']:
            score -= 1.0
        if c['word_count'] > 18:
            score -= 0.5*(c['word_count'] - 18)
        c['score'] = score
        if score >= 2.5:  # threshold
            out.append(c)
    return out


