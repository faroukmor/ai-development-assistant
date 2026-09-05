import os

# Dotted entries (.git, .idea, .vscode, .gitignore, ...) are already skipped
# by the startswith(".") check below; these are the non-dotted ones.
IGNORED = {"__pycache__", "venv"}


def walk_paths(path):
    files = []
    directories = []
    for entry in os.listdir(path):
        if entry in IGNORED or entry.startswith("."):
            continue

        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            directories.append(full_path)
            sub_files, sub_directories = walk_paths(full_path)
            files.extend(sub_files)
            directories.extend(sub_directories)
        else:
            files.append(full_path)

    return files, directories

