import core.retrieval.hybrid_retriever as HR
import core.project.project as P
import core.project.project_indexer as PI


path = r"C:\Users\HP\Documents\PYTHON Project\ai-development-assistant"
project = P.Project(path)

PI.ProjectIndexer(project).build()
for file in project.files:

    for symbol in file.symbols:
        print(symbol.name)

        if symbol.parent:
            print(" parent:", symbol.parent.name)

        print(" children:", [c.name for c in symbol.children])


