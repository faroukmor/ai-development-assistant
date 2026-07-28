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
        self.structure = None
        self.dependencies = None

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
            

path = "C:\\Users\\HP\\Documents\\PYTHON Project\\ai-development-assistant"

project  = Project(path)
print(f"{project.name=}")
print(f"{project.languages=}")
project.load_files()
project.build_index()
print(f"{project.languages=}")
print(f"{project.readme=}")
print(f"{project.total_size=}")

