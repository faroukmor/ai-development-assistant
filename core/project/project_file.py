import os 
import core.project.file_reader as fr

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
        self.stem , self.ext = os.path.splitext(self.name)
        self.stem = self.stem.lower()
        self.size = os.path.getsize(path)
        self.keywords = self.stem.split("_")
        self.content = ""
        self.programming_language = EXTENSION_MAP.get(self.ext.lower(), "unknown")
        self.last_time_edited = os.path.getmtime(path) 
        self.symbols = None
    def read_content(self):
        self.content = fr.read(self.path)


def files_to_objects(files_list):
    files_obj = []
    for file in files_list:
        files_obj.append(ProjectFile(file))
        
    return files_obj

