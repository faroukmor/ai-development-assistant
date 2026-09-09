import core.retrieval.file_search as FS
import core.retrieval.symbol_search as SS
import core.project.project as P
from core.retrieval.tokenizer import tokenize
class HybridRetriever:
    def __init__(self, project, embedding_search=None):
        self.project = project
        self.embedding_search = embedding_search

    def rank_results(self, results):
        merged = {}
        for result in results:
            key = result.file.path

            if key in merged:
                if result.score > merged[key].score:
                    result.symbol = result.symbol or merged[key].symbol
                    merged[key] = result
                else:
                    merged[key].symbol = merged[key].symbol or result.symbol
            else:
                merged[key] = result

        final = list(merged.values())
        final = self.drop_partial_duplicates(final)     # ← البند الجديد فقط
        return sorted(final, key=lambda r: r.score, reverse=True)

    def drop_partial_duplicates(self, results):
        symbol_results = [r for r in results if r.symbol]
        partials = []
        for r in symbol_results:
            r_tokens = tokenize(r.symbol.name)
            if len(r_tokens) == 1:
                for other in symbol_results:
                    other_tokens = tokenize(other.symbol.name)
                    if (other is not r and r.score == other.score
                            and len(other_tokens) > 1
                            and r_tokens[0] in other_tokens):
                        partials.append(r)
                        break
        return [r for r in results if r not in partials]

    def search(self,question):
        results = []
        results += FS.FileSearch(self.project).search(question)
        results += SS.SymbolSearch(self.project).search(question)
        if self.embedding_search:
            results += self.embedding_search.search(question)
        return self.rank_results(results)
    
