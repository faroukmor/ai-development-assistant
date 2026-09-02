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
Retrieval (File Search + Symbol Search)
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
├── retrieval/   File search, symbol search, hybrid retriever
├── context/     Context builders: files, symbols, dependencies
├── llm/         Ollama client
└── assistant/   Top-level orchestrator: ask → answer
```

## Requirements

- Python 3.10 or newer
- Ollama running locally with a model (default: `qwen2.5-coder:3b`)
- Python packages: `ollama`, `rich`

## Run

```
pip install ollama rich
ollama pull qwen2.5-coder:3b
python main.py
```

Note: the project path to analyze is set at the top of `main.py` (`project_path`).

Type a question about the analyzed project and press Enter. Type `q` to quit.

## Development Status

The project follows a phase-based roadmap with clear priorities:

See [docs/roadmap.md](docs/roadmap.md)

## License

MIT
