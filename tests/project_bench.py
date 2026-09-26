"""Track 1 instrument: run the whole pipeline against a real project and report
what breaks, with numbers for every stage.

Usage:
    python -m tests.project_bench <project_path> [--embed] [--ask "question"]

Stages: scan + index, AST analysis, keyword retrieval, embedding index
(--embed), context + tokens, LLM answer (--ask). A failing stage is reported
and the run continues, so one breakage cannot hide the rest.
"""
import sys
import time
import traceback

sys.path.insert(0, __file__.rsplit("tests", 1)[0].rstrip("\\/"))

from core.project.project import Project
from core.project.project_indexer import ProjectIndexer
from core.retrieval.hybrid_retriever import HybridRetriever
from tests.token_counter import count_tokens

CONTEXT_WINDOW = 32768


def stage(number, title):
    print()
    print(f"--- stage {number}: {title} " + "-" * max(0, 46 - len(title)))


def report_failure(stage_name, error):
    print(f"FAILURE in {stage_name}: {type(error).__name__}: {error}")
    traceback.print_exc()


def build_project(path):
    stage(1, "scan + index")
    import core.analyzers.analysis_pipeline as AP
    import core.project.project_loader as PL

    project = Project(path)

    # Mirrors ProjectIndexer.build(), but timed phase by phase so a slowdown
    # can be attributed to scanning, indexing or AST analysis.
    started = time.time()
    PL.ProjectLoader().load_files(project)
    loaded = time.time() - started

    started = time.time()
    ProjectIndexer(project).index_files()
    indexed = time.time() - started

    started = time.time()
    AP.ProjectAnalyzer(project).analyze()
    analyzed = time.time() - started

    print(f"time              : {loaded + indexed + analyzed:.2f}s")
    print(f"  load files      : {loaded:.2f}s")
    print(f"  index metadata  : {indexed:.2f}s")
    print(f"  AST analysis    : {analyzed:.2f}s")
    print(f"files             : {len(project.files)}")
    print(f"languages         : { {k: v for k, v in project.languages.items() if v} }")
    print(f"total size        : {project.total_size / 1048576:.1f} MB")
    print(f"type              : {project.type}")
    print(f"entry points      : {len(project.entry_points)}")
    print(f"readme            : {project.readme.name if project.readme else None}")
    return project


def stage_analysis(project):
    stage(2, "AST analysis")
    symbols = [s for f in project.files for s in f.symbols]
    print(f"symbols           : {len(symbols)}")
    print(f"classes           : {len([s for s in symbols if s.type == 'class'])}")
    print(f"functions/methods : {len([s for s in symbols if s.type != 'class'])}")
    print(f"with parent       : {len([s for s in symbols if s.parent])}")
    print(f"with docstring    : {len([s for s in symbols if s.docstring])}")
    print(f"calls extracted   : {sum(len(s.calls) for s in symbols)}")
    print(f"variable bindings : {sum(len(s.variable_bindings) for s in symbols)}")
    print(f"file errors       : {len(project.analysis_errors)}")
    for path, kind, message in project.analysis_errors[:5]:
        print(f"   - {path}: {kind}: {message}")
    return symbols


def stage_retrieval(project, questions):
    stage(3, "keyword retrieval")
    retriever = HybridRetriever(project)
    for question in questions:
        started = time.time()
        try:
            results = retriever.search(question)
        except Exception as e:
            report_failure(f"retrieval: {question}", e)
            continue
        elapsed = time.time() - started
        hits = [(r.file.name, r.symbol.name if r.symbol else None) for r in results]
        print(f"{elapsed:6.3f}s  {question!r} -> {len(hits)} hits  {hits[:3]}")
    return retriever


def stage_embedding(project):
    stage(4, "embedding index")
    from core.retrieval.embedding_search import EmbeddingSearch
    search = EmbeddingSearch(project)
    started = time.time()
    try:
        search.build_index()
    except Exception as e:
        report_failure("embedding build", e)
        return search
    print(f"build time        : {time.time() - started:.2f}s")
    print(f"embedded entries  : {len(search.knowledge_base)}")
    return search


def stage_context(project, question, embedding_search):
    stage(5, "context + tokens")
    from core.context.context_builder import ProjectContextBuilder

    retriever = HybridRetriever(project, embedding_search)
    try:
        started = time.time()
        results = retriever.search(question)
        print(f"retrieval time    : {time.time() - started:.2f}s ({len(results)} hits)")

        started = time.time()
        context = ProjectContextBuilder(project, results).build_context()
        elapsed = time.time() - started
    except Exception as e:
        report_failure("context build", e)
        return

    tokens = count_tokens(context)
    print(f"context build     : {elapsed:.2f}s")
    print(f"context chars     : {len(context)}")
    print(f"context tokens    : {tokens}")
    print(f"window            : {CONTEXT_WINDOW}  ({100 * tokens / CONTEXT_WINDOW:.1f}% used)")
    if tokens > 0.75 * CONTEXT_WINDOW:
        print("WARNING: over the 75% budget — Track 1 guard would trip here")


def stage_ask(project, question):
    stage(6, "LLM answer")
    from core.assistant.ai_assistant import AIDevelopmentAssistant
    try:
        assistant = AIDevelopmentAssistant(project.path)
    except Exception as e:
        report_failure("assistant init", e)
        return
    started = time.time()
    try:
        answer = assistant.answer(question)
    except Exception as e:
        report_failure("ask", e)
        return
    print(f"time              : {time.time() - started:.2f}s")
    print(f"answer:\n{answer}")


PROBE_QUESTIONS = [
    "how does Connection execute a statement",
    "where is the session flushed",
    "what does Query.all do",
]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    path = sys.argv[1]
    embed = "--embed" in sys.argv
    ask = sys.argv[sys.argv.index("--ask") + 1] if "--ask" in sys.argv else None

    project = build_project(path)
    stage_analysis(project)
    stage_retrieval(project, PROBE_QUESTIONS)
    embedding_search = stage_embedding(project) if embed else None
    stage_context(project, PROBE_QUESTIONS[0], embedding_search)
    if ask:
        stage_ask(project, ask)