<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Setup Checklist

- [x] Create .github directory and copilot-instructions.md file
- [x] Set up virtual environment
- [x] Create project structure
- [x] Install dependencies
- [x] Create README.md
- [x] Verify setup
- [x] Create CLI argument parser module
- [x] Create code analyzer module
- [x] Create code optimizer module
- [x] Create documentation generator
- [x] Create utility functions
- [x] Integrate all modules with main.py
- [x] Update requirements with dependencies
- [x] Test all CLI commands

## Project Information

**Project Type:** Python CLI Tool
**Python Version:** 3.11+
**Purpose:** Clean Code Bot - Transform dirty code into clean, optimized, documented code

## Features Implemented

- **Code Analysis**: Detects SOLID violations, missing documentation, and complexity issues
- **Code Optimization**: Improves readability, naming conventions, and applies refactoring patterns
- **Documentation Generation**: Automatically adds Google-style docstrings
- **CLI Interface**: User-friendly command-line interface with analyze and optimize commands
- **Type Hints Support**: Optional type annotation capability
- **Code Formatting**: Black-style code formatting

## Setup Instructions

1. Create and activate virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`

## CLI Usage

**Analyze a file:**

```bash
python -m src.main analyze <file> [--verbose]
```

**Optimize a file:**

```bash
python -m src.main optimize <file> [--output <file>] [--optimize <type>] [--add-types] [--format] [--verbose]
```

## Testing

- Run tests: `python -m pytest tests/`
- Test sample: See test_optimized.py for example output
