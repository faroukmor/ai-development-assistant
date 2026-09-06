import core.analyzers.python_symbol_visitor as PSV

class SymbolAnalyzer:
    def __init__(self, project):
        self.project = project
        
    def detect_symbols(self):
        for file in self.project.files:

            if file.programming_language == "Python":
                PSV.PythonSymbolVisitor(file).analyze()

            elif file.programming_language == "Java":
                print("this program doesn`t support JAVA for now")