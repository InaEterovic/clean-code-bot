"""
Utility functions for Clean Code Bot.

Provides common utilities for file handling, reporting, and output formatting.
"""

from pathlib import Path
from typing import Optional
from dataclasses import asdict

from .analyzer import AnalysisReport, Issue


def print_analysis_report(report: AnalysisReport, verbose: bool = False) -> None:
    """
    Print a formatted analysis report to console.

    Args:
        report: The AnalysisReport to print.
        verbose: Whether to show detailed information.
    """
    print(f"\n{'='*70}")
    print(f"Code Analysis Report: {report.file_path}")
    print(f"{'='*70}\n")

    if report.total_issues == 0:
        print("✓ No issues found! Your code looks great.\n")
    else:
        print(f"Found {report.total_issues} issues:\n")

        # Group issues by severity
        errors = report.get_issues_by_severity("error")
        warnings = report.get_issues_by_severity("warning")
        infos = report.get_issues_by_severity("info")

        if errors:
            print(f"ERRORS ({len(errors)}):")
            for issue in errors:
                print(f"  • {issue}")
                if verbose and issue.suggestion:
                    print(f"    Suggestion: {issue.suggestion}")
            print()

        if warnings:
            print(f"WARNINGS ({len(warnings)}):")
            for issue in warnings:
                print(f"  • {issue}")
                if verbose and issue.suggestion:
                    print(f"    Suggestion: {issue.suggestion}")
            print()

        if infos:
            print(f"INFO ({len(infos)}):")
            for issue in infos:
                print(f"  • {issue}")
                if verbose and issue.suggestion:
                    print(f"    Suggestion: {issue.suggestion}")
            print()

    # Print metrics
    if report.metrics:
        print("Code Metrics:")
        print(f"  • Total Lines: {report.metrics.get('total_lines', 0)}")
        print(f"  • Classes: {report.metrics.get('total_classes', 0)}")
        print(f"  • Functions: {report.metrics.get('total_functions', 0)}")
        print()

    print(f"Summary: {report.summary}")
    print(f"{'='*70}\n")


def print_optimization_summary(
    input_file: str,
    output_file: str,
    optimizations: list,
    verbose: bool = False,
) -> None:
    """
    Print a summary of optimizations applied.

    Args:
        input_file: Path to input file.
        output_file: Path to output file.
        optimizations: List of optimizations applied.
        verbose: Whether to show detailed information.
    """
    print(f"\n{'='*70}")
    print("Code Optimization Complete!")
    print(f"{'='*70}\n")

    print(f"Input:  {input_file}")
    print(f"Output: {output_file}\n")

    if optimizations:
        print(f"Applied {len(optimizations)} optimization(s):")
        for opt in set(optimizations):
            print(f"  ✓ {opt.replace('_', ' ').title()}")
    else:
        print("No optimizations were needed.")

    print(f"\n{'='*70}\n")


def print_documentation_summary(
    input_file: str,
    output_file: str,
    docstrings_added: int,
    verbose: bool = False,
) -> None:
    """
    Print a summary of documentation added.

    Args:
        input_file: Path to input file.
        output_file: Path to output file.
        docstrings_added: Number of docstrings added.
        verbose: Whether to show detailed information.
    """
    print(f"\n{'='*70}")
    print("Documentation Generation Complete!")
    print(f"{'='*70}\n")

    print(f"Input:  {input_file}")
    print(f"Output: {output_file}\n")
    print(f"Added {docstrings_added} docstring(s)\n")

    print(f"{'='*70}\n")


def generate_output_filename(input_file: str, suffix: str = "_optimized") -> str:
    """
    Generate an output filename based on input filename.

    Args:
        input_file: Path to input file.
        suffix: Suffix to add before file extension.

    Returns:
        str: Generated output filename.
    """
    path = Path(input_file)
    return str(path.parent / f"{path.stem}{suffix}.py")


def validate_and_read_file(file_path: str) -> str:
    """
    Validate and read a Python file.

    Args:
        file_path: Path to the file to read.

    Returns:
        str: File contents.

    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If file is not a Python file.
        IOError: If file cannot be read.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix != ".py":
        raise ValueError(f"Expected Python file (.py), got: {path.suffix}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except IOError as e:
        raise IOError(f"Error reading file: {e}")


def write_output_file(output_path: str, content: str) -> None:
    """
    Write content to an output file.

    Args:
        output_path: Path to write to.
        content: Content to write.

    Raises:
        IOError: If file cannot be written.
    """
    path = Path(output_path)

    # Create parent directories if needed
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Error writing file: {e}")
