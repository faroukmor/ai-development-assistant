import core.core.analyzers.project_type_analyzer as pt
import core.core.analyzers.entry_point_analyzer as ep


class ProjectAnalyzer:
    def __init__(self,project):
        self.project = project
    def analyze(self):
        if self.project.type is not None:
            return
        pt.ProjectTypeAnalyzer(self.project).detect_project_type()
        ep.EntryPointAnalyzer(self.project).detect_entry_points()
    