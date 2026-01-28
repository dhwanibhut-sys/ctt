import ast


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        func_info = {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "lineno": node.lineno
        }

        self.functions.append(func_info)

        # Continue walking nested functions
        self.generic_visit(node)


def extract_functions(code: str):
    """
    Parse Python code using AST and extract:
    - function name
    - arguments
    - line number
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            "error": f"SyntaxError: {str(e)}"
        }

    visitor = FunctionVisitor()
    visitor.visit(tree)

    return visitor.functions
