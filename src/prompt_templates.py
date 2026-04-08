"""Prompt engineering module using Chain of Thought (CoT) technique."""

from typing import Dict, List, Optional
from enum import Enum


class AnalysisPhase(Enum):
    """Phases of the Chain of Thought analysis."""
    UNDERSTANDING = "understanding"
    ANALYSIS = "analysis"
    REASONING = "reasoning"
    RECOMMENDATION = "recommendation"


class PromptTemplate:
    """Base class for prompt templates using Chain of Thought technique."""

    COT_PREFIX = """You are an expert Python code reviewer and refactor specialist.
Use the following Chain of Thought (CoT) approach to analyze and improve code:

1. UNDERSTANDING: First, understand what the code does, its purpose, and functionality.
2. ANALYSIS: Identify specific code quality issues, violations of best practices, and areas for improvement.
3. REASONING: Explain why these issues matter and how they impact code maintainability.
4. RECOMMENDATION: Propose specific, actionable improvements with explanations.

Focus on:
- SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion)
- Code readability and maintainability
- Performance optimization
- Security concerns
- Documentation quality
- Type safety and hints

Be concise but thorough. Provide concrete examples and code snippets."""

    @staticmethod
    def code_analysis_prompt(code: str, language: str = "python") -> str:
        return f"""{PromptTemplate.COT_PREFIX}

Now, analyze this {language} code using the CoT approach:

```{language}
{code}
```

Provide your analysis in the following structure:

**UNDERSTANDING:**
[Explain what this code does]

**ANALYSIS:**
[Identify issues and problems]

**REASONING:**
[Explain why these issues matter]

**RECOMMENDATION:**
[Propose specific improvements with code examples]

Format improvements as actionable code snippets."""

    @staticmethod
    def code_improvement_prompt(code: str, improvement_type: str = "all") -> str:
        focus_areas = {
            "all": "readability, performance, SOLID principles, and security",
            "readability": "naming conventions, structure, and clarity",
            "performance": "computational efficiency and resource usage",
            "security": "input validation, injection prevention, and safe practices",
        }

        focus = focus_areas.get(improvement_type, focus_areas["all"])

        return f"""{PromptTemplate.COT_PREFIX}

Improve this Python code focusing on {focus}.

```python
{code}
```

Apply the CoT approach:

**UNDERSTANDING:**
[Summarize what the code does]

**ANALYSIS:**
[Identify specific improvement opportunities]

**REASONING:**
[Explain how these improvements help]

**RECOMMENDATION:**
[Provide refactored code with explanations]

Important:
- Return the complete improved code
- Add comprehensive docstrings in Google style
- Include type hints
- Add inline comments for complex logic"""

    @staticmethod
    def documentation_prompt(code: str, existing_docs: Optional[str] = None) -> str:
        docs_context = f"\nExisting documentation:\n{existing_docs}\n" if existing_docs else ""

        return f"""{PromptTemplate.COT_PREFIX}

Generate comprehensive documentation for this Python code.{docs_context}

```python
{code}
```

Apply the CoT approach:

**UNDERSTANDING:**
[Understand the code's purpose and functionality]

**ANALYSIS:**
[Identify what needs documentation]

**REASONING:**
[Explain how good documentation improves the code]

**RECOMMENDATION:**
[Provide complete, well-documented code]

Documentation requirements:
- Module-level docstring
- Class docstrings with purpose and usage
- Function/method docstrings in Google style (Args, Returns, Raises, Examples)
- Complex algorithm explanations
- Type hints throughout"""

    @staticmethod
    def refactoring_prompt(code: str, issues: List[str]) -> str:
        issues_str = "\n".join(f"- {issue}" for issue in issues)

        return f"""{PromptTemplate.COT_PREFIX}

Refactor this Python code to address the following issues:

{issues_str}

Code to refactor:
```python
{code}
```

Apply the CoT approach:

**UNDERSTANDING:**
[Understand the current code and issues]

**ANALYSIS:**
[Analyze how to fix each issue]

**REASONING:**
[Explain why refactoring improves the code]

**RECOMMENDATION:**
[Provide refactored code addressing all issues]

Ensure:
- All issues are resolved
- Code quality is improved
- SOLID principles are followed
- Documentation is comprehensive"""

    @staticmethod
    def security_review_prompt(code: str) -> str:
        return f"""{PromptTemplate.COT_PREFIX}

Perform a security review of this Python code and identify vulnerabilities.

```python
{code}
```

Apply the CoT approach:

**UNDERSTANDING:**
[Understand the code's functionality and potential attack vectors]

**ANALYSIS:**
[Identify specific security vulnerabilities]

**REASONING:**
[Explain the severity and impact of each vulnerability]

**RECOMMENDATION:**
[Propose secure fixes with code examples]

Focus on:
- Input validation and sanitization
- SQL/Command injection prevention
- XXE and deserialization attacks
- Authentication and authorization
- Cryptographic best practices
- Dependency vulnerabilities"""


class ChainOfThought:
    """Implements Chain of Thought reasoning for code analysis."""

    @staticmethod
    def extract_cot_phases(response: str) -> Dict[AnalysisPhase, str]:
        phases = {}
        current_phase = None
        content = ""

        for line in response.split("\n"):
            for phase in AnalysisPhase:
                if phase.value.upper() in line:
                    if current_phase and content.strip():
                        phases[current_phase] = content.strip()
                    current_phase = phase
                    content = ""
                    break
            else:
                if current_phase:
                    content += line + "\n"

        if current_phase and content.strip():
            phases[current_phase] = content.strip()

        return phases

    @staticmethod
    def format_cot_analysis(phases: Dict[AnalysisPhase, str]) -> str:
        """
        Format extracted CoT phases for display.

        Args:
            phases: Dictionary of CoT phases and content.

        Returns:
            str: Formatted analysis report.
        """
        output = "Chain of Thought Analysis:\n"
        output += "=" * 60 + "\n\n"

        for phase in AnalysisPhase:
            if phase in phases:
                output += f"📊 {phase.value.upper()}:\n"
                output += phases[phase] + "\n\n"

        return output
