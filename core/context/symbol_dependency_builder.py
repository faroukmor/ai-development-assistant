import core.retrieval.symbol_search as SS
class SymbolDependencyBuilder:
    def __init__(self,project):
        self.project = project
        self.symbol_search = SS.SymbolSearch(project)
