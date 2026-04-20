---
name: rdd-implement
description: This skill should be used when the user says "start implementing", "rdd implement", "let's code", "make tests green", or wants to begin writing business code to pass existing tests. Also triggers on "开始实现", "让测试通过".
---

# RDD Step-by-Step Implementation

Guide implementation of business code one requirement at a time.

## When to Use

- Requirement tables exist in `docs/requirements/`
- Test files exist in `tests/`
- Tests are RED (failing) and need to turn GREEN
- User is ready to write business code

## Prerequisites

- Requirement files at `docs/requirements/req_*.md`
- Test files at `tests/test_*.py`
- Tests are failing (this is expected - RED phase)

## Process

### Step 1: Assess Current State

Run `pytest tests/ --tb=line -q` to see which tests fail.
Identify the first failing test by requirement ID order.

### Step 2: Pick One Requirement

Select the lowest-numbered failing test:
```
Next: AUTH-01 (正常登录)
File: tests/test_auth.py
Requirement: docs/requirements/req_auth.md
```

### Step 3: Read the Requirement

Read the specific requirement row from the requirement file.
Understand exactly what input -> output is expected.

### Step 4: Implement Minimal Code

Write the **simplest** code that makes THIS ONE test pass:
- Create or edit the source file in `src/`
- Only implement what's needed for this specific test
- Do NOT implement features for future requirements

### Step 5: Verify

Run the specific test:
```bash
pytest tests/test_{module}.py -v -k "{ID}"
```

If GREEN -> move to next requirement.
If RED -> debug and fix, then re-verify.

### Step 6: Repeat

Go back to Step 2 and pick the next failing test.
Continue until all tests are GREEN.

## Implementation Rules

1. **One requirement at a time** - never implement multiple requirements in one pass
2. **Minimal implementation** - only write enough code to pass the current test
3. **Verify immediately** - run the test after each implementation step
4. **Dependency order** - implement base modules before dependent modules
5. **No speculative code** - don't add features not in the requirement table

## Dependency Ordering

If modules depend on each other, implement in this order:
1. Core/data modules (no dependencies)
2. Processing/logic modules (depend on core)
3. Integration/API modules (depend on logic)
4. Interface modules (depend on everything)

## Completion

When all tests are GREEN:
- Run `pytest tests/ -v` to confirm full suite passes
- Suggest running `rdd-verify` skill for final verification
