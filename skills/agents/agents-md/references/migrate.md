# Migrate a legacy `agents.d/`

Project agent documents live under `docs/agents/`. An `agents.d/` under the target is the retired location. Move its documents before placing anything, under the same Safety as every other write in [`writes.md`](writes.md). No `agents.d/` → nothing to migrate.

1. **Compare before writing.** For each file under `agents.d/`, look at the same relative path under `docs/agents/`:
   - Absent under `docs/agents/` → move it.
   - Same bytes (`cmp`) → delete the `agents.d/` copy.
   - Different bytes → collision.
2. **Any collision → change neither directory nor any reference to either.** Name both paths of every colliding pair, say that their contents differ, and ask which to keep. Never choose a version, merge the two texts, or overwrite a file. `--yes` does not choose. The run writes no other file into either directory.
3. **No collision → migrate.** Move each file (`git mv` in git). Keep every file already under `docs/agents/` as it is. Drop `agents.d/.gitkeep` instead of moving it when `docs/agents/` holds another file. Remove the emptied `agents.d/`.
4. **Rewrite every reference to an `agents.d/` path** to its `docs/agents/` counterpart: References lines, `@` imports, path references in other files, and relative links elsewhere in the target. Fix path references and relative links inside each moved file, which now sits one level deeper. Change nothing else in any file, and leave released history such as changelog entries and decision records as it stands. A reference in `docs/` outside `docs/agents/` stays a proposal, even under `--yes`: name the file and the new path for a human to write.
5. **Report** each move, each deleted duplicate, each rewritten reference, and each proposed one.

Done when no `agents.d/` remains, each of its documents exists once under `docs/agents/` with its content unchanged apart from paths, every rewritten reference resolves, and every reference left for a human is proposed. On a collision, done when both directories and every reference to them are unchanged and each colliding pair is reported.
