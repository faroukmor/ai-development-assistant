import re

WORD_RE = re.compile(r"[A-Za-z0-9]+")
CASE_SPLIT_RE = re.compile(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[0-9]+")

STOPWORDS = {"a", "an", "the", "is", "are", "do", "does", "how",
             "what", "where", "when", "why", "which", "we", "i",
             "my", "to", "in", "of", "and", "or", "for", "on", "with"}

STEM_MAP = {
    "built": "build",
    "files": "file",
    "classes": "class",
    "tests": "test",
    "functions": "function",
    "methods": "method",
    "matches": "match",
    "loads": "load",
    "reads": "read",
    "calls": "call",
}


def stem(token):
    return STEM_MAP.get(token, token)


def tokenize(text):
    tokens = []
    for word in WORD_RE.findall(text):
        tokens.extend(CASE_SPLIT_RE.findall(word))
    tokens = [stem(token.lower()) for token in tokens]
    return [token for token in tokens if token not in STOPWORDS]


def match_tokens(name_tokens, question_tokens):
    if not name_tokens:
        return False
    return all(token in question_tokens for token in name_tokens)