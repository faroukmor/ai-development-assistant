import os 


class Project:
    def __init__(self,path):
        self.name = os.path.basename(path)
        self.path = path
        self.files = None
        self.readme = None
        self.total_size = 0
        self.type = None
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

    
    def get_file_by_path(self,path):
        for file in self.files: 
            if path == file.path:
                return file

        return None

    def get_files_by_language(self,language_name):
        files = []
        for file in self.files:
            if language_name == file.programming_language:
                files.append(file)

        return files

#just for testing
"""
path = "C:\\Users\\HP\\Documents\\PYTHON Project\\ai-development-assistant"
project  = Project(path)
print(f"{project.name=}")
print(f"{project.languages=}")
project.load_files()
project.build_index()
for file in project.files:
     print(file.name)
"""
