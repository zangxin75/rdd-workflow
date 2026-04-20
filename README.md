# RDD Workflow - Claude Code Plugin

Requirement-Driven Development (RDD) workflow plugin for Claude Code.

## Philosophy

Define "what counts as done" BEFORE writing code.

**Flow**: Requirement Tables -> Parameterized Tests -> Business Code

## Quick Start

### Install

```bash
cd ~/.claude/plugins/
git clone <this-repo-url> rdd-workflow
```

Restart Claude Code, then:

```
/rdd-init          # Initialize project structure
/rdd               # Check RDD status
```

### Workflow

1. **`/rdd-init`** - Create `docs/requirements/`, `tests/`, `src/` directories
2. **Say "write requirements for ..."** - Generate requirement tables
3. **Say "generate tests"** - Convert requirements to parameterized pytest
4. **Say "start implementing"** - Step-by-step code implementation
5. **Say "verify RDD"** - Full completion check

## Components

### Skills (5)
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `rdd-init` | "initialize RDD", "rdd init" | Create project structure |
| `rdd-req` | "write requirements", "create req table" | Generate requirement tables |
| `rdd-test` | "generate tests", "rdd test" | Convert requirements to pytest |
| `rdd-implement` | "start implementing", "rdd implement" | Step-by-step coding |
| `rdd-verify` | "verify RDD", "rdd verify" | Completion check |

### Agents (2)
| Agent | Model | Role |
|-------|-------|------|
| `rdd-analyst` | opus | Analyze requirements, decompose modules |
| `rdd-test-gen` | sonnet | Generate test files from requirements |

### Hooks (2)
| Hook | Event | Purpose |
|------|-------|---------|
| `guard_source` | PreToolUse | Block code writes without requirements |
| `guard_stop` | Stop | Remind incomplete work on session end |

## License

MIT
