"""
mismatch.py -- the formal object.

    python3 mismatch.py            # the table
    python3 mismatch.py --check    # does the principle PREDICT the results?

The review that produced this file was right about the central weakness: X7, X8
and X9 could be read as three known control limitations placed next to each
other, grouped afterwards by someone who wanted them grouped. A formalism that
merely re-describes three results in notation would be the same defect wearing
a better suit.

So this file is written to be falsifiable in the only way a formalism can be:
it assigns each control-harm pair a specification, derives a verdict from the
specification ALONE, and then checks that verdict against what the experiments
actually did. If the derivation disagrees with an experiment, the formalism is
wrong and `--check` fails.

---------------------------------------------------------------------------
THE PRINCIPLE

  A control cannot discriminate harmful from legitimate execution when the
  protected property is defined outside the control's observation boundary.

"Outside" takes exactly two forms, and keeping them distinct is what stops the
principle being a slogan:

  EXTENT MISMATCH   the property ranges over a strictly larger compositional
                    extent -- more actions, more principals, or a longer
                    horizon -- than the control observes and retains.

  SUBJECT MISMATCH  the property is about a different entity than the control's
                    predicate, and the map from the control's subject to the
                    property's subject is not injective. No amount of extra
                    history fixes this one; it is a projection failure, not a
                    memory failure.

---------------------------------------------------------------------------
THE LOAD-BEARING CONSEQUENCE

A control is not "strong" or "weak". A control-HARM PAIR either matches or does
not. H1 and G1 below are the SAME SAP control -- FI tolerance groups -- against
two different harms, and the formalism derives "holds" for one and "cannot
discriminate" for the other from the specifications alone, before looking at
any result. That pair is the sharpest available evidence that this formalism
does work rather than decorating work already done.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Compositional extent: three axes, each a containment order.
# ---------------------------------------------------------------------------

ACTIONS = ["single", "sequence", "aggregate"]
PRINCIPALS = ["one", "many"]
HORIZON = ["instant", "session", "period"]


@dataclass(frozen=True)
class Extent:
    actions: int
    principals: int
    horizon: int

    def covers(self, other: "Extent") -> bool:
        """Componentwise containment. A partial order, deliberately: two
        extents can be incomparable, and the code must not pretend otherwise."""
        return (self.actions >= other.actions
                and self.principals >= other.principals
                and self.horizon >= other.horizon)

    def short(self) -> str:
        return "%s/%s/%s" % (ACTIONS[self.actions], PRINCIPALS[self.principals],
                             HORIZON[self.horizon])


SINGLE_ACTION = Extent(0, 0, 0)


@dataclass(frozen=True)
class Pair:
    """A control paired with the harm it is being asked to prevent.

    The six fields the review asked for, plus the two the derivation needs.
    """
    id: str
    control: str
    control_subject: str        # what entity the predicate is about
    observes: Extent            # what it can see at decision time
    retains: str                # what history it keeps
    protected_property: str
    property_subject: str       # what entity the property is about
    property_extent: Extent
    subject_map_injective: bool  # control subject -> property subject
    # COMPOSITIONAL CLOSURE. The refinement that stops the principle
    # degenerating into "a broader property needs a broader control".
    #
    # Sometimes a local invariant is globally sufficient: if every action
    # outside the permitted organisational unit is refused, no sequence
    # composed of permitted actions can leave the unit. The property is closed
    # under the control's locally enforced predicate, the extents differ, and
    # the control still guarantees the property.
    #
    # H2 is that case and it is why this field exists. G1 is not: no
    # per-document predicate that admits the legitimate population implies a
    # bound on the sum.
    closed_under_composition: bool
    # WHERE THE EXTENT COMES FROM. The obvious objection to this file is
    # circularity: the author assigns the extents, so of course they predict
    # the results. The defence is that every extent must be readable off code
    # written before this file existed -- a harm predicate, a gate, a log
    # schema -- and this field says which. An extent with no source is an
    # extent that was fitted, and --check refuses it.
    extent_source: str
    # What the experiments actually found. Used ONLY by --check, never by the
    # derivation.
    observed: str               # "holds" | "cannot-discriminate" | "untested"
    evidence: str

    # -- the derivation ---------------------------------------------------

    def extent_wider(self) -> bool:
        """The property ranges further than the control observes."""
        return not self.observes.covers(self.property_extent)

    def extent_mismatch(self) -> bool:
        """A wider property is a MISMATCH only if it is not closed under the
        control's local predicate. An extent difference alone proves nothing."""
        return self.extent_wider() and not self.closed_under_composition

    def subject_mismatch(self) -> bool:
        return not self.subject_map_injective

    def kinds(self) -> list[str]:
        k = []
        if self.extent_mismatch():
            k.append("extent")
        if self.subject_mismatch():
            k.append("subject")
        return k

    def predicted(self) -> str:
        return "cannot-discriminate" if self.kinds() else "holds"

    def axes(self) -> str:
        """Which axes the property outruns the control on."""
        o, p = self.observes, self.property_extent
        out = []
        if p.actions > o.actions:
            out.append("actions %s>%s" % (ACTIONS[p.actions],
                                          ACTIONS[o.actions]))
        if p.principals > o.principals:
            out.append("principals %s>%s" % (PRINCIPALS[p.principals],
                                             PRINCIPALS[o.principals]))
        if p.horizon > o.horizon:
            out.append("horizon %s>%s" % (HORIZON[p.horizon],
                                          HORIZON[o.horizon]))
        note = ", ".join(out) or "—"
        if self.extent_wider() and self.closed_under_composition:
            note += "  *(closed under composition — no mismatch)*"
        return note


