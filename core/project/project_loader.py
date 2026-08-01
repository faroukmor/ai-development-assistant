import core.project.project_scanner as ps
import core.project.project_file as pf

class ProjectLoader:
    def __init__(self,project):
        self.project = project

    def load_files(self):
            if self.project.files is not None:
                return
            elements = ps.scan_project(self.project.path)
            files = ps.get_files(elements)
    
            self.project.files = pf.files_to_objects(files)
    