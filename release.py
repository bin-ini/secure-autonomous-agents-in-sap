"""
release.py -- what has to be true before this leaves the building.

    python3 release.py            # the release state
    python3 release.py --check    # blockers open == not releasable, loudly

The three remaining blockers are evidence determinations, not ideas. This file
holds them, refuses to report the work as releasable while any is open, and
carries the two statements a reader needs in order to inspect the claim rather
than trust it: what artefacts exist, and what date the evidence was frozen at.

The evidence cutoff matters more than it looks. SAP documentation changes.
Without a frozen date, a later revision silently rewrites what this paper
claimed to have reviewed, and the paper's own account of its sources becomes
unfalsifiable — which is the one thing nothing in this repository is allowed
to be.
"""
from __future__ import annotations

import subprocess
import sys

# THE TITLE RULE, in two parts, because they are different rules.
#
#   The MAIN TITLE may not assert that anything failed. It may name the
#   system: the author's decision, taken deliberately, is that SAP is the
#   subject of the study rather than an incidental evaluation environment,
#   and a title that hid that would be coy rather than careful. What it may
#   not do is deliver a verdict the evidence does not support, which is what
#   a title containing "fails" or "insecure" would do.
#
#   The SUBTITLE MAY name the evaluation environment -- that is what a
#   subtitle is for -- but it must consume the evidence level. While the
#   blockers are open it must say what was actually evaluated, and it may
#   never say "tested against SAP".
#
# An earlier version had a subtitle reading "Evaluated on SAP Financial
# Authorization" sitting directly above a release-state line reading
# "Evaluated on a reconstructed SAP FI authorization model". The two
# disagreed by exactly the amount the paper is not entitled to.
TITLE = "Secure Autonomous Agents in SAP Systems"

SUBTITLE_OPEN = ("A Control-Property Review Evaluated on a Reconstructed SAP "
                 "FI Authorization Model")
SUBTITLE_CLOSED = ("A Control-Property Review Validated Against a Specified "
                   "SAP S/4HANA FI Control Path")

# Frozen at release. Empty until the primary-source pass happens, because a
# cutoff date asserted before the review would be a fiction.
EVIDENCE_CUTOFF = None            # e.g. "12 August 2026"
PRODUCT_SCOPE = None              # e.g. "SAP S/4HANA 2023, on-premise, FI"

BLOCKERS = [
    ("B1", "Fix the precise SAP scope",
     "Product, deployment model, module and release. 'SAP' is not a scope and "
     "neither is 'S/4HANA'. Choose the release the reconstructed mechanisms "
     "actually represent — not the one whose documentation is easiest to "
     "reach — then rebuild or annotate every mismatch.",
     lambda: PRODUCT_SCOPE is not None),

    ("B2", "Verify M2 from primary documentation",
     "For the named release: exact configuration name, exact field semantics, "
     "enforcement point, whether each limit binds per document, per line, per "
     "clearing transaction, per run, per account or per period, and whether "
     "ANY state persists across documents. If one does, the second half of "
     "the finding is wrong.",
     lambda: _mech_at_sap_level("M2")),

    ("B3", "Resolve the cumulative countermechanisms against the exact path",
     "Path-binding, not a survey. Can F110, Availability Control or another "
     "standard mechanism preventively evaluate cumulative credited value for "
     "the exact credit-memo process, control object, product and release used "
     "in X7? The four interpretations are pre-registered as D1 — committed "
     "before the sources are read, and two of them remove the finding.",
     lambda: _mech_at_sap_level("M2") and EVIDENCE_CUTOFF is not None),
]

