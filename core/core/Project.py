import project_scanner


class Project:
    def __init__(self,path):
        self.path = path
        self.files = None
        self.pyrhon_files = None
        self.readme = None
        self.total_size = None
        self.languages = None
        self.structure = None
        self.dependencies = None

    def load_files(self):
        self.files = project_scanner.scan_project_obj(self.path)
    