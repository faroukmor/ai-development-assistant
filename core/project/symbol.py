class Symbol:
    def __init__(self,name,symbol_type,line,parent=None,signature=None,docstring=None):
        self.name = name
        self.type = symbol_type
        self.line = line
        self.parent = parent
        self.children = []
        self.signature = signature
        self.docstring = docstring
