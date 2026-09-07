import core.retrieval.search_result as SR
from core.retrieval.tokenizer import tokenize, match_tokens

class SymbolSearch:
    def __init__(self, project):
        self.project = project

    def search(self, question):
        search_results = []
        question_tokens = tokenize(question)

        for file in self.project.files:
            for symbol in file.symbols:
                if match_tokens(tokenize(symbol.name), question_tokens):
                    search_results.append(SR.SearchResult(
                                                    file=file,
                                                    score=SR.SYMBOL_MATCH,
                                                    reason="Matched symbol",
                                                    symbol=symbol))
        return search_results
    def find_by_name(self,name):
        search_results = []
        name = name.lower().split(".")[-1].replace("()", "")
        for file in self.project.files:
            for symbol in file.symbols:
                if symbol.name.lower() == name:
                    search_results.append(SR.SearchResult(
                                                  file=file,
                                                  score=SR.DIRECT_LOOKUP,
                                                  reason="find_by_name",
                                                  symbol=symbol))
                    
        return search_results