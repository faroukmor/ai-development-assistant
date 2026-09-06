import os

def read_file(file_path):
    if os.path.isdir(file_path):
        return 
    
    with open(file_path, encoding="utf-8") as f:
        file_content = f.read()
    return file_content

