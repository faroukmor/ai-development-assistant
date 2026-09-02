import core.retrieval.symbol_search as SS
class SymbolDependencyBuilder:
    def __init__(self,project):
        self.project = project
        self.symbol_search = SS.SymbolSearch(project)
        self.class_names = set()

    def find_call_symbols(self, symbol, file):
        for Tfile in self.project.files:
            for Tsymbol in Tfile.symbols:
                if Tsymbol.type == "class":
                    self.class_names.add(Tsymbol.name)

        parent = symbol.parent.name if symbol.parent != None else ""
        called_symbol = f"""{file.name}:{symbol.name}:{parent}"""
        search_results = []
        for call in symbol.calls:
            calls_parts = call.replace("()", "").split(".")
            if len(calls_parts) >= 2 and calls_parts[-2] in symbol.variable_bindings:
                calls_parts[-2] = symbol.variable_bindings[calls_parts[-2]]
                    
            result_symbols = self.symbol_search.find_by_name(calls_parts[-1])
            if len(calls_parts) >= 2 and calls_parts[-2] in self.class_names:
                for result_symbol in result_symbols:
                    if result_symbol.symbol.parent.name == calls_parts[-2]:
                        search_results.append(result_symbol)
            else:
                for result_symbol in result_symbols:
                    result_parent = result_symbol.symbol.parent.name if result_symbol.symbol.parent != None else ""
                    if f"""{result_symbol.file.name}:{result_symbol.symbol.name}:{result_parent}""" == called_symbol:
                        continue
                    else:
                        search_results.append(result_symbol) 
        return search_results
    