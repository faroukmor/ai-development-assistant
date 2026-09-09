import core.retrieval.search_result as SR
import json
import urllib.request
import numpy as np

EMBED_MODEL = "nomic-embed-text"
EMBED_URL = "http://localhost:11434/api/embed"
THRESHOLD = 0.60

class EmbeddingSearch:
    def __init__(self, project):
        self.project = project
        self.knowledge_base = []

    def search(self, question):
        query_embed = self.get_embedding(question)
        if query_embed is None:
            return []

        results = []
        for symbol, file_path, text, embedding in self.knowledge_base:
            similarity = self.cosine_similarity(query_embed, embedding)
            if similarity >= THRESHOLD:
                results.append(SR.SearchResult(
                    file=self.project.get_file_by_path(file_path),
                    score=round(similarity * 100, 1),
                    reason="semantic match",
                    symbol=symbol
                ))

        return sorted(results, key=lambda r: r.score, reverse=True)

    def build_index(self):
        if self.knowledge_base:
            return

        entries = []
        texts = []
        for file in (self.project.files or []):
            for symbol in file.symbols:
                text = f"{symbol.name} {symbol.type} {file.name}"
                entries.append((symbol, file.path, text))
                texts.append(text)

        if not texts:
            return

        embeddings = self.get_embeddings(texts)
        for (symbol, file_path, text), embedding in zip(entries, embeddings):
            if embedding is None:
                continue
            self.knowledge_base.append((symbol, file_path, text, embedding))

    def get_embeddings(self, texts):
        data = json.dumps({"model": EMBED_MODEL, "input": texts}).encode('utf-8')

        try:
            req = urllib.request.Request(EMBED_URL, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))

                return [np.array(embedding) for embedding in result["embeddings"]]

        except Exception as e:
            print(f"(get_embeddings) Error: {e}")

    def get_embedding(self, text):
        embeddings = self.get_embeddings([text])
        if embeddings is None:
            return None
        return embeddings[0]

    def cosine_similarity(self, v1, v2):
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        dot_product = np.dot(v1, v2)
        return dot_product / (norm1 * norm2)