# Two independent reviews, neither of which this toolchain can perform, and
# both of which GATE the release. An earlier version listed them beneath the
# blockers and computed releasability from the blockers alone, which made them
# socially required and mechanically advisory -- exactly the gap between a
# stated stopping condition and an enforced one.
#
# `complete` is set only when the review has actually happened. Nothing in this
# repository can set it, which is correct: a review the author can mark done is
# not an independent review.
REVIEWS = [
    ("R1", "An SAP FI/GRC practitioner reviews the control-surface "
           "specification only",
     "Not the prose, not the finding. The question is whether the surface is "
     "faithfully described. Showing them the conclusion first would measure "
     "their agreement with us rather than the fidelity of the model.",
     False),
    ("R2", "Inter-rater reliability — independent researchers reproduce the "
           "Control-Property Review for the decisive H1/G1 pair, in two stages: "
           "verdict reproducibility under fixed specifications (R2A) and "
           "specification-sensitivity reproducibility (R2B)",
     "If the instrument only works in the hands of the person who wrote it, it "
     "is not an instrument; if two careful readers reach different verdicts on "
     "the same case, the categories are not carving anything real. Agreement "
     "across independent raters is the first real test of the paper's actual "
     "contribution, and it is what would falsify the method rather than a "
     "claim. Scope, stated so it cannot be overgeneralised: this covers the "
     "H1/G1 decisive pair only. A successful outcome establishes that "
     "independent reviewers reproduced the analysis for that pair and "
     "independently evaluated its specification sensitivity — not that CPR has "
     "demonstrated reliability across all seven verdict classes. A full "
     "instrument study (compositional closure via H2, a contested "
     "specification via G2 or G3, misspecification via P1, and a genuinely "
     "unsupported case) belongs to the research programme, not this release.",
     False),
]

ARTIFACTS = """
**Artifacts.** The pre-registrations, control-surface specification,
experiment implementation, configuration manifest, generated results, loss
register, specification-sensitivity audit, claim ledger, narrative spine and
Control-Property Review instrument are released with the paper. Every reported
numeric result and every narrative summary is generated from, or checked
against, the same manifests that produced the experimental artefacts: the
build runs {n_checks} consistency checks and writes nothing if any of them
fails.
""".strip()


def _mech_at_sap_level(mid: str) -> bool:
    try:
        from surface import MECHANISMS
        return any(m.id == mid and m.level == "SAP" for m in MECHANISMS)
    except Exception:                             # noqa: BLE001
        return False


def open_blockers():
    return [b for b in BLOCKERS if not b[3]()]


def incomplete_reviews():
    return [r for r in REVIEWS if not r[3]]


def frozen_build() -> str | None:
    """A git tag, not a constant. A frozen build the author can assert by
    editing a variable is not a frozen build."""
    try:
        tags = subprocess.run(["git", "tag", "--points-at", "HEAD"],
                              capture_output=True, text=True,
                              check=True).stdout.split()
        rel = [t for t in tags if t.startswith("release-")]
        return rel[0] if rel else None
    except Exception:                             # noqa: BLE001
        return None


def gates():
    """Every gate, and its state. Releasability is the conjunction."""
    return [
        ("Evidence blockers", "%d open / %d total"
         % (len(open_blockers()), len(BLOCKERS)), not open_blockers()),
        ("Required independent reviews", "%d complete / %d required"
         % (len(REVIEWS) - len(incomplete_reviews()), len(REVIEWS)),
         not incomplete_reviews()),
        ("Evidence cutoff", EVIDENCE_CUTOFF or "not frozen",
         EVIDENCE_CUTOFF is not None),
        ("Frozen release build", frozen_build() or "not created",
         frozen_build() is not None),
    ]


def releasable() -> bool:
    return all(ok for _, _, ok in gates())


def subtitle() -> str:
    """Computed, never chosen. The title obeys the same evidence-level
    transition as the body."""
    return SUBTITLE_CLOSED if not open_blockers() else SUBTITLE_OPEN


# Kept as a module attribute so importers get the computed value.
def __getattr__(name):
    if name == "SUBTITLE":
        return subtitle()
    raise AttributeError(name)


def wording() -> str:
    return ("Validated against the specified SAP S/4HANA FI control path"
            if not open_blockers() else
            "Evaluated on a reconstructed SAP FI authorization model")


def commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:                             # noqa: BLE001
        return "unknown"


