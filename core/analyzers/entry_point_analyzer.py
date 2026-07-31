ENTRY_POINT_NAMES = {
    "main.py",
    "app.py",
    "run.py",
    "server.py",
    "manage.py",
}

class EntryPointAnalyzer:
    def __init__(self,project):
        self.project = project
    
    def detect_entry_points(self):
        self.project.entry_points = []
        for file in self.project.files:
            if file.name in ENTRY_POINT_NAMES: self.project.entry_points.append(file)

        return self.project.entry_points