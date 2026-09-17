# AI Development Assistant — Roadmap

> Rule: no goal without a real failing case or a real user need.
> The benchmark is the referee — every fix must be measurable through it.

## Achievements — shipped in v0.1 (tag: v0.1)

### Analysis & indexing
- [x] Scan project files; detect project type, languages, entry points, dependencies
- [x] Parse Python files with `ast`: classes, functions, nested structures
- [x] Extract signatures, docstrings, parent/child relations, calls
- [x] Hardened scanner (`walk_paths` returns files + directories as a pair)

### Retrieval → context
- [x] Separated builders: `ProjectContextBuilder`, `ProjectContextFormatter`, `FileContextBuilder`, `SymbolContextBuilder`, `SymbolDependencyBuilder`
- [x] Relevant files + symbols retrieved; exact source and metadata in the context
- [x] Calls resolved to target symbols with their source
- [x] Stable context format (`===Project===` / `===SYMBOL===` / Relevant Files)
- [x] Dangling headers cleaned; no-README crash fixed; context repetition reduced

---

### Dependency resolution
- [x] Exclude the caller from its own call targets
- [x] Filter call targets by class hint from the full call chain
- [x] `Class.method()` and `self.method()` resolved via variable bindings
- [x] Reliable resolution — verified through the retrieval benchmark
- [x] Same symbol never rendered twice; caller excluded from its targets
- [x] Method source skipped when its parent class is already rendered

### Context quality
- [x] Stable hierarchy: project header → primary symbols → called symbols
- [x] Relevant symbols prioritized (merge by max score, deterministic order)
- [x] Context quality tested with real project questions

### Retrieval quality
- [x] Tokenizer: `snake_case`, `CamelCase`, dotted names, stopwords
- [x] Small stem map (`built→build`, `files→file`, `reads→read`, …)
- [x] Semantic embedding search (batch `/api/embed` — 115 symbols in ~7s), integrated into `HybridRetriever`
- [x] Named scoring constants; merge by max score; partial-name duplicates dropped
- [x] Benchmark: 10/10 keyword, 2/2 semantic (`--semantic`)

---

### LLM interaction

---

### LLM interaction
- [x] Ollama client connected; grounded system prompt + grounding suffix near the question
- [x] Consistent refusal when the context does not cover the question
- [x] Friendly errors: Ollama down / model missing; `num_ctx` = 32k; embedding timeout
- [x] Model evaluation: `1.5b` default (fast), `3b` for depth

### Testing & tooling
- [x] `PythonSymbolVisitor`, call extraction, nested-structure tests
- [x] Context formatting tests; end-to-end context check
- [x] Keyword + semantic retrieval benchmarks; context token counter

### CLI
- [x] Basic CLI with panels and markdown rendering
- [x] Interactive project path (Enter = default project)
- [x] Quit command (`q` / `ض`)

---

## Track 1 — Survive a real, larger project

The system has only ever been tested on itself (56 files).
Goal: survive a codebase 5–10× larger without quality or speed collapse.

- [ ] Run the assistant on a real open-source Python project (300+ files) and record every breakage
- [ ] Measure and record on that project: index time, embedding build time, retrieval latency, LLM latency
- [ ] Per-project embedding cache on disk (revisit the "no cache needed" decision with measured numbers)
- [ ] Re-index only changed files (content hash)
- [ ] Token budget guard: warn above 75% of the window (`token_counter.py` becomes a runtime check)
- [ ] Context trimming policy: docstrings first, then sources — never signatures
- [ ] Clear separation of primary symbols vs dependency symbols in the context
- [ ] Distinguish project symbols from external/library calls in the context
- [ ] Make context fully deterministic (stable ordering at every stage)

Exit criterion: a correct, grounded answer about that project with context under 75%.

---

## Track 2 — Close the measured retrieval gaps

Every documented failure in the benchmark becomes a passing case.

- [ ] Enrich embedding text (`name + signature + docstring`) — attack the three documented semantic misses
- [ ] Re-evaluate `THRESHOLD` with evidence from the semantic suite
- [ ] Multilingual questions: one explicit decision — defer in writing, or adopt a cross-lingual embedding model
- [ ] Handle nested classes/functions correctly in dependency resolution
- [ ] Unit tests for `SymbolDependencyBuilder` and `SymbolContextBuilder` accuracy

---

## Track 3 — Answer quality (the user's actual experience)

The benchmark measures retrieval. Nothing measures answers yet.

- [ ] Answer-level rubric: expected facts per benchmark question, judged by hand, recorded
- [ ] Answers must cite `file:symbol` consistently — mechanically checkable
- [ ] Tighten answer verbosity (`num_predict`, prompt) using the rubric
- [ ] `/model` command: `1.5b` (fast) ↔ `3b` (deep) — speed/quality in the user's hands

---

## Track 4 — Ship as a tool

Goal: someone who is not the author can install and use it.

- [ ] `pyproject.toml` → pip installable
- [ ] CLI polish: readable sections, syntax highlighting, progress indicators
- [ ] CLI commands: `/files`, `/symbols`, `/context`, `/help`
- [ ] Logging/debug mode
- [ ] README install path verified on a clean machine

Exit: tag `v0.2`.

---

## Future — advanced code understanding

- [ ] Complete symbol dependency graph
- [ ] Resolve imports, module-level references, aliases
- [ ] Resolve inheritance and method overrides
- [ ] Track references beyond calls; variable/reference relationships
- [ ] Support additional programming languages
- [ ] Code-change awareness; project-wide reasoning

---

## Deferred

Moved here on 2026-09-03: no real question has failed because of missing
transitive context yet, and recursive expansion multiplies context size
before the current context quality is proven. The roadmap is a record,
not a boss — revisit when a real question shows missing `A → B → C` context.

- [ ] Implement recursive dependency expansion
- [ ] Prevent repeated dependency expansion
- [ ] Prevent dependency cycles
- [ ] Define maximum dependency depth
- [ ] Test `A → B → C`
- [ ] Test `A → B → C → D`
- [ ] Test circular dependencies