def check() -> list[str]:
    problems = []
    if releasable() and EVIDENCE_CUTOFF is None:
        problems.append("releasable() is true with no evidence cutoff -- the "
                        "gate list is not doing its job")
    if EVIDENCE_CUTOFF is None and not open_blockers():
        problems.append("blockers are closed but no evidence cutoff is "
                        "frozen -- later documentation changes would silently "
                        "rewrite what this paper reviewed")
    # Part one: the main title.
    low = TITLE.lower()
    if any(w in low for w in ("break", "fails", "failure of", "insecure",
                              "broken", "cannot secure")):
        problems.append("the main title asserts failure. The paper's own "
                        "audit withdrew two of its verdicts and narrowed a "
                        "third; a title may not claim what the body refuses")
    # Part two: the subtitle consumes the evidence level.
    sub = subtitle().lower()
    if "tested against sap" in sub:
        problems.append("the subtitle says 'tested against SAP'; nothing has "
                        "been tested against SAP")
    if open_blockers() and "reconstructed" not in sub:
        problems.append("blockers are open but the subtitle does not say the "
                        "model is reconstructed -- it would claim more than "
                        "the release-state line beneath it")
    if not open_blockers() and "reconstructed" in sub:
        problems.append("blockers are closed but the subtitle still says "
                        "reconstructed")
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   release state: %s. %s"
              % ("RELEASABLE" if releasable() else "NOT RELEASABLE",
                 "; ".join("%s: %s" % (n, st) for n, st, _ in gates())))
        return

    from buildreg import n_artifacts, n_checks
    print("# Scope, Limitations and Future Validation")
    print()
    print("*%s — %s*" % (TITLE, subtitle()))
    print()
    print("## %s" % subtitle())
    print()
    print("*Release state at commit `%s`.*" % commit())
    print()
    print("| | |")
    print("|:---|:---|")
    print("| product and release scope | %s |"
          % (PRODUCT_SCOPE or "**to be fixed — validation item B1**"))
    print("| evidence cutoff | %s |"
          % (EVIDENCE_CUTOFF or "**to be frozen at the validated edition**"))
    print("| accurate wording | *%s* |" % wording())
    print("| build | %d checks, %d generated artefacts |"
          % (n_checks(), n_artifacts()))
    print()
    print("## Validation still to complete")
    print()
    print("*This edition (v1.0) is a complete independent study. The four "
          "items below are the external validation still to be done before a "
          "validated edition; none is a conceptual gap in the study itself.*")
    print()
    print("| gate | state | |")
    print("|:---|:---|:--|")
    for name, state, ok in gates():
        print("| %s | %s | %s |" % (name, state, "done" if ok else "**pending**"))
    print()
    if not releasable():
        failing = [n for n, _, ok in gates() if not ok]
        print("> **Validation status — v1.0.** This edition is complete as "
              "an independent study. Still pending before a validated "
              "edition: %s. None of it is a conceptual gap in the study."
              % ", ".join(failing).lower())
        print()
    print("## Validation items — the primary-source pass")
    print()
    for bid, name, detail, done in BLOCKERS:
        print("### %s — %s  *(%s)*"
              % (bid, name, "done" if done() else "**pending**"))
        print()
        print(detail)
        print()
    print("## Independent review (planned)")
    print()
    print("Neither can be performed by the toolchain that built this "
          "repository, and that is the point of both.")
    print()
    for rid, name, why, done in REVIEWS:
        print("**%s — %s.** *(%s)* %s"
              % (rid, name, "complete" if done else "**planned**", why))
        print()
    print("## Statements for the paper")
    print()
    print(ARTIFACTS.format(n_checks=n_checks()))
    print()
    if EVIDENCE_CUTOFF and PRODUCT_SCOPE:
        print("**Evidence cutoff.** SAP product documentation and "
              "countermechanism review current through %s. Product and "
              "release scope: %s." % (EVIDENCE_CUTOFF, PRODUCT_SCOPE))
    else:
        print("**Evidence cutoff.** *Not yet frozen.* No evidence-cutoff date "
              "or fixed product-and-release scope is asserted while the gates "
              "above are open — asserting either before the primary-source "
              "pass would be a fiction. Both are frozen at release, and this "
              "line states them once they are.")
    print()
    print("## Until the blockers close")
    print()
    print("| may not appear | why |")
    print("|:---|:---|")
    print("| any title or subtitle saying *tested against SAP* | no mechanism "
          "has reached SAP evidence level |")
    print("| any deployment-level conclusion | the surface is a "
          "reconstruction |")
    print("| any claim that the tested path lacks cumulative enforcement | "
          "Availability Control is unresolved against that path |")
    print("| any claim that a deployed SAP control environment has failed "
          "this test | it has not been tested; a model of it has |")


if __name__ == "__main__":
    main()
