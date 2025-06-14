import json

# Load chunks
try:
    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks_data = json.load(f)
except Exception as e:
    print(f"ERROR loading chunks.json: {e}")
    chunks_data = []

# Document priority
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
    except:
        return 5

# Scoring logic
def calculate_score(chunk, query_words):
    try:
        text = chunk.get("text", "").lower()
        doc_title = chunk.get("document", "")
        priority = get_priority(doc_title)
        keyword_hits = sum(text.count(word) for word in query_words)
        first_pos = min([text.find(word) for word in query_words if word in text] or [9999])
        return (
            (5 - priority) * 0.4 +
            (-keyword_hits) * 0.4 +
            (first_pos / 1000) * 0.2
        )
    except:
        return 9999

# Main answer logic
def get_answer(question, selected_documents=None, refine_keywords=None):
    try:
        question_clean = (question or "").strip()
        query_words = [w for w in question_clean.split() if w]
        refine_keywords = [w.strip() for w in (refine_keywords or []) if w.strip()]

        try:
            selected_documents = set(doc.get("label") for doc in selected_documents) if selected_documents else None
        except:
            selected_documents = None

        results = []

        for chunk in chunks_data:
            try:
                text = chunk.get("text", "")
                doc = chunk.get("document", "")
                section = chunk.get("section", "")

                if selected_documents and doc not in selected_documents:
                    continue

                # 🛡️ HARD MATCH – raw word presence, case-insensitive
                if not any(word.lower() in text.lower() for word in query_words):
                    continue

                results.append({
                    "text": text,
                    "document": doc,
                    "section": section if section != "Uncategorised" else "",
                    "score": calculate_score(chunk, [w.lower() for w in query_words])
                })

            except:
                continue

        # Refine logic
        if refine_keywords:
            results = [
                r for r in results
                if all(word.lower() in r["text"].lower() for word in refine_keywords)
            ]

        results.sort(key=lambda r: r["score"])
        for r in results:
            r.pop("score", None)

        print(f"DEBUG: {len(results)} results for query: '{question}'")
        return results

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        return []
