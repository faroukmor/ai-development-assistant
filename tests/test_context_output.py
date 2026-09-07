import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.project.project import Project
from core.context.context_builder import ProjectContextBuilder
from core.context.context_formatter import ProjectContextFormatter

PROJECT_PATH = r"C:\Users\HP\Documents\PYTHON Project\ai-development-assistant"


class FakeFile:
    name = "fake_module.py"
    content = "def a():\n    pass\n"

    def read_content(self):
        pass


class FakeRetriever:
    symbol = None
    file = FakeFile()
    score = 0.9
    reason = "unit test"


class FakeReadme:
    content = "# Test Project\n\nFake readme for context output test."


def run_checks():
    project = Project(PROJECT_PATH)
    project.readme = FakeReadme()

    # Case 1: empty dependencies -> formatter must render an empty string
    project.dependencies = []
    formatter = ProjectContextFormatter(project)
    assert formatter.build_dependencies() == "", \
        "empty dependencies must render an empty string, not a dangling header"

    # Case 2: real dependencies -> full block with header and items
    project.dependencies = ["rich>=13.0", "ollama"]
    block = formatter.build_dependencies()
    assert block.startswith("Dependencies:\n"), \
        "non-empty dependencies must start with the Dependencies header"
    assert "rich>=13.0" in block and "ollama" in block, \
        "every dependency item must appear in the rendered block"

    # Case 3: full context build -> no dangling Dependencies header, no ==File==
    project.dependencies = []
    builder = ProjectContextBuilder(project, [FakeRetriever()])
    context = builder.build_context()

    assert "Dependencies:" not in context, \
        "dangling 'Dependencies:' header must be gone when there are no dependencies"
    assert "==File==" not in context, \
        "dangling '==File==' header must be gone when no file section is rendered"
    assert "Relevant Files:" in context, \
        "Relevant Files section must always be present when retrievers exist"
    assert "README:" in context and "# Test Project" in context, \
        "readme content must appear in the context when a readme exists"

    print("ALL CONTEXT OUTPUT CHECKS PASSED")


if __name__ == "__main__":
    run_checks()