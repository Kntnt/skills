# Portable skills only; no harness command files

Claude Code distinguishes slash-command files (`commands/*.md`, preprocessed `$ARGUMENTS` / `@file` / `!shell`) from skills. Other harnesses do not implement that preprocessor, and the collection must behave the same everywhere. Therefore the collection never authors `commands/` files. What the user starts by name is a user-invoked skill: a static `SKILL.md` the model carries out with its own tools.
