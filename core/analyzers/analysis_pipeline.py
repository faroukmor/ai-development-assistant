from core.analyzers.project_type_analyzer import ProjectTypeAnalyzer
from core.analyzers.entry_point_analyzer import EntryPointAnalyzer
from core.analyzers.symbols_analyzer import SymbolAnalyzer


class ProjectAnalyzer:
    def __init__(self,project):
        self.project = project
    def analyze(self):
        if self.project.type is not None:
            return
        ProjectTypeAnalyzer(self.project).detect_project_type()
        EntryPointAnalyzer(self.project).detect_entry_points()
        SymbolAnalyzer(self.project).detect_symbols()

    