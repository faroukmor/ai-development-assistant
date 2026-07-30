EXTENSION_MAP = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.cpp': 'C++',
        '.c': 'C',
        '.java': 'Java',
        '.rb': 'Ruby',
        ".json": "JSON",
        ".md": "Markdown",
        '.go': 'Go',
        '.rs': 'Rust',
        '.html': 'HTML',
        '.css': 'CSS'
}
for ext in EXTENSION_MAP:
    print(ext + "  " + EXTENSION_MAP[ext])