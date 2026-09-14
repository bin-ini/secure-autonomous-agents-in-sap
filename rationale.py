"""
rationale.py -- why publish this. One page, for the author.

    python3 rationale.py            # the page, and whether it may be signed yet
    python3 rationale.py --check    # it must not mention the case study

The last artefact, and the only one written for an audience of one.

The instruction it implements: when the gates close, write a page explaining
why this should be published — and the page must not mention SAP, agents, or
autonomous systems. If the reason to publish needs the case study, the
contribution is the case study, and the case study is one reconstructed
instance of one module of one product. `--check` enforces the omission, because
a rationale that reaches for the interesting domain is telling you something.

It cannot be SIGNED while any release gate is open. A reason to publish
composed before the evidence is in is a wish, and this project has spent a very
long time learning to tell those apart. Nothing in this repository can sign it;
the signature is a human saying they still believe the page after reading it
cold.
"""
from __future__ import annotations

import sys

# The rationale may not reach for the case study to make itself interesting.
FORBIDDEN = ("sap", "agent", "autonomous", "erp", "s/4hana", "enterprise "
             "resource")

SIGNED_BY = None            # set by a person, or not at all
SIGNED_ON = None

DRAFT = """
This paper introduces a review procedure that decides whether a control has
failed against a stated property. It distinguishes seven outcomes, four of
which are refusals. Five describe what was found: the control
observes the property directly; the property is wider but the local predicate
composes into it; the property lies outside the observation boundary and is not
closed, so the control cannot discriminate; the apparent failure rests on a
property the researcher substituted for the one the organisation claims; and
the strongest existing countermeasure was never tested, so no verdict is owed.
The other two refuse the experiment rather than the control: the test could not
have come out otherwise, and there is no evidence either way.

Applied to one reconstructed control surface, it admitted one mismatch,
preserved one control through compositional closure, rejected one claimed
failure because the protected property had been substituted, blocked one
result until the strongest existing countermeasure was tested, and refused one
of its own predictions as unfairly specified before that prediction was ever
run. The two blocked items were then worked rather than argued away: the
countermeasure was tested and the gap survived smaller, and the refused
prediction was respecified, run, confirmed exactly where it was aimed, and made
irrelevant by the same experiment.

A literature search, run last, took the principle itself away. It is a
specialisation of a characterisation published in 2000, its wider form was
named in 1989, and its repair has had a model since 2004. What is left is the
procedure and what the procedure did.

The contribution is not any mismatch it found. It is that of the claims its
own author wanted to make, exactly one survived the procedure intact — and it
is a measurement rather than an idea. One was rejected outright. One was
narrowed until it was about a proposed property rather than a control. One was
blocked, worked, and returned smaller. One was refused before it was ever run,
respecified, run, and made irrelevant by its own result. And one was retracted
after the fact, because the model it rested on could not have produced any
other answer.
""".strip()


def _gate_state():
    from release import gates, releasable
    return gates(), releasable()


def check() -> list[str]:
    problems = []
    low = DRAFT.lower()
    for f in FORBIDDEN:
        if f in low:
            problems.append(
                "the rationale mentions %r. If the reason to publish needs the "
                "case study, the case study is the contribution -- and it is "
                "one reconstructed instance of one module of one product."
                % f)
    _, ok = _gate_state()
    if SIGNED_BY and not ok:
        problems.append("the rationale is signed while release gates are open; "
                        "a reason to publish composed before the evidence is "
                        "in is a wish")
    if SIGNED_BY and not SIGNED_ON:
        problems.append("signed without a date")
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        _, ok = _gate_state()
        print("   rationale: %d words, names no case study, %s."
              % (len(DRAFT.split()),
                 "signed" if SIGNED_BY else
                 "unsigned (%s)" % ("signable" if ok else "gates open")))
        return

    gates, ok = _gate_state()
    print("# Why publish this")
    print()
    print("*For the author. Not for reviewers, not for a preface. The test is "
          "whether this page is still believed when read cold.*")
    print()
    print(DRAFT)
    print()
    print("---")
    print()
    if SIGNED_BY:
        print("Signed by **%s**, %s." % (SIGNED_BY, SIGNED_ON))
        return
    if ok:
        print("**Unsigned, and signable.** Every release gate is closed. Read "
              "the page cold. If it is still believed, sign it and publish; if "
              "it is not, the honest move is that nothing above was ever worth "
              "the word *contribution*, and that is a finding too.")
    else:
        print("**Version 1.0.** This edition is released as a complete "
              "independent study; the closing signature is held until the "
              "external validation set out earlier — %s — is finished."
              % ", ".join(n.lower() for n, _, g in gates if not g))
        print()
        print("A reason to publish written before that validation is in is a "
              "wish. The page is drafted now so it is not composed under the "
              "pressure of wanting to be finished — the author signs it once "
              "the validation completes, and nothing in this repository can "
              "sign it on their behalf.")


if __name__ == "__main__":
    main()
