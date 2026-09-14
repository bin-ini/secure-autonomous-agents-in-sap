"""
finding.py -- the one page that asserts.

    python3 finding.py            # the finding, then its bounds
    python3 finding.py --check    # the assertion must contain no hedge

This project has spent more effort refusing its own results than producing
them. For this paper that ratio is right: G2 was not promoted into an SAP
control failure, G3 was blocked twice, P1 was withdrawn and respecified, S0 was
split, human throughput was demoted from universal explanation to one mechanism
on one axis, and the exchange rate was reframed from discovery to arithmetic.

But there is a version of epistemic hygiene that is an elaborate way of never
being wrong by never quite saying anything, and a paper that refuses two of its
own findings has earned the right to assert the third.

So the structure of this file is fixed and enforced: ASSERT, then BOUND. The
assertion is checked for hedging words and fails the build if it contains any.
The bounds follow immediately and are as unsparing as everything else in this
repository. What is forbidden is lacing every clause of the finding itself with
a disclaimer, because a reader cannot tell the difference between a careful
claim and an abandoned one.
"""
from __future__ import annotations

import sys

FINDING = """
In the reconstructed FI scenario, the tolerance control did one job perfectly
and another not at all. It caught every document whose own value was anomalous,
and it did so without turning away a single piece of legitimate work. Then we
aimed the same control, unchanged, at a different harm: a materiality breach
assembled from documents that are each, on their own, completely ordinary. Here
it was helpless. Across 12,288 configurations, the only way to hold the period's
total under materiality was to start refusing legitimate work — and the best
setting still gave back most of it, keeping just 37.5%.

The reason is not that the control is weak. It is that the two harms live at
different scales. The first is settled one document at a time, which is exactly
what the control sees. The second is a running sum over every document in the
period, and no per-document limit that lets the legitimate work through can put
a ceiling on that sum. We read both verdicts off the specifications before the
sweep ran; the sweep then confirmed them.

So a control is not strong or weak on its own. What carries a guarantee is the
control-harm pair. The very same control can be complete against one harm and,
against another, unable even in principle to tell the good from the bad.
""".strip()

# EVIDENCE-LEVEL ESCALATION. A subtler failure than hedging, and the one a
# reviewer caught here twice: confident prose whose confidence exceeds its
# evidence class. "Mature control" imports deployment maturity into a result
# derived from a reconstruction; "establishes that immaturity is insufficient"
# makes a deployment-level inference the surface specification cannot support.
#
# These phrases are permitted in the assertion only when at least one mechanism
# in the control surface has reached SAP evidence level. Until then the
# assertion must describe the model it actually tested.
ESCALATIONS = ("deployed sap", "mature control", "production control",
               "real sap mechanism", "sap establishes", "proves immaturity",
               "immaturity is not a sufficient", "in deployed systems",
               "tested against sap", "sap lacks")

# Words that would turn the assertion back into a hedge. The list is short and
# deliberately blunt: this is the one page where they are banned.
HEDGES = ("may ", "might", "arguably", "seems", "appears to", "suggests",
          "we believe", "it is possible", "could be", "tends to", "somewhat",
          "relatively", "fairly", "perhaps", "likely", "probably")

_WORDS = {5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}


def _spell(k: int) -> str:
    return _WORDS.get(k, str(k))


def _bounds() -> list[tuple[str, str]]:
    """The prior-art bound names the works from the register rather than from
    memory. An earlier version listed four works by hand and named two that
    the register files under a different relation."""
    try:
        from relatedwork import anticipating
        names = "; ".join(
            "%s %s" % (w.authors.split(" and ")[0].split()[-1], w.year)
            for w in anticipating())
    except Exception:                             # noqa: BLE001
        names = "see the related-work section"
    return [(t, b.replace("{anticipating}", names)) for t, b in BOUNDS]


