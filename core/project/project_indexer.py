from core.analyzers.analysis_pipeline import ProjectAnalyzer
from core.project.project_loader import ProjectLoader
class ProjectIndexer:
    def __init__(self,project):
        self.project = project
        

    def index_files(self):
        if self.project.is_indexed:
            return
        for file in (self.project.files or []):
            if file.programming_language in self.project.languages:
                self.project.languages[file.programming_language] += 1
                if file.stem == "readme": 
                    self.project.readme = file
            else:
                self.project.languages["unknown"] += 1
        
                    
            self.project.total_size += file.size
        self.project.is_indexed = True

    def build(self):
        ProjectLoader().load_files(self.project)
        self.index_files()
        ProjectAnalyzer(self.project).analyze()
    