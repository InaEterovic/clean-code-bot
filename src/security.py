"""Security module for input validation and sanitization."""

import re
from typing import Tuple, List
from pathlib import Path


class PromptInjectionDetector:
    """Detects potential prompt injection attempts in code input."""

    SUSPICIOUS_PATTERNS = [
        r"(ignore|forget|override|bypass|disable|bypass|system.*prompt)",
        r"(instruction|command|directive).*:",
        r"('|\")\s*\+\s*[a-zA-Z_]",  # String concatenation with variables
        r"(\{|\[).*(\}|\])",  # Template/variable injection
        r"(eval|exec|__import__|compile|globals|locals)",  # Dynamic execution
    ]

    DANGEROUS_KEYWORDS = [
        "prompt_injection",
        "jailbreak",
        "bypass_filter",
        "ignore_system",
        "override_instruction",
    ]

    @staticmethod
    def detect_injection_patterns(code: str) -> Tuple[bool, List[str]]:
        detected_patterns = []
        code_lower = code.lower()

        # Check for dangerous keywords
        for keyword in PromptInjectionDetector.DANGEROUS_KEYWORDS:
            if keyword.lower() in code_lower:
                detected_patterns.append(f"Dangerous keyword: '{keyword}'")

        # Check for suspicious patterns
        for pattern in PromptInjectionDetector.SUSPICIOUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                detected_patterns.append(f"Suspicious pattern detected: {pattern}")

        return len(detected_patterns) > 0, detected_patterns

    @staticmethod
    def get_risk_level(code: str) -> str:
        is_suspicious, patterns = PromptInjectionDetector.detect_injection_patterns(code)

        if not is_suspicious:
            return "safe"

        pattern_count = len(patterns)
        if pattern_count <= 1:
            return "low"
        elif pattern_count <= 3:
            return "medium"
        else:
            return "high"


class InputValidator:
    """Validates code input for safety and compliance."""

    MAX_CODE_SIZE = 10 * 1024 * 1024
    MAX_LINES = 10000

    @staticmethod
    def validate_code_input(code: str) -> Tuple[bool, str]:
        if not code or not code.strip():
            return False, "Code input is empty"

        if len(code.encode("utf-8")) > InputValidator.MAX_CODE_SIZE:
            return False, f"Code exceeds maximum size of {InputValidator.MAX_CODE_SIZE / 1024 / 1024:.1f} MB"

        line_count = len(code.split("\n"))
        if line_count > InputValidator.MAX_LINES:
            return False, f"Code exceeds maximum of {InputValidator.MAX_LINES} lines"

        if "\x00" in code:
            return False, "Code contains null bytes"

        try:
            code.encode("utf-8").decode("utf-8")
        except UnicodeEncodeError:
            return False, "Code contains invalid UTF-8 characters"

        return True, ""

    @staticmethod
    def validate_file_input(file_path: str) -> Tuple[bool, str]:
        path = Path(file_path)

        if not path.exists():
            return False, f"File not found: {file_path}"

        if not path.is_file():
            return False, f"Path is not a file: {file_path}"

        file_size = path.stat().st_size
        if file_size > InputValidator.MAX_CODE_SIZE:
            return False, f"File exceeds maximum size of {InputValidator.MAX_CODE_SIZE / 1024 / 1024:.1f} MB"

        if path.suffix != ".py":
            return False, f"File must be a Python file (.py), got: {path.suffix}"

        return True, ""


class InputSanitizer:
    """Sanitizes and normalizes code input."""

    @staticmethod
    def sanitize_code(code: str) -> str:
        code = code.replace("\x00", "")

        code = code.replace("\r\n", "\n").replace("\r", "\n")
        code = code.strip()

        return code

    @staticmethod
    def remove_sensitive_patterns(code: str) -> str:
        sensitive_patterns = [
            (r"(api[_-]?key|apikey|password|secret|token|credential)\s*=\s*['\"]?[^'\"]*['\"]?",
             r"\1 = '***REDACTED***'"),
            (r"(https?://[^\s/'\"\\)]*:[^\s/'\"\\)]*@)",
             "***REDACTED***://***:***@"),
        ]

        sanitized = code
        for pattern, replacement in sensitive_patterns:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        return sanitized

    @staticmethod
    def prepare_for_llm(code: str) -> str:
        is_valid, error_msg = InputValidator.validate_code_input(code)
        if not is_valid:
            raise ValueError(f"Invalid code input: {error_msg}")

        is_suspicious, patterns = PromptInjectionDetector.detect_injection_patterns(code)
        if is_suspicious:
            risk_level = PromptInjectionDetector.get_risk_level(code)
            if risk_level == "high":
                raise ValueError(f"High-risk input detected. Refusing to process. Patterns: {patterns}")

        code = InputSanitizer.sanitize_code(code)
        code = InputSanitizer.remove_sensitive_patterns(code)

        return code
