PROJECT_TYPE_RULES = {
    "requirements.txt"  : "Python",
    "pyproject.toml"    : "Python",
    "setup.py"          : "Python",
    "package.json"      : "JavaScript",
    "Cargo.toml"        : "Rust",
    "pom.xml"           : "Java",
}

EXTENSION_POINTS = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".cpp": "C++", ".cc": "C++", ".hpp": "C++",
    ".c": "C", ".h": "C",
    ".java": "Java", ".rb": "Ruby",
    ".go": "Go", ".rs": "Rust",
    ".html": "HTML", ".css": "CSS",
}


class ProjectTypeAnalyzer:
    def __init__(self, project):
        self.project = project

    def detect_project_type(self):
        language_points = {
            "Python": 0, "JavaScript": 0, "TypeScript": 0, "C++": 0,
            "C": 0, "Java": 0, "Ruby": 0, "Go": 0, "Rust": 0,
            "HTML": 0, "CSS": 0,
        }
        for file in self.project.files:
            if file.name in PROJECT_TYPE_RULES:
                language_points[PROJECT_TYPE_RULES[file.name]] += 5
                continue
            language = EXTENSION_POINTS.get(file.ext.lower())
            if language is not None:
                language_points[language] += 1

        if all(points == 0 for points in language_points.values()):
            self.project.type = "Unknown"
            return self.project.type

        best_language = max(language_points, key=lambda lang: language_points[lang])
        self.project.type = best_language
        return self.project.type
