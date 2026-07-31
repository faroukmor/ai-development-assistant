import os

"""
def read_file(file):
    if os.path.isdir(file.path):
        return 
    
    with open(file.path, encoding="utf-8") as f:
        file.content = f.read()
"""
def read(file_path):
    if os.path.isdir(file_path):
        return 
    
    with open(file_path, encoding="utf-8") as f:
        file_content = f.read()
    return file_content


"""
path = r"C:\\Users\\HP\\Documents\\PYTHON Project\\ai-development-assistant"
files = prs.scan_project(path)

file = pf.ProjectFile(files[3])
print(file.path)
print(file.name)
print(file.ext)
print(file.size)
print(file.programming_language)
print(file.last_time_edited)

read(file)

print(file.content)
"""