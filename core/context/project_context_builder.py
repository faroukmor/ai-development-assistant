class ProjectContextBuilder:
    def __init__(self,project,results):
        self.project = project
        self.result_files = results


    def build_languages(self):
        languages = ""
        for language in self.project.languages:
            if  self.project.languages[language] == 0: continue
            languages += language + ":" + str(self.project.languages[language]) 
        return languages


    def build_selected_files(self):
        text = ""

        for result in self.result_files:

            file = result.file

            if not file.content:
                file.read_content()

            symbols = ""
            for symbol in file.symbols:
                symbols += f"""
                    Name: {symbol.name}
                    Type: {symbol.type}
                    Signature: {symbol.signature}
                    Line: {symbol.line}
                    Docstring: {symbol.docstring}
                    Parent: {symbol.parent.name if symbol.parent else None}
                    """

            text += f"""
                    File: {file.name}

                    Relevance: {result.score}
                    Reason: {result.reason}

                    Symbols:
                    {symbols}

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
            entry_points += entry_point.name +":"+ entry_point.content +"\n"
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
                Project Name: 
                
                {self.project.name}

                README: 
                
                {self.project.readme.name}  

                content: 
                
                {self.project.readme.content}    

                Project Type: 
                
                {self.project.type}

                Languages: 
                
                {self.build_languages()}

                Entry Points: 
                
                {self.build_entry_points()}

                Dependencies: 
                
                {self.build_dependencies()}

                Relevant Files:

                {self.build_selected_files()}
                """
        print(f"{context=}")
        return context