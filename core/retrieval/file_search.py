from core.retrieval.search_result import SearchResult,FILENAME_MATCH
from core.retrieval.tokenizer import tokenize, match_tokens

class FileSearch:
    def __init__(self, project):
        self.project = project

    def search(self, question):
        result = []
        question_tokens = tokenize(question)

        for file in (self.project.files or []):
            if match_tokens(tokenize(file.stem), question_tokens):
                result.append(
                    SearchResult(
                        file=file,
                        score=FILENAME_MATCH,
                        reason="Matched filename"
                    )
                )

        return result