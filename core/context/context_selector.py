
class ContextSelector:
    def __init__(self,project):
        self.project = project

    def get_relevant_files(self,question):
        files = []
        question = question.lower()
        for file in self.project.files:
            for word in file.keywords:
                if word in question:
                    files.append(file)
                    break
        return files

