import ast
import core.project.symbol as S
class PythonSymbolVisitor(ast.NodeVisitor):
    def __init__(self,file):
        super().__init__()
        self.file = file
        self.current_parent = None
        self.current_class = None

    def build_signature(self, node):
        args = [arg.arg for arg in node.args.args]
        return f"{node.name}({', '.join(args)})"

    def visit_ClassDef(self, node):
        sym = S.Symbol(
                        name=node.name,
                        symbol_type="class",
                        line=node.lineno,
                        end_line=node.end_lineno,
                        docstring=ast.get_docstring(node)
                        )
        old_class = self.current_class
        self.current_class = node.name

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
        self.current_class = old_class

    def get_callable_name(self, node):
        parts = []

        if isinstance(node, ast.Name):
            return node.id

        elif isinstance(node, ast.Attribute):
            parts.append(node.attr)
            parts.append(self.get_callable_name(node.value))
            
            
            parts.reverse()
            
            if None in parts:
                return None
            for i, part in enumerate(parts):
                if part == "self":
                    parts[i] = self.current_class
            return ".".join(parts)

        elif isinstance(node, ast.Call):
            call_name = self.get_callable_name(node.func)

            if call_name is None:
                return None

            return call_name + "()"

        elif isinstance(node, ast.Constant):
            return None


    def visit_Call(self, node):
        if self.current_parent:
            call_name = self.get_callable_name(node)

            if call_name is not None:
                self.current_parent.calls.append(call_name)

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        sym = S.Symbol(name=node.name,
                       symbol_type="function",
                       line=node.lineno,
                       end_line=node.end_lineno,
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
                        end_line=node.end_lineno,
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

    def visit_Assign(self, node):
        if self.current_parent is None:
            self.generic_visit(node)
            return

        if isinstance(node.value, ast.Call) and isinstance(node.targets[0], ast.Name):

            variable = node.targets[0].id

            call_name = self.get_callable_name(node.value)
            if call_name is not None:
                class_name = call_name.replace("()", "").split(".")[-1]

                self.current_parent.variable_bindings[variable] = class_name

        self.generic_visit(node)

