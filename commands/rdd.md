---
description: "Show RDD workflow status: requirement files, test coverage, pass rate, and next step suggestion"
argument-hint: "[module name] to check specific module status"
---

# RDD Status Command

Display the current RDD workflow status for this project.

## What to Show

### 1. Project Structure
Check and display which RDD directories exist:
- `docs/requirements/` - Requirement tables
- `tests/` - Test files
- `src/` - Business code

### 2. Requirement Summary
For each `docs/requirements/req_*.md`:
- Module name
- Number of requirement rows
- IDs present

### 3. Test Coverage
For each requirement file, check if corresponding test exists:
- `tests/test_{module}.py` present?
- IDs in test match IDs in requirement?

### 4. Test Results
Run `pytest tests/ --tb=no -q` and show:
- Total tests / passed / failed / errors
- Failing test IDs if any

### 5. Next Step
Based on status, suggest the next action:
- No requirements -> "Use rdd-req to create requirement tables"
- Requirements but no tests -> "Use rdd-test to generate tests"
- Tests failing -> "Use rdd-implement to start coding"
- All passing -> "Use rdd-verify for final verification"

## Output Format

```
RDD Status
==========
Structure: docs/requirements/ (3 files) | tests/ (3 files) | src/ (2 files)

Requirements:
  auth: 5 scenarios (AUTH-01..AUTH-05)
  calc: 4 scenarios (CALC-01..CALC-04)
  parse: 3 scenarios (PARSE-01..PARSE-03)

Tests:
  test_auth.py: 5/5 IDs matched
  test_calc.py: 4/4 IDs matched
  test_parse.py: MISSING

Results: 9 passed, 0 failed

Next: Generate tests for parse module (rdd-test)
```
