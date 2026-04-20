#!/usr/bin/env python3
"""
RDD Stop Guard: Check RDD completion status before session ends.

Checks:
  1. All requirement files have corresponding test files
  2. Quick test status summary
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def get_tool_input():
    """Read tool input from stdin (Claude Code hook protocol)."""
    try:
        return json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return {}


def find_requirement_files() -> list[Path]:
    """Find all requirement files."""
    files = []
    for pattern_dir in ["docs/requirements", "文档/需求"]:
        p = Path(pattern_dir)
        if p.exists():
            files.extend(p.glob("req_*.md"))
    return sorted(files)


def module_from_req(req_path: Path) -> str:
    """Extract module name from requirement file path."""
    # req_auth.md -> auth
    stem = req_path.stem  # req_auth
    if stem.startswith("req_"):
        return stem[4:]
    return stem


def check_tests_exist(req_files: list[Path]) -> list[dict]:
    """Check which requirement files have corresponding tests."""
    results = []
    for req_file in req_files:
        module = module_from_req(req_file)
        test_candidates = [
            Path(f"tests/test_{module}.py"),
            Path(f"代码/测试代码/test_{module}.py"),
        ]
        has_test = any(t.exists() for t in test_candidates)
        test_path = next((t for t in test_candidates if t.exists()), None)
        results.append({
            "module": module,
            "req_file": req_file,
            "has_test": has_test,
            "test_file": test_path,
        })
    return results


def run_tests_quick() -> dict | None:
    """Run pytest quickly to get pass/fail counts."""
    try:
        result = subprocess.run(
            ["python3", "-m", "pytest", "tests/", "--tb=no", "-q", "--no-header"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout + result.stderr
        return {"output": output, "returncode": result.returncode}
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def main():
    req_files = find_requirement_files()

    # No requirement files - nothing to check
    if not req_files:
        sys.exit(0)

    # Check test coverage
    coverage = check_tests_exist(req_files)
    missing_tests = [c for c in coverage if not c["has_test"]]

    # Build messages
    messages = []

    if missing_tests:
        modules = ", ".join(c["module"] for c in missing_tests)
        messages.append(
            f"RDD reminder: {len(missing_tests)} module(s) missing tests: {modules}"
        )
        messages.append("  Use rdd-test skill to generate tests before stopping.")

    # Quick test run
    if not missing_tests:
        test_result = run_tests_quick()
        if test_result and test_result["returncode"] != 0:
            messages.append("RDD reminder: some tests are still failing.")
            messages.append(f"  {test_result['output'].strip()}")

    # Output reminders
    if messages:
        print("hook info: RDD workflow status check")
        for msg in messages:
            print(f"  {msg}")

    sys.exit(0)


if __name__ == "__main__":
    main()
