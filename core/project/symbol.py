class Symbol:
    def __init__(self,name,symbol_type,line,parent=None):
        self.name = name
        self.type = symbol_type
        self.line = line
        self.parent = parent
