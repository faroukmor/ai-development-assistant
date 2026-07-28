import os 

EXTENSION_MAP = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.cpp': 'C++',
        '.c': 'C',
        '.java': 'Java',
        '.rb': 'Ruby',
        ".json": "JSON",
        ".md": "Markdown",
        '.go': 'Go',
        '.rs': 'Rust',
        '.html': 'HTML',
        '.css': 'CSS'
}

class ProjectFile:
    def __init__(self,path):
        self.path = path
        self.name = os.path.basename(path)
        _ , self.ext = os.path.splitext(path)
        self.size = os.path.getsize(path)
        self.content = ""
        self.programming_language = EXTENSION_MAP.get(self.ext.lower(), "unknown")
        self.last_time_edited = os.path.getmtime(path) 
    


