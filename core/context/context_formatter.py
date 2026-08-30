class ProjectContextFormatter:
    def __init__(self,project):
        self.project = project

    def build_languages(self):
        languages = ""
        for language in self.project.languages:
            if  self.project.languages[language] == 0: continue
            languages += language + ":" + str(self.project.languages[language]) + "\n"
        return languages

    def build_dependencies(self):
        dependencies = ""
        for dependencie in self.project.dependencies:
            dependencies += dependencie + "\n"
        return dependencies

    def build_entry_points(self):
        entry_points = ""
        for entry_point in self.project.entry_points:
            if not entry_point.content:
                entry_point.read_content()
            entry_points += entry_point.name + ":\n" + entry_point.content + "\n"
        return entry_points