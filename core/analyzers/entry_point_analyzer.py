ENTRY_POINT_NAMES = {
    "main",
    "app",
    "run",
    "server",
    "manage",
}

class EntryPointAnalyzer:
    def __init__(self,project):
        self.project = project
    
    def detect_entry_points(self):
        self.project.entry_points = []
        for file in (self.project.files or []):
            if file.stem in ENTRY_POINT_NAMES: self.project.entry_points.append(file)