# ---------------------------------------------------------------------------
# The pairs. Held controls and surviving gaps, specified identically, because
# the whole point is that they are the same kind of object.
# ---------------------------------------------------------------------------

PAIRS = [
    # -- the decisive pair: one control, two harms ------------------------
    Pair(
        "H1", "FI tolerance group (per-document / per-line amount)",
        "document", SINGLE_ACTION, "none",
        "no posting of anomalous value", "document",
        Extent(0, 0, 0), True, False,
        "`workload.fraud_above_band()` -- the harmful documents differ from "
        "legitimate ones in per-document amount, so the property is "
        "decided one document at a time",
        "holds",
        "X7 positive control: clean separation, 100% legitimate throughput"),

    Pair(
        "G1", "FI tolerance group (per-document / per-line amount)",
        "document", SINGLE_ACTION, "none",
        "cumulative credited value in the period below materiality",
        "the period's ledger",
        Extent(2, 0, 2), True, False,
        "`Ledger.credited_total()` against MATERIALITY -- a sum over every "
        "document in the period, written in `experiments.py` before "
        "this file existed",
        "cannot-discriminate",
        "X7 primary: 12,288 configurations, best retains 37.5% throughput"),

    # -- authorisation ----------------------------------------------------
    Pair(
        "H2", "PFCG organisational-level restriction (AUTHORITY-CHECK)",
        "action against an org unit", SINGLE_ACTION, "none",
        "no part of the workflow touches an org unit outside the grant",
        "the workflow",
        Extent(1, 0, 1), True, True,
        "`Authorization.permits()` -- the predicate reads the fields of one "
        "action and nothing else",
        "holds",
        "X7/verify: all 120 documents refused for the wrong company code"),

    # -- segregation of duties --------------------------------------------
    Pair(
        "H3", "GRC Access Risk Analysis (static, per principal)",
        "one principal's grant set", Extent(1, 0, 2), "the grant set",
        "no principal holds both sides of a conflicting duty pair",
        "one principal's grant set",
        Extent(1, 0, 2), True, False,
        "`SodRuleset.violations(p)` -- takes ONE principal and reads that "
        "principal's grants",
        "holds",
        "X8: the technical user accumulating both grants IS flagged"),

    Pair(
        "G2", "GRC Access Risk Analysis (static, per principal)",
        "one principal's grant set", Extent(1, 0, 2), "the grant set",
        "no single decision process completes both sides of a conflicting "
        "duty pair", "the workflow",
        Extent(1, 1, 2), True, False,
        "the harm predicate in `x8()` reads `led.payments` for a payment to "
        "an altered account -- a state two principals produced in "
        "sequence",
        "cannot-discriminate",
        "X8: both propagated principals clean, composition completes"),

    # -- evidence ----------------------------------------------------------
    Pair(
        "G3", "Security Audit Log record",
        "authenticated principal", SINGLE_ACTION, "the log",
        "attribution of the action to the entity that SELECTED it",
        "the deciding actor",
        SINGLE_ACTION, False, False,          # <- the map is not injective
        "`SalRecord` carries `user`; `actor` is None unless the field is "
        "switched on. The non-injectivity is in the schema, not in "
        "our reading of it",
        "cannot-discriminate",
        "X12, which repairs loss L2. 512 conditions. Retention depth changed "
        "nothing in any of the 18 condition groups where no recorded field "
        "separated the actors, and the best accuracy reached in any of them "
        "is chance. Every condition that did attribute had a field naming the "
        "origin. For the agent-versus-human question the objection actually "
        "raises, the upper bound on ANY procedure reading principal, "
        "transaction, terminal and timestamp equals the do-nothing majority "
        "baseline at every action rate tested."),

    # -- a prediction, on a pair no experiment has touched ------------------
    Pair(
        "P1", "CTS transport release (S_TRANSPRT, ACTVT 43)",
        "the transport request", SINGLE_ACTION, "none",
        "released code does not change system behaviour in an unauthorised "
        "way", "the behaviour of the transported objects",
        SINGLE_ACTION, False, False,
        "`Cts.release()` checks S_TRANSPRT ACTVT 43 and never inspects "
        "`tr.objects` -- the control does not read the content at all",
        "cannot-discriminate",
        "**PREDICTION MADE BEFORE THE EXPERIMENT, THEN TESTED.** X11: across "
        "every configuration whose active steps range only over the request, "
        "none discriminates and all forty harmful transports reach production "
        "in every one of them, at every setting of every parameter. The "
        "prediction held at the pair it names — and X11 also found what the "
        "counterfactual audit said it would, which is that the same surface "
        "contains content-ranging decisions the prediction had ignored. See "
        "H4."),
    # -- the pair the counterfactual audit said P1 should have named ------
    Pair(
        "H4", "Static check and pre-release review of the transported objects "
        "(ATC check variant, peer review, quality-system exercise)",
        "the behaviour of the transported objects", SINGLE_ACTION, "none",
        "released code does not change system behaviour in an unauthorised "
        "way", "the behaviour of the transported objects",
        SINGLE_ACTION, True, False,
        "`transport.run_one()` -- steps T2, T3 and T5 read `o.behaviour`, the "
        "same entity the property is about. T1 and T4 read the request and "
        "never open it",
        "holds",
        "X11: 2,512 of 12,800 configurations discriminate and every one of "
        "them has a content-ranging preventive step active. **Close to "
        "definitional, and reported as such** — a control that reads the "
        "property's own subject is not a surprising thing to find sufficient, "
        "and loss L6 records what happened when the cost side of it was "
        "reported as a measurement. What the pair does establish is the "
        "contrast in KIND: the same surface, one step away, cannot "
        "discriminate at any setting of any parameter."),
]


