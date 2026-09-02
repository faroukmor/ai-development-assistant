import core.context.context_builder as PCB
import core.llm.llm_client as llm_client
import core.project.project_indexer as PI
import core.retrieval.hybrid_retriever as HR
class AIDevelopmentAssistant:
    def __init__(self,project):
        self.project = project

    def ask(self,user_prompt):
        PI.ProjectIndexer(self.project).build()
        
        retriever = HR.HybridRetriever(self.project)

        retrievers = retriever.search(user_prompt)
        
        context = PCB.ProjectContextBuilder(self.project,retrievers).build_context()
        messages = [
                    {
                        "role": "system",
                        "content": """You are an AI Development Assistant specialized in software engineering.
Rules:
- Answer ONLY using the provided project context.
- Never invent relationships between files, classes, functions, or calls.
- Distinguish between facts explicitly present in the context and assumptions.
- Answer the user's question directly.
- Do not repeat the question.
- Do not provide generic explanations unless they are necessary.
- Do not describe your reasoning process.
- Prefer concrete project facts over general programming knowledge.
- Mention file names and symbol names when relevant.
- If the context does not contain enough information, say:
"I don't have enough information from the current project context."
- Keep the answer concise.
- Use short paragraphs or bullet points when appropriate.
"""
                    },
                    {
                    "role": "system",
                    "content": f"""Project Context
The following information describes the current software project.
Use it as your only source of truth.
{context}"""
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
        model = llm_client.LLMClient('qwen2.5-coder:3b')
        response = model.ask(messages)
        return response
