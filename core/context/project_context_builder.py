class ProjectContextBuilder:
    def __init__(self,project,results):
        self.project = project
        self.result_files = results


    def build_languages(self):
        languages = ""
        for language in self.project.languages:
            if  self.project.languages[language] == 0: continue
            languages += language + ":" + str(self.project.languages[language]) + "\n"
        return languages


    def build_selected_files(self):
        text = ""

        for result in self.result_files:
            if result.symbol:
                matched_symbol = f"""
                        Relevant Symbol:
                        Name: {result.symbol.name}
                        Type: {result.symbol.type}
                        Signature: {result.symbol.signature}
                        Line: {result.symbol.line}
                        Parent: {result.symbol.parent.name if result.symbol.parent else ""}
                        Docstring: {result.symbol.docstring}"""
            else: matched_symbol = ""
            file = result.file

            if not file.content:
                file.read_content()

            text += f"""
                    -----------------------
                    File: {file.name}
                    Relevance: {result.score}
                    Reason: {result.reason}
                    {matched_symbol}
                    Source:

                    {file.content}
                    -----------------------
                    """

        return text
    
    def build_files(self):
        Files = ""
        for file in self.project.files:
            Files += file.name + "\n"
        return Files
    
    def build_entry_points(self):
        entry_points = ""
        for entry_point in self.project.entry_points:
            if not entry_point.content:
                entry_point.read_content()
            entry_points += entry_point.name+"\n"+"content:"+ entry_point.content+"\n"+"---------------------\n"
        return entry_points

    def build_dependencies(self):
        dependencies = ""
        for dependencie in self.project.dependencies:
            dependencies += dependencie + "\n"
        return dependencies

    def build_context(self):
        
        if self.project.readme and not self.project.readme.content:
            self.project.readme.read_content()
        context = f"""
                Project Name: {self.project.name}

                README: {self.project.readme.name}  
                content: 
                {self.project.readme.content}    
                ----------------------------
                Project Type: {self.project.type}

                Languages: 
                {self.build_languages()}

                Entry Points:
                {self.build_entry_points()}

                Dependencies: {self.build_dependencies()}

                Relevant Files:
                {self.build_selected_files()}
                """
        with open("context_test.txt", "w", encoding="utf-8") as file:
            file.write(context)

        return context