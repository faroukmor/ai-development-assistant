from core.project.project_file import ProjectFile
from core.project.project_scanner import walk_paths

class ProjectLoader:
    def __init__(self):
        pass

    def load_files(self, project):
        if project.files is not None:
            return
        files, _ = walk_paths(project.path)
        project.files = [ProjectFile(path) for path in files]
    