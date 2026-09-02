import core.context.symbol_dependency_builder as SDB
class SymbolContextBuilder:
    def __init__(self,project,retrievers):
        self.project = project
        self.retrievers = retrievers
        self.dependency_builder = SDB.SymbolDependencyBuilder(self.project)
        
    

    def get_symbol_source(self, symbol, file):
        if not file.content:
            file.read_content()
    
        lines = file.content.splitlines()
    
        return "\n".join(
            lines[symbol.line - 1:symbol.end_line]
        )
    def get_symbol_calls(self, symbol):
        return "\n".join(
            f"- {call}"
            for call in symbol.calls
        )
        
    def format_symbol(self, symbol, file, already_called_symbols, score=None, reason=None):
        symbol_source = self.get_symbol_source(symbol, file)
        symbol_calls = self.get_symbol_calls(symbol)
        parent = symbol.parent.name if symbol.parent != None else ""
        current_symbol = f"""{file.name}:{symbol.name}:{parent}"""
        if current_symbol in already_called_symbols:
            return ""
        else:
            already_called_symbols.add(current_symbol)

        called_symbols = ""
        results = self.dependency_builder.find_call_symbols(symbol, file)

        i = 1
        for result in results:
            parent = result.symbol.parent.name if result.symbol.parent != None else ""
            called_symbol = f"""{result.file.name}:{result.symbol.name}:{parent}"""
            if called_symbol in already_called_symbols: 
                continue
            called_symbols += f"""{i}. {result.symbol.name}
Type: {result.symbol.type}
File: {result.file.name}
Signature: {result.symbol.signature}

Source:
{self.get_symbol_source(result.symbol,result.file)}

"""
            already_called_symbols.add(called_symbol)
            i += 1
        return f"""Name: {file.name}
Relevance: {score if score is not None else ""}
Reason: {reason if reason else ""}

===SYMBOL===
Name: {symbol.name}
Type: {symbol.type}
Signature: {symbol.signature}
Parent: {symbol.parent.name if symbol.parent else ""}
Docstring: {symbol.docstring}

Source:
{symbol_source}

calls:
{symbol_calls}

Called Symbols:
{called_symbols}
"""

    def build_symbol_context(self):
        symbol_context = ""
        already_called_symbols = set()
        for retriever in self.retrievers:
            if retriever.symbol:
                symbol_context += self.format_symbol(
                    symbol=retriever.symbol,
                    file=retriever.file,
                    already_called_symbols=already_called_symbols,
                    score=retriever.score,
                    reason=retriever.reason
                )

        return symbol_context