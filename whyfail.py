"""
whyfail.py -- why existing control evaluations misclassify, and what this
review contributes.

    python3 whyfail.py            # the motivation section
    python3 whyfail.py --check    # the four failure modes and the contributions

The method chapters describe HOW to evaluate a control-property pair. This one
says WHY the ordinary way of doing it repeatedly reaches the wrong answer, so
that the instrument reads as necessary rather than merely tidy. Each failure
mode names a specific step of the Control-Property Review that exists to prevent
it, and the numbers of controls and pairs are read from the same sources the
rest of the paper uses, never typed here.
"""
from __future__ import annotations

import sys

# Each mode: the name, the mistake, the consequence, and the step of the
# instrument that catches it.
MODES = [
    ("Property inflation",
     "The evaluator quietly replaces the property the control actually claims "
     "to enforce with a stronger one the control was never asked to guarantee, "
     "then reports the control as failing against the substituted property.",
     "A control that correctly enforces its stated property is recorded as a "
     "failure, and the report cannot distinguish a real gap from a moved "
     "goalpost. In this work it is the difference between what SAP's "
     "segregation-of-duties control claims and the stronger decision-layer "
     "property a researcher can substitute for it.",
     "the specification-sensitivity audit, which forces the smallest "
     "defensible alternative property into view and marks the verdict "
     "*contested* when a substitution is what produced it"),

    ("Comparator omission",
     "The evaluation runs the harmful workload through the control and observes "
     "harm, without ever running an equally ordinary but legitimate workload "
     "through the same control to see what it costs to stop.",
     "A control that cannot tell the two workloads apart looks exactly like one "
     "that can, because only one side was measured. The exchange rate between "
     "harm prevented and legitimate work refused — the whole commercial "
     "question — is invisible.",
     "the paired positive control in every sweep, which measures the legitimate "
     "workload beside the harmful one and reports the throughput a control "
     "gives back to buy its coverage"),

    ("Countermechanism neglect",
     "The evaluator concludes that a control cannot address a harm without "
     "searching, through more than one route, for the strongest existing "
     "mechanism a practitioner would actually reach for — often in a different "
     "module of the same product.",
     "A mismatch is declared structural when the product already ships the "
     "missing control shape somewhere else. This nearly happened here: a single "
     "retrieval route missed SAP Availability Control, the one native mechanism "
     "capable of overturning this paper's principal finding.",
     "the countermechanism test, which owes no verdict until the strongest "
     "existing mechanism has been searched through independent routes and "
     "tested at the correct process scope"),

    ("Observation-boundary confusion",
     "The evaluator treats every case where a property is wider than what a "
     "control observes as a failure, without asking whether the control's local "
     "predicate nonetheless composes into the wider property.",
     "The category collapses two opposite situations: a control that is locally "
     "correct and globally sufficient, and one that is locally correct and "
     "globally silent. They look identical in a control matrix and require "
     "opposite responses — fund the control, or relocate it.",
     "the closure test, which asks whether local enforcement forces the global "
     "property before any mismatch is concluded, and is the case that stops the "
     "principle degenerating into 'a wider property needs a wider control'"),
]


def _counts():
    from mismatch import PAIRS
    from surface import MECHANISMS
    return len(PAIRS), len(MECHANISMS)


def check() -> list[str]:
    problems = []
    if len(MODES) != 4:
        problems.append("there are %d failure modes; the section is written "
                        "around four" % len(MODES))
    for name, mistake, consequence, step in MODES:
        for label, text in (("mistake", mistake), ("consequence", consequence),
                            ("catching step", step)):
            if len(text.split()) < 12:
                problems.append("%s: the %s is too short to be a real claim"
                                % (name, label))
    # Every failure mode must name the step of the instrument that catches it,
    # or the section is a list of complaints rather than a motivation for the
    # method.
    catch_terms = ("audit", "positive control", "countermechanism", "closure")
    for name, _m, _c, step in MODES:
        if not any(t in step.lower() for t in catch_terms):
            problems.append("%s does not name the step of the review that "
                            "prevents it" % name)
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   why-existing-evaluations-fail: %d failure modes, each tied "
              "to the step that prevents it." % len(MODES))
        return

    n_pairs, n_mech = _counts()
    print("# Why existing control evaluations misclassify")
    print()
    print("A control catalogue is an inventory of controls, not an inventory "
          "of guarantees, and the ordinary way of auditing one reaches the "
          "wrong verdict in four recurring ways. Each is a specific mistake, "
          "each produces a specific misclassification, and each is the reason a "
          "particular step of the Control-Property Review exists. Naming them "
          "first is what makes the instrument that follows necessary rather "
          "than merely orderly.")
    print()
    for i, (name, mistake, consequence, step) in enumerate(MODES, 1):
        print("## %d. %s" % (i, name))
        print()
        print("*The mistake.* %s" % mistake)
        print()
        print("*What it does.* %s" % consequence)
        print()
        print("*What catches it.* %s." % (step[0].upper() + step[1:]))
        print()
    print("Across the %d control-property pairs specified in this paper, and "
          "the %d SAP mechanisms modelled, every misclassification the review "
          "prevented is one of these four. That is the argument for the "
          "instrument: not that it is elegant, but that without an explicit "
          "control-property analysis, documentation of individual controls does "
          "not by itself establish which wider properties follow under "
          "autonomous execution." % (n_pairs, n_mech))
    print()
    print("## What this review contributes")
    print()
    print("Stated plainly, and in the order of what survives longest:")
    print()
    print("1. **The Control-Property Review** — a structured method for "
          "deciding whether a named control can enforce a named property at "
          "all, with seven verdicts of which four are refusals.")
    print()
    print("2. **The specification-sensitivity audit** — a general test that "
          "marks a claim *contested* when a small, defensible change of "
          "specification would flip its verdict. This is the most portable "
          "idea here and works far outside SAP.")
    print()
    print("3. **Countermechanism review** — a discipline that owes no "
          "conclusion of structural failure until the strongest existing "
          "mechanism has been searched through independent routes and tested.")
    print()
    print("4. **A reconstructed autonomous-agent case study** in SAP FI that "
          "applies the three above and, in doing so, eliminates, narrows or "
          "reclassifies most of the findings its own author set out to make.")
    print()
    print("The first three are the durable contribution: they stand even if "
          "every SAP-specific result in the case study is eventually "
          "overturned. The case study is how they were earned, not what they "
          "depend on.")
    print()


if __name__ == "__main__":
    main()
