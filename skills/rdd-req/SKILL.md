---
name: rdd-req
description: This skill should be used when the user says "write requirements", "create requirement table", "rdd req", describes a feature to implement, or wants to define what a module should do before coding. Also triggers on "写需求", "创建需求表", "需求表".
---

# RDD Requirement Table Generation

Interactive skill for generating structured requirement tables from feature descriptions.

## When to Use

- User describes a feature they want to implement
- User explicitly asks to create a requirement table
- User says "write requirements for X"
- Before any business code is written (RDD enforcement)

## Core Principle

**Every requirement must have concrete, testable inputs and outputs.**

- Specific input: `"创建一个 100x100x50mm 的方块"` (not: `"一段创建零件的自然语言"`)
- Specific output: `action="create", object="part"` (not: `"返回正确结果"`)

## Process

### Step 1: Analyze Feature Description

Read the user's feature description. Identify:
1. **Modules**: Can this be split into independent modules?
2. **Inputs**: What data enters each module?
3. **Outputs**: What should each module produce?
4. **Edge cases**: What could go wrong?

### Step 2: Module Decomposition

If the feature has multiple independent concerns, suggest splitting into modules:
- Each module = one requirement file
- Each module = one test file
- Each module = one source file

Ask the user to confirm the module split before proceeding.

### Step 3: Generate Requirement Table

For each module, create a requirement file at `docs/requirements/req_{module_name}.md`.

**Format:**

```markdown
## Feature: {Module Name}

**Parent Module**: {parent}
**Dependencies**: {none or list}
**Type**: Unit Test / Integration Test

### Requirement Table

| ID | Scenario | Input | Expected Output | Notes |
|----|----------|-------|-----------------|-------|
| XX-01 | {normal scenario} | {concrete input} | {concrete output} | |
| XX-02 | {normal scenario} | {concrete input} | {concrete output} | |
| XX-03 | {boundary scenario} | {concrete input} | {concrete output} | |
| XX-04 | {error scenario} | {concrete input} | {concrete output} | |
```

**ID Convention**: Module abbreviation + sequence (e.g., AUTH-01, CALC-03, PARSE-02)

### Step 4: Coverage Rules

Every requirement table MUST have:
- At least **2 normal scenarios** (happy path)
- At least **1 boundary scenario** (edge case: empty, max, zero, None)
- At least **1 error scenario** (invalid input, missing data)

### Step 5: Write and Confirm

1. Write the file using the Write tool
2. Display the table to the user for review
3. Ask: "Does this cover all the scenarios you need?"
4. If the user requests changes, edit the file

## Example

For a "user authentication" feature, see the example file in the examples directory.

## Quality Checklist

Before finalizing, verify:
- [ ] Every input is a concrete value (not vague description)
- [ ] Every expected output is assertable (can be compared with ==)
- [ ] IDs follow the module abbreviation + number convention
- [ ] At least 4 rows (2 normal + 1 boundary + 1 error)
- [ ] File is at `docs/requirements/req_{module_name}.md`
