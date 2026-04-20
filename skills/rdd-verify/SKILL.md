---
name: rdd-verify
description: This skill should be used when the user says "verify RDD", "rdd verify", "check completion", "check requirements met", "validate RDD", or wants to confirm all requirements have been implemented. Also triggers on "验证 RDD", "检查完成度", "需求验证".
---

# RDD Verification

Comprehensive verification that the RDD workflow is complete.

## When to Use

- User asks to verify RDD completion
- After implementing all requirements
- Before committing or creating a PR
- As a final quality gate

## Verification Checklist

Run each check in order. Report results as PASS/FAIL.

### Check 1: Requirement Files Exist

Use Glob to find all requirement files:
- `docs/requirements/req_*.md`

For each requirement file, verify:
- File has a proper header with module name
- Table has at least 4 rows (2 normal + 1 boundary + 1 error)
- All IDs follow the module abbreviation + number convention

### Check 2: Test Files Correspond

For each `docs/requirements/req_{module}.md`:
- Verify `tests/test_{module}.py` exists
- If missing: FAIL - "Missing test file for {module}"

### Check 3: Test IDs Match Requirement IDs

For each test file:
- Extract IDs from the `ids=[...]` list or test parametrize decorator
- Compare with IDs in the corresponding requirement table
- Report any missing or extra IDs

### Check 4: All Tests Pass

Run `pytest tests/ -v --tb=short`:
- Count total tests, passed, failed, errors
- If any tests FAIL: report which ones by ID
- If all tests PASS: mark as complete

### Check 5: No Extra Features

Compare source files with requirement tables:
- Each source file in `src/` should correspond to a requirement file
- Flag any source files without corresponding requirements as "potentially untracked"

## Output Format

```
RDD Verification Report
========================

Requirements:
  [PASS] 3 requirement files found
  [PASS] All tables have minimum coverage (2+ normal, 1+ boundary, 1+ error)

Tests:
  [PASS] test_auth.py <-> req_auth.md (4/4 IDs matched)
  [FAIL] test_calc.py <-> req_calc.md: missing IDs CALC-03, CALC-04

Test Results:
  [PASS] 12 tests passed, 0 failed

Extra Files:
  [WARN] src/utils.py has no corresponding requirement file

Overall: 3/4 checks passed. See details above.
```

## Verdict

- **All PASS**: RDD workflow is complete. Safe to commit/PR.
- **Any FAIL**: List specific issues and suggest fixes.
- **WARN only**: Minor issues that don't block completion.
