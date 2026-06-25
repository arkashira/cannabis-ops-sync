<h3 align="center">🛠️ cannabis-ops-sync</h3>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language: Python](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/)
[![Build: pytest](https://img.shields.io/badge/build-pytest-green.svg)](https://docs.pytest.org/)
[![Stars: 0](https://img.shields.io/github/stars/axentx/cannabis-ops-sync.svg)](https://github.com/axentx/cannabis-ops-sync/stargazers)

</div>

---

# 🚀 cannabis-ops-sync

**Power cannabis operators with role-validation and user data management.**

## Why cannabis-ops-sync?

- **Role Validation**: Ensures only valid roles (Operations Manager, Admin, Guest) are accepted.
- **Minimal CLI**: Lightweight command-line interface for quick user info retrieval.
- **Built for Cannabis Operators**: Designed for system admins managing access in regulated environments.
- **Error Handling**: Gracefully rejects invalid inputs with clear error messages.
- **Extensible Design**: Easy to expand with additional fields or validation rules.
- **Sandbox Tested**: Verified in test environments before deployment.
- **Open Source**: MIT licensed for community-driven enhancements.

## Feature Overview

| Feature              | Description                                               |
|----------------------|-----------------------------------------------------------|
| Role Validation      | Checks if a user role is one of: Operations Manager, Admin, Guest |
| User Info Output     | Prints user data as a dictionary                          |
| Command-Line Interface | Simple CLI using argparse                                 |
| Error Reporting      | Clear error messages for invalid roles                    |

## Tech Stack

- **Python** (v3.10+)

## Project Structure

```
.
├── business/
├── docs/
│   ├── BMC.md
│   ├── PRD.md
│   ├── REQUIREMENTS.md
│   ├── TECH_SPEC.md
│   ├── STORIES.md
│   └── ROADMAP.md
├── pyproject.toml
├── README.md
├── src/
│   └── cannabis_ops_sync/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_main.py
```

## Getting Started

### Prerequisites

- Python 3.10 or higher

### Installation

```bash
pip install -e .
```

### Run

```bash
cannabis-ops-sync --name "John Doe" --role "Admin"
```

### Test

```bash
pytest tests/
```

## Deploy

This is a CLI tool. Deployment involves installing via pip or packaging into a distributable format like a wheel or tarball.

To publish to PyPI:

```bash
python -m build
twine upload dist/*
```

## Status

⚠️ **Stage: Skeleton**  
Last updated: 2026-06-24  
Recent commits:  
- `eba0008`: feat(cannabis-ops-sync): real, sandbox-tested implementation  
- `0575df2`: readme-keeper: generate proper project README  
- `0beb7c7`: feat(cannabis-ops-sync): real, sandbox-tested implementation  

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.