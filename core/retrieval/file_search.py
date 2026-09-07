import os
import core.retrieval.search_result as SR
from core.retrieval.tokenizer import tokenize, match_tokens

class FileSearch:
    def __init__(self, project):
        self.project = project

    def search(self, question):
        result = []
        question_tokens = tokenize(question)

        for file in self.project.files:
            if match_tokens(tokenize(file.stem), question_tokens):
                result.append(
                    SR.SearchResult(
                        file=file,
                        score=SR.FILENAME_MATCH,
                        reason="Matched filename"
                    )
                )

        return result