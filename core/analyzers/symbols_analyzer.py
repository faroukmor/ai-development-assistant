import core.project.symbol as S
import ast

class SymbolAnalyzer:
    def __init__(self, project):
        self.project = project


    

    def detect_python_symbols(self,file):

        with open(file.path, "r", encoding="utf-8") as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                sym = S.Symbol(name=node.name,symbol_type="class",line=node.lineno)
                file.symbols.append(sym)
            elif isinstance(node, ast.FunctionDef):
                sym = S.Symbol(name=node.name,symbol_type="function",line=node.lineno)
                file.symbols.append(sym)
            elif isinstance(node, ast.AsyncFunctionDef):
                sym = S.Symbol(name=node.name,symbol_type="async_function",line=node.lineno)
                file.symbols.append(sym)


    def detect_java_symbols(self,file):
        pass

    def detect_symbols(self):
        for file in self.project.files:

            if file.programming_language == "Python":
                self.detect_python_symbols(file)

            elif file.programming_language == "Java":
                self.detect_java_symbols(file)