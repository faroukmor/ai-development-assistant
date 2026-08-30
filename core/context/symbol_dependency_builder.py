import core.retrieval.symbol_search as SS
class SymbolDependencyBuilder:
    def __init__(self,project):
        self.project = project
        self.symbol_search = SS.SymbolSearch(project)

    def find_call_symbols(self, symbol):
        search_results = []
        for call in symbol.calls:
            call = call.replace("()", "")
            call = call.split(".")[-1]
            search_results += self.symbol_search.find_by_name(call)
        return search_results