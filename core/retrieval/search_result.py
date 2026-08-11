class SearchResult:
    def __init__(self, file, score, reason,symbol=None):
        self.file = file
        self.score = score
        self.reason = reason
        self.symbol = symbol