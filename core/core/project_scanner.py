import os


path = ""
IGNORED = {".git", "__pycache__", "venv", ".idea", ".vscode", ".gitignore"}
def scan_project(path):
    elements_list = []
    for f in os.listdir(path):
        if f in IGNORED or f.startswith("."): 
            continue

        full_path = os.path.join(path, f)
        if os.path.isdir(full_path):
            elements_list.append(full_path+ os.sep)
            elements_list.extend(scan_project(full_path))
        else:
            elements_list.append(full_path)
            
    return elements_list

def get_files(elements):
    files_list = []
    for f in elements:
        if not os.path.isdir(f):
            files_list.append(f)
    return files_list

def get_directories(elements):
    dir_list = []
    for f in elements:
        if os.path.isdir(f):
            dir_list.append(f)
    return dir_list

