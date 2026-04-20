#!/usr/bin/env python3
"""
RDD PreToolUse Guard: Block source code writes without requirement tables.

Checks:
  1. If editing src/ files, verify a corresponding requirement file exists.
  2. If editing src/ files, warn if no corresponding test file exists.
"""

import json
import os
import sys
import re
from pathlib import Path


def get_tool_input():
    """Read tool input from stdin (Claude Code hook protocol)."""
    try:
        return json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return {}


def extract_module_name(file_path: str) -> str | None:
    """Extract module name from a source file path."""
    # Normalize path separators
    file_path = file_path.replace("\\", "/")

    # Match src/module_name.py or src/subdir/module_name.py
    match = re.search(r"src/(?:.+/)?([^/]+)\.py$", file_path)
    if match:
        return match.group(1)

    # Match Chinese path: 代码/Python脚本/module_name.py
    match = re.search(r"(?:Python脚本|src)/(?:.+/)?([^/]+)\.py$", file_path)
    if match:
        return match.group(1)

    return None


def find_requirement_file(module_name: str) -> Path | None:
    """Check if a requirement file exists for this module."""
    # Standard paths
    candidates = [
        Path(f"docs/requirements/req_{module_name}.md"),
        Path(f"文档/需求/req_{module_name}.md"),
    ]

    # Also check with different naming conventions
    # e.g., module_name "user_auth" -> try "user-auth" and "userauth"
    name_variants = [
        module_name,
        module_name.replace("_", "-"),
        module_name.replace("-", "_"),
    ]

    all_candidates = []
    for variant in name_variants:
        all_candidates.extend([
            Path(f"docs/requirements/req_{variant}.md"),
            Path(f"文档/需求/req_{variant}.md"),
        ])

    for candidate in all_candidates:
        if candidate.exists():
            return candidate

    return None


def find_test_file(module_name: str) -> Path | None:
    """Check if a test file exists for this module."""
    candidates = [
        Path(f"tests/test_{module_name}.py"),
        Path(f"代码/测试代码/test_{module_name}.py"),
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def main():
    tool_input = get_tool_input()

    # Get the file path being written/edited
    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "")
    file_path = ""

    # Try to extract file path from tool input
    if isinstance(tool_input, dict):
        file_path = tool_input.get("file_path", "")
        if not file_path:
            file_path = tool_input.get("path", "")

    if not file_path:
        # Not a file write we care about
        sys.exit(0)

    # Only guard src/ files (business code)
    normalized = file_path.replace("\\", "/")
    is_src = "/src/" in normalized or "/Python脚本/" in normalized

    if not is_src:
        sys.exit(0)

    module_name = extract_module_name(file_path)
    if not module_name:
        sys.exit(0)

    # Check 1: Does a requirement file exist?
    req_file = find_requirement_file(module_name)
    if not req_file:
        print(f"hook error: RDD violation - no requirement table found for module '{module_name}'.")
        print(f"  Create docs/requirements/req_{module_name}.md first (use rdd-req skill).")
        print(f"  File being written: {file_path}")
        sys.exit(0)

    # Check 2: Does a test file exist? (warning only)
    test_file = find_test_file(module_name)
    if not test_file:
        print(f"hook warning: RDD - no test file found for module '{module_name}'.")
        print(f"  Consider generating tests first: use rdd-test skill.")
        print(f"  Requirement file: {req_file}")
        sys.exit(0)


if __name__ == "__main__":
    main()
