import project_scanner as prs
import os
import projectFile as pf

def read_file(file_path):
    if os.path.isdir(file_path):
        return 
    
    with open(file_path, encoding="utf-8") as f:
        file_content = f.read()
    return file_content


def read_file_obj(file):
    if os.path.isdir(file.path):
        return 
    
    with open(file.path, encoding="utf-8") as f:
        file.content = f.read()


path = r"C:\Users\HP\Documents\PYTHON Project\ai-development-assistant"
files = prs.scan_project(path)


file = pf.ProjectFile(files[3])
print(file.path)
print(file.name)
print(file.ext)
print(file.size)
print(file.programingLanguage)
print(file.last_time_edited)

read_file_obj(file)

print(file.content)