"""Clean Code Bot - Main CLI Entry Point"""

import sys
from pathlib import Path

from .cli import parse_arguments, validate_input_file
from .analyzer import analyze_file
from .optimizer import optimize_file
from .documenter import add_documentation
from .security import InputValidator, InputSanitizer, PromptInjectionDetector
from .utils import (
    print_analysis_report,
    print_optimization_summary,
    print_documentation_summary,
    generate_output_filename,
    validate_and_read_file,
    write_output_file,
)


def handle_optimize_command(args) -> int:
    try:
        input_file = validate_input_file(args.input_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1

    output_file = args.output or generate_output_filename(args.input_file)

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            source_code = f.read()

        optimized_code, optimizations = optimize_file(
            input_file,
            Path(output_file),
            optimization_type=args.optimize,
            add_types=args.add_types,
            format_code=args.format,
        )

        documented_code = add_documentation(optimized_code)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(documented_code)
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
    args = parse_arguments()

    if not args.command:
        print("Clean Code Bot - Transform dirty code into clean, documented code!")
        print("\nUsage: python -m src.main <command> [options]")
        print("\nCommands:")
        print("  analyze    Analyze a Python file for code quality issues")
        print("  optimize   Optimize and document a Python file")
        print("  improve    AI-powered code improvement using Chain of Thought")
        print("  security   AI-powered security review")
        print("\nUse 'python -m src.main <command> --help' for more information.")
        return 0

    if args.command == "optimize":
        return handle_optimize_command(args)
    elif args.command == "analyze":
        return handle_analyze_command(args)
    elif args.command == "improve":
        return handle_improve_command(args)
    elif args.command == "security":
        return handle_security_command(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


def handle_improve_command(args) -> int:
    try:
        input_file = validate_input_file(args.input_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1

    # Determine output file
    output_file = args.output or generate_output_filename(args.input_file, "_improved")

    try:
        # Read and validate input
        with open(input_file, "r", encoding="utf-8") as f:
            source_code = f.read()

        print("🔐 Validating input for security...")
        is_valid, error_msg = InputValidator.validate_code_input(source_code)
        if not is_valid:
            print(f"❌ Validation failed: {error_msg}")
            return 1

        is_suspicious, patterns = PromptInjectionDetector.detect_injection_patterns(source_code)
        if is_suspicious:
            risk_level = PromptInjectionDetector.get_risk_level(source_code)
            print(f"⚠️  Risk level: {risk_level.upper()}")
            if args.verbose:
                for pattern in patterns:
                    print(f"   - {pattern}")

        sanitized_code = InputSanitizer.prepare_for_llm(source_code)

        try:
            from .llm_integrator import create_llm_integrator
            from .prompt_templates import PromptTemplate, ChainOfThought
        except ImportError as e:
            print(f"❌ LLM integration not available: {e}")
            print("💡 Install required packages: pip install groq python-dotenv")
            return 1

        print(f"🤖 Initializing Groq LLM...")
        try:
            llm = create_llm_integrator(
                api_key=args.api_key,
                model=args.model
            )
            provider_info = llm.get_provider_info()
            print(f"   Using: {provider_info['model']}")
        except ValueError as e:
            print(f"❌ LLM initialization failed: {e}")
            return 1

        print("🧠 Generating Chain of Thought analysis...")
        prompt = PromptTemplate.code_improvement_prompt(sanitized_code, args.type)

        print("⏳ Waiting for AI analysis...")
        try:
            response = llm.generate(prompt)
        except RuntimeError as e:
            print(f"❌ LLM error: {e}")
            return 1

        if args.verbose:
            phases = ChainOfThought.extract_cot_phases(response)
            formatted = ChainOfThought.format_cot_analysis(phases)
            print(formatted)

        improved_code = extract_code_from_response(response)
        write_output_file(output_file, improved_code)

        # Print summary
        print(f"✅ Improvement complete!")
        print(f"📄 Output saved to: {output_file}")
        print(f"\n💡 Tip: Review the improved code carefully before using in production.")

        return 0

    except Exception as e:
        print(f"❌ Error during improvement: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def handle_security_command(args) -> int:
    try:
        input_file = validate_input_file(args.input_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            source_code = f.read()

        print("🔐 Validating input...")
        is_valid, error_msg = InputValidator.validate_code_input(source_code)
        if not is_valid:
            print(f"❌ Validation failed: {error_msg}")
            return 1

        sanitized_code = InputSanitizer.prepare_for_llm(source_code)

        try:
            from .llm_integrator import create_llm_integrator
            from .prompt_templates import PromptTemplate, ChainOfThought
        except ImportError as e:
            print(f"❌ LLM integration not available: {e}")
            return 1

        # Initialize LLM
        print(f"🤖 Initializing Groq LLM for security review...")
        try:
            llm = create_llm_integrator(
                api_key=args.api_key
            )
        except ValueError as e:
            print(f"❌ LLM initialization failed: {e}")
            return 1

        # Generate security review prompt
        print("🔍 Generating security review prompt...")
        prompt = PromptTemplate.security_review_prompt(sanitized_code)

        # Get LLM response
        print("⏳ Analyzing code for security vulnerabilities...")
        response = llm.generate(prompt)

        # Extract and display CoT phases
        phases = ChainOfThought.extract_cot_phases(response)
        formatted = ChainOfThought.format_cot_analysis(phases)
        print("\n" + formatted)

        if not args.verbose:
            print("💡 Use --verbose for additional details")

        return 0

    except Exception as e:
        print(f"❌ Error during security review: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def extract_code_from_response(response: str) -> str:
    """
    Extract Python code from LLM response.

    Looks for code blocks marked with triple backticks.

    Args:
        response: LLM response text.

    Returns:
        str: Extracted code or original response if no code found.
    """
    import re

    # Look for Python code blocks
    pattern = r"```(?:python)?\n(.*?)\n```"
    matches = re.findall(pattern, response, re.DOTALL)

    if matches:
        # Return the first code block found
        return matches[0].strip()

    # If no code blocks, return the response as-is
    return response


if __name__ == "__main__":
    sys.exit(main())
