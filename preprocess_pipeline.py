import re

def clean_text(text):
    # Remove MS Word-style footnotes e.g. [1], [2], etc.
    text = re.sub(r'\[\d{1,3}\]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)  # normalise spacing
    return text.strip()
