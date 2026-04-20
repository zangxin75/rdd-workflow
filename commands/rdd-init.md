---
description: "Quick initialize RDD project structure (docs/requirements, tests, src, config files)"
---

# Quick RDD Init

Initialize the RDD project structure immediately.

## Steps

1. Check if directories already exist (Glob for `docs/requirements/`, `tests/`, `src/`)
2. Create missing directories with `mkdir -p`:
   - `docs/requirements/`
   - `tests/`
   - `src/`
3. Write configuration files if missing:
   - `pytest.ini` with standard pytest config
   - `tests/conftest.py` with project root path setup
   - `.gitkeep` files in empty directories
4. Display created structure and next step

## pytest.ini content
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*
addopts = -v --tb=short
```

## conftest.py content
```python
import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@pytest.fixture
def project_root():
    return PROJECT_ROOT
```

After init, suggest: "Ready! Describe a feature to create your first requirement table."
