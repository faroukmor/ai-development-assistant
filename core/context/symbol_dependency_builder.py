import core.retrieval.symbol_search as SS
class SymbolDependencyBuilder:
    def __init__(self, project):
        self.project = project
        self.symbol_search = SS.SymbolSearch(project)
        self.class_names = set()
        for file in (project.files or []):
            for symbol in file.symbols:
                if symbol.type == "class":
                    self.class_names.add(symbol.name)

    def get_symbol_identity(self,symbol,file):
        parent = symbol.parent.name if symbol.parent != None else ""
        return f"""{file.name}:{symbol.name}:{parent}"""
    
    def find_call_symbols(self, symbol, file):
        symbol_identity = self.get_symbol_identity(symbol,file)
        call_results = []
        for call in symbol.calls:
            call_parts = call.replace("()", "").split(".")
            if len(call_parts) >= 2 and call_parts[-2] in symbol.variable_bindings:
                call_parts[-2] = symbol.variable_bindings[call_parts[-2]]
                    
            matches = self.symbol_search.find_by_name(call_parts[-1])
            if len(call_parts) >= 2 and call_parts[-2] in self.class_names:
                for call_result in matches:
                    if call_result.symbol.parent.name == call_parts[-2]:
                        call_results.append(call_result)
            else:
                for call_result in matches:
                    result_identity = self.get_symbol_identity(call_result.symbol,call_result.file)
                    if result_identity == symbol_identity:
                        continue
                    else:
                        call_results.append(call_result) 
        return call_results
    