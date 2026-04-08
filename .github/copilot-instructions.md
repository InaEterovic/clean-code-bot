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
- [x] Implement LLM integration (OpenAI & Groq)
- [x] Create Chain of Thought prompt engineering
- [x] Implement input validation and sanitization
- [x] Add security/injection prevention
- [x] Create examples folder with before/after samples
- [x] Add AI-powered improve command
- [x] Add AI-powered security command
- [x] Update documentation

## Project Information

**Project Type:** Python CLI Tool
**Python Version:** 3.11+
**Purpose:** Clean Code Bot - AI-powered transformation of dirty code into clean, optimized, documented code

## Features Implemented

### Static Analysis & Optimization

- **Code Analysis**: Detects SOLID violations, missing documentation, and complexity issues
- **Code Optimization**: Improves readability, naming conventions, and applies refactoring patterns
- **Documentation Generation**: Automatically adds Google-style docstrings
- **CLI Interface**: User-friendly command-line interface with multiple commands
- **Type Hints Support**: Optional type annotation capability
- **Code Formatting**: Black-style code formatting

### AI-Powered Features

- **Chain of Thought (CoT) Reasoning**: Structured AI analysis in 4 phases
  - Understanding, Analysis, Reasoning, Recommendation
- **LLM Integration**: Support for both OpenAI and Groq APIs
- **AI-Powered Code Improvement**: Transform code with `improve` command
- **AI-Powered Security Review**: Vulnerability detection with `security` command
- **Input Validation**: Size limits, encoding validation, null byte detection
- **Prompt Injection Prevention**: Pattern detection and risk assessment
- **Sensitive Data Masking**: Automatic redaction of credentials

## Setup Instructions

1. Create and activate virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Set API key (choose one):
   - Groq: `$env:GROQ_API_KEY = "your-key"`
   - OpenAI: `$env:OPENAI_API_KEY = "your-key"`

## CLI Commands

### Static Commands

**Analyze a file:**

```bash
python -m src.main analyze <file> [--verbose]
```

**Optimize a file:**

```bash
python -m src.main optimize <file> [--output <file>] [--optimize <type>] [--add-types] [--format] [--verbose]
```

### AI-Powered Commands

**Improve with AI (requires LLM):**

```bash
python -m src.main improve <file> [--provider groq|openai] [--type <type>] [--verbose]
```

**Security review with AI (requires LLM):**

```bash
python -m src.main security <file> [--provider groq|openai] [--verbose]
```

## Project Modules

- `cli.py` - Command-line argument parsing with subcommands
- `analyzer.py` - AST-based code quality analysis
- `optimizer.py` - Static code optimization and refactoring
- `documenter.py` - Docstring generation
- `llm_integrator.py` - LLM provider abstraction (OpenAI/Groq)
- `prompt_templates.py` - Chain of Thought prompt engineering
- `security.py` - Input validation and injection prevention
- `utils.py` - Formatting and utility functions

## Testing

- Run tests: `python -m pytest tests/`
- Examples: See `examples/before_example.py` and `examples/after_example.py`
