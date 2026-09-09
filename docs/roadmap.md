# AI Development Assistant — Roadmap

## Phase 1 — Codebase Analysis

- [x] Scan project files
- [x] Detect project type
- [x] Detect programming languages
- [x] Detect entry points
- [x] Detect dependencies
- [x] Parse Python files using `ast`
- [x] Detect classes
- [x] Detect functions
- [x] Detect nested classes/functions
- [x] Extract function signatures
- [x] Extract docstrings
- [x] Extract parent/child relationships
- [x] Extract function/method calls
- [x] Improve callable-name extraction
- [x] Create `SymbolSearch`
- [x] Create `FileSearch`
- [x] Create `HybridRetriever`

---

## Phase 2 — Retrieval → Context

- [x] Separate context responsibilities
  - [x] `ProjectContextBuilder`
  - [x] `ProjectContextFormatter`
  - [x] `FileContextBuilder`
  - [x] `SymbolContextBuilder`
  - [x] `SymbolDependencyBuilder`
- [x] Retrieve relevant files
- [x] Retrieve relevant symbols
- [x] Extract exact symbol source
- [x] Add symbol metadata to context
- [x] Add direct calls to context
- [x] Resolve calls → target symbols
- [x] Add target symbol source to context
- [x] Remove obvious duplicate called symbols
- [ ] Clean and standardize context structure
- [ ] Reduce unnecessary context repetition
- [ ] Define a stable context format

---

## Phase 3 — Symbol Dependency Graph

- [x] Exclude the caller itself from its call targets
- [x] Filter call targets by class hint from the full call chain
- [ ] Make `SymbolDependencyBuilder` resolve calls reliably
- [ ] Distinguish project symbols from external/library calls
- [ ] Handle `Class.method()` correctly
- [ ] Handle `self.method()` correctly
- [ ] Handle nested classes/functions correctly
- [ ] Test `A → B`

---

## Phase 4 — Context Quality

- [ ] Design final context hierarchy
- [ ] Separate primary symbols from dependency symbols
- [ ] Mark dependency depth
- [x] Prevent the same symbol from appearing multiple times
- [ ] Deduplicate method source included inside its containing class source
- [ ] Prioritize relevant symbols
- [ ] Limit context size
- [ ] Add source truncation for large symbols
- [ ] Make context deterministic
- [ ] Test context quality with real project questions

---

## Phase 5 — Retrieval Quality

- [ ] Improve filename matching
- [ ] Improve symbol-name matching
- [ ] Improve query tokenization
- [x] Handle `snake_case`
- [x] Handle `CamelCase`
- [x] Handle dotted names
- [x] Handle simple inflections (`built→build`, `files→file`)
- [x] Add semantic/embedding search (batch `/api/embed` — 115 symbols in ~7s)
- [x] Integrate embedding search into `HybridRetriever`
- [ ] Improve file/symbol scoring
- [ ] Improve result ranking

---

## Phase 6 — LLM Interaction

- [x] Connect LLM client
- [x] Create system prompt
- [x] Force context-only answers
- [x] Prevent unsupported claims
- [x] Evaluate and select the best local model
- [ ] Improve system prompt
- [ ] Improve answer formatting
- [ ] Reduce unnecessary verbosity
- [ ] Make answers reference files and symbols
- [ ] Handle insufficient-context responses consistently
- [ ] Test answer accuracy against the actual codebase

---

## Phase 7 — Testing

- [x] Test `PythonSymbolVisitor`
- [x] Test call extraction
- [x] Test nested structures
- [ ] Add `SymbolDependencyBuilder` tests
- [ ] Add recursive dependency tests
- [ ] Add duplicate dependency tests
- [ ] Add `SymbolContextBuilder` tests
- [x] Add context formatting tests
- [ ] Add retrieval tests
- [ ] Add end-to-end assistant tests
- [ ] Create a benchmark of project questions

---

## Phase 8 — User Interface

- [x] Basic CLI
- [ ] Improve CLI output formatting
- [ ] Add readable sections
- [ ] Add syntax highlighting
- [ ] Add loading/progress indicators
- [x] Accept project path from the user (interactive prompt, Enter = default)
- [ ] Add `/files` command
- [ ] Add `/symbols` command
- [ ] Add `/context` command
- [ ] Add `/help` command
- [ ] Add `/quit` command

---

## Phase 9 — Architecture & Performance

- [ ] Avoid rebuilding the entire project index for every question
- [ ] Cache project analysis
- [ ] Cache symbol relationships
- [ ] Re-index only changed files
- [ ] Separate indexing from querying
- [ ] Separate retrieval from context construction
- [ ] Separate context construction from LLM communication
- [ ] Add logging/debug mode
- [ ] Measure retrieval latency
- [ ] Measure context-building latency
- [ ] Measure LLM latency

---

## Phase 10 — Advanced Code Understanding

- [ ] Build a complete symbol dependency graph
- [ ] Resolve imports
- [ ] Resolve module-level references
- [ ] Resolve aliases
- [ ] Resolve inheritance
- [ ] Resolve method overrides
- [ ] Track symbol references beyond function calls
- [ ] Add variable/reference relationships
- [ ] Support additional programming languages
- [ ] Add code-change awareness
- [ ] Add project-wide reasoning

---

## Current Priority

1. [x] Clean context output — remove dangling `==File==` header and empty `Dependencies:` line
2. [x] Fix crash when the project has no README (`build_context` dereferences `readme.content` on `None` — found by `tests/test_context_output.py`)
3. [ ] Deduplicate method source included inside its containing class source
4. [x] Build a reference question benchmark (tests/retrieval_benchmark.py — 10/10)
5. [x] Test context quality with real project questions
6. [ ] Improve retrieval quality

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
