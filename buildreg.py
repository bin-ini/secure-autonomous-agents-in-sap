"""
buildreg.py -- the build registry. One list, consumed by everything.

    python3 buildreg.py --checks      # module names, one per line, for build.sh
    python3 buildreg.py --artifacts   # module:output pairs, for build.sh

This exists because a sentence in the release document said the build runs ten
checks while the build ran eleven, and a human corrected it by counting. That
is precisely the drift every other artefact in this repository is built to
prevent, occurring in the artefact that describes the prevention.

So the counts are no longer written anywhere. `build.sh` iterates this list,
`release.py` reports its length, and if a check is added tomorrow the prose
changes by itself.
"""
from __future__ import annotations

import sys

# module -> generated artefact. A module with no artefact is a check only.
REGISTRY = [
    ("abstract", "ABSTRACT"),
    ("whymature", "WHYMATURE"),
    ("facts", "FACTS"),
    ("whyfail", "WHYFAIL"),
    ("mismatch", "MISMATCH"),
    ("figures", "FIGURES"),
    ("counterfactual", "COUNTERFACTUAL"),
    ("boundary", "BOUNDARY_SAP"),
    ("surface", "SURFACE"),
    ("manifest_sap", "STATUS_SAP"),
    ("losses_sap", "LOSSES_SAP"),
    ("prereg_sap", "PREREG_SAP"),
    ("relatedwork", "RELATEDWORK"),
    ("review", "REVIEW"),
    ("finding", "FINDING"),
    ("impact", "IMPACT"),
    ("narrative", "NARRATIVE"),
    ("release", "RELEASE"),
    ("rationale", "RATIONALE"),
    ("claims_sap", "CLAIMS_SAP"),      # no --check; generated only
    ("run", "RESULTS_SAP"),            # no --check; generated only
]

# The assembly. Not an artefact like the others: it writes no new prose, it
# places the artefacts in an order. It is listed separately because it must run
# LAST -- it reads the files the loop above has just written -- while its check
# can run with the others, since the check only reads the registry.
FINAL = [("paper", "PAPER")]

# Modules that implement --check.
CHECKED = ([m for m, _ in REGISTRY if m not in ("claims_sap", "run")]
           + [m for m, _ in FINAL])


def n_checks() -> int:
    return len(CHECKED)


def n_artifacts() -> int:
    return len(REGISTRY) + len(FINAL)


def main():
    if "--checks" in sys.argv:
        print("\n".join(CHECKED))
    elif "--artifacts" in sys.argv:
        print("\n".join("%s:%s" % (m, a) for m, a in REGISTRY))
    elif "--final" in sys.argv:
        print("\n".join("%s:%s" % (m, a) for m, a in FINAL))
    else:
        print("%d checks, %d artefacts" % (n_checks(), n_artifacts()))


if __name__ == "__main__":
    main()
