from core.context.context_builder import ProjectContextBuilder
from core.llm.llm_client import LLMClient
from core.project.project import Project
from core.project.project_indexer import ProjectIndexer
from core.retrieval.embedding_search import EmbeddingSearch
from core.retrieval.hybrid_retriever import HybridRetriever


DEFAULT_MODEL = "qwen2.5-coder:1.5b"


class AIDevelopmentAssistant:
    def __init__(self,project_path,llm_client=None):
        self.project = Project(project_path)
        ProjectIndexer(self.project).build()
        self.embedding_search = None
        self.llm_client = llm_client

    @property
    def model_info(self):
        """Model name and where it runs."""
        if self.llm_client is None:
            return f"{DEFAULT_MODEL} (Ollama, local)"
        base = self.llm_client.base_url.split("//")[-1].rstrip("/")
        return f"{self.llm_client.model_name} ({base}, external)"

    def _prepare_context(self, question):
        """Build the context for a question: index, retrieve, assemble."""
        if self.embedding_search is None:
            self.embedding_search = EmbeddingSearch(self.project)
            self.embedding_search.build_index()

        retriever = HybridRetriever(self.project, self.embedding_search)
        retrieval_results = retriever.search(question)

        return ProjectContextBuilder(self.project, retrieval_results).build_context()

    def _build_messages(self, context, question):
        """Build the message list sent to the model."""
        return [
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
                        "content": question + (
                            "\n\n(Answer using ONLY the project context above. "
                            "Reply in the same language as the user's question. "
                            "If the context does not cover this question, say: "
                            "\"I don't have enough information from the current project context.\")"
                        )
                    }
                ]

    def _llm(self):
        """The configured client, or a local Ollama one."""
        return self.llm_client or LLMClient(DEFAULT_MODEL)

    def answer(self, question):
        messages = self._build_messages(self._prepare_context(question), question)
        return self._llm().chat(messages)

    def answer_stream(self, question):
        """Yield the answer in chunks; the context is built on the first next()."""
        messages = self._build_messages(self._prepare_context(question), question)
        yield from self._llm().chat_stream(messages)
