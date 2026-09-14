#!/usr/bin/env bash
# build.sh -- every check, then every artefact.
#
# The list of both lives in buildreg.py and nowhere else. An earlier version
# hardcoded them here and in the release prose, and the two disagreed.
set -euo pipefail
cd "$(dirname "$0")"
for c in $(python3 buildreg.py --checks); do
  printf '%-16s' "$c"; python3 "$c.py" --check
done
echo
for pair in $(python3 buildreg.py --artifacts); do
  python3 "${pair%%:*}.py" > "${pair##*:}.md"
  printf '  %-20s %s\n' "${pair##*:}.md" "$(wc -l < "${pair##*:}.md") lines"
done
echo
# Last, because it reads what the loop above just wrote.
for pair in $(python3 buildreg.py --final); do
  python3 "${pair%%:*}.py" > "${pair##*:}.md"
  printf '  %-20s %s\n' "${pair##*:}.md" "$(wc -l < "${pair##*:}.md") lines"
done