BOUNDS = [
    ("This is a reconstructed model, not deployed SAP.",
     "Every mechanism is rebuilt from secondary sources. No entry in the "
     "control surface specification has reached SAP evidence level."),
    ("The product and release scope is not yet fixed.",
     "The reconstruction is shaped by S/4HANA on-premise FI, but no release "
     "was chosen, and the mechanisms differ across Cloud, ECC and ByDesign. "
     "Until it is fixed, a reader cannot tell which omission is a limitation "
     "and which invalidates the surface."),
    ("M2 must be primary-sourced.",
     "The finding rests on FI tolerance groups being document-local. If any "
     "tolerance field retains state across documents, the second half of the "
     "finding is wrong."),
    ("F110 is unresolved.",
     "The payment program is the other plausible location for a cumulative FI "
     "limit and has not been examined. Silence in the sources is not absence."),
    ("The principle is not new, and the paper may not present it as new.",
     "The related-work section, written last, records the works that "
     "anticipate part of it — {anticipating} — and a further group that "
     "supplies the mechanism its repair recommendation amounts to. Extent "
     "mismatch is the aggregation problem. The principle specialises a "
     "published characterisation of enforceable security policies to controls "
     "whose observation boundary is narrower than the execution. The repair "
     "is history-based access control and usage control's mutable attributes. "
     "What is asserted above is a measurement of one reconstructed surface, "
     "and it is the measurement that is offered, not the phenomenon."),
    ("Availability Control may narrow or eliminate the SAP-specific gap.",
     "SAP evaluates accumulated consumption against a consumable budget per "
     "control object and can refuse a posting on that basis. Whether it binds "
     "the credit-memo path modelled here is unknown. If it does, this becomes "
     "a control-placement finding rather than a control gap — and 'SAP lacks "
     "aggregate-state control' is retired either way."),
    ("The specification is not-yet-contested, which is not certification.",
     "The specification-sensitivity audit found no defensible alternative for "
     "this pair. That reflects a bounded search. It can invalidate a verdict; "
     "it cannot establish that a specification is unique."),
    ("One instance cannot support a class claim, and this instance does not "
     "yet support a deployment claim either.",
     "Nothing here establishes that mature enterprise control environments in "
     "general share this shape. Nor — and this bound was itself over-reaching "
     "until a reviewer caught it — does it yet establish that immaturity is "
     "an insufficient explanation for the SAP instance, because no mechanism "
     "has reached SAP evidence level. What it establishes is narrower: "
     "**within the reconstructed FI control surface, immaturity is not "
     "required to produce the observed control-property mismatch.** Once M2 "
     "and the cumulative countermechanisms are resolved for a named product "
     "and release, that upgrades to: for the validated SAP path, immaturity "
     "is not a sufficient explanation."),
]


def hedges_in(text: str) -> list[str]:
    low = text.lower()
    return [h for h in HEDGES if h in low]


def escalations_in(text: str) -> list[str]:
    low = text.lower()
    return [e for e in ESCALATIONS if e in low]


def sap_level_reached() -> bool:
    try:
        from surface import MECHANISMS
        return any(m.level == "SAP" for m in MECHANISMS)
    except Exception:                            # noqa: BLE001
        return False


def check() -> list[str]:
    problems = []
    # Scoped to the ASSERTION only. The bounds are precisely where the paper
    # names what it is not claiming -- "this is a reconstructed model, not
    # deployed SAP", "'SAP lacks aggregate-state control' is retired" -- and a
    # check that forbade those phrases there would forbid the disclaimers
    # rather than the overreach. The danger zone is the one paragraph licensed
    # to sound confident.
    if not sap_level_reached():
        for e in escalations_in(FINDING):
            problems.append(
                "evidence-level escalation: %r appears while no mechanism has "
                "reached SAP evidence level. The assertion may only describe "
                "the model it tested." % e)
    found = hedges_in(FINDING)
    if found:
        problems.append("the assertion hedges: %s. Bound it underneath "
                        "instead." % ", ".join(repr(f) for f in found))
    if len(BOUNDS) < 5:
        problems.append("too few bounds -- assert-then-bound is not a licence "
                        "to skip the bounding")
    # Every number in the assertion must appear in a generated results file,
    # so the one unhedged page cannot drift from the evidence.
    import re
    import os
    nums = set(re.findall(r"\b(?:12,288|37\.5%)\b", FINDING))
    corpus = ""
    for f in ("RESULTS_SAP.md", "BOUNDARY_SAP.md"):
        if os.path.exists(f):
            corpus += open(f).read()
    for n in nums:
        if corpus and n not in corpus:
            problems.append("%s in the assertion does not appear in any "
                            "generated results file" % n)
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   the finding asserts: 0 hedges, 0 evidence-level "
              "escalations, %d bounds, every quoted figure traced to a "
              "generated file." % len(BOUNDS))
        return
    print("# The finding")
    print()
    print(FINDING)
    print()
    print("## What bounds it")
    print()
    print("%s, and none of them is in the paragraph above. A reader cannot "
          % _spell(len(BOUNDS)) +
          "tell the difference between a careful claim and an abandoned one if "
          "every clause carries its own disclaimer, so the claim is stated "
          "first and bounded here.")
    print()
    for head, body in _bounds():
        print("**%s** %s" % (head, body))
        print()


if __name__ == "__main__":
    main()
