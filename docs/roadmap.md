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
- [ ] Prevent dependency cycles
- [ ] Prevent repeated dependency expansion
- [ ] Define maximum dependency depth
- [ ] Implement recursive dependency expansion
- [ ] Test `A → B`
- [ ] Test `A → B → C`
- [ ] Test `A → B → C → D`
- [ ] Test circular dependencies

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
- [ ] Handle `snake_case`
- [ ] Handle `CamelCase`
- [ ] Handle dotted names
- [ ] Improve file/symbol scoring
- [ ] Improve result ranking
- [ ] Add semantic/embedding search
- [ ] Compare keyword retrieval with embedding retrieval
- [ ] Integrate embedding search into `HybridRetriever`

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
- [ ] Add context formatting tests
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
- [ ] Accept project path from the user
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

1. [x] Filter call targets by class hint from the full call chain
2. Implement recursive dependency resolution
3. Prevent dependency cycles
4. Define maximum dependency depth
5. Finalize the context structure
6. Test context quality
7. Improve retrieval
8. Add semantic/embedding search
9. Improve project-wide reasoning
