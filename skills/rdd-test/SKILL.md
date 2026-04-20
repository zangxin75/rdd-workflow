---
name: rdd-test
description: This skill should be used when the user says "generate tests", "write tests", "rdd test", "convert requirements to tests", or wants to create test code from requirement tables. Also triggers on "生成测试", "写测试", "需求转测试".
---

# RDD Test Generation

Convert requirement tables into parameterized pytest test files.

## When to Use

- Requirement tables exist in `docs/requirements/`
- User asks to generate tests from requirements
- User says "convert requirements to tests"
- After rdd-req skill has been completed

## Prerequisites

- Requirement file(s) must exist at `docs/requirements/req_*.md`
- `tests/` directory must exist
- pytest must be available

## Process

### Step 1: Identify Requirement Files

Use Glob to find all requirement files:
- `docs/requirements/req_*.md`
- Also check `文档/需求/req_*.md` for Chinese paths

### Step 2: Parse Requirement Tables

For each requirement file:
1. Read the file content
2. Extract the module name from filename: `req_auth.md` -> `auth`
3. Extract the table rows (ID, Scenario, Input, Expected Output)
4. Identify the module abbreviation from IDs (e.g., "AUTH" from "AUTH-01")

### Step 3: Generate Test File

Create `tests/test_{module_name}.py` using this template:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Module: {module_display_name}
Requirement File: docs/requirements/req_{module_name}.md
"""
import pytest
import sys
from pathlib import Path

# Project path setup
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# ============================================================
# Test Data - from requirement table
# ============================================================

TEST_CASES = [
    # (ID, scenario, input_data, expected_output)
    ("{ID-01}", "{scenario}", {input}, {expected}),
    ("{ID-02}", "{scenario}", {input}, {expected}),
    ("{ID-03}", "{scenario}", {input}, {expected}),
    ("{ID-04}", "{scenario}", {input}, {expected}),
]

# ============================================================
# Parameterized Tests
# ============================================================

@pytest.mark.parametrize(
    "case_id, description, input_data, expected",
    TEST_CASES,
    ids=[c[0] for c in TEST_CASES]
)
def test_{module_name}(case_id, description, input_data, expected):
    """
    Requirement ID: {case_id}
    Scenario: {description}
    """
    # Arrange - setup

    # Act - execute
    result = {module_function}(input_data)

    # Assert - verify
    assert result == expected, \
        f"{case_id} [{description}]: expected {expected!r}, got {result!r}"
```

### Step 4: Write Test File

Use the Write tool to create the test file. Make sure:
- The function being tested is imported or called correctly
- The test function name matches the module
- All requirement IDs appear in the `ids` list
- Assertions use the exact expected values from the requirement table

### Step 5: Verify Test Discovery

Run `pytest tests/ --collect-only -q` to verify tests are discovered.
Do NOT run the tests (they should fail since business code doesn't exist yet).

## Multi-File Handling

If multiple requirement files exist:
- Process them one at a time
- Each requirement file = one test file
- Ask the user which one to process first, or process all

## Notes

- Tests MUST initially fail (RED phase) - this is correct behavior
- Do not implement any business logic in the test file
- Use `@pytest.mark.parametrize` for all test cases from the table
- The test file header must reference the requirement file path
