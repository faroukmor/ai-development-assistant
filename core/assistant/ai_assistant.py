from core.context.context_builder import ProjectContextBuilder
from core.llm.llm_client import LLMClient
from core.project.project import Project
from core.project.project_indexer import ProjectIndexer
from core.retrieval.embedding_search import EmbeddingSearch
from core.retrieval.hybrid_retriever import HybridRetriever


DEFAULT_MODEL = "qwen2.5-coder:3b"


class AIDevelopmentAssistant:
    def __init__(self,project_path,llm_client=None):
        self.project = Project(project_path)
        self.embedding_search = None
        self.llm_client = llm_client

    @property
    def model_info(self):
        """Which model answers right now, and where it runs."""
        if self.llm_client is None:
            return f"{DEFAULT_MODEL} (Ollama, local)"
        base = self.llm_client.base_url.split("//")[-1].rstrip("/")
        return f"{self.llm_client.model_name} ({base}, external)"

    def _prepare_context(self, question):
        """Index the project, retrieve relevant code, and assemble its context."""
        ProjectIndexer(self.project).build()

        if self.embedding_search is None:
            self.embedding_search = EmbeddingSearch(self.project)
            self.embedding_search.build_index()

        retriever = HybridRetriever(self.project, self.embedding_search)
        retrieval_results = retriever.search(question)

        return ProjectContextBuilder(self.project, retrieval_results).build_context()

    def _build_messages(self, context, question):
        """Assemble the prompt sent to the model, with the context as source of truth."""
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
        """The client that talks to a model: the external one if configured, Ollama otherwise."""
        return self.llm_client or LLMClient(DEFAULT_MODEL)

    def answer(self, question):
        messages = self._build_messages(self._prepare_context(question), question)
        return self._llm().ask(messages)

    def answer_stream(self, question):
        """Yield the answer incrementally; the setup runs inside the first next()."""
        messages = self._build_messages(self._prepare_context(question), question)
        yield from self._llm().ask_stream(messages)
