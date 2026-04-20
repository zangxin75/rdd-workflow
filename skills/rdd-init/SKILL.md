---
name: rdd-init
description: This skill should be used when the user says "initialize RDD", "rdd init", "create RDD project", "set up RDD directories", or wants to start a new RDD-based project. Also triggers on "初始化 RDD", "创建 RDD 项目".
---

# RDD Project Initialization

Initialize the Requirement-Driven Development project structure.

## When to Use

- Starting a new project that will use RDD workflow
- Setting up RDD in an existing empty project
- User explicitly asks to initialize RDD

## Process

### Step 1: Check Current State

Use Glob to check if RDD directories already exist:
- `docs/requirements/` or `文档/需求/`
- `tests/` or `代码/测试代码/`
- `src/` or `代码/Python脚本/`

If all directories exist, inform the user and skip to Step 3.

### Step 2: Create Directory Structure

Create the following directories and files:

```
{project_root}/
├── docs/
│   └── requirements/              <- Requirement tables
│       └── .gitkeep
├── src/                           <- Business code
│   └── .gitkeep
├── tests/                         <- Test code
│   ├── __init__.py
│   └── conftest.py               <- Shared fixtures
└── pytest.ini                    <- Pytest configuration
```

Use Bash `mkdir -p` for directories, then Write for files.

### Step 3: Write Configuration Files

**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*
addopts = -v --tb=short
```

**tests/conftest.py:**
```python
import sys
from pathlib import Path

import pytest

# Ensure src/ is importable
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@pytest.fixture
def project_root():
    """Provide project root path."""
    return PROJECT_ROOT
```

### Step 4: Confirm and Guide

After creation, display:
1. Directory tree created
2. Next step: Use `rdd-req` skill to create first requirement table
3. Example: "Describe a feature you want to implement"

## Notes

- Respect Chinese directory names if the user prefers (`文档/需求/`, `代码/`)
- Do NOT overwrite existing files - only create missing ones
- Always create `.gitkeep` in empty directories for git tracking
