PROJECT_TYPE_RULES = {
    "requirements.txt"  : "Python",
    "pyproject.toml"    : "Python",
    "setup.py"          : "Python",
    "package.json"      : "JavaScript",
    "Cargo.toml"        : "Rust",
    "pom.xml"           : "Java",
}
ENTRY_POINT_NAMES = {
    "main.py",
    "app.py",
    "run.py",
    "server.py",
    "manage.py",
}
class ProjectAnalyzer:
    def __init__(self,project):
        self.project = project
    def detect_project_type(self):
        language_points = {
            'Python'     : 0,
            'JavaScript' : 0,
            'TypeScript' : 0,
            'C++'        : 0,
            'C'          : 0,
            'Java'       : 0,
            'Ruby'       : 0,
            'Go'         : 0,
            'Rust'       : 0,
            'HTML'       : 0,
            'CSS'        : 0,
}
        for file in self.project.files:
            if file.name in PROJECT_TYPE_RULES: language_points[PROJECT_TYPE_RULES[file.name]] += 5

        most_used_language = max(self.project.languages, key=self.project.languages.get)   
        language_points[most_used_language]+=2

        
        self.project.type = max(language_points, key=language_points.get)
        return self.project.type

    def detect_entry_points(self):
        for file in self.project.files:
            if file.name in ENTRY_POINT_NAMES: self.project.entry_points.append(file)

        return self.project.entry_points