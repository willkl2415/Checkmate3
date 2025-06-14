import json
from rapidfuzz import fuzz

# Load chunks
try:
    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks_data = json.load(f)
except Exception as e:
    print(f"ERROR loading chunks.json: {e}")
    chunks_data = []

# Document priority scoring
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
    except Exception as e:
        print(f"ERROR in get_priority: {e}")
        return 5

# Relevance scoring model
def calculate_score(chunk, query_words):
    try:
        text = chunk.get("text", "").lower()
        doc_title = chunk.get("document", "")
        priority = get_priority(doc_title)
        keyword_hits = sum(text.count(word) for word in query_words)
        positions = [text.find(word) for word in query_words if word in text]
        first_pos = min(positions) if positions else 9999
        fuzzy_score = max([fuzz.partial_ratio(word, text) for word in query_words]) if query_words else 0

        score = (
            (100 - fuzzy_score) * 0.4 +
            (5 - priority) * 0.3 +
            (-keyword_hits) * 0.2 +
            (first_pos / 1000) * 0.1
        )
        return score
    except Exception as e:
        print(f"ERROR in calculate_score: {e}")
        return 9999

# Main answer engine
def get_answer(question, selected_documents=None, refine_keywords=None):
    try:
        question_clean = (question or "").strip().lower()
        query_words = [w for w in question_clean.split() if w]
        refine_keywords = [w.strip().lower() for w in (refine_keywords or []) if w.strip()]

        # ✅ FIX: unpack list of dicts to extract document labels
        try:
            selected_documents = set(doc.get("label") for doc in selected_documents) if selected_documents else None
        except Exception as e:
            print(f"DOCUMENT FILTER PARSE ERROR: {e}")
            selected_documents = None

        results = []

        for chunk in chunks_data:
            try:
                text = chunk.get("text", "")
                text_lower = text.lower()
                doc = chunk.get("document", "")
                section = chunk.get("section", "")

                if selected_documents and doc not in selected_documents:
                    continue

                # ✅ Fuzzy matching (passes if any keyword ≥ 70%)
                if not any(fuzz.partial_ratio(word, text_lower) >= 70 for word in query_words):
                    continue

                results.append({
                    "text": text,
                    "document": doc,
                    "section": section if section != "Uncategorised" else "",
                    "score": calculate_score(chunk, query_words)
                })

            except Exception as e:
                print(f"ERROR processing chunk: {e}")
                continue

        # Apply refine filtering
        if refine_keywords:
            results = [
                r for r in results
                if all(word in r["text"].lower() for word in refine_keywords)
            ]

        # Final sort by calculated score
        results.sort(key=lambda r: r["score"])
        for r in results:
            r.pop("score", None)

        print(f"DEBUG: Returned {len(results)} results for query: '{question}'")
        return results

    except Exception as e:
        print(f"FATAL ERROR in get_answer: {e}")
        return []
