class FileContextBuilder:
    def __init__(self,project,retrievers):
        self.project = project
        self.retrievers = retrievers
    def build_file_context(self):
        file_context = "==File=="
        for retriever in self.retrievers:
            if not retriever.symbol:
                if not retriever.file.content:
                    retriever.file.read_content()

                file_context += f"""
Name: {retriever.file.name}
Relevance: {retriever.score}
Reason: {retriever.reason}
Source:
{retriever.file.content}
  
"""
        return file_context
    