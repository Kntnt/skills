# Coding standard — Python

Read before writing or changing Python.

Applies whenever the project contains Python code.

### Baseline

- Standalone scripts: pin runtime via `requires-python` in PEP 723 inline metadata, provisioned by `uv`. Newest Python can lack wheels for some dependencies — don't force absolute latest at install time.
- Full type hints on every function signature and module-level declaration. Checked statically (see *Python tooling*).

### Style

- Idiomatic, modern Python. Prefer standard library where it suffices.
- `pathlib.Path` over `os.path`.
- `dataclasses` over hand-rolled `__init__`; `pydantic` only when validation is part of the contract.
- f-strings; never `%` or `.format()`.
- Context managers (`with`) for any resource with a close/release lifecycle.
- No bare `except:`. Name the exception, or `except Exception` with a comment explaining why a broad catch is appropriate.
- Early returns to flatten nesting.

### Starting a process

Every `subprocess` call names the working directory it runs in, by passing `cwd`. A call that deliberately inherits the caller's says so in the comment above it, in those words — *working directory*, or `cwd` — because an inheritance nobody wrote down is indistinguishable from one nobody thought about, and because that comment is what the suite reads to tell the two apart. Launchers are written as `subprocess.run(...)` and its siblings on the module rather than imported out of it by name, so that every process this collection starts is written the one way that rule is read off.

The reason is that a process outlives its own working directory. A directory is a name for an inode, and a running process holds the inode: replace or remove that directory and the process keeps a handle on something no path leads to any more, at which point a launcher started from it — `uv`, and anything else that resolves a project from where it stands — fails with its own *No such file or directory* before reaching the program it was asked to run. This collection replaces directories while it runs. A Global Update stages the Manager unconditionally and, where the staged tree differs, publishes the new one and unlinks the retired one while the same run is still going, so the directory the invoking agent stood in can be gone by the time a later seam starts a process (issue #257).

Pick the directory the call actually needs, and prefer one nothing in the run can remove: the Manager's two integration seams run a Skill's declared script from `home()`, which is what Global paths resolve against and what no verb of this collection deletes. Where a resolution can fail — `Path.home()` raises `RuntimeError` on a machine with no home — the failure joins whatever the call already reports rather than becoming a new way for it to raise.

### Doc comments

Docstrings on every module, class, and public function. Document the contract and the why; type hints show the shape. Pick a docstring convention (Google or NumPy style) per project, stay consistent. Use `Args:` / `Returns:` / `Raises:` where they add real value.

### Standalone-script metadata (PEP 723)

Single-file scripts: declare dependencies and required Python version inline at the top:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx==0.27.0",
#     "rich==13.7.1",
# ]
# ///
```

Pin exact versions. `uv run` resolves and caches the environment automatically.

A script meant to run from the terminal uses the env-based shebang `#!/usr/bin/env -S uv run --script`, so `uv` provisions the environment from this PEP 723 metadata on invocation. Packaging shape (command-style in `bin/` vs internal) follows the universal *Standalone-script packaging* rules in the general module.

### Python tooling

- **uv** as runtime, package manager, and virtualenv tool. `uv run` executes a PEP 723 script directly; for project work, `uv` manages the project venv and lockfile.
- **ruff** as the single linter and formatter (replaces black, isort, flake8, pylint).
- **mypy** or **pyright** for static type checking — pick one per project. Strict mode on new code.
- **pytest** for tests.
