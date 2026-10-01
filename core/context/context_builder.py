from core.context.context_formatter import ProjectContextFormatter
from core.context.file_context_builder import FileContextBuilder
from core.context.symbol_context_builder import SymbolContextBuilder
from core.llm.llm_client import MAX_TOKENS

MAX_TOKENS_ALLOWED = int(MAX_TOKENS * 0.75)
class ProjectContextBuilder:
    def __init__(self,project,retrievers):
        self.project = project
        self.retrievers = retrievers
        self.formatter = ProjectContextFormatter(project)
        self.file_builder = FileContextBuilder(project, retrievers)
        self.symbol_builder = SymbolContextBuilder(project, retrievers)

    def handle_context_explod(self,context):
        from tests.token_counter import count_tokens 
        tokens = count_tokens(context)
        if tokens <= MAX_TOKENS_ALLOWED:
            return context
        
        keep = int(len(context) * MAX_TOKENS_ALLOWED / tokens)
        cut = context[:keep]
        last_nl = cut.rfind("\n")
        return cut[:last_nl] if last_nl > 0 else cut
    
        

    
    def build_context(self):
        context = f"""===Project===
Name: {self.project.name}
Type: {self.project.type}       
Languages: 
{self.formatter.build_languages()}"""
        
        if self.retrievers:
            if self.project.readme:
                if not self.project.readme.content:
                    self.project.readme.read_content()
                readme_text = self.project.readme.content
            else:
                readme_text = ""
            context += f"""
README: 
{readme_text}    

Entry Points:
{self.formatter.build_entry_points()}
{self.formatter.build_dependencies()}
Relevant Symbols:
{self.symbol_builder.build_symbol_context()}
Relevant Files:
{self.file_builder.build_file_context()}
"""     
        estimated = len(context) // 3.5
        if estimated > MAX_TOKENS_ALLOWED:
            context = self.handle_context_explod(context)

        with open(r"debug\FINAL_CONTEXT.txt", "w", encoding="utf-8") as file:
            file.write(context)
            

        return context