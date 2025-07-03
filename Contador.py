import ast

class ColumnNameCollector(ast.NodeVisitor):
    def __init__(self):
        self.names = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.names.append(target.id)
        self.generic_visit(node)

with open("models/playerseasonstat.py", "r") as f:  # Cambia a tu archivo Python
    tree = ast.parse(f.read())
    collector = ColumnNameCollector()
    collector.visit(tree)

from collections import Counter
counter = Counter(collector.names)
for name, count in counter.items():
    if count > 1:
        print(f"Atributo duplicado: {name} ({count} veces)")
