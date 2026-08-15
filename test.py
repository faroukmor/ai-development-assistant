import ast

from core.analyzers.python_symbol_visitor import PythonSymbolVisitor


class FakeFile:
    def __init__(self):
        self.symbols = []


source = """
def test(name):
    print(name)
    self.save()
    obj.service.save()
    get_service().save()
    save(calculate(name))
"""


file = FakeFile()

tree = ast.parse(source)

visitor = PythonSymbolVisitor(file)
visitor.visit(tree)


for symbol in file.symbols:
    print(f"Symbol: {symbol.name}")
    print(f"Type: {symbol.type}")
    print(f"Parent: {symbol.parent.name if symbol.parent else None}")
    print(f"Calls: {symbol.calls}")
    print(f"Children: {[child.name for child in symbol.children]}")
    print("-" * 40)