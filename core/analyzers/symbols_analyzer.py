import core.analyzers.python_symbol_visitor as PSV
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

        visitor = PSV.PythonSymbolVisitor(file)
        visitor.visit(tree)
        

    def detect_java_symbols(self,file):
        pass

    def detect_symbols(self):
        for file in self.project.files:

            if file.programming_language == "Python":
                self.detect_python_symbols(file)

            elif file.programming_language == "Java":
                self.detect_java_symbols(file)