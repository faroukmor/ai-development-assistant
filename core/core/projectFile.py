import os 
class ProjectFile:
    def __init__(self,path):
        self.path = path
        self.name = os.path.basename(path)
        self.ext = os.path.splitext(path)[1]
        self.size = os.path.getsize(path)
        self.content = ""
        self.programingLanguage = "unknown"
        if self.ext == ".py": self.programingLanguage = "Python" 
        if self.ext == ".c": self.programingLanguage = "C" 
        if self.ext == ".json": self.programingLanguage = "Json" 
        if self.ext == ".java": self.programingLanguage = "Java" 
        if self.ext == ".md": self.programingLanguage = "Mark down" 
        self.last_time_edited = os.path.getmtime(path) 
    


