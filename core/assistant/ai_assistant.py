import core.context.project_context_builder as PCB
import core.llm.llm_client as llm_client
import core.project.project_indexer as PI
import core.context.context_selector as cs
class AIDevelopmentAssistant:
    def __init__(self,project):
        self.project = project

    def ask(self,user_prompt):
        PI.ProjectIndexer(self.project).build()
        
        selector = cs.ContextSelector(self.project)

        relevant_files = selector.get_relevant_files(user_prompt)

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
        model = llm_client.LLMClient('qwen2.5:3b')
        response = model.ask(messages)
        return response
