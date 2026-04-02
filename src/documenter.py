"""
Documentation generator module for creating comprehensive docstrings.

Generates docstrings following Google style guide for functions and classes.
"""

import ast
import re
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path


class DocstringGenerator(ast.NodeVisitor):
    """
    Generates comprehensive docstrings for Python code.

    Follows Google style guide format for docstrings.
    """

    def __init__(self, source_code: str):
        """
        Initialize the documentation generator.

        Args:
            source_code: The Python code to document.
        """
        self.source_code = source_code
        self.docstrings_added: int = 0

    def generate(self) -> str:
        """
        Generate comprehensive documentation for code.

        Returns:
            str: Code with added/improved docstrings.
        """
        try:
            tree = ast.parse(self.source_code)
            documented = self._add_docstrings(tree)
            return documented
        except SyntaxError:
            return self.source_code

    def _add_docstrings(self, tree: ast.AST) -> str:
        """
        Add docstrings to AST nodes and return modified code.

        Args:
            tree: AST tree to process.

        Returns:
            str: Code with added docstrings.
        """
        lines = self.source_code.split("\n")
        insertions: List[tuple] = []  # (line_number, docstring)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = self._generate_function_docstring(node)
                if docstring and not ast.get_docstring(node):
                    insertions.append((node.lineno, docstring, "function"))

            elif isinstance(node, ast.ClassDef):
                docstring = self._generate_class_docstring(node)
                if docstring and not ast.get_docstring(node):
                    insertions.append((node.lineno, docstring, "class"))

        # Apply insertions in reverse order to maintain line numbers
        for line_num, docstring, _ in sorted(insertions, reverse=True):
            # Find the line and add docstring after it
            if line_num <= len(lines):
                indent = len(lines[line_num - 1]) - len(lines[line_num - 1].lstrip())
                indent_str = " " * (indent + 4)
                lines.insert(line_num, indent_str + docstring)
                self.docstrings_added += 1

        return "\n".join(lines)

    def _generate_function_docstring(self, node: ast.FunctionDef) -> Optional[str]:
        """
        Generate a docstring for a function.

        Args:
            node: AST FunctionDef node.

        Returns:
            str: Generated docstring in Google style format.
        """
        # Extract argument names
        args = [arg.arg for arg in node.args.args]
        args = [arg for arg in args if arg != "self" and arg != "cls"]

        # Build docstring
        lines = ['"""', f"Function: {node.name}"]

        if node.name not in ["__init__", "__str__", "__repr__"]:
            lines.append("")
            lines.append("Brief description of what this function does.")

        if args:
            lines.append("")
            lines.append("Args:")
            for arg in args:
                lines.append(f"    {arg}: Description of {arg}.")

        # Check for return annotation or return statements
        if node.returns:
            lines.append("")
            lines.append("Returns:")
            lines.append("    Description of return value.")
        elif any(isinstance(n, ast.Return) and n.value for n in ast.walk(node)):
            lines.append("")
            lines.append("Returns:")
            lines.append("    Description of return value.")

        lines.append('"""')

        return "\n".join(lines)

    def _generate_class_docstring(self, node: ast.ClassDef) -> Optional[str]:
        """
        Generate a docstring for a class.

        Args:
            node: AST ClassDef node.

        Returns:
            str: Generated docstring in Google style format.
        """
        lines = ['"""', f"Class: {node.name}", ""]

        lines.append("Brief description of the class purpose and usage.")
        lines.append("")

        # Find attributes set in __init__
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute):
                                lines.append(f"Attributes:")
                                lines.append(f"    {target.attr}: Description.")

        lines.append('"""')
        return "\n".join(lines)


def add_documentation(source_code: str) -> str:
    """
    Add comprehensive documentation to Python code.

    Args:
        source_code: The source code to document.

    Returns:
        str: Code with added documentation.
    """
    generator = DocstringGenerator(source_code)
    return generator.generate()


def document_file(input_path: Path, output_path: Optional[Path] = None) -> Tuple[str, int]:
    """
    Add documentation to a Python file.

    Args:
        input_path: Path to the input file.
        output_path: Path to save documented code (optional).

    Returns:
        Tuple of (documented_code, number_of_docstrings_added).
    """
    with open(input_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    generator = DocstringGenerator(source_code)
    documented_code = generator.generate()

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(documented_code)

    return documented_code, generator.docstrings_added

