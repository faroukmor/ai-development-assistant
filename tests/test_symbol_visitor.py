import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.analyzers.python_symbol_visitor import PythonSymbolVisitor


class FakeFile:
    def __init__(self, path):
        self.path = path
        self.symbols = []


def analyze(source):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as handle:
        handle.write(source)
        path = handle.name

    try:
        fake = FakeFile(path)
        PythonSymbolVisitor(fake).analyze()
        return fake.symbols
    finally:
        os.remove(path)


def find(symbols, name):
    for s in symbols:
        if s.name == name:
            return s
    raise AssertionError(f"symbol {name!r} not found in {[s.name for s in symbols]}")


def run_visitor_checks():
    # Regression: a module-level helper taking `self` as a plain parameter
    # (sqlalchemy sql/base.py:295) used to join a None into the call name and
    # abort the analysis of the whole project with a TypeError.
    symbols = analyze(
        "def _generative(fn, self, *args, **kw):\n"
        "    self = self._generate()\n"
        "    return self\n"
    )
    generative = find(symbols, "_generative")
    assert generative.calls == [], \
        "`self` outside a class is unresolvable — the call must be dropped, not crash"

    # Inside a class the same call must still resolve through the class name.
    symbols = analyze(
        "class LLMClient:\n"
        "    def ask(self, messages):\n"
        "        return self.post(messages)\n"
        "\n"
        "    def post(self, messages):\n"
        "        return messages\n"
    )
    ask = find(symbols, "ask")
    assert ask.calls == ["LLMClient.post()"], \
        f"self.x() must resolve through the class name, got {ask.calls}"

    # unnameable call targets (Subscript, Lambda) are dropped, call chains kept
    symbols = analyze(
        "def caller(mapping, model):\n"
        "    mapping['key']()\n"
        "    (lambda: 1)()\n"
        "    return model.create().run()\n"
    )
    caller = find(symbols, "caller")
    assert caller.calls == ["model.create().run()", "model.create()"], \
        f"unnameable targets must be dropped, resolvable chains kept — got {caller.calls}"

    # Nested classes and nested functions keep their parent chain.
    symbols = analyze(
        "class Outer:\n"
        "    class Inner:\n"
        "        def deep(self):\n"
        "            def leaf():\n"
        "                pass\n"
        "            return leaf\n"
    )
    outer, inner = find(symbols, "Outer"), find(symbols, "Inner")
    deep, leaf = find(symbols, "deep"), find(symbols, "leaf")
    assert outer.type == "class" and inner.type == "class"
    assert inner.parent is outer, "nested class must point at its outer class"
    assert deep.parent is inner, "method must point at its class"
    assert leaf.parent is deep, "nested function must point at its enclosing function"

    # Signatures, docstrings and the class link survive.
    symbols = analyze(
        'class Service:\n'
        '    """Service docstring."""\n'
        '\n'
        '    def start(self, port):\n'
        '        """Start it."""\n'
        '        pass\n'
    )
    service = find(symbols, "Service")
    start = find(symbols, "start")
    assert service.docstring == "Service docstring."
    assert start.signature == "start(self, port)", f"got {start.signature!r}"
    assert start.docstring == "Start it."
    assert start.parent is service

    # Constructor bindings let `model.ask()` resolve to LLMClient.ask later.
    symbols = analyze("def build():\n    model = LLMClient()\n    return model\n")
    assert find(symbols, "build").variable_bindings == {"model": "LLMClient"}

    # A file that does not parse yields no symbols and no exception.
    assert analyze("def broken(:\n") == [], \
        "a syntax error must skip the file, not raise"


def run_analyzer_resilience_check():
    from core.project.project import Project
    from core.project.project_indexer import ProjectIndexer

    root = tempfile.mkdtemp()
    try:
        with open(os.path.join(root, "good.py"), "w", encoding="utf-8") as handle:
            handle.write("def works():\n    return 1\n")

        # not valid UTF-8: reading it raises, and the project must survive
        with open(os.path.join(root, "bad_bytes.py"), "wb") as handle:
            handle.write(b"\xff\xfe\x00 not utf-8")

        project = Project(root)
        ProjectIndexer(project).build()

        assert len(project.analysis_errors) == 1, \
            f"exactly the broken file must be reported, got {project.analysis_errors}"
        assert project.analysis_errors[0][1] == "UnicodeDecodeError", \
            f"the recorded error keeps its type, got {project.analysis_errors[0][1]}"
        assert project.get_file_by_path(os.path.join(root, "good.py")).symbols, \
            "one unreadable file must not stop the symbols of the others"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def run_checks():
    run_visitor_checks()
    run_analyzer_resilience_check()
    print("ALL SYMBOL VISITOR CHECKS PASSED")


if __name__ == "__main__":
    run_checks()
