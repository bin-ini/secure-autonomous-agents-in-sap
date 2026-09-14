"""
counterfactual.py -- specification sensitivity.

    python3 counterfactual.py            # the audit
    python3 counterfactual.py --check    # refuse to publish a contested verdict

`mismatch.py` answers HISTORICAL circularity: every extent is readable off code
that predates the formalism. It does not answer SEMANTIC circularity, and the
distinction matters.

    Historical:  did you write the specification after seeing the result?
    Semantic:    of the several defensible ways to specify this control and
                 this property, did you pick the one that produces the verdict
                 you wanted?

The second cannot be answered by provenance. It can only be answered by naming,
for each pair, the SMALLEST DEFENSIBLE ALTERNATIVE specification that would
change the verdict, and then asking whether that alternative is inconsistent
with independent evidence -- or merely inconsistent with the result we
observed. If it is only the latter, the verdict is CONTESTED and the formalism
has not earned it.

The decisive question underneath all of this:

    Is the protected property one the ORGANISATION claims to guarantee, or a
    stronger one the author wishes it guaranteed?

A control that holds against its own stated property and fails against ours is
not a control that failed. It is a control we moved the goalposts on, and the
paper has to argue for the stronger property in the open rather than encode it
in a specification and call the difference a finding.

This audit is allowed to damage the formalism, and on its first run it does:
three of the seven pairs come back contested, including one of the two the paper
was planning to publish as a gap.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

from mismatch import PAIRS


# ---------------------------------------------------------------------------
# THE ASYMMETRY. The audit is not a symmetric instrument and the vocabulary
# must not let it look like one.
#
# Finding one defensible alternative specification invalidates a verdict.
# Failing to find one establishes nothing about whether a second, sixth or
# tenth exists -- the search is bounded by the imagination of whoever ran it.
# That is the same limitation the first book recorded against pre-registration
# in its E.5 ("a pre-registration is bounded by the author's imagination"),
# arriving in a new instrument, and it belongs beside the audit rather than in
# a limitations section.
ASYMMETRY = (
    "The specification-sensitivity audit can INVALIDATE a claim by finding a "
    "defensible alternative specification. It cannot CERTIFY one: failure to "
    "find an alternative reflects a bounded search, not specification "
    "uniqueness."
)

AUDIT_STATUS = {
    "rejected":
        "independent evidence contradicts the specification or the verdict",
    "contested":
        "at least one defensible alternative specification changes the verdict",
    "not-yet-contested":
        "the bounded search found no such alternative. **This is not "
        "certification.**",
    "replicated":
        "an independent reviewer applied the protocol and reached the same "
        "specification",
}

# Words this project may not use about its own verdicts.
FORBIDDEN = ("uncontestable", "uncontested and certain", "certified by the "
             "audit", "proven unique", "specification is unique")


@dataclass(frozen=True)
class Counterfactual:
    pair: str
    alternative: str          # the smallest defensible alternative spec
    flips_to: str             # the verdict it would produce
    defensible: bool          # consistent with INDEPENDENT evidence?
    grounds: str              # what makes it defensible, or what rules it out
    if_contested: str         # what the paper must then do


CF = [
    Counterfactual(
        "H1",
        "Specify the control as observing a principal's accumulated postings "
        "rather than one document — i.e. treat the tolerance group as holding "
        "state.",
        "holds (unchanged, but for a different reason) / would also rescue G1",
        False,
        "The mechanism's own field names are per-document and per-line "
        "quantities, and nothing in the reviewed material describes a "
        "tolerance field that survives a document. **This is the weakest "
        "'not defensible' in the file**: it rests on secondary sources, and "
        "surface spec M2 lists exactly this as the assumption that would "
        "destroy G1 if wrong.",
        "Verify M2 against primary documentation. Until then the ruling out "
        "is provisional and should be described as such."),

    Counterfactual(
        "G1",
        "Specify the protected property as 'no single document exceeds "
        "materiality' rather than 'cumulative credited value in the period "
        "stays below materiality'.",
        "holds",
        False,
        "Materiality is an audit concept defined over a reporting period, not "
        "over a document. No auditor states it per document, and an "
        "organisation that did would be describing a different property "
        "altogether. The period-level definition is the one the business "
        "claims, not one we invented.",
        "—"),

    Counterfactual(
        "H2",
        "Specify the property as 'no action outside the granted org unit at "
        "any point in the workflow' — a workflow-extent version.",
        "cannot-discriminate",
        False,
        "The stronger property is satisfied by the weaker one here: if every "
        "single action is refused outside the unit, no sequence of them can "
        "escape it. The extents differ and the verdict does not, because the "
        "property is closed under composition. That is a genuine feature of "
        "this control-property pair and not a lucky encoding.",
        "—"),

    Counterfactual(
        "H3",
        "None available that flips it. The control and the property are the "
        "same sentence: SAP's own documentation defines the SoD control as "
        "detecting conflicting access assigned to a user.",
        "holds",
        False,
        "This pair is the formalism's easiest case precisely because the "
        "vendor states the property. It is also the reason G2 is hard.",
        "—"),

    Counterfactual(
        "G2",
        "Keep H3's property — 'no principal holds both sides of a conflicting "
        "pair' — instead of substituting 'no single decision process completes "
        "both sides'.",
        "holds",
        True,          # <-- CONTESTED
        "**This alternative is defensible and it is what SAP actually claims.** "
        "The delivered SoD control is documented as distributing access rights "
        "among users and detecting conflicting access assigned to a user. "
        "Against that property the control holds; our experiment confirms it "
        "does (H3). G2 exists only because we substituted a decision-layer "
        "property the vendor never claimed. That substitution may well be the "
        "right thing to argue for — but it is an argument, not a measurement, "
        "and encoding it in a specification does not make it evidence.",
        "G2 may not be published as 'SAP SoD failed'. It must be published as: "
        "*the deployed control holds against the property it claims; here is "
        "why autonomous execution makes a stronger decision-layer property "
        "necessary, and here is the measurement that distinguishes the two.* "
        "The measurement is the open item in S0c — how many separately "
        "accountable decision-makers does the workflow contain — and until it "
        "exists G2 is a formal result about a newly proposed property."),

    Counterfactual(
        "G3",
        "Specify the property's subject as the ACCOUNTABLE PRINCIPAL rather "
        "than the DECIDING ACTOR — i.e. accept that an audit trail's stated "
        "objective is to name who is answerable, not who chose.",
        "holds",
        True,          # <-- CONTESTED
        "Defensible, and arguably the conventional reading. An audit trail "
        "that names the authenticated principal is doing exactly what audit "
        "trails have always been for: establishing accountability, not "
        "reconstructing decision provenance. If that is the property, the "
        "record is correct and there is no subject mismatch.",
        "The paper must argue that autonomous mediation breaks the assumption "
        "that made those two the same thing — that naming the accountable "
        "principal used to name the decider because they were one entity. "
        "That is a real argument and it is not yet made anywhere in the "
        "manuscript.\n"
        "\n"
        "**One of those two grounds has since been cleared.** X12 tested the "
        "correlates loss L2 records as never tried, and they do not recover "
        "the actor; the rule-3 block is lifted and the gap survives smaller. "
        "The contested specification stands, and it is the ground that "
        "matters: the countermechanism question is settled and the property "
        "question is not."),

    Counterfactual(
        "H4",
        "Specify the property as 'released code behaves as the change request "
        "described', rather than 'released code does not change system "
        "behaviour in an unauthorised way' — i.e. make the property about "
        "conformance to an intent stated elsewhere rather than about the "
        "behaviour itself.",
        "cannot discriminate",
        True,          # <-- CONTESTED
        "**Defensible, and it is what a static check actually does.** An ATC "
        "check variant matches patterns; it does not read the change request "
        "and cannot tell whether the behaviour is the one that was asked for. "
        "A peer reviewer can, and a check variant cannot, so specifying the "
        "control as one thing collapses a distinction that matters. Under the "
        "alternative property, the system-enforced half of H4 loses its "
        "subject match and only the human half retains it — which relocates "
        "the whole result onto a step whose coverage X11 had to sweep because "
        "nothing guarantees it.",
        "H4 must not be published as 'the transport surface holds'. It must "
        "be published as: *the surface contains decisions that range over the "
        "property's own subject, and how much of the property they cover "
        "depends on which property is meant and on a coverage parameter no "
        "mechanism enforces.* The narrow reading is the honest one and it is "
        "the one the paper takes."),

    Counterfactual(
        "P1",
        "Specify the control as the COMPLETE transport-governance surface — "
        "ATC checks, code review, approval steps, test-system promotion — "
        "rather than the single authorisation object `S_TRANSPRT ACTVT 43`.",
        "possibly holds",
        True,          # <-- MISSPECIFIED
        "**The prediction as written is unfairly specified and would deserve "
        "to be dismissed.** Release authorisation has never claimed that "
        "released code is behaviourally safe; it claims that a permitted "
        "principal may release. A SAP reviewer answers in one sentence: "
        "authorisation establishes who may release, and ATC, review, approval "
        "and testing assess what is released. That answer does not falsify "
        "the principle — it shows we selected the wrong control-harm pair.",
        "Respecify P1 before running it: *does the complete transport-"
        "governance control set contain a content-ranging decision capable of "
        "discriminating the defined harmful transport BEFORE release?* Then "
        "three outcomes are informative rather than one. If such a control "
        "exists, the prediction narrows. If only authorisation exists, the "
        "subject mismatch survives against the full surface. If review catches "
        "it but does not prevent release, the paper must separate preventive "
        "from detective coverage — which it has not yet had to do anywhere.\n"
        "\n"
        "**RESPECIFIED AND RUN — X11.** All three branches were informative "
        "and two of them fired. The surface does contain content-ranging "
        "preventive decisions, so the prediction narrows to the authorisation "
        "object and transport leaves the paper's list of open mismatches; and "
        "wherever the only content-ranging step is detective, forty of forty "
        "harmful transports are flagged and forty of forty are in "
        "production, so the preventive/detective separation the audit "
        "anticipated is now a measured result rather than a possibility. A "
        "third thing the experiment produced was a retraction: its first "
        "version had no channel through which a content-ranging step could "
        "stop a benign change, reported zero cost as a measurement, and that "
        "is loss L6. The "
        "contested marking stands: it records that the ORIGINAL P1 "
        "specification was unfair, and running a better-specified experiment "
        "does not retroactively make the original one fair."),
]


BY_PAIR = {c.pair: c for c in CF}


def contested() -> list[Counterfactual]:
    return [c for c in CF if c.defensible]


def status_of(pair_id: str) -> str:
    c = BY_PAIR.get(pair_id)
    if c is None:
        return "not-yet-contested"
    return "contested" if c.defensible else "not-yet-contested"


def check() -> list[str]:
    problems = []
    ids = {p.id for p in PAIRS}
    for pid in ids:
        if pid not in BY_PAIR:
            problems.append("%s has no counterfactual — every pair must name "
                            "the smallest alternative specification that would "
                            "change its verdict, or the verdict is unearned"
                            % pid)
    for c in CF:
        if c.pair not in ids:
            problems.append("%s is not a pair in mismatch.py" % c.pair)
        if not c.grounds.strip():
            problems.append("%s: no independent grounds given" % c.pair)
        if any(f in (c.grounds + c.if_contested).lower() for f in FORBIDDEN):
            problems.append("%s uses language the audit cannot support -- it "
                            "can refuse a verdict, never certify one" % c.pair)
        if c.defensible and not c.if_contested.strip():
            problems.append("%s is contested and says nothing about what the "
                            "paper must do instead" % c.pair)
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        con = contested()
        print("   %d pairs audited, %d CONTESTED: %s"
              % (len(CF), len(con), ", ".join(c.pair for c in con)))
        print("   a contested verdict may not be published as a measured "
              "mismatch without the argument named in its entry.")
        return

    print("# Specification sensitivity")
    print()
    print("*Generated by `python3 counterfactual.py`.*")
    print()
    print("`mismatch.py` shows every extent comes from code that predates the "
          "formalism, which answers **historical** circularity. It cannot "
          "answer **semantic** circularity: of the several defensible ways to "
          "specify a control and a property, did the author choose the one "
          "that yields the wanted verdict?")
    print()
    print("For each pair, the smallest defensible alternative specification "
          "that would change the verdict, and whether that alternative is "
          "ruled out by evidence independent of the experiment we ran.")
    print()
    print("> **The question underneath: is the protected property one the "
          "organisation claims to guarantee, or a stronger one the author "
          "wishes it guaranteed?**")
    print()
    print("## The instrument is asymmetric")
    print()
    print("> **%s**" % ASYMMETRY)
    print()
    print("| status | meaning |")
    print("|:---|:---|")
    for k, v in AUDIT_STATUS.items():
        print("| `%s` | %s |" % (k, v))
    print()
    print("So the strongest thing sayable about G1 is that it is **not yet "
          "contested by a bounded search** — and that sentence has to appear "
          "wherever G1 does. A reviewer who invents a sixth specification "
          "tomorrow has not caught us out; they have used the instrument as "
          "intended.")
    print()
    print("| pair | alternative specification | would give | ruled out by "
          "independent evidence? |")
    print("|:--|:---|:---|:---|")
    for c in CF:
        print("| **%s** | %s | %s | %s |"
              % (c.pair, c.alternative, c.flips_to,
                 "no — **CONTESTED**" if c.defensible else "yes"))
    print()
    for c in CF:
        print("### %s%s" % (c.pair, " — CONTESTED" if c.defensible else ""))
        print()
        print("*Grounds:* %s" % c.grounds)
        print()
        if c.defensible:
            print("*What the paper must do instead:* %s" % c.if_contested)
            print()

    con = contested()
    print("---")
    print()
    print("**%d of %d pairs are contested: %s.** The remainder are `not-yet-contested`, which is a statement about our search and not about their specifications."
          % (len(con), len(CF), ", ".join(c.pair for c in con)))
    print()
    _tested = [p for p in PAIRS if p.observed != "untested"]
    _survive = [p.id for p in PAIRS if p.id not in {c.pair for c in con}]
    print("That is a worse result for the paper than the formalism's "
          "%d-of-%d agreement suggested, and it is the more useful number. "
          "The verdicts that survive this audit — %s — are the ones where the "
          "property is the organisation's own. **G1 is therefore the paper's "
          "only uncontested gap**, and the H1/G1 pair is the only place where "
          "one control, two harms and two derived verdicts all rest on "
          "properties nobody has to be argued into."
          % (len(_tested), len(_tested),
             ", ".join(_survive[:-1]) + " and " + _survive[-1]))


if __name__ == "__main__":
    main()
