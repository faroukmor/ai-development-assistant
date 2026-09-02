import core.retrieval.symbol_search as SS
class SymbolDependencyBuilder:
    def __init__(self,project):
        self.project = project
        self.symbol_search = SS.SymbolSearch(project)

    def find_call_symbols(self, symbol, file):
        parent = symbol.parent.name if symbol.parent != None else ""
        called_symbol = f"""{file.name}:{symbol.name}:{parent}"""
        search_results = []
        for call in symbol.calls:
            call = call.replace("()", "")
            call = call.split(".")[-1]
            result_symbols = self.symbol_search.find_by_name(call)
            for result_symbol in result_symbols:
                result_parent = result_symbol.symbol.parent.name if result_symbol.symbol.parent != None else ""
                if f"""{result_symbol.file.name}:{result_symbol.symbol.name}:{result_parent}""" == called_symbol:
                    continue
                else:
                    search_results.append(result_symbol) 
        return search_results