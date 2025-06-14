import json

# Load chunks
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Priority logic
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

# Ranking function
def rank_results(results, refine_keywords):
    def score(chunk):
        text = chunk["text"].lower()
        keyword_hits = sum(text.count(word.lower()) for word in refine_keywords)
        first_pos = min([text.find(word.lower()) for word in refine_keywords if word.lower() in text] or [9999])
        priority = get_priority(chunk["document"])
        return (priority, -keyword_hits, first_pos)  # Lower values are better
    results.sort(key=score)
    return results

# Main search function
def get_answer(question, selected_documents=None, refine_keywords=None):
    question_lower = question.lower()
    refine_keywords = [w.strip() for w in refine_keywords or []]

    results = []

    for chunk in chunks_data:
        text = chunk["text"].lower()
        if all(q in text for q in question_lower.split()):
            if selected_documents and chunk["document"] not in selected_documents:
                continue
            results.append({
                "text": chunk["text"],
                "document": chunk["document"],
                "section": chunk["section"] if chunk["section"] != "Uncategorised" else ""
            })

    # Apply refine search if keywords exist
    if refine_keywords:
        results = [
            r for r in results
            if all(word.lower() in r["text"].lower() for word in refine_keywords)
        ]
        results = rank_results(results, refine_keywords)

    return results
