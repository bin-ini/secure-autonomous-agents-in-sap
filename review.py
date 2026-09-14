"""
review.py -- the Control-Property Review, blank and worked.

    python3 review.py            # the instrument, with our four pairs filled in
    python3 review.py --blank    # the template alone
    python3 review.py --check    # every worked example must fill every field

This is the paper's last chapter and its only reusable part.

An earlier plan ended the paper on accounting: one mismatch admitted, two
refused, one prediction respecified. That is the honest summary and it is the
wrong final chapter, because a reader cannot apply a narrative of what the
method cost us. The accounting belongs in the abstract. The instrument belongs
at the end, blank, with our own pairs as worked examples an Oracle EBS,
Workday, ServiceNow or core-banking team can read past.

The one thing the template must not become is a checklist that feels like
progress. Every section below can produce the answer "we do not know", and
three of the four verdicts it can issue are refusals.
"""
from __future__ import annotations

import sys

SECTIONS = [
    ("Control", [
        "Control name",
        "Product, module and release — *'SAP' is not a scope*",
        "Enforcement point",
        "Preventive, detective, corrective, or evidentiary",
    ]),
    ("Control specification", [
        "Control subject — what entity is the predicate about?",
        "Observation boundary — what can it see at decision time?",
        "Retained state — what history does it keep?",
        "Local predicate — what does it decide, per evaluation?",
        "Decision outputs",
        "Source of the specification",
        "Independent evidence for the specification "
        "*(primary documentation, vendor statement, or reconstruction)*",
    ]),
    ("Protected property", [
        "Property statement",
        "Property subject — what entity is the property about?",
        "Extent across actions — single, sequence, aggregate",
        "Extent across principals — one, many",
        "Time horizon — instant, session, period",
        "Source of the property",
        "**Who claims this property — the organisation, the vendor, a "
        "regulator, or the researcher?**",
    ]),
    ("Closure test", [
        "If the local predicate holds for every action, does the protected "
        "property necessarily hold for the complete workflow?",
        "If yes — state the closure argument",
        "If no — give the smallest counterexample",
    ]),
    ("Specification-sensitivity audit", [
        "Smallest defensible alternative CONTROL specification",
        "Smallest defensible alternative PROPERTY specification",
        "Does either alternative change the verdict?",
        "What independent evidence prefers the specification chosen?",
        "Audit status — rejected, contested, not-yet-contested, replicated",
        "*Absence of an identified alternative does not certify uniqueness. "
        "The search is bounded by the imagination of whoever ran it.*",
    ]),
    ("Countermechanism test", [
        "Strongest existing mechanism a practitioner would claim closes this",
        "Was it tested?",
        "Was it tested at the correct business-process scope?",
        "Is there an equivalent mechanism ELSEWHERE in the same product?",
        "**Through how many independent retrieval routes was the "
        "countermechanism search performed?** *A control-surface review is "
        "incomplete until the strongest countermechanisms have been searched "
        "through independent routes. This question exists because a single "
        "route missed Availability Control — the one mechanism capable of "
        "overturning this paper's principal finding. See loss L3.*",
        "What result would eliminate the claim?",
    ]),
]

VERDICTS = [
    ("holds directly", "the control observes the property"),
    ("holds by compositional closure",
     "the property is wider, and the local predicate composes into it"),
    ("cannot discriminate",
     "the property is outside the boundary and is not closed"),
    ("contested specification",
     "a defensible alternative specification changes the verdict"),
    ("countermechanism untested",
     "the strongest existing mechanism was never tried"),
    ("non-discriminating experiment",
     "the test could not have come out otherwise"),
    ("unsupported", "no evidence either way"),
]

# A one-line gloss per section, so the condensed procedure below is generated
# from the same SECTIONS the full instrument uses and cannot drift from it.
STEP_GLOSS = {
    "Control": "Name the control, its enforcement point, and its type.",
    "Control specification": "State what it observes at decision time, what "
                             "state it retains, and the local predicate it "
                             "enforces.",
    "Protected property": "State the property, its extent across actions, "
                          "principals and time, and — decisively — WHO claims "
                          "it.",
    "Closure test": "Ask whether the local predicate, holding for every action, "
                    "forces the property over the whole workflow.",
    "Specification-sensitivity audit": "Name the smallest defensible "
                                       "alternative specification. If it flips "
                                       "the verdict, the claim is contested.",
    "Countermechanism test": "Search, through more than one route, for the "
                             "strongest existing mechanism that would close "
                             "this — and test it before concluding.",
}

# When the METHOD itself would be wrong — not a claim it evaluates, the
# instrument. Stated so a reviewer does not have to ask.
FRAMEWORK_FAILURE = [
    "Independent reviewers, applying the instrument to the same case from the "
    "same evidence, reach systematically different verdicts. (This is what "
    "review R2 is for, and it is an open gate.)",
    "A small, defensible change to a specification produces an arbitrary rather "
    "than an explicable change of verdict — so the categories are not carving "
    "anything real.",
    "The instrument cannot separate a control everyone agrees enforces its "
    "property directly from one everyone agrees cannot, on cases whose answer "
    "is not in dispute.",
    "Adding the countermechanism test does not improve the accuracy of the "
    "verdicts over omitting it — in which case that step is ceremony, not "
    "method.",
]

# ---------------------------------------------------------------------------
# The worked examples. Deliberately one of each interesting verdict.
# ---------------------------------------------------------------------------

