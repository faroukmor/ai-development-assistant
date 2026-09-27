class DependencyAnalyzer:
    def __init__(self,project):
        self.project = project

    def detect_dependency(self):
        for file in (self.project.files or []):
            if file.name == "requirements.txt":
                if file.content == "":
                    file.read_content()
                self.project.dependencies = file.content.splitlines()
                break
