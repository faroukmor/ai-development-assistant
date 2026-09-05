import core.project.project_scanner as ps
import core.project.project_file as pf

class ProjectLoader:
    def __init__(self):
        pass

    def load_files(self, project):
            if project.files is not None:
                return
            elements = ps.scan_project(project.path)
            files = ps.get_files(elements)
    
            project.files = pf.files_to_objects(files)

            return project
    