import core.context.project_context_builder as PCB
import core.llm.llm_client as llm_client
import core.project.project_indexer as PI
import core.retrieval.hybrid_retriever as HR
class AIDevelopmentAssistant:
    def __init__(self,project):
        self.project = project

    def ask(self,user_prompt):
        PI.ProjectIndexer(self.project).build()
        
        retriever = HR.HybridRetriever(self.project)

        results = retriever.search(user_prompt)
        for result in results:
            print(f"{result.file.name=}")
            print(f"{result.score=}")
            print(f"{result.reason=}")

        relevant_files = [r.file for r in results]

        
        context = PCB.ProjectContextBuilder(self.project,relevant_files).build_context()
        messages = [
                    {
                        "role": "system",
                        "content": """
                You are an AI Development Assistant specialized in software engineering.

                Rules:
                - Always answer in English.
                - Base your answers ONLY on the provided project context.
                - Never invent information.
                - If the answer cannot be inferred from the context, say:
                "I don't have enough information from the current project context."
                - When possible, mention relevant file names, classes, or functions.
                - Keep answers concise and technical.
                """
                    },
                    {
                    "role": "system",
                    "content": f"""
                    Project Context

                    The following information describes the current software project.

                    Use it as your only source of truth.

                    {context}
                    """
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
        exit
        model = llm_client.LLMClient('qwen2.5:3b')
        response = model.ask(messages)
        return response
