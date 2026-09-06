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
        # unique identity across the project, in the form file:name:parent
        parent = symbol.parent.name if symbol.parent != None else ""
        return f"""{file.name}:{symbol.name}:{parent}"""
    
    def parse_call(self, call, symbol):
        parts = call.replace("()", "").split(".")
        if len(parts) >= 2 and parts[-2] in symbol.variable_bindings:
            parts[-2] = symbol.variable_bindings[parts[-2]]
        return parts

    def filter_matches(self, matches, parts, caller_identity):
        owner = parts[-2] if len(parts) >= 2 else None
        if owner in self.class_names:
            return [match for match in matches if match.symbol.parent.name == owner]
        return [match for match in matches
                if self.get_symbol_identity(match.symbol, match.file) != caller_identity]

    def find_call_symbols(self, symbol, file):
        caller_identity = self.get_symbol_identity(symbol, file)
        call_results = []
        for call in symbol.calls:
            parts = self.parse_call(call, symbol)
            matches = self.symbol_search.find_by_name(parts[-1])
            call_results.extend(self.filter_matches(matches, parts, caller_identity))
        return call_results
    