# preprocess_pipeline.py
import re
from bs4 import BeautifulSoup

def clean_text(text):
    # Remove footnotes like "1 E.g. Some Footnote." or similar numbered footnotes
    text = re.sub(r"\n?\s*\d+\s+E\.g\..*?(\n|$)", " ", text)
    text = re.sub(r"\n?\s*\[\d+\].*?(\n|$)", " ", text)
    text = re.sub(r"\n?\s*Footnote:.*?(\n|$)", " ", text)

    # Remove excessive whitespace and leftover numbering
    text = re.sub(r"\s{2,}", " ", text)
    text = BeautifulSoup(text, "html.parser").get_text()
    return text.strip()
