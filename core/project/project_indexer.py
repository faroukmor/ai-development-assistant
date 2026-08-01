import core.analyzers.analysis_pipeline as AP
import core.project.project_loader as PL
class ProjectIndexer:
    def __init__(self,project):
        self.project = project
        

    def index_files(self):
        if self.project.is_indexed:
            return
        for file in self.project.files:
            if file.programming_language in self.project.languages:
                self.project.languages[file.programming_language] += 1
                if file.name.lower() == "readme.md": 
                    self.project.readme = file
            else:
                self.project.languages["unknown"] += 1
        
                    
            self.project.total_size += file.size
        self.project.is_indexed = True

    def build(self):
        PL.ProjectLoader(self.project).load_files()
        self.index_files()
        AP.ProjectAnalyzer(self.project).analyze()
    