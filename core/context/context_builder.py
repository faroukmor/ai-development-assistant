from core.context.context_formatter import ProjectContextFormatter
from core.context.file_context_builder import FileContextBuilder
from core.context.symbol_context_builder import SymbolContextBuilder

class ProjectContextBuilder:
    def __init__(self,project,retrievers):
        self.project = project
        self.retrievers = retrievers

        self.formatter = ProjectContextFormatter(project)
        self.file_builder = FileContextBuilder(project, retrievers)
        self.symbol_builder = SymbolContextBuilder(project, retrievers)

    
    def build_context(self):
        context = f"""===Project===
Name: {self.project.name}
Type: {self.project.type}       
Languages: 
{self.formatter.build_languages()}"""
        
        if self.retrievers: 
            if self.project.readme and not self.project.readme.content:
                                self.project.readme.read_content()
            context += f"""
README: 
{self.project.readme.content}    

Entry Points:
{self.formatter.build_entry_points()}
Dependencies: {self.formatter.build_dependencies()}
Relevant Files:
{self.file_builder.build_file_context()}
{self.symbol_builder.build_symbol_context()}
"""
        with open(r"debug\FINAL_CONTEXT.txt", "w", encoding="utf-8") as file:
            file.write(context)

        return context