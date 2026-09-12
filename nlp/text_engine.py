class TextEngine:
    def __init__(self):
        self.model = None
        self.error = None
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            self.error = str(e)

    def similarity(self, a, b):
        if not a or not b:
            return 0.0
        if self.model is None:
            return self._keyword_similarity(a, b)
        vectors = self.model.encode([a, b], normalize_embeddings=True)
        return float(vectors[0] @ vectors[1])

    @staticmethod
    def _keyword_similarity(a, b):
        sa = set(a.lower().split())
        sb = set(b.lower().split())
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)
