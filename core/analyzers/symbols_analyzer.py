from core.analyzers.python_symbol_visitor import PythonSymbolVisitor

class SymbolAnalyzer:
    def __init__(self, project):
        self.project = project
        
    def detect_symbols(self):
        for file in (self.project.files or []):

            if file.programming_language == "Python":
                try:
                    PythonSymbolVisitor(file).analyze()
                except Exception as e:
                    # one bad file must not abort the whole scan
                    self.project.analysis_errors.append(
                        (file.path, type(e).__name__, str(e))
                    )

            elif file.programming_language == "Java":
                print("this program doesn`t support JAVA for now")