class SymbolContextBuilder:
    def __init__(self,project,retrievers):
        self.project = project
        self.retrievers = retrievers
    

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
        
    def format_symbol(self, symbol, file, score=None, reason=None):
        symbol_source = self.get_symbol_source(symbol, file)
        symbol_calls = self.get_symbol_calls(symbol)
        return f"""
    File: {file.name}
    Relevance: {score if score is not None else ""}
    Reason: {reason if reason else ""}
    
    Symbol:
    Name: {symbol.name}
    Type: {symbol.type}
    Signature: {symbol.signature}
    Parent: {symbol.parent.name if symbol.parent else ""}
    Docstring: {symbol.docstring}
    Source:
    {symbol_source}
    calls:
    {symbol_calls}
    """

    def build_symbol_context(self):
        symbol_context = ""

        for retriever in self.retrievers:
            if retriever.symbol:
                symbol_context += self.format_symbol(
                    symbol=retriever.symbol,
                    file=retriever.file,
                    score=retriever.score,
                    reason=retriever.reason
                )

        return symbol_context