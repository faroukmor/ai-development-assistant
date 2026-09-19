# Track 1 findings — running on a real project

**Subject:** [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) at `--depth 1`
(911 files, 673 `.py`, 29 MB, 40,482 symbols).

**Command:**

```
python -m tests.project_bench "C:/Users/HP/Documents/PYTHON Project/bench/sqlalchemy" [--embed]
```

The subject is kept outside this repository (sibling `bench/` folder) so nothing
of it is ever committed here.

**Why it matters:** the project had only ever been run on itself (under 50
`.py` files, ~115 symbols at v0.1). The first run against SQLAlchemy failed
before producing a single result — the whole analysis died on one file.

---

## What held up

| Stage | Measured on 673 `.py` files |
|---|---|
| scan + index + AST analysis (`ProjectIndexer.build`) | 9.10s |
| files seen | 893 (673 Python, 220 unknown extension) |
| project type | Python |
| symbols | 40,482 (8,798 classes, 31,684 functions/methods) |
| symbols with a parent | 34,734 |
| symbols with a docstring | 6,372 |
| calls extracted | 183,130 |
| variable bindings | 31,759 |
| keyword retrieval | 0.13s per question, no failures |
| context for a real question | 23,606 chars / 5,036 tokens = **15.4%** of the 32k window |

Keyword retrieval and context building scale fine: sub-second and well under the
token budget. The failures were all in analysis and in the embedding build.

---

## Breakages found

### 1. A module-level `self` kills the symbol visitor — fatal

**Evidence (real files):**

```
lib/sqlalchemy/sql/base.py:295          self = self._generate()
lib/sqlalchemy/orm/collections.py:1139  self.insert(i + start, item)
```

Both sit in functions that take `self` as a plain parameter
(`def _generative(fn, self: _SelfGenerativeType, ...)`) — perfectly legal Python,
with no class in scope.

**Root cause:** `PythonSymbolVisitor.get_callable_name` resolved `self` by
looking up `self.current_class` and substituting it into the call name. Outside a
class that attribute is `None`, so a `None` was joined into the name:

```
TypeError: sequence item 0: expected str instance, NoneType found
```

**Impact:** the exception escaped `SymbolAnalyzer.detect_symbols` and aborted the
analysis of all 673 files. The very first bench run printed nothing but a
traceback — no symbols, no retrieval, no context.

**Fix:** when there is no class in scope the call is unresolvable and is dropped
(`return None`); an explicit `return None` now also documents what happens for
node types that have no name (`Subscript`, `Lambda`, ...).
Regression test: `tests/test_symbol_visitor.py` — after the fix
**673/673 files analyze cleanly, 0 recorded errors**.

### 2. One broken file aborted the entire project scan — fatal

**Root cause:** `SymbolAnalyzer.detect_symbols` called the visitor without a
guard, and `PythonSymbolVisitor.analyze` only caught `SyntaxError`. Any other
error (our `TypeError`, an `UnicodeDecodeError`, a `RecursionError` from a huge
nested literal) ended the whole project run.

**Fix:** per-file `try/except` in the analyzer; the failure is recorded on
`project.analysis_errors` as `(path, error_type, message)` so it stays visible
instead of vanishing. The test asserts that the broken file is reported *and*
that the other files still get their symbols.

### 3. The embedding build dies on a real project — fatal and silent

**Evidence:**

```
(get_embeddings) Error: timed out

FAILURE in embedding build: TypeError: 'NoneType' object is not iterable
```

**Root cause:** `build_index` sent **one** `/api/embed` request containing all
40,482 symbol texts, with a 60s timeout. `get_embeddings` swallowed the timeout,
returned `None`, and `zip(entries, None)` raised.

**Measured ceiling of one request** (scratch probe, not committed):

| texts in one request | result |
|---|---|
| 32 | 3.8s |
| 512 | 26.0s (19.7 texts/s) |
| 2048 | **HTTP 400 Bad Request** |

**Impact:** semantic search is completely unavailable on a large project, and it
did not fail loudly — retrieval silently degraded to keyword-only. Worse, every
query still paid an embedding round trip against an empty index: 0.13s →
**2.24s** per question for identical keyword results.

**Fix:** embed in batches of 256 (safe margin: 512 works, 2048 is rejected),
timeout 120s per batch, progress printed every 10 batches, and a clear
`embedding index unavailable — semantic search disabled` message instead of a
`None` that crashes later. `search()` now returns immediately when the index is
empty, so a broken index costs nothing per query.

### 3b. The HTTP 400 is intermittent, not a bad input

The first batched run reached **7,424 / 40,482 symbols in 421s (~17.6 texts/s)**
and then died with `HTTP Error 400: Bad Request`. The natural suspicion — one
pathological symbol — is wrong. Measured:

| Test | Result |
|---|---|
| the exact failing batch (`texts[7424:7680]`) on its own | **OK**, 256 vectors, 12.2s |
| same batch retried twice | OK both times |
| batch sizes 64 / 128 / 192 / 256 / 320 / 512 | all OK (5.7s … 24.1s) |
| a batch of 200 duplicated texts (duplicate hypothesis) | OK |
| longest text in the corpus (108 chars) alone | OK |

The corpus has 3,691 duplicated texts (`__init__ function basic_association.py`
appears three times) and none of that matters. The 400 is a server-side,
state-dependent response that disappears on a retry, so the fix is to **retry,
then split** rather than to hunt for a bad input:

- `EMBED_RETRIES = 2` with a 2s pause between attempts;
- if the batch still fails, split it in half and retry both halves;
- a single text that is still refused is recorded as `None` and skipped, which
  keeps the vectors aligned with the symbols (`build_index` already skips
  `None`), instead of discarding the whole 40k index;
- the return value always has one entry per input, so alignment can never drift.

**Verified on the full build:** 40,482 / 40,482 symbols embedded in 2,237s
(~37 min, ~18 texts/s). Two transient `HTTP 400`s occurred along the way; both
were recovered by the first retry — no batch ever had to be split, and no vector
was dropped. A second full run reproduced it: **2,370s (~40 min)**, nine
transient 400s, again all recovered by retry, zero splits, zero dropped vectors.

### 4. Test coverage had been deleted without a trace — process defect

`tests/ast_test.py`, `tests/test.py`, `tests/test2.py` and an **empty**
`tests/test_symbol_visitor.py` were deleted from the working tree while the
roadmap still claimed visitor/call/nested tests existed. The claim was false, and
that is exactly why breakage #1 reached a real project unnoticed.

**Fix:** the claim was corrected and `tests/test_symbol_visitor.py` now exists as
a real test: module-level `self`, `self.x()` → `ClassName.x()`, unnameable call
targets, nested class/function parents, signatures, docstrings, variable
bindings, syntax errors, and per-file resilience.

---

## Gaps found (no crash, but wrong context)

- **Entry points: 0.** `ENTRY_POINT_NAMES` only matches `main.py`, `app.py`,
  `run.py`, `server.py`, `manage.py`. Real libraries declare entry points in
  `pyproject.toml` / `setup.py` (`[project.scripts]`) or via
  `if __name__ == "__main__"` blocks — none of that is read, so the context's
  "Entry Points" section is empty on this project.
- **Dependencies: never detected.** `DependencyAnalyzer.detect_dependency()` is an
  empty stub and `ProjectAnalyzer.analyze()` never calls it, so
  `project.dependencies` is always `[]` and `build_dependencies()` always returns
  `""` — for any project, not just this one.
- **README: `None`.** Only a file named `readme.md` is recognized; SQLAlchemy
  ships `README.rst`, so the readme silently disappears from the context.
- **`project.languages` counts 220 files as `unknown`** — `.rst`, `.cfg`, `.ini`,
  `.txt`, `.toml` are not mapped; they are counted in `total_size` but not
  described.

---

## Cost facts for the next Track 1 items

- Embedding throughput is ~17–18 texts/s on real symbols; the full 40,482-symbol
  index took **2,237–2,370s (≈37–40 minutes) across two runs** — and the
  assistant rebuilds it on every start (`AIDevelopmentAssistant.ask` builds the
  index lazily, once per process). This is the measured justification for the
  on-disk embedding cache.
- Scanning + AST analysis of 673 files measured 9.1s (13.9s under load) —
  acceptable, but it also runs on every start, so change-only re-indexing has a
  real, measurable target.
- Context size depends entirely on what retrieval returns: keyword-only it was
  5,036 tokens (15.4% of the window), but with semantic hits enabled the same
  question produced **146,021 tokens (445% of the window)** — 18 hits instead
  of 8. The token-budget guard and a trimming policy are now the most urgent
  Track 1 item, not a later nicety: without them the LLM stage cannot run on a
  large project.

---

## Open after this pass

- The full embedding build completed with batching: 40,482 / 40,482 entries in
  2,237s, two transient 400s both recovered by retry (numbers above). The
  context overflow once semantic hits are enabled (146k tokens) is the new top
  item — the LLM stage on a large project is blocked behind it.
- Entry points, dependencies and readme detection are now Track 1 items with
  concrete evidence behind them.
