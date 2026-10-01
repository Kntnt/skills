#!/bin/sh
# inventory.sh OUTPUT DIR [DIR ...]
#
# Writes one "<sha256>  <path>" line per regular file under each DIR to OUTPUT,
# sorted by path. Nothing is skipped: dotfiles, empty files and nested
# directories are all hashed, so that a diff of two inventories is the whole
# truth about what a run created, replaced or removed.
#
# A DIR that does not exist is recorded as a "missing" line rather than passed
# over, so that a before/after pair shows a directory coming into existence.
# Errors from shasum are left on stderr, never suppressed.
#
# macOS: shasum -a 256.

set -eu

if [ "$#" -lt 2 ]; then
    echo "usage: $0 OUTPUT DIR [DIR ...]" >&2
    exit 2
fi

out=$1
shift

: > "$out"

for dir in "$@"; do
    if [ -d "$dir" ]; then
        find "$dir" -type f -exec shasum -a 256 {} + >> "$out" || true
    else
        printf 'missing  %s\n' "$dir" >> "$out"
    fi
done

LC_ALL=C sort -k 2 -o "$out" "$out"
