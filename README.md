# Clean Code Bot

A Python project for clean code analysis and improvement.

## Setup

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. Create virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
clean-code-bot/
├── src/              # Source code
├── tests/            # Test files
├── requirements.txt  # Project dependencies
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## Development

### CLI Usage

Clean Code Bot provides two main commands: `optimize` and `analyze`.

#### Optimize Command

Transform dirty or undocumented code into clean, optimized code:

```bash
python -m src.main optimize <input_file> [options]
```

**Options:**

- `--output, -o <file>`: Output file path (default: `<input>_optimized.py`)
- `--optimize <type>`: Optimization type: `all`, `solid`, `performance`, or `readability` (default: `all`)
- `--add-types`: Add type hints to functions and variables
- `--format`: Format code using black style
- `--verbose, -v`: Show detailed optimization report

**Example:**

```bash
python -m src.main optimize dirty_code.py --output clean_code.py --optimize all --add-types --verbose
```

#### Analyze Command

Analyze a Python file for code quality issues:

```bash
python -m src.main analyze <input_file> [options]
```

**Options:**

- `--verbose, -v`: Show detailed analysis report with suggestions

**Example:**

```bash
python -m src.main analyze my_code.py --verbose
```

#### Improve Command (AI-Powered)

Transform code using AI with Chain of Thought reasoning:

```bash
python -m src.main improve <input_file> [options]
```

**Options:**

- `--provider {openai|groq}`: LLM provider (default: groq, free tier available)
- `--model <model>`: Specific model to use (optional)
- `--type {all|readability|performance|security}`: Focus area (default: all)
- `--output, -o <file>`: Output file path (default: `<input>_improved.py`)
- `--api-key <key>`: API key (or set env var OPENAI_API_KEY/GROQ_API_KEY)
- `--verbose, -v`: Show detailed Chain of Thought analysis

**Example:**

```bash
# Using free Groq API (requires GROQ_API_KEY env var)
python -m src.main improve messy_code.py --provider groq --verbose

# Using OpenAI GPT (requires OPENAI_API_KEY env var)
python -m src.main improve messy_code.py --provider openai --type readability

# Specific model
python -m src.main improve messy_code.py --provider groq --model mixtral-8x7b-32768
```

#### Security Command (AI-Powered)

AI-powered security vulnerability analysis:

```bash
python -m src.main security <input_file> [options]
```

**Options:**

- `--provider {openai|groq}`: LLM provider (default: groq)
- `--api-key <key>`: API key (or set env var)
- `--verbose, -v`: Show detailed analysis

**Example:**

```bash
python -m src.main security app.py --provider groq --verbose
```

## AI Features Setup

### Prerequisites

Clean Code Bot supports two LLM providers: **Groq** (free) and **OpenAI** (paid).

#### Option 1: Groq (Recommended - Free Tier)

1. Sign up at [https://console.groq.com](https://console.groq.com)
2. Get your free API key
3. Set environment variable:

   ```bash
   # Windows PowerShell
   $env:GROQ_API_KEY = "your-api-key"

   # Windows CMD
   set GROQ_API_KEY=your-api-key

   # macOS/Linux
   export GROQ_API_KEY="your-api-key"
   ```

#### Option 2: OpenAI (Paid)

1. Sign up at [https://platform.openai.com](https://platform.openai.com)
2. Add $5+ credit to your account
3. Get your API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Set environment variable:

   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY = "sk-..."

   # macOS/Linux
   export OPENAI_API_KEY="sk-..."
   ```

### Install AI Dependencies

```bash
# Install both providers (recommended)
pip install -r requirements.txt

# Or install only what you need:
pip install groq  # For Groq
pip install openai  # For OpenAI
```

### Running Tests

```bash
python -m pytest tests/
```

### Project Structure

```
clean-code-bot/
├── src/
│   ├── main.py                # CLI entry point
│   ├── cli.py                 # CLI argument parser
│   ├── analyzer.py            # Code quality analysis
│   ├── optimizer.py           # Code optimization
│   ├── documenter.py          # Documentation generation
│   ├── llm_integrator.py      # LLM provider integration
│   ├── prompt_templates.py    # Chain of Thought prompts
│   ├── security.py            # Input validation & injection prevention
│   ├── utils.py               # Utility functions
│   └── __init__.py
├── examples/                  # Before/after code examples
│   ├── before_example.py      # Dirty code sample
│   ├── after_example.py       # Cleaned code sample
│   └── README.md              # Examples documentation
├── tests/                     # Test files
├── requirements.txt           # Project dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

### Features

#### Static Analysis & Optimization

- **Code Analysis**: Detects SOLID principle violations, missing documentation, and complexity issues
- **Code Optimization**: Applies readability improvements, naming conventions, and code refactoring
- **Documentation Generation**: Automatically adds comprehensive docstrings in Google style format
- **Type Hints**: Optional type annotation support
- **Code Formatting**: Black-style formatting for consistent code style

#### AI-Powered Features

- **Chain of Thought (CoT) Reasoning**: AI guides through structured analysis phases:
  - **Understanding**: What does the code do?
  - **Analysis**: What are the issues?
  - **Reasoning**: Why do they matter?
  - **Recommendation**: How to fix them?

- **Security Analysis**: AI detects vulnerabilities and suggests secure practices
- **Multi-Provider Support**: Use either Groq (free) or OpenAI (paid)
- **Input Validation**: Prevents prompt injection attacks and validates code safety

## Security & Safety

✅ **Input Validation**: All code inputs are validated for size and encoding
✅ **Prompt Injection Protection**: Detects and prevents malicious prompt attempts
✅ **Sensitive Data Masking**: Automatically masks API keys and credentials
✅ **Safe LLM Integration**: Secure API communication with error handling

## Examples

Check the [examples/](examples/) folder for before-and-after code samples:

- `before_example.py`: Common code quality issues
- `after_example.py`: Improved, clean version
- `examples/README.md`: Detailed explanations

## Troubleshooting

### "No module named 'openai'" or "No module named 'groq'"

```bash
pip install -r requirements.txt
```

### "API key not provided"

Set your environment variable:

```bash
# Groq
$env:GROQ_API_KEY = "your-key"

# OpenAI
$env:OPENAI_API_KEY = "your-key"
```

### "High-risk input detected"

Your code contains patterns that might be injection attempts. If this is a false positive, you can still process the code using static analysis commands (`analyze`, `optimize`).

## License

MIT
