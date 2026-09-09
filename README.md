# AI Development Assistant

An offline AI-powered software engineering assistant.

The goal of this project is to build an intelligent assistant capable of understanding software projects instead of simply answering questions.

Unlike traditional AI chatbots, the assistant builds knowledge about an entire codebase and helps developers navigate, understand, maintain, and improve it.

## How It Works

```
Project
   ↓
Project Scanner
   ↓
Project Indexer
   ↓
Code Analysis (AST)
   ↓
Symbols + Calls + Relationships
   ↓
Retrieval (File Search + Symbol Search + Semantic Embedding Search)
   ↓
Dependency Resolution
   ↓
Context Construction
   ↓
Local LLM (Ollama)
   ↓
Codebase-Aware Answer
```

## Project Structure

```
core/
├── project/     Scanning, loading, indexing, file and symbol models
├── analyzers/   AST analysis: project type, entry points, symbols, calls
├── retrieval/   Keyword search, semantic embedding search, hybrid ranking
├── context/     Context builders: files, symbols, dependencies
├── llm/         Ollama client
└── assistant/   Top-level orchestrator: ask → answer
```

## Requirements

- Python 3.10 or newer
- Ollama running locally with:
  - a chat model (default: `qwen2.5-coder:1.5b`)
  - an embedding model: `nomic-embed-text`
- Python packages: `ollama`, `rich`, `numpy`

## Run

```
pip install ollama rich numpy
ollama pull qwen2.5-coder:1.5b
ollama pull nomic-embed-text
python main.py
```

Note: on launch the assistant asks for a project path — press Enter to
analyze the default project (`DEFAULT_PROJECT_PATH` at the top of `main.py`),
or type any other project path.

Type a question about the analyzed project and press Enter. Type `q` to quit.

## Development Status

The project follows a phase-based roadmap with clear priorities:

See [docs/roadmap.md](docs/roadmap.md)

## License

MIT
