import core.project.project_scanner as ps
import core.project.project_file as pf

class ProjectLoader:
    def __init__(self):
        pass

    def load_files(self, project):
        if project.files is not None:
            return
        files, _ = ps.walk_paths(project.path)
        project.files = pf.files_to_objects(files)
    