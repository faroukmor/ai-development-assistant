import core.retrieval.hybrid_retriever as HR
import core.project.project as P
import core.project.project_indexer as PI


path = r"C:\Users\HP\Documents\PYTHON Project\ai-development-assistant"
project = P.Project(path)

PI.ProjectIndexer(project).build()
results = HR.HybridRetriever(project).search("what is build , HybridRetriever")


