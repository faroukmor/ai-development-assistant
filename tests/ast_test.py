import ast 

"""
code = ""
import core.project.symbol as S
import ast

class SymbolAnalyzer:
    def __init__(self, project):
        self.project = project

    def detect_python_symbols(self, file):
        Classes = []
        Functions = []
        AsyncFunction = []

        with open(file.path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                Classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                Functions.append(node.name)
            elif isinstance(node, ast.AsyncFunctionDef):
                AsyncFunction.append(node.name)

    def detect_java_symbols(self, file):
        pass

    def detect_symbols(self):
        for file in self.project.files:
            if file.programming_language == "Python":
                self.detect_python_symbols(file)
            elif file.programming_language == "Java":
                self.detect_java_symbols(file)
""
Classes = []
Functions = []
AsyncFunction = []


tree = ast.parse(code)

for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        Classes.append(node.name)
    elif isinstance(node, ast.FunctionDef):
        Functions.append(node.name)
    elif isinstance(node, ast.AsyncFunctionDef):
        AsyncFunction.append(node.name)

print("Classes:", Classes)
print("Functions:", Functions)
print("Async Functions:", AsyncFunction)
"""


source = """
def hello(name):
    print(name)
    self.calculate(name)
    obj.service.save(name)
    obj.service.save.value()
"""

tree = ast.parse(source)

class CallVisitor(ast.NodeVisitor):

    def visit_Call(self, node):
        parts = []
        current = node.func
        while not isinstance(current, ast.Name):
            parts.append(current.attr)
            current = current.value

        parts.append(current.id) 
        parts.reverse()
        call_name = ".".join(parts)
        print(call_name)

visitor = CallVisitor()
visitor.visit(tree)