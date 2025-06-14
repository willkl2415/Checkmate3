import json
from rapidfuzz import fuzz

# Load data
try:
    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks_data = json.load(f)
except Exception as e:
    print(f"Error loading chunks.json: {e}")
    chunks_data = []

# Priority logic
def get_priority(doc_title):
    try:
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
    except Exception:
        return 5

# Ranking logic for refine
def rank_results(results, refine_keywords):
    try:
        def score(chunk):
            text = chunk.get("text", "").lower()
            keyword_hits = sum(text.count(word.lower()) for word in refine_keywords)
            first_pos = min([text.find(word.lower()) for word in refine_keywords if word.lower() in text] or [9999])
            priority = get_priority(chunk.get("document", ""))
            return (priority, -keyword_hits, first_pos)
        results.sort(key=score)
        return results
    except Exception as e:
        print(f"Ranking error: {e}")
        return results

# Main search function with fuzzy matching
def get_answer(question, selected_documents=None, refine_keywords=None):
    try:
        question_clean = question.strip().lower()
        refine_keywords = [w.strip() for w in (refine_keywords or []) if w.strip()]
        selected_documents = set(selected_documents) if selected_documents else None

        results = []
        match_threshold = 70  # fuzzy match score threshold (0–100)

        for chunk in chunks_data:
            text = chunk.get("text", "")
            doc = chunk.get("document", "")
            section = chunk.get("section", "")
            text_lower = text.lower()

            # ✅ Fuzzy match using rapidfuzz
            match_score = fuzz.partial_ratio(question_clean, text_lower)
            if match_score >= match_threshold:
                if selected_documents and doc not in selected_documents:
                    continue
                results.append({
                    "text": text,
                    "document": doc,
                    "section": section if section != "Uncategorised" else ""
                })

        # Apply refine + rerank
        if refine_keywords:
            results = [
                r for r in results
                if all(word.lower() in r["text"].lower() for word in refine_keywords)
            ]
            results = rank_results(results, refine_keywords)

        return results

    except Exception as e:
        print(f"Search error: {e}")
        return []
