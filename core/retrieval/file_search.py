import os
import core.retrieval.search_result as SR


class FileSearch:
    def __init__(self, project):
        self.project = project

    def search(self, question):
        result = []

        question_words = [
            os.path.splitext(word.lower())[0]
            for word in question.replace("?", "").split()
        ]

        for file in self.project.files:
            file_name = os.path.splitext(file.name.lower())[0]

            if file_name in question_words:
                result.append(
                    SR.SearchResult(
                        file=file,
                        score=SR.FILENAME_MATCH,
                        reason="Matched filename"
                    )
                )

        return result