WORKED = [
    {
        "id": "H1/G1",
        "headline": "One control, two properties — the method admitting a "
                    "mismatch",
        "Control name": "FI tolerance group (per-document / per-line amount)",
        "Product, module and release": "S/4HANA on-premise FI — "
                                       "**release unspecified; blocking**",
        "Enforcement point": "document posting",
        "Type": "preventive",
        "Control subject": "one document",
        "Observation boundary": "single action / one principal / instant",
        "Retained state": "none",
        "Local predicate": "document total ≤ limit, and every line ≤ line limit",
        "Property A": "no posting of anomalous value (document-local)",
        "Property B": "cumulative credited value in the period below "
                      "materiality",
        "Who claims them": "both the organisation. Materiality is an audit "
                           "concept defined over a reporting period; neither "
                           "property was authored here",
        "Closure": "A: boundary aligned. B: **not closed** — no per-document "
                   "predicate admitting the legitimate population implies a "
                   "bound on the sum",
        "Audit status": "not-yet-contested (bounded search)",
        "Countermechanism": "tolerance groups, release strategies, org level, "
                            "document type — swept exhaustively. **Availability "
                            "Control was missed and may be fatal**",
        "Verdict": "A holds directly · B cannot discriminate",
        "Result": "A: clean separation, 100% legitimate throughput. "
                  "B: 12,288 configurations, best retains 37.5%, none 95%",
    },
    {
        "id": "H2",
        "headline": "A wider property a local control still guarantees — the "
                    "case that stops the principle degenerating",
        "Control name": "PFCG organisational-level restriction",
        "Product, module and release": "S/4HANA on-premise — unspecified",
        "Enforcement point": "AUTHORITY-CHECK, per action",
        "Type": "preventive",
        "Control subject": "one action against one org unit",
        "Observation boundary": "single action / one principal / instant",
        "Retained state": "none",
        "Local predicate": "the action's org unit is in the grant",
        "Property A": "no part of the workflow touches an org unit outside "
                      "the grant",
        "Property B": "—",
        "Who claims them": "the organisation",
        "Closure": "**closed.** If every out-of-unit action is refused, no "
                   "sequence of permitted actions can leave the unit. The "
                   "property is wider than the boundary and holds anyway",
        "Audit status": "not-yet-contested",
        "Countermechanism": "n/a — the control holds",
        "Verdict": "holds by compositional closure",
        "Result": "all 120 documents refused for the wrong company code",
    },
    {
        "id": "H3/G2",
        "headline": "The method refusing a result because the property was "
                    "ours",
        "Control name": "GRC Access Risk Analysis (static, per principal)",
        "Product, module and release": "GRC Access Control — unspecified",
        "Enforcement point": "offline analysis of role assignments",
        "Type": "detective",
        "Control subject": "one principal's grant set",
        "Observation boundary": "sequence / one principal / period",
        "Retained state": "the grant set",
        "Local predicate": "no principal spans both sides of a conflicting pair",
        "Property A": "no principal holds both sides — **the vendor's own "
                      "stated property**",
        "Property B": "no single decision process completes both sides — "
                      "**ours**",
        "Who claims them": "A: SAP. B: the researcher. That difference is the "
                           "whole finding",
        "Closure": "not applicable to B; the property ranges over principals "
                   "the analysis never considers together",
        "Audit status": "**contested** — keeping property A is defensible and "
                        "is what SAP claims",
        "Countermechanism": "ARA per principal and against the accumulating "
                            "technical user, both tested. SAP Business "
                            "Workflow **not** tested and is process-scoped",
        "Verdict": "A holds directly · B contested specification",
        "Result": "A: the technical user accumulating both grants is flagged. "
                  "B: both propagated principals clean, composition completes "
                  "— published as a proposed property, never as a failure",
    },
    {
        "id": "G3",
        "headline": "The method refusing a result twice",
        "Control name": "Security Audit Log record",
        "Product, module and release": "S/4HANA — unspecified",
        "Enforcement point": "after the fact",
        "Type": "evidentiary",
        "Control subject": "authenticated principal",
        "Observation boundary": "single action / one principal / instant",
        "Retained state": "the log",
        "Local predicate": "record the principal, transaction and time",
        "Property A": "name the accountable principal",
        "Property B": "attribute the action to the entity that SELECTED it",
        "Who claims them": "A: conventional audit practice. B: the researcher",
        "Closure": "not applicable — this is a subject mismatch, and no "
                   "retained history repairs a non-injective map",
        "Audit status": "**contested** — A is a legitimate audit objective",
        "Countermechanism": "**tested, late.** Timing density, session "
                            "identifiers and terminal fields were named in "
                            "the pre-registration, left untried for eight "
                            "days (loss L2), and finally measured in X12: "
                            "retained history changes nothing where no "
                            "recorded field separates the actors, and the "
                            "best accuracy available to any procedure over "
                            "the modelled record equals the do-nothing "
                            "baseline",
        "Verdict": "contested specification",
        "Result": "blocked on two grounds — *contested specification* and "
                  "*countermechanism untested* — one of which has since been "
                  "cleared by doing the work rather than by arguing it away. "
                  "What survives is a bound over one modelled evidence stream "
                  "and a property nobody has agreed on",
    },
]

FIELDS = ["Control name", "Product, module and release", "Enforcement point",
          "Type", "Control subject", "Observation boundary", "Retained state",
          "Local predicate", "Property A", "Property B", "Who claims them",
          "Closure", "Audit status", "Countermechanism", "Verdict", "Result"]


def check() -> list[str]:
    problems = []
    for w in WORKED:
        for f in FIELDS:
            if f not in w or not str(w[f]).strip():
                problems.append("%s: %s is empty" % (w["id"], f))
    # A pair may carry one verdict per property, written "A holds directly ·
    # B cannot discriminate", and a pair may fail on two grounds at once.
    names = {n for n, _ in VERDICTS}
    for w in WORKED:
        for part in w["Verdict"].split(" · "):
            for clause in part.split(" **and** "):
                v = clause.strip()
                for prefix in ("A ", "B "):
                    if v.startswith(prefix):
                        v = v[len(prefix):]
                if v not in names:
                    problems.append("%s: %r is not one of the defined verdicts"
                                    % (w["id"], v))
    # The instrument must be able to refuse. If every worked example holds,
    # the template is a checklist that feels like progress.
    if not any("contested" in w["Verdict"] or "untested" in w["Verdict"]
               for w in WORKED):
        problems.append("no worked example ends in a refusal -- the template "
                        "would read as a form you can pass")
    # Every section must have a one-line gloss for the condensed procedure,
    # except the final classify step which is the verdict table itself.
    for title, _f in SECTIONS:
        if title != "Verdict" and title not in STEP_GLOSS:
            problems.append("section %r has no one-line gloss, so the one-page "
                            "procedure would omit or invent a step" % title)
    # An instrument that states no condition under which it is wrong is not a
    # method, and this project does not get to demand falsifiability of others
    # and skip it here.
    if len(FRAMEWORK_FAILURE) < 3:
        problems.append("the framework states fewer than three conditions "
                        "under which it would be wrong")
    return problems


