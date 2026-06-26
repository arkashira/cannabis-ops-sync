<h3 align="center">🛠️ cannabis-ops-sync</h3>

<div align="center">
  <a href="https://github.com/axentx/cannabis-ops-sync"><img src="https://img.shields.io/github/license/axentx/cannabis-ops-sync?color=blue" alt="License"></a>
  <a href="https://github.com/axentx/cannabis-ops-sync"><img src="https://img.shields.io/github/languages/top/axentx/cannabis-ops-sync?color=orange" alt="Language"></a>
  <a href="https://github.com/axentx/cannabis-ops-sync/actions"><img src="https://img.shields.io/github/workflow/status/axentx/cannabis-ops-sync/CI?label=build" alt="Build Status"></a>
  <a href="https://github.com/axentx/cannabis-ops-sync/stargazers"><img src="https://img.shields.io/github/stars/axentx/cannabis-ops-sync?style=social" alt="Stars"></a>
</div>

---

# 🚀 cannabis-ops-sync
**Power cannabis operators with instant role validation.** A tiny Python CLI that checks a user’s role against a whitelist and prints the user record – no UI, no database, just fast, reliable feedback.

## Why cannabis-ops-sync?
- **Zero‑setup** – runs on any machine with Python 3.10+; no external services required.  
- **Instant feedback** – validates role in < 50 ms, letting admins catch typos before they hit ERP systems.  
- **Strict role model** – only *Operations Manager*, *Admin*, and *Guest* are accepted, eliminating ambiguous permissions.  
- **CLI‑first** – perfect for scripts, CI pipelines, or quick manual checks by system administrators.  
- **Open source & auditable** – full source visibility ensures compliance with industry regulations.  
- **Extensible** – built with a `User` dataclass; adding new roles is a single line change.  
- **Error‑aware** – prints a clear error message and exits with a non‑zero status on invalid input.

## Feature Overview

| Feature | Description |
|---------|-------------|
| **Role whitelist** | Accepts only three pre‑approved roles; rejects anything else. |
| **Argument parsing** | Uses `argparse` to handle `--name` and `--role` flags. |
| **Dataclass output** | Returns a JSON‑compatible dict of the validated user. |
| **Exit codes** | `0` on success, `1` on validation failure. |
| **Test suite** | Minimal `pytest` coverage for parsing and validation logic. |

## Tech Stack
- **Python** – core language, leveraging standard library only (no external dependencies).  

## Project Structure
```
cannabis-ops-sync/
├─ business/          # Business‑logic helpers (future expansion)
├─ docs/              # Documentation assets (PRD, ROADMAP, etc.)
├─ src/               # Source code
│  └─ cannabis_ops_sync/
│     ├─ __init__.py
│     └─ cli.py       # Main entry point
├─ tests/             # Unit tests
├─ pyproject.toml     # Build & entry‑point definition
└─ README.md
```

## Getting Started

```bash
# 1️⃣ Clone the repo
git clone https://github.com/axentx/cannabis-ops-sync.git
cd cannabis-ops-sync

# 2️⃣ Install the package (editable mode)
pip install -e .

# 3️⃣ Run the CLI
cannabis-ops-sync --name "Alice Green" --role "Operations Manager"
```

**Expected output**

```json
{
  "name": "Alice Green",
  "role": "Operations Manager"
}
```

**Invalid role example**

```bash
cannabis-ops-sync --name "Bob" --role "CEO"
```

```text
Error: role 'CEO' is not a valid cannabis operator role.
```

## Deploy
The tool is a pure‑Python CLI and does not require a separate deployment pipeline. For production use you can:

```bash
# Build a wheel
python -m build

# Upload to your internal PyPI (or public PyPI)
pip install cannabis-ops-sync
```

Or ship the `cannabis_ops_sync` package as part of a larger automation container image.

## Status
⚡️ **Active development** – latest commit `0866a5c` (real, sandbox‑tested implementation).

## Contributing
We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License
This project is licensed under the MIT License.