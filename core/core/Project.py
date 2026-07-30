import project_scanner as ps
import projectFile
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
        

    def load_files(self):
        elements = ps.scan_project(self.path)
        files = ps.get_files(elements)

        self.files = projectFile.files_to_objects(files)


    def build_index(self):
        for file in self.files:
            if file.programming_language in self.languages:
                self.languages[file.programming_language] += 1
                if file.name.lower() == "readme.md": 
                                self.readme = file.path
            else:
                self.languages["unknown"] += 1

            
            self.total_size += file.size

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
