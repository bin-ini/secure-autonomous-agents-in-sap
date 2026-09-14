"""
paper.py -- assemble the paper from the artefacts, adding no prose of its own.

    python3 paper.py > PAPER.md
    python3 paper.py --check     # every registered artefact must be placed

This file was lost once. It was the only module in the repository that had
never been committed -- written in a session, used to produce a manuscript and
a docx, and never added -- so the paper existed and the thing that built it did
not. That is recorded here rather than quietly repaired, because it is the same
failure class as loss L4 and loss L5: the checks all pointed at the artefacts
and none pointed at the tooling.

The rule this file obeys is the one that made the paper trustworthy in the
first place: **there is no second copy of the text.** Every section below is a
generated markdown file, read from disk, its headings demoted one level so the
part headers can sit above them. Nothing is retyped, and `--check` fails if any
artefact in the build registry has no place in the running order -- so adding a
module to `buildreg.py` without deciding where it belongs in the argument
breaks the build instead of silently dropping it.
"""
from __future__ import annotations

import os
import re
import sys

from buildreg import REGISTRY
from release import (TITLE, commit, gates, open_blockers, releasable,
                     subtitle, wording)

HERE = os.path.dirname(os.path.abspath(__file__))
# Front-matter constants that are external facts, not generated results. Each
# may be set at build time so the deposit build fills them in without a code
# edit, e.g.  ZENODO_DOI=10.5281/zenodo.21700000 PUB_DATE="13 September 2026"
# The defaults are the last hand-set values.
DATE = os.environ.get("PUB_DATE", "8 August 2026")
# Authors, in order, with ORCIDs. B.P. is the lead author; M.P. joined as a
# co-author on the strength of SAP GRC domain review and the practitioner
# validation he is undertaking. The contribution of each is stated explicitly
# below rather than left implicit, so the author line carries the same honesty
# discipline as every other claim in the paper.
AUTHORS = [
    ("Bindiya Priyadarshini", "0009-0005-7559-3896"),
    ("Martin Pankraz", "0009-0008-1567-4223"),
]
AUTHOR = " · ".join(n for n, _ in AUTHORS)
CONTRIBUTIONS = (
    "**Author contributions.** B.P. conceived the study, built the "
    "reconstructed surface, testbed and experiments, ran the analysis, and "
    "wrote the manuscript. M.P. contributed SAP GRC and integration-security "
    "domain review across multiple rounds and is undertaking the independent "
    "practitioner-fidelity validation (R1). The validation items in Part Five "
    "remain open for both authors.")
DOI = os.environ.get("ZENODO_DOI", "10.5281/zenodo.PENDING")
# "No One Signs" — the fourth paper. Set ZENODO_DOI_NOS once it is deposited so
# the reference resolves instead of dangling.
_NOS_DOI = os.environ.get("ZENODO_DOI_NOS", "")
_NOS = "*No One Signs*" + (" (%s)" % _NOS_DOI if _NOS_DOI else "")
SERIES = ("Fifth paper in a series on enterprise AI agent security, following "
          "*Calibrated to Act* (10.5281/zenodo.21157411), *Proven Exploitable* "
          "(10.5281/zenodo.21159028), *Ghost in the Stack* "
          "(10.5281/zenodo.21499947) and %s." % _NOS)

# The running order. Each entry is a part title and the artefacts under it, in
# the order a reader meets them.
PARTS = [
    ("Part One — The argument",
     ["WHYMATURE", "NARRATIVE", "FINDING", "IMPACT"]),
    ("Part Two — The method",
     ["WHYFAIL", "MISMATCH", "COUNTERFACTUAL", "REVIEW", "RELATEDWORK"]),
    ("Part Three — The evidence",
     ["RESULTS_SAP", "FIGURES", "BOUNDARY_SAP", "SURFACE"]),
    ("Part Four — The record",
     ["PREREG_SAP", "CLAIMS_SAP", "LOSSES_SAP", "STATUS_SAP"]),
    ("Part Five — What is not done",
     ["RELEASE", "FACTS", "RATIONALE"]),
]

# Placed before Part One, without a part header of its own.
FRONT = ["ABSTRACT"]

PLACED = FRONT + [a for _t, arts in PARTS for a in arts]


def artefacts() -> list[str]:
    return [a for _m, a in REGISTRY]


def demote(md: str, drop_title: bool = False) -> str:
    """Push every heading down one level so a part header can sit above it.

    `drop_title` removes the artefact's own H1 and everything up to its first
    H2 -- used for the abstract, whose H1 is the paper's own title page and
    would otherwise appear twice.
    """
    lines = md.splitlines()
    if drop_title:
        for i, line in enumerate(lines):
            if line.startswith("## "):
                lines = lines[i:]
                break
    out = []
    for line in lines:
        out.append("#" + line if re.match(r"^#{1,5} ", line) else line)
    return "\n".join(out).strip()


def read(name: str) -> str:
    path = os.path.join(HERE, "%s.md" % name)
    if not os.path.exists(path):
        raise SystemExit("%s.md has not been generated -- run ./build.sh"
                         % name)
    return open(path).read()


def check() -> list[str]:
    problems = []
    known = set(artefacts())
    for a in PLACED:
        if a not in known:
            problems.append("%s is placed in the paper and is not in the "
                            "build registry" % a)
    for a in known:
        if a not in PLACED:
            problems.append("%s is generated and has no place in the running "
                            "order. Decide where it belongs in the argument, "
                            "or take it out of the registry -- an artefact "
                            "nobody reads is a check nobody runs." % a)
    if len(PLACED) != len(set(PLACED)):
        problems.append("an artefact is placed twice, which would put a "
                        "second copy of the text in the paper")
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   %d artefacts placed across %d parts, no text duplicated."
              % (len(PLACED), len(PARTS)))
        return

    print("# %s" % TITLE)
    print()
    print("### %s" % subtitle())
    print()
    print("**%s**" % AUTHOR)
    print()
    print("*%s*" % "  ·  ".join("%s — ORCID %s" % (n, o) for n, o in AUTHORS))
    print()
    print("**%s**" % DATE)
    print()
    print("**Version 1.0 · Independent research study**")
    print()
    print("*Licence: text CC BY 4.0, code MIT. You may share and adapt this "
          "work, including commercially, with attribution.*")
    print()
    print("*doi:%s*" % DOI)
    print()
    print(SERIES)
    print()
    from release import EVIDENCE_CUTOFF, PRODUCT_SCOPE
    print("*Product and release scope: **%s**. Evidence cutoff: **%s**.*"
          % (PRODUCT_SCOPE or "to be fixed at the validated edition",
             EVIDENCE_CUTOFF or "to be frozen at the validated edition"))
    print()
    if not releasable():
        print("> **Version 1.0 — a complete independent study.** The work "
              "is reported on a *%s*: no modelled mechanism has yet been "
              "verified against primary vendor documentation, the exact "
              "product and release scope is not yet fixed, and independent "
              "practitioner review and replication are planned. Its scope, the "
              "limits of what it establishes, and the external validation "
              "still to be completed are set out in full in Part Five under "
              "*Scope, Limitations and Future Validation*."
              % (wording()[0].lower() + wording()[1:]))
        print()
    print(CONTRIBUTIONS)
    print()
    print("---")
    print()
    print("## How this document was produced — and what \"generated\" means "
          "here")
    print()
    print("The argument, the interpretation and the prose of this paper are "
          "the author's. What is mechanised is *consistency*, not authorship: "
          "every figure and every number is generated from the code that "
          "produced it, and each section is assembled from a single source "
          "with no second copy of the text — so a written claim and the "
          "evidence behind it cannot silently drift apart. This is a "
          "reproducibility discipline, not a substitute for writing the paper. "
          "The build runs %d such checks and refuses to emit the document if "
          "any of them fails: the assertion in Part One is checked for hedging "
          "words and for language exceeding its evidence class; the abstract "
          "may not be more confident than the release state, and may not claim "
          "novelty the related-work section has taken away; every figure "
          "carries a digest of the data it was drawn from; the claims "
          "trajectory is derived from the audit and the loss register rather "
          "than written from memory; and the subtitle above is computed from "
          "the release state rather than chosen." % len(_checks()))
    print()
    print("No customer, proprietary or vendor-licensed material appears "
          "anywhere in this work. Every scenario is synthetic.")
    print()
    print("---")
    print()

    for name in FRONT:
        print(demote(read(name), drop_title=True))
        print()
        print("---")
        print()

    for title, arts in PARTS:
        print(r"\newpage")
        print()
        print("# %s" % title)
        print()
        for name in arts:
            print(r"\newpage")
            print()
            print(demote(read(name)))
            print()

    print("---")
    print()
    print("*Generated at commit `%s`.*" % commit())


def _checks():
    from buildreg import CHECKED
    return CHECKED


if __name__ == "__main__":
    main()
