import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.project.project import Project
from core.project.project_indexer import ProjectIndexer
from core.retrieval.hybrid_retriever import HybridRetriever
from tests.retrieval_benchmark import RETRIEVAL_BENCHMARK

PROJECT_PATH = r"C:\Users\HP\Documents\PYTHON Project\ai-development-assistant"


def hits_as_pairs(results):
    return [(r.file.name, r.symbol.name if r.symbol else None) for r in results]


def run_benchmark():
    project = Project(PROJECT_PATH)
    ProjectIndexer(project).build()
    retriever = HybridRetriever(project)

    passed = 0
    failed = []

    for case in RETRIEVAL_BENCHMARK:
        results = retriever.search(case["question"])
        hits = hits_as_pairs(results)

        errors = []
        for expected in case["must"]:
            file_name, symbol_name = expected
            ok = any(h[0] == file_name and
                     (symbol_name is None or h[1] == symbol_name)
                     for h in hits)
            if not ok:
                errors.append(f"missing {file_name}:{symbol_name or '*'}")

        for banned in case.get("must_not", []):
            file_name, symbol_name = banned
            bad = any(h[0] == file_name and
                      (symbol_name is None or h[1] == symbol_name)
                      for h in hits)
            if bad:
                errors.append(f"forbidden {file_name}:{symbol_name or '*'} present")

        if case.get("expect_empty") and hits:
            errors.append(f"expected no hits, got {hits[:3]}")

        if errors:
            failed.append((case["question"], errors, hits))
            print(f"FAIL  {case['question']}")
            for e in errors:
                print(f"        - {e}")
            print(f"        hits: {hits[:5]}")
        else:
            passed += 1
            print(f"PASS  {case['question']}  ({len(hits)} hits)")

    print()
    print(f"BENCHMARK: {passed}/{len(RETRIEVAL_BENCHMARK)} passed")
    return failed


if __name__ == "__main__":
    failures = run_benchmark()
    sys.exit(1 if failures else 0)