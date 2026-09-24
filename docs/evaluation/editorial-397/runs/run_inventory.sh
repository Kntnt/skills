#!/bin/sh
# run_inventory.sh OUTPUT RUNDIR INSTALLDIR
#
# Scopes 1 and 2 of the inventory for one run. Writes a digest of the staged
# install's full listing, then the run directory's listing in full, so that the
# file stays small enough to commit while the install is still covered
# byte for byte by the digest.
set -eu
out=$1; rundir=$2; install=$3
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT 0
find "$install" -type f -exec shasum -a 256 {} + > "$tmp/install.txt"
LC_ALL=C sort -k 2 -o "$tmp/install.txt" "$tmp/install.txt"
{
  printf '# staged install: %s\n' "$install"
  printf '# staged install digest: %s\n' "$(shasum -a 256 < "$tmp/install.txt" | cut -d' ' -f1)"
  printf '# staged install files: %s\n' "$(wc -l < "$tmp/install.txt" | tr -d ' ')"
  printf '# run directory:\n'
  if [ -d "$rundir" ]; then
    ( cd "$rundir" && find . -type f -exec shasum -a 256 {} + | LC_ALL=C sort -k 2 )
  else
    printf 'missing  %s\n' "$rundir"
  fi
} > "$out"
