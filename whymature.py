"""
whymature.py -- why SAP, why its maturity is the point, and what to remember.

    python3 whymature.py            # the thesis section
    python3 whymature.py --check    # the thesis sentence and the maturity claim

This is the section that decides what the reader leaves with. The manuscript can
be read as three different papers — a SAP finding, a method, a critique of
overclaiming — and all three are true. This section fixes which one leads: the
autonomous-agent story in SAP, with the method as the instrument that earned it.
It states the thesis once, says why a mature environment is the whole point of
the choice, and hands the reader the sentence to carry.

Counts are read from the registers, never typed, so the maturity argument cannot
drift from the surface it describes.
"""
from __future__ import annotations

import sys

# The thesis everything else supports. Stated so it leads with SAP and
# maturity without claiming the reconstruction has already proved the maturity
# conclusion — that is gated behind B1–B3 and D1.
THESIS = (
    "Autonomous agents can make a guarantee depend on more than any one control "
    "was built to watch — a whole period, workflow, or set of principals — a "
    "control-property mismatch. This paper studies that mismatch on a "
    "reconstructed SAP FI authorization surface, chosen on purpose: SAP is a "
    "demanding, commercially mature control environment, so blaming the gap on "
    "immature access-control design is exactly the easy answer that deserves "
    "the hardest scrutiny.")


def _counts():
    from boundary import HELD
    from counterfactual import contested
    from mismatch import PAIRS
    from surface import MECHANISMS
    return {
        "pairs": len(PAIRS),
        "held": len(HELD),
        "contested": len(contested()),
        "mechanisms": len(MECHANISMS),
    }


def check() -> list[str]:
    problems = []
    if len(THESIS.split()) > 75:
        problems.append("the thesis is %d words; it has grown past a lead a "
                        "reader carries" % len(THESIS.split()))
    for term in ("autonomous agent", "mismatch", "mature", "immatur"):
        if term not in THESIS.lower():
            problems.append("the thesis no longer names %r, which the section "
                            "is built to establish" % term)
    # The thesis must stay conditional: the maturity conclusion is gated, so the
    # lead may not assert it as established.
    banned = ("hardest, most audited", "cannot simply be dismissed",
              "cannot be dismissed as immaturity", "proves", "establishes that "
              "immaturity")
    low = THESIS.lower()
    for b in banned:
        if b in low:
            problems.append("the thesis asserts the maturity conclusion the "
                            "gates have not permitted: %r" % b)
    c = _counts()
    if c["contested"] * 2 < c["pairs"]:
        problems.append("fewer than half the pairs are contested; the "
                        "'it cost the author something' claim below overstates")
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   thesis stated in %d words; maturity argument tied to the "
              "registers." % len(THESIS.split()))
        return

    c = _counts()
    print("# Why SAP, and why its maturity is the argument")
    print()
    print("**%s**" % THESIS)
    print()
    print("## What to remember")
    print()
    print("If you read nothing else, read this. When an agent acts, it can make "
          "a guarantee depend on something bigger than any single control was "
          "built to watch — a whole period, a whole workflow, a set of people "
          "acting in turn. The control still checks each action, and each "
          "action still passes. The gap opens above them, in the sum. It is not "
          "a bug in any one control. It is the point where an organisation's "
          "controls and the promises it makes on their strength quietly stop "
          "being the same thing. This paper finds that point in a reconstructed "
          "SAP FI surface, measures what it costs there, and says exactly what "
          "evidence would settle whether the same gap exists on a real, named "
          "path in production. Just as often, it declines to call something a "
          "failure when the evidence has not earned the word.")
    print()
    print("## The two things agents change here")
    print()
    print("Two findings in this paper are specific to autonomous execution, and "
          "they do not depend on each other, and only the first is about "
          "throughput. The first is aggregate: a document-local control cannot "
          "discriminate a harmful period-level sum from legitimate work when "
          "both are composed from documents indistinguishable on every field "
          "the control reads. It can throttle the total, but only by refusing "
          "legitimate work drawn from the same distribution. The second needs "
          "no aggregation, and no volume, at all. **Within the reconstruction, "
          "the architecture commonly preferred because it avoids standing agent "
          "privilege — principal propagation, in which the agent acts under a "
          "human's just-in-time identity — is the one that renders a composed "
          "segregation-of-duties conflict invisible to per-principal "
          "analysis.** Each propagated principal is individually clean; the "
          "conflict is completed across sessions that no static per-principal "
          "check ever considers together. A technical user who actually "
          "accumulated both grants *is* reported, which is how we know the "
          "ruleset is not simply inert. The finding is not that the control is "
          "broken; it is that removing the agent's standing privilege — sound "
          "advice on its own terms — moves the conflict to where the control is "
          "not looking.")
    print()
    print("## Why SAP, and not something easier")
    print()
    print("SAP was not chosen because it is popular, or because it is an ERP. "
          "It was chosen because SAP's authorization environment — PFCG "
          "authorization objects, FI tolerance groups, GRC access-risk "
          "analysis and its segregation-of-duties rulesets, the Security Audit "
          "Log, principal propagation, transport governance — is among the most "
          "mature, most heavily audited and most operationally hardened access "
          "control systems in commercial computing, refined across decades of "
          "financial-audit and regulatory pressure. %d such mechanisms are "
          "modelled here." % c["mechanisms"])
    print()
    print("That maturity is the point of the choice, and it sharpens the "
          "question rather than settling it. If a control-property mismatch "
          "survived only in a young or careless product, the right conclusion "
          "would be *fix the product*. If the shape survives validation against "
          "a named SAP product, release and business-process path, it becomes "
          "less plausibly attributable to immature access-control design and "
          "more plausibly attributable to where the control's observation "
          "boundary sits relative to what autonomous composition can assemble. "
          "**Until that validation is complete, the reconstruction establishes "
          "the argument's testable form, not its deployment-level "
          "conclusion.** What can be said now is narrower and still worth "
          "saying: the mismatch is not reducible, in the reconstruction, to the "
          "absence of aggregate-state control as a design concept, because SAP "
          "provides that control shape elsewhere, as the reversal in this paper "
          "records — whether it is available to the modelled path remains "
          "unresolved. SAP FI is not the victim of this paper; it is the "
          "environment demanding enough to make the question worth asking under "
          "scrutiny.")
    print()
    print("## What would change the SAP conclusion")
    print()
    print("The SAP conclusion is conditional, and the conditions are named "
          "before the evidence, not after. If FI tolerance groups turn out to "
          "retain relevant cross-document state, or if F110, Availability "
          "Control or another supported mechanism binds preventively to the "
          "modelled credit-memo path, the principal SAP finding becomes a "
          "control-placement or configuration result rather than a control "
          "gap. Those outcomes are pre-committed in determination D1 and remain "
          "open publication blockers (B1–B3). The opening above is written to "
          "survive either way: it is a claim about where an observation "
          "boundary sits, not a claim that SAP has failed.")
    print()
    print("## How to read what follows")
    print()
    # The pairs, by name, derived from the registers so the "not built around
    # one example" defence cannot drift from what the instrument actually did.
    from boundary import GAPS, HELD
    from counterfactual import contested as _contested
    _held = [h.id for h in HELD]
    _gaps = [g.id for g in GAPS]
    _con = {x.pair for x in _contested()}
    _contested_gaps = [g for g in _gaps if g in _con]
    _survivor = [g for g in _gaps if g not in _con]
    _respecified = [p for p in sorted(_con)
                    if p not in _held and p not in _gaps]
    print("This is not a paper hunting for a SAP gap to publish. Of the %d "
          "control-property pairs it specifies, one survives as an uncontested "
          "mismatch; %d controls hold; %d of the %d pairs are published as "
          "*contested* — a defensible alternative specification changes their "
          "verdict — and one earlier cost result was retracted. These "
          "categories are not disjoint: a pair can have an observed result "
          "while its specification stays contested, one held control is also "
          "contested, and the retraction concerns an earlier cost claim rather "
          "than an additional control-property pair. The claim-trajectory "
          "table later in the paper keeps what each experiment observed "
          "separate from whether its specification is still contested, for that "
          "reason."
          % (c["pairs"], c["held"], c["contested"], c["pairs"]))
    print()
    print("By name, so the point is impossible to miss: **%s hold; %s produce "
          "observed mismatches whose protected-property specifications remain "
          "contested; %s was withdrawn as misspecified, respecified against the "
          "full transport surface, and run; and %s is the only uncontested "
          "mismatch.** That is the same instrument reaching several different "
          "verdicts on pairs subjected to the same procedure, including "
          "verdicts adverse to the paper's original claims. This pattern is "
          "evidence against the method having been reverse-engineered merely to "
          "manufacture %s. The instrument that generated this attrition is the "
          "paper's method, and the pages that follow are the case that earned "
          "it, not a showcase built around a single finding."
          % (", ".join(_held), " and ".join(_contested_gaps),
             " and ".join(_respecified) or "one prediction",
             " and ".join(_survivor), " and ".join(_survivor)))
    print()


if __name__ == "__main__":
    main()
