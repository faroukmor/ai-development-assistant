import search_result as SR

class FileSearch:
    def __init__(self,project):
        self.project = project

    def search(self,question):
        files = set()
        question_words = question.lower().replace("?", "").split()

        for file in self.project.files:
            for term in file.search_terms:
                if term in question_words:
                    files.add(file)
                    break
#        for file in files:
#            print(f"returned {file.name=}")
        return [
                SR.SearchResult(
                    file=file,
                    score=40,
                    reason="Matched filename"
                )
        ]

