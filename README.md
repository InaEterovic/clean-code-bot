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

Run the application:

```bash
python -m src.main
```

Run tests:

```bash
python -m pytest tests/
```

## License

MIT
