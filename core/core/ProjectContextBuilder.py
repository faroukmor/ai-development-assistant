class ProjectContextBuilder:
    def __init__(self,project):
        self.project = project


    def build_languages(self):
        languages = ""
        for language in self.project.languages:
            if  self.project.languages[language] == 0: continue
            languages += language + ":" + str(self.project.languages[language]) 
        return languages

    def build_files(self):
        files = ""
        for file in self.project.files:
            files += file.name + "\n"
        return files
    
    def build_entry_points(self):
        entry_points = ""
        for entry_point in self.project.entry_points:
            entry_points += entry_point.name + "\n"
        return entry_points

    def build_dependencies(self):
        dependencies = ""
        for dependencie in self.project.dependencies:
            dependencies += dependencie + "\n"
        return dependencies

    def build_context(self):
        if self.project.context is not None:
            return self.project.context
        context = f"""
                Project Name: {self.project.name}

                README: {self.project.readme}       

                Project Type: {self.project.type}

                Languages: {self.build_languages()}

                Entry Points: {self.build_entry_points()}

                Dependencies: {self.build_dependencies()}

                Files: {self.build_files()}
                """
        self.project.context = context
        return context