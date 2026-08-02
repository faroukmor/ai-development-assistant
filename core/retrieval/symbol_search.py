import search_result as SR
class SymbolSearch:
    def __init__(self, project):
        self.project = project

    def search(self, question):
        files = set()
        question_words = question.lower().replace("?", "").split()

        for file in self.project.files:
            for symbol in file.symbols:
                if symbol.name.lower() in question_words:
                    files.add(file)
                    break
        return [
        SR.SearchResult(
            file=file,
            score=80,
            reason="Matched symbol"
        )
]