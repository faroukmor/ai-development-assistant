import core.project.symbol as S

class SymbolAnalyzer:
    def __init__(self,project):
        self.project = project

    def detect_symbols(self):
        for file in self.project.files:
            file.symbols.append(S.Symbol())
        