FILENAME_MATCH = 50
SYMBOL_MATCH   = 80
DIRECT_LOOKUP  = 100   
class SearchResult:
    def __init__(self, file, score, reason,symbol=None):
        self.file = file
        self.score = score
        self.reason = reason
        self.symbol = symbol