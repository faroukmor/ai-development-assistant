
class ContextSelector:
    def __init__(self,project):
        self.project = project

    def get_relevant_files(self,question):
        files = []
        question_words = question.lower().replace("?", "").split()

        for file in self.project.files:
            for word in file.search_terms:
                if word in question_words:
                    files.append(file)
                    break
#        for file in files:
#            print(f"returned {file.name =}")
        return files

