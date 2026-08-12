class ProjectContextBuilder:
    def __init__(self,project,retrievers):
        self.project = project
        self.retrievers = retrievers


    def build_languages(self):
        languages = ""
        for language in self.project.languages:
            if  self.project.languages[language] == 0: continue
            languages += language + ":" + str(self.project.languages[language]) + "\n"
        return languages

    def build_symbol_context(self):
        symbol_context = ""
        for retriever in self.retrievers:
            if retriever.symbol:
                start_line = retriever.symbol.line
                end_line = retriever.symbol.end_line

                if not retriever.file.content:
                    retriever.file.read_content()
                
                symbol_source = retriever.file.content.splitlines()
                symbol_source = symbol_source[start_line-1:end_line]
                symbol_source = "\n".join(symbol_source)

                symbol_context += f"""
File: {retriever.file.name}
Relevance: {retriever.score}
Reason: {retriever.reason}
                
Relevant Symbol:
Name: {retriever.symbol.name}
Type: {retriever.symbol.type}
Signature: {retriever.symbol.signature}
Parent: {retriever.symbol.parent.name if retriever.symbol.parent else ""}
Docstring: {retriever.symbol.docstring}

{retriever.symbol.name}: 
{symbol_source}
"""
        return symbol_context
        
    def build_file_context(self):
        file_context = ""
        for retriever in self.retrievers:
            if not retriever.symbol:
                if not retriever.file.content:
                    retriever.file.read_content()

                file_context += f"""
    File: {retriever.file.name}
    Relevance: {retriever.score}
    Reason: {retriever.reason}
    Source:
    {retriever.file.content}
    -----------------------
    """
        return file_context
    
    """def build_files(self):
        Files = ""
        for file in self.project.files:
            Files += file.name + "\n"
        return Files"""
    
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
        context = f"""
Project Name: {self.project.name}
        
Project Type: {self.project.type}
        
Languages: 
{self.build_languages()}
                
"""
        

        if self.retrievers: 
            if self.project.readme and not self.project.readme.content:
                                self.project.readme.read_content()
            context += f"""
README: {self.project.readme.name}  
content: 
{self.project.readme.content}    
----------------------------

Entry Points:
{self.build_entry_points()}

Dependencies: {self.build_dependencies()}

Relevant Files:
{self.build_symbol_context()}
{self.build_file_context()}

"""
        with open("context_test.txt", "w", encoding="utf-8") as file:
            file.write(context)

        return context