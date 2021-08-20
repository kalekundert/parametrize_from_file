#!/usr/bin/env bash
set -euo pipefail

# Have to run each documentation example separately, because otherwise pytest 
# gets confused by the duplicate file names.  I tried to work around this by 
# playing with `--import-mode`, but to no avail.  The closest I got 
# was by adding an `__init__.py` file to each test directory, but then the 
# scripts weren't able to `import vector`.

cd $(git rev-parse --show-toplevel)

for f in docs/**/test_*.py; do
  pytest $f
done