# ---------------------------------------------------------------------------
# The check: does the derivation agree with the experiments?
# ---------------------------------------------------------------------------

def check() -> list[str]:
    problems = []
    tested = [p for p in PAIRS if p.observed != "untested"]
    if not tested:
        problems.append("nothing to check the formalism against")
    for p in PAIRS:
        if not p.extent_source.strip():
            problems.append("%s: no source for its extent -- an extent with "
                            "no source is an extent that was fitted" % p.id)
    for p in tested:
        if p.predicted() != p.observed:
            problems.append(
                "%s: the principle predicts %r, the experiment observed %r. "
                "The formalism is wrong, not the experiment."
                % (p.id, p.predicted(), p.observed))

    # Closure must do work somewhere, or the field is decoration and the
    # principle really is "a broader property needs a broader control".
    if not any(p.extent_wider() and p.closed_under_composition for p in PAIRS):
        problems.append("no pair exercises compositional closure -- the "
                        "refinement is untested and should be removed rather "
                        "than carried")

    # The formalism earns its place only if it SEPARATES. A rule that predicts
    # the same verdict everywhere agrees with any dataset that happens to be
    # uniform and has told us nothing.
    verdicts = {p.predicted() for p in tested}
    if len(verdicts) < 2:
        problems.append("the principle assigns every tested pair the same "
                        "verdict, so it discriminates nothing")

    # The decisive pair must actually be one control against two harms.
    same = [p for p in PAIRS if p.id in ("H1", "G1")]
    if len({p.control for p in same}) != 1:
        problems.append("H1 and G1 are no longer the same control, which "
                        "removes the sharpest evidence that the formalism "
                        "does work rather than describing it")
    if same[0].predicted() == same[1].predicted():
        problems.append("H1 and G1 receive the same verdict; the formalism "
                        "is not distinguishing harm from control")
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        n = len([x for x in PAIRS if x.observed != "untested"])
        print("   the principle predicts %d of %d tested pairs correctly, "
              "and separates them." % (n, n))
        print("   H1 and G1: one control, two harms, two verdicts, derived "
              "from the specification alone.")
        return

    print("# The Control-Composition Mismatch Principle")
    print()
    print("> **A control cannot discriminate harmful from legitimate "
          "execution when the protected property lies outside its observation "
          "boundary, the executions are indistinguishable on the control's "
          "inputs, and the locally enforced predicate does not compose into "
          "the property.**")
    print()
    print("The final clause is not decoration. An extent difference alone is "
          "insufficient: compositional closure must first be excluded, which is "
          "exactly what H2 below demonstrates — a property wider than the "
          "boundary that the local predicate nonetheless guarantees.")
    print()
    print("Two forms. **Extent mismatch:** the property ranges over more "
          "actions, more principals, or a longer horizon than the control "
          "observes and retains. **Subject mismatch:** the property is about a "
          "different entity than the control's predicate, and the map between "
          "them is not injective — which no amount of retained history "
          "repairs.")
    print()
    print("Each row's verdict is derived from its specification alone. In every "
          "tested pair the observed outcome matched that derived verdict, so the "
          "summary table below carries only what a reader needs to follow the "
          "argument; the full observation boundary, subject and extent for each "
          "pair are drawn in Figure 1 and set out in the per-pair discussion.")
    print()
    print("| pair | control | the property it is asked to guarantee | mismatch "
          "| verdict |")
    print("|:--|:---|:---|:---|:---|")
    for p in PAIRS:
        print("| **%s** | %s | %s | %s | **%s** |"
              % (p.id, p.control, p.protected_property,
                 "+".join(p.kinds()) or "none", p.predicted()))
    print()
    print("*(The paired detail — what each control observes at decision time "
          "versus what its property ranges over — is the substance of Figure 1 "
          "and the sections that follow; collapsing it into one ten-column table "
          "made it unreadable, so it is shown where there is room to see it.)*")
    print()
    print("## The decisive pair")
    print()
    h1, g1 = [p for p in PAIRS if p.id in ("H1", "G1")]
    print("**H1 and G1 are the same SAP control.** FI tolerance groups, "
          "unchanged, against two different harms.")
    print()
    print("| | H1 | G1 |")
    print("|:---|:---|:---|")
    print("| harm | %s | %s |" % (h1.protected_property, g1.protected_property))
    print("| property extent | `%s` | `%s` |"
          % (h1.property_extent.short(), g1.property_extent.short()))
    print("| control outrun on | %s | %s |" % (h1.axes(), g1.axes()))
    print("| derived verdict | **%s** | **%s** |"
          % (h1.predicted(), g1.predicted()))
    print("| experiment | %s | %s |" % (h1.evidence, g1.evidence))
    print()
    print("This is why the paper is not a list of SAP defects. A control is not "
          "strong or weak; a control-harm pair either matches or it does not. "
          "The same tolerance group is a correct and sufficient control against "
          "a document-local harm and cannot discriminate at all against a "
          "period-aggregate one, and the difference is derivable before any "
          "experiment runs.")
    print()
    print("## What the experiments become")
    print()
    print("| experiment | pair | form | where the boundary is crossed |")
    print("|:---|:--|:---|:---|")
    rows = [("X7", "G1"), ("X8", "G2"), ("X9/X12", "G3"), ("X11", "P1"),
            ("X11", "H4")]
    for exp, pid in rows:
        p = [q for q in PAIRS if q.id == pid][0]
        form = ("subject mismatch" if p.subject_mismatch()
                else "extent mismatch" if p.extent_mismatch()
                else "no mismatch — the pair holds")
        if p.subject_mismatch():
            where = ("the control's predicate is about %s; the property is "
                     "about %s, and the map between them is not injective"
                     % (p.control_subject, p.property_subject))
        elif p.extent_mismatch():
            where = p.axes()
        else:
            where = ("nowhere — the control's subject IS the property's "
                     "subject")
        print("| **%s** | %s | %s | %s |" % (exp, pid, form, where))
    print()
    print("They are not observations that happened to sit near each other. "
          "Two are the same failure along different axes of one extent, two "
          "are the other form of the same boundary, and the last is what the "
          "boundary looks like from the inside — a control in the same "
          "governance surface whose predicate is about the property's own "
          "subject.")
    print()
    print("## The prediction that was made before the experiment")
    print()
    p1 = [p for p in PAIRS if p.id == "P1"][0]
    print("**%s — %s.** %s" % (p1.id, p1.control, p1.evidence))


if __name__ == "__main__":
    main()
