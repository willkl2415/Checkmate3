import json
from rapidfuzz import fuzz

# Load data
try:
    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks_data = json.load(f)
except Exception as e:
    print(f"ERROR loading chunks.json: {e}")
    chunks_data = []

# Document priority function
def get_priority(doc_title):
    title = doc_title.lower()
    if "jsp 822" in title:
        return 1
    elif "dtsm" in title:
        return 2
    elif "jsp" in title:
        return 3
    elif "mod" in title or "defence" in title:
        return 4
    else:
        return 5

# Conventional scoring model
def calculate_score(chunk, query_words):
    text = chunk.get("text", "").lower()
    doc_title = chunk.get("document", "")
    priority = get_priority(doc_title)

    # Score elements
    keyword_hits = sum(text.count(word) for word in query_words)
    positions = [text.find(word) for word in query_words if word in text]
    first_pos = min(positions) if positions else 9999
    fuzzy_score = max([fuzz.partial_ratio(word, text) for word in query_words]) if query_words else 0

    # Weighted scoring model (lower = better)
    score = (
        (100 - fuzzy_score) * 0.4 +
        (5 - priority) * 0.3 +
        (-keyword_hits) * 0.2 +
        (first_pos / 1000) * 0.1
    )
    return score

# Main search function
def get_answer(question, selected_documents=None, refine_keywords=None):
    question_clean = question.strip().lower()
    query_words = [w for w in question_clean.split() if w]
    refine_keywords = [w.strip().lower() for w in (refine_keywords or []) if w.strip()]
    selected_documents = set(selected_documents) if selected_documents else None

    results = []

    for chunk in chunks_data:
        text = chunk.get("text", "")
        text_lower = text.lower()
        doc = chunk.get("document", "")
        section = chunk.get("section", "")

        # Document filter
        if selected_documents and doc not in selected_documents:
            continue

        # ✅ Fuzzy match (passes if any word ≥ 70% match)
        if not any(fuzz.partial_ratio(word, text_lower) >= 70 for word in query_words):
            continue

        # Add result with score
        results.append({
            "text": text,
            "document": doc,
            "section": section if section != "Uncategorised" else "",
            "score": calculate_score(chunk, query_words)
        })

    # Refine filter (exact match)
    if refine_keywords:
        results = [
            r for r in results
            if all(word in r["text"].lower() for word in refine_keywords)
        ]

    # Sort by ranking score (ascending)
    results.sort(key=lambda r: r["score"])

    # Clean up scores
    for r in results:
        r.pop("score", None)

    return results
