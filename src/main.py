"""
Clean Code Bot - Main CLI Entry Point

A command-line tool that transforms dirty or undocumented code into clean,
optimized code following SOLID principles with comprehensive documentation.

Usage:
    python -m src.main optimize <file> [--output <output_file>]
    python -m src.main analyze <file> [--verbose]
"""

import sys
from pathlib import Path

from .cli import parse_arguments, validate_input_file
from .analyzer import analyze_file
from .optimizer import optimize_file
from .documenter import add_documentation
from .utils import (
    print_analysis_report,
    print_optimization_summary,
    print_documentation_summary,
    generate_output_filename,
    validate_and_read_file,
    write_output_file,
)


def handle_optimize_command(args) -> int:
    """
    Handle the optimize command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    try:
        input_file = validate_input_file(args.input_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1

    # Determine output file
    output_file = args.output or generate_output_filename(args.input_file)

    try:
        # Read source code
        with open(input_file, "r", encoding="utf-8") as f:
            source_code = f.read()

        # Optimize code
        optimized_code, optimizations = optimize_file(
            input_file,
            Path(output_file),
            optimization_type=args.optimize,
            add_types=args.add_types,
            format_code=args.format,
        )

        # Add documentation
        documented_code = add_documentation(optimized_code)

        # Write output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(documented_code)

        # Print summary
        if args.verbose:
            print_optimization_summary(
                str(input_file),
                output_file,
                optimizations,
                verbose=True,
            )
        else:
            print(f"\n✓ Optimization complete! Output saved to: {output_file}\n")

        return 0

    except Exception as e:
        print(f"Error during optimization: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def handle_analyze_command(args) -> int:
    """
    Handle the analyze command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    try:
        input_file = validate_input_file(args.input_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1

    try:
        report = analyze_file(input_file)
        print_analysis_report(report, verbose=args.verbose)

        # Return exit code based on errors found
        error_count = len(report.get_issues_by_severity("error"))
        return 1 if error_count > 0 else 0

    except Exception as e:
        print(f"Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main() -> int:
    """
    Main entry point for Clean Code Bot CLI.

    Returns:
        int: Exit code.
    """
    args = parse_arguments()

    if not args.command:
        print("Clean Code Bot - Transform dirty code into clean, documented code!")
        print("\nUsage: python -m src.main <command> [options]")
        print("\nCommands:")
        print("  optimize  Optimize and document a Python file")
        print("  analyze   Analyze a Python file for code quality issues")
        print("\nUse 'python -m src.main <command> --help' for more information.")
        return 0

    if args.command == "optimize":
        return handle_optimize_command(args)
    elif args.command == "analyze":
        return handle_analyze_command(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
