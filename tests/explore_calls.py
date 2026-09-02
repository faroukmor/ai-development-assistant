# Exploration tool: print every symbol and its raw call chains.
# Run from the project root:  python tests/explore_calls.py

import os
sys_path_fix = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(0, sys_path_fix)
import core.project.project as P
import core.project.project_indexer as PI

project_path = r"C:\\Users\\HP\\Documents\\PYTHON Project\\ai-development-assistant"

project = P.Project(project_path)
PI.ProjectIndexer(project).build()

print("=" * 70)
print("REAL CLASSES IN PROJECT (symbol.type == class)")
print("=" * 70)

class_names = set()
for file in project.files:
    for symbol in file.symbols:
        if symbol.type == "class":
            class_names.add(symbol.name)
            print(f"{file.name:28} {symbol.name}")

print()
print("=" * 70)
print("CALLS PER SYMBOL")
print("=" * 70)

total_calls = 0
with_hint = 0
with_self = 0
plain = 0

for file in project.files:
    for symbol in file.symbols:
        if not symbol.calls:
            continue
        owner_parent = symbol.parent.name if symbol.parent else ""
        print()
        print(f"{file.name}:{owner_parent}.{symbol.name}")
        for call in symbol.calls:
            total_calls += 1
            chain = call.replace("()", "")
            parts = chain.split(".")
            last = parts[-1]
            hint = parts[-2] if len(parts) >= 2 else ""
            if hint == "self":
                with_self += 1
                note = "   <- self (caller class: " + owner_parent + ")"
            elif hint and hint in class_names:
                with_hint += 1
                note = "   <- real class hint"
            elif hint:
                note = "   <- hint is NOT a known class (variable or module?)"
            else:
                plain += 1
                note = "   <- plain name, no hint"
            print(f"    chain: {call}")
            print(f"      last : {last}")
            print(f"      hint : {hint or chr(45)}{note}")

print()
print("=" * 70)
print(f"TOTAL calls: {total_calls}   real class hint: {with_hint}   self: {with_self}   plain: {plain}")
print("=" * 70)
