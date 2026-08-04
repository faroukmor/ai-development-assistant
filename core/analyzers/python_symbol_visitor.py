import ast
import core.project.symbol as S
class PythonSymbolVisitor(ast.NodeVisitor):
    def __init__(self,file):
        super().__init__()
        self.file = file
        self.current_parent = None

    def build_signature(self, node):
        args = [arg.arg for arg in node.args.args]
        return f"{node.name}({', '.join(args)})"

    def visit_ClassDef(self, node):
        sym = S.Symbol(
                        name=node.name,
                        symbol_type="class",
                        line=node.lineno,
                        docstring=ast.get_docstring(node)
                        )

        if self.current_parent:
            sym.parent = self.current_parent
            self.current_parent.children.append(sym)

        self.file.symbols.append(sym)

        old_parent = self.current_parent
        self.current_parent = sym

        #دخلنا للدوال اللي داخل الكلاس
        self.generic_visit(node)

        #رجعنا الاب القديم 
        self.current_parent = old_parent

    def visit_FunctionDef(self, node):
        sym = S.Symbol(name=node.name,
                       symbol_type="function",
                       line=node.lineno,
                       parent=self.current_parent,
                       signature=self.build_signature(node),
                       docstring=ast.get_docstring(node)
        )
        
        if self.current_parent:
            self.current_parent.children.append(sym)
        
        self.file.symbols.append(sym)

        old_parent = self.current_parent
        self.current_parent = sym
        self.generic_visit(node)
        self.current_parent = old_parent

    def visit_AsyncFunctionDef(self, node):
        sym = S.Symbol( name=node.name,
                        symbol_type="async_function",
                        line=node.lineno,
                        parent=self.current_parent,
                        signature=self.build_signature(node),
                        docstring=ast.get_docstring(node)
        )
                
        if self.current_parent:
            self.current_parent.children.append(sym)
                
        self.file.symbols.append(sym)

        old_parent = self.current_parent
        self.current_parent = sym
        self.generic_visit(node)
        self.current_parent = old_parent