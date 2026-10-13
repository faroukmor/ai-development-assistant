from core.retrieval.search_result import SearchResult
import json
import time
import urllib.request
import numpy as np
import os

EMBED_MODEL = "nomic-embed-text"
EMBED_URL = "http://localhost:11434/api/embed"
THRESHOLD = 0.60

# Largest batch that stays inside the timeout (see docs/track1-findings.md).
EMBED_BATCH_SIZE = 256
EMBED_TIMEOUT = 120
EMBED_RETRIES = 2
EMBED_RETRY_PAUSE = 2.0


class EmbeddingSearch:
    def __init__(self, project):
        self.project = project
        self.knowledge_base = []

    def search(self, question):
        if not self.knowledge_base:
            return []

        query_embed = self.get_embedding(question)
        if query_embed is None:
            return []

        results = []
        for symbol, file_path, text, embedding in self.knowledge_base:
            similarity = self.cosine_similarity(query_embed, embedding)
            if similarity >= THRESHOLD:
                results.append(SearchResult(
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
        if embeddings is None:
            print("(build_index) embedding index unavailable — semantic search disabled")
            return

        for (symbol, file_path, text), embedding in zip(entries, embeddings):
            if embedding is None:
                continue
            self.knowledge_base.append((symbol, file_path, text, embedding))

        self.save_index()


    def cache_path(self):
        cache_dir = os.path.join(self.project.path, ".ai_assistant_cache")
        return os.path.join(cache_dir, "embeddings.json")

    def is_cache_valid(self, payload):
        saved_at = payload.get("saved_at", 0)
        try:
            newest = max(
                os.path.getmtime(f.path) for f in (self.project.files or [])
            )
        except (OSError, ValueError):
            return False
        return newest <= saved_at

    def save_index(self):
        entries = {}
        for symbol, file_path, text, embedding in self.knowledge_base:
            vec = embedding.tolist() if hasattr(embedding, "tolist") else embedding
            entries.setdefault(file_path, []).append([symbol.name, text, vec])
        payload = {"saved_at": time.time(), "entries": entries}
        try:
            os.makedirs(os.path.dirname(self.cache_path()), exist_ok=True)
            with open(self.cache_path(), "w", encoding="utf-8") as f:
                json.dump(payload, f)
        except (OSError, TypeError, ValueError) as e:
            print(f"(save_index) could not write cache: {e}")

    def load_index(self):
        path = self.cache_path()
        if not os.path.exists(path):
            return False
        try:
            with open(path, encoding="utf-8") as f:
                payload = json.load(f)
        except (OSError, ValueError) as e:
            print(f"(load_index) ignoring corrupt cache: {e}")
            return False
        if not self.is_cache_valid(payload):
            return False
        entries = payload.get("entries", {})
        loaded = []
        for file_path, rows in entries.items():
            file = self.project.get_file_by_path(file_path)
            if file is None:
                continue
            by_name = {s.name: s for s in file.symbols}
            for row in rows:
                if len(row) < 3:
                    continue
                symbol_name, text, vec = row[0], row[1], row[2]
                symbol = by_name.get(symbol_name)
                if symbol is None:
                    continue
                loaded.append((symbol, file_path, text, np.array(vec)))
        if not loaded:
            return False
        self.knowledge_base = loaded
        print(f"(load_index) loaded {len(loaded)} entries from cache.")
        return True
    def get_embeddings(self, texts, verbose=True):
        """Embed every text in batches."""
        embeddings = []
        total = len(texts)

        for start in range(0, total, EMBED_BATCH_SIZE):
            batch = texts[start:start + EMBED_BATCH_SIZE]
            batch_embeddings = self.get_embedding_batch(batch, start, total, verbose)
            if batch_embeddings is None:
                return None
            embeddings.extend(batch_embeddings)

        return embeddings

    def get_embedding_batch(self, texts, start, total, verbose=True):
        """Vectors in the same order as texts; None for a text the server rejects.
        A failing batch is retried, then split in half. The result always has
        `len(texts)` entries, so vectors stay aligned with symbols.
        """
        if not texts:
            return []

        for attempt in range(EMBED_RETRIES + 1):
            embeddings = self.post_embedding_batch(texts)
            if embeddings is not None:
                if verbose and (start // EMBED_BATCH_SIZE) % 10 == 0:
                    print(f"(embeddings) {min(start + len(texts), total)}/{total} symbols")
                return embeddings
            if attempt < EMBED_RETRIES:
                time.sleep(EMBED_RETRY_PAUSE)

        if len(texts) == 1:
            print(f"(get_embeddings) skipping symbol {start}/{total}: the server rejected it")
            return [None]

        middle = len(texts) // 2
        print(f"(get_embeddings) splitting the batch at {start} ({len(texts)} texts) after "
              f"{EMBED_RETRIES + 1} failed attempts")

        left = self.get_embedding_batch(texts[:middle], start, total, verbose)
        right = self.get_embedding_batch(texts[middle:], start + middle, total, verbose)
        if left is None or right is None:
            return None
        return left + right

    def post_embedding_batch(self, texts):
        data = json.dumps({"model": EMBED_MODEL, "input": texts}).encode('utf-8')

        try:
            req = urllib.request.Request(EMBED_URL, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=EMBED_TIMEOUT) as response:
                result = json.loads(response.read().decode('utf-8'))
                return [np.array(embedding) for embedding in result["embeddings"]]

        except Exception as e:
            print(f"(get_embeddings) Error: {e}")
            return None

    def get_embedding(self, text):
        embeddings = self.get_embeddings([text], verbose=False)
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
