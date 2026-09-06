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
        
    def format_symbol(self, symbol, file, rendered_identities, score=None, reason=None):
        symbol_source = self.get_symbol_source(symbol, file)
        symbol_calls = self.get_symbol_calls(symbol)
        
        symbol_identity = self.dependency_builder.get_symbol_identity(symbol, file)
        if symbol_identity in rendered_identities:
            return ""
        else:
            rendered_identities.add(symbol_identity)

        called_symbols_text = ""
        call_results = self.dependency_builder.find_call_symbols(symbol, file)

        i = 1
        for call_result in call_results:
            call_identity = self.dependency_builder.get_symbol_identity(call_result.symbol, call_result.file)
            if call_identity in rendered_identities: 
                continue
            called_symbols_text += f"""{i}. {call_result.symbol.name}
Type: {call_result.symbol.type}
File: {call_result.file.name}
Signature: {call_result.symbol.signature}

Source:
{self.get_symbol_source(call_result.symbol,call_result.file)}

"""
            rendered_identities.add(call_identity)
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
{called_symbols_text}
"""

    def build_symbol_context(self):
        symbol_context = ""
        rendered_identities = set()
        for retriever in self.retrievers:
            if retriever.symbol:
                symbol_context += self.format_symbol(
                    symbol=retriever.symbol,
                    file=retriever.file,
                    rendered_identities=rendered_identities,
                    score=retriever.score,
                    reason=retriever.reason
                )

        return symbol_context