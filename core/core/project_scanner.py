import os
import projectFile as pf
path = "C:\\Users\\HP\\Documents\\PYTHON Project\\ai-development-assistant"

IGNORED = {".git", "__pycache__", "venv", ".idea", ".vscode", ".gitignore"}
def scan_project(path):
    files_list = []
    for f in os.listdir(path):
        if f in IGNORED or f.startswith("."): 
            continue

        full_path = os.path.join(path, f)
        if os.path.isdir(full_path):
            files_list.append(full_path+ os.sep)
            files_list.extend(scan_project(full_path))
        else:
            files_list.append(full_path)
            
    return files_list


def scan_project_obj(path):
    files_obj = []
    files_list = scan_project(path)
    
    for file in files_list:
        files_obj.append(pf.ProjectFile(file))
        
    return files_obj

"""def get_files_path(path):
    files_list = []
    files_obj = []
    for f in os.listdir(path):
        if f in IGNORED or f.startswith("."): 
            continue

        full_path = os.path.join(path, f)
        if os.path.isdir(full_path):
            files_list.extend(scan_project(full_path))
        else:
            files_list.append(full_path)
    

    return files_files"""
