# See how ast walks an assignment line: what node types exist, what names and values they carry.
# Run from project root:  python tests/explore_assign.py

import ast

SOURCE = """
model = LLMClient()
retriever = HR.HybridRetriever(project)
answer = assistant.ask(user_input)
self.client = LLMClient(qwen)
"""

tree = ast.parse(SOURCE)

print("=" * 60)
print("WALK 1: every node type we meet")
print("=" * 60)
for node in ast.walk(tree):
    print(type(node).__name__)

print()
print("=" * 60)
print("WALK 2: only assignments - full anatomy")
print("=" * 60)
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        print("Assign found")
        print("  TARGETS:")
        for t in node.targets:
            print("    type:", type(t).__name__)
            print("    name:", getattr(t, "id", getattr(t, "attr", "?")))
        print("  VALUE:")
        v = node.value
        print("    type:", type(v).__name__)
        if isinstance(v, ast.Call):
            f = v.func
            print("    call on:", type(f).__name__)
            parts = []
            cur = f
            while isinstance(cur, ast.Attribute):
                parts.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                parts.append(cur.id)
            parts.reverse()
            print("    dotted call:", ".".join(parts))
        else:
            print("    (not a call - skip)")
        print("-" * 40)
