"""Code analyzer module for identifying code quality issues."""

import ast
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class Issue:
    """Represents a single code quality issue."""

    line_number: int
    issue_type: str
    severity: str  # "error", "warning", "info"
    message: str
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] Line {self.line_number}: {self.message}"


@dataclass
class AnalysisReport:
    """Comprehensive analysis report for a code file."""

    file_path: str
    total_issues: int = 0
    issues: List[Issue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    summary: str = ""

    def add_issue(self, issue: Issue) -> None:
        self.issues.append(issue)
        self.total_issues += 1

    def get_issues_by_severity(self, severity: str) -> List[Issue]:
        return [issue for issue in self.issues if issue.severity == severity]


class CodeAnalyzer(ast.NodeVisitor):
    """Analyzes Python code for quality issues using AST."""

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.issues: List[Issue] = []
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None
        self.line_map: Dict[int, str] = {}
        self._build_line_map()

    def _build_line_map(self) -> None:
        for idx, line in enumerate(self.source_code.split("\n"), start=1):
            self.line_map[idx] = line.strip()

    def analyze(self) -> AnalysisReport:
        try:
            tree = ast.parse(self.source_code)
            self.visit(tree)
        except SyntaxError as e:
            self.issues.append(
                Issue(
                    line_number=e.lineno or 0,
                    issue_type="syntax_error",
                    severity="error",
                    message=f"Syntax error: {e.msg}",
                )
            )

        report = AnalysisReport(file_path="<unknown>", total_issues=len(self.issues))
        report.issues = self.issues
        report.metrics = self._calculate_metrics()
        report.summary = self._generate_summary()

        return report

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        old_function = self.current_function
        self.current_function = node.name

        # Check for missing docstring
        if not ast.get_docstring(node):
            self.issues.append(
                Issue(
                    line_number=node.lineno,
                    issue_type="missing_docstring",
                    severity="warning",
                    message=f"Function '{node.name}' is missing docstring",
                    suggestion="Add a docstring to document the function's purpose, args, and return value",
                )
            )

        func_length = node.end_lineno - node.lineno
        if func_length > 50:
            self.issues.append(
                Issue(
                    line_number=node.lineno,
                    issue_type="function_too_long",
                    severity="warning",
                    message=f"Function '{node.name}' is {func_length} lines (consider breaking it down)",
                    suggestion="Extract logical sections into separate functions (Single Responsibility Principle)",
                )
            )

        complexity = self._calculate_cyclomatic_complexity(node)
        if complexity > 10:
            self.issues.append(
                Issue(
                    line_number=node.lineno,
                    issue_type="high_complexity",
                    severity="warning",
                    message=f"Function '{node.name}' has high cyclomatic complexity ({complexity})",
                    suggestion="Simplify logic by extracting branches into separate functions",
                )
            )

        if len(node.args.args) > 5:
            self.issues.append(
                Issue(
                    line_number=node.lineno,
                    issue_type="too_many_parameters",
                    severity="info",
                    message=f"Function '{node.name}' has {len(node.args.args)} parameters",
                    suggestion="Consider using a configuration object or breaking into multiple functions",
                )
            )

        self.generic_visit(node)
        self.current_function = old_function

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        old_class = self.current_class
        self.current_class = node.name

        if not ast.get_docstring(node):
            self.issues.append(
                Issue(
                    line_number=node.lineno,
                    issue_type="missing_docstring",
                    severity="warning",
                    message=f"Class '{node.name}' is missing docstring",
                    suggestion="Add a class-level docstring explaining its purpose and usage",
                )
            )

        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        if len(methods) > 15:
            self.issues.append(
                Issue(
                    line_number=node.lineno,
                    issue_type="too_many_methods",
                    severity="warning",
                    message=f"Class '{node.name}' has {len(methods)} methods (violates Single Responsibility)",
                    suggestion="Consider splitting this class into multiple focused classes",
                )
            )

        self.generic_visit(node)
        self.current_class = old_class

    def visit_Import(self, node: ast.Import) -> None:
        """Check import statements."""
        # This is a placeholder for import analysis
        self.generic_visit(node)

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate code metrics."""
        try:
            tree = ast.parse(self.source_code)
        except SyntaxError:
            return {}

        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]

        return {
            "total_lines": len(self.source_code.split("\n")),
            "total_classes": len(classes),
            "total_functions": len(functions),
            "error_count": len(self._get_issues_by_severity("error")),
            "warning_count": len(self._get_issues_by_severity("warning")),
            "info_count": len(self._get_issues_by_severity("info")),
        }

    def _get_issues_by_severity(self, severity: str) -> List[Issue]:
        """Get issues of a specific severity."""
        return [issue for issue in self.issues if issue.severity == severity]

    def _generate_summary(self) -> str:
        """Generate a summary of the analysis."""
        errors = len(self._get_issues_by_severity("error"))
        warnings = len(self._get_issues_by_severity("warning"))
        infos = len(self._get_issues_by_severity("info"))

        return (
            f"Found {errors} errors, {warnings} warnings, and {infos} info messages"
        )


def analyze_file(file_path: Path) -> AnalysisReport:
    """
    Analyze a Python file.

    Args:
        file_path: Path to the Python file to analyze.

    Returns:
        AnalysisReport: Detailed analysis report.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    analyzer = CodeAnalyzer(source_code)
    report = analyzer.analyze()
    report.file_path = str(file_path)

    return report
