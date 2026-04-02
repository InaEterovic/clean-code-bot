"""
CLI (Command Line Interface) module for Clean Code Bot.

Provides argument parsing and command-line interface for code optimization.
"""

import argparse
from pathlib import Path


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the CLI argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser for Clean Code Bot.
    """
    parser = argparse.ArgumentParser(
        prog="clean-code-bot",
        description="Transform dirty or undocumented code into clean, optimized "
                    "code following SOLID principles with comprehensive documentation.",
        epilog="Example: python -m src.main optimize input.py --output output.py --optimize all"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Optimize command
    optimize_parser = subparsers.add_parser(
        "optimize",
        help="Optimize and document a Python code file"
    )
    optimize_parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input Python file to optimize"
    )
    optimize_parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path (default: <input>_optimized.py)"
    )
    optimize_parser.add_argument(
        "--optimize",
        choices=["all", "solid", "performance", "readability"],
        default="all",
        help="Type of optimization to apply (default: all)"
    )
    optimize_parser.add_argument(
        "--add-types",
        action="store_true",
        help="Add type hints to functions and variables"
    )
    optimize_parser.add_argument(
        "--format",
        action="store_true",
        help="Format code using black style"
    )
    optimize_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed optimization report"
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a Python file for code quality issues"
    )
    analyze_parser.add_argument(
        "input_file",
        type=str,
        help="Path to the Python file to analyze"
    )
    analyze_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed analysis report"
    )

    return parser


def parse_arguments(args=None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Optional list of arguments (for testing).

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = create_parser()
    return parser.parse_args(args)


def validate_input_file(file_path: str) -> Path:
    """
    Validate that the input file exists and is a Python file.

    Args:
        file_path: Path to the file to validate.

    Returns:
        Path: Validated Path object.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file is not a Python file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if path.suffix != ".py":
        raise ValueError(f"File must be a Python file (.py), got: {path.suffix}")

    return path
