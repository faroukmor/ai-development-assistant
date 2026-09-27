import os 
from typing import Optional

from core.project.project_file import ProjectFile


class Project:
    def __init__(self,path):
        self.name = os.path.basename(path)
        self.path = path
        self.files: Optional[list[ProjectFile]] = None
        self.readme: Optional[ProjectFile] = None
        self.total_size = 0
        self.type: Optional[str] = None
        self.entry_points = []
        self.structure = None
        self.dependencies = []
        self.languages = {
        'Python'     : 0,
        'JavaScript' : 0,
        'TypeScript' : 0,
        'C++'        : 0,
        'C'          : 0,
        'Java'       : 0,
        'Ruby'       : 0,
        "JSON"       : 0,
        "Markdown"   : 0,
        'Go'         : 0,
        'Rust'       : 0,
        'HTML'       : 0,
        'CSS'        : 0,
        "unknown"    : 0
}
        self.is_indexed = False
        self.analysis_errors = []

    
    def get_file_by_path(self,path):
        for file in (self.files or []): 
            if path == file.path:
                return file

        return None

    def get_files_by_language(self,language_name):
        files = []
        for file in (self.files or []):
            if language_name == file.programming_language:
                files.append(file)

        return files
