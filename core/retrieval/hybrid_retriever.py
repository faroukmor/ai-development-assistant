import core.retrieval.file_search as FS
import core.retrieval.symbol_search as SS
import core.project.project as P
class HybridRetriever:
    def __init__(self,project):
        self.project = project

    def rank_results(self, results):
        merged = {}

        for result in results:
            key = result.file.path

            if key in merged:
                merged[key].score += result.score
            else:
                merged[key] = result

        return sorted(
            merged.values(),
            key=lambda r: r.score,
            reverse=True
        )
    def search(self,question):
        results = []

        results += FS.FileSearch(self.project).search(question)
        results += SS.SymbolSearch(self.project).search(question)
        #results += EmbeddingSearch(self.project).search(question)
        print(self.rank_results(results))
        return self.rank_results(results)
