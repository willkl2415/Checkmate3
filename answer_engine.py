import json
import re

def match_query_to_chunk(chunk, query, document_filter, section_filter):
    query = query.lower()
    content = chunk["content"].lower()
    heading = chunk["heading"].lower()
    document = chunk["document"].lower()

    if document_filter and document_filter.lower() != document:
        return False
    if section_filter and section_filter.lower() not in heading:
        return False

    return query in content or query in heading

def answer_question(query, document_filter="", section_filter=""):
    with open("chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    matches = []
    for chunk in chunks:
        if match_query_to_chunk(chunk, query, document_filter, section_filter):
            matches.append(chunk)

    return matches