def one_page():
    """The whole procedure on one page: the steps a reader follows, and the
    verdicts they can reach. Generated from SECTIONS and VERDICTS so it cannot
    disagree with the full instrument beneath it."""
    print("# The Control-Property Review — the procedure in one page")
    print()
    print("*Apply this to one control against one protected property. It takes "
          "minutes, and it is built to return a refusal as readily as a "
          "finding.*")
    print()
    for i, (title, _fields) in enumerate(SECTIONS, 1):
        gloss = STEP_GLOSS.get(title, "")
        print("**Step %d — %s.** %s" % (i, title, gloss))
        print()
    print("**Step %d — classify.** The verdict is one of:" % (len(SECTIONS) + 1))
    print()
    print("| verdict | when |")
    print("|:---|:---|")
    for name, when in VERDICTS:
        print("| **%s** | %s |" % (name, when))
    print()
    print("Four of the seven are refusals. A review that can only conclude "
          "*works* or *failed* cannot tell you that you moved the goalposts, or "
          "that you never tried the obvious countermeasure.")
    print()
    print("## When this review is wrong")
    print()
    print("The instrument makes claims, so it must say what would falsify it. "
          "The Control-Property Review would be inadequate if any of the "
          "following held:")
    print()
    for cond in FRAMEWORK_FAILURE:
        print("- %s" % cond)
        print()
    print("None of these is idle: the first is the open review gate R2, and the "
          "second and fourth are the reasons the specification-sensitivity "
          "audit and the countermechanism test are in the procedure at all.")
    print()
    print("---")
    print()


def blank():
    print("# The Control-Property Review")
    print()
    print("*One control, one protected property, one verdict. Fill it in "
          "before claiming a control failed.*")
    print()
    for title, fields in SECTIONS:
        print("## %s" % title)
        print()
        for f in fields:
            print("- %s" % f)
            print()
    print("## Verdict")
    print()
    print("| verdict | when |")
    print("|:---|:---|")
    for name, when in VERDICTS:
        print("| **%s** | %s |" % (name, when))
    print()
    print("Four of the seven are refusals. That is the point of the "
          "instrument: a review that can only conclude *the control works* or "
          "*the control failed* has no way to tell you that you moved the "
          "goalposts, or that you never tried the obvious countermeasure.")


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   review instrument consistent: %d sections, %d verdicts, "
              "%d worked examples, %d ending in a refusal, %d framework-failure "
              "conditions."
              % (len(SECTIONS), len(VERDICTS), len(WORKED),
                 sum(1 for w in WORKED
                     if "contested" in w["Verdict"] or "untested" in w["Verdict"]),
                 len(FRAMEWORK_FAILURE)))
        return
    one_page()
    blank()
    if "--blank" in sys.argv:
        return
    print()
    print("---")
    print()
    print("# Worked examples")
    print()
    print("Our own four pairs, filled in. One admits a mismatch, one is held "
          "by closure, one is refused because the property was ours, one is "
          "refused twice.")
    print()
    for w in WORKED:
        print("## %s — %s" % (w["id"], w["headline"]))
        print()
        print("| | |")
        print("|:---|:---|")
        for f in FIELDS:
            print("| %s | %s |" % (f, w[f]))
        print()


if __name__ == "__main__":
    main()
