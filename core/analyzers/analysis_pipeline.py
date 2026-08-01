import project_type_analyzer as pta
import entry_point_analyzer as epa
import symbols_analyzer as sa


class ProjectAnalyzer:
    def __init__(self,project):
        self.project = project
    def analyze(self):
        if self.project.type is not None:
            return
        pta.ProjectTypeAnalyzer(self.project).detect_project_type()
        epa.EntryPointAnalyzer(self.project).detect_entry_points()
        sa.SymbolAnalyzer(self.project).detect_symbols()

    