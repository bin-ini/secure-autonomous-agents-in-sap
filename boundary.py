"""
boundary.py -- the boundary map: controls that held, and gaps that survived.

    python3 boundary.py            # the map
    python3 boundary.py --check    # enforce the four rules on the held register

This file exists because the held register is the part the author is motivated to
write badly. The standing conflict is recorded in the manifest: this paper's
falsification condition is a statement about the first book, by the same
author, and the interest points towards finding gaps. Emphasis is the one thing
pre-registration cannot protect, and emphasis is the held register.

So the protection is mechanical rather than intentional. Five rules, all
checked, and all printed into the generated artefact so that a reference to
"rule 3" resolves for a reader who has only the paper:

  RULE 1  Parity of resolution. A control that held must be reported at the
          same evidentiary depth as a control that failed. Enforced by
          comparing the two registers and failing when the held register is
          materially thinner.

  RULE 2  Every success carries its architectural interpretation. Not "SAP
          blocked this" but "a mature control already governs the variable the
          autonomous sequence tried to create harm on." That is what lets
          the held register refine the first book instead of flattering SAP.

  RULE 3  A gap may not enter the gap register until the strongest existing
          a practitioner would reasonably claim closes it has been named AND
          tested. Enforced: `admissible` is False unless
          `strongest_alternative_tested` is True.

  RULE 4  "Not found" is not "does not exist". Every record carries one of six
          evidence statuses and the two are different values.

  RULE 5  The registers are named, never numbered. Added after the two of them
          were referred to by chapter number in twenty-nine places while the
          chapter table gave those numbers to two different chapters.

Rule 3 found a hole in our own work the first time it ran. See G3.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# RULE 4 -- the six statuses. "not found" and "confirmed absent" are different
# values because collapsing them is the most available dishonesty in this paper.
# ---------------------------------------------------------------------------

STATUS = {
    "present_and_tested":
        "present in the control surface and exercised by an experiment",
    "present_not_representable":
        "present, but not representable in the current testbed",
    "primary_untested":
        "located in primary vendor documentation, not tested",
    "secondary_only":
        "found only in secondary material; no primary source read",
    "not_found":
        "not found in the reviewed control surface — **this is a statement "
        "about our review, not about SAP**",
    "confirmed_absent":
        "confirmed absent within a stated product and version scope",
}

# Where in the sequence a control intervenes. Recorded because "it blocked the
# attack" hides the difference between refusing an action and noticing a
# consequence afterwards.
STAGE = ("plan", "grant", "action", "flow", "persistence", "consequence")


@dataclass
class Held:
    """A control that held. Every field is required; see RULE 1."""
    id: str
    control: str
    failure_definition: str      # defined independently of the control
    strongest_attack: str
    mechanism: str               # the exact thing that blocked it
    stage: str                   # one of STAGE
    config_assumptions: str
    operational_cost: str
    boundary: str                # where the result stops generalising
    interpretation: str          # RULE 2
    status: str                  # RULE 4
    reproduce: str               # how a reader re-runs it

    def words(self) -> int:
        return sum(len(getattr(self, f).split()) for f in
                   ("failure_definition", "strongest_attack", "mechanism",
                    "config_assumptions", "operational_cost", "boundary",
                    "interpretation"))


RULES = [
    (1, "**Parity of resolution.** A control that held must be reported at "
        "the same evidentiary depth as a control that failed.",
        "the two registers' mean evidence length is compared, and the build "
        "fails when the held register is materially thinner"),
    (2, "**Every success carries its architectural interpretation.** Not "
        "*this control blocked it* but *a control already governs the "
        "variable the autonomous sequence tried to create harm on* — which "
        "is what lets the held register refine the first book rather than "
        "flatter the vendor.",
        "an interpretation shorter than twenty-five words is rejected as a "
        "summary"),
    (3, "**A gap may not be published until the strongest existing "
        "countermechanism a practitioner would reasonably claim closes it "
        "has been named AND tested.**",
        "`admissible` is false unless `strongest_alternative_tested` is "
        "true; this rule blocked G3 for eight days"),
    (4, "**\"Not found\" is not \"does not exist\".** Every record carries "
        "one of six evidence statuses and those two are different values.",
        "an unknown status fails the build"),
    (5, "**The registers are named, never numbered.**",
        "no source may refer to the held or gap register by chapter number; "
        "that numbering collided with the chapter table once and no check "
        "could see it"),
]


@dataclass
class Gap:
    """A gap that survived. May not enter the gap register unless RULE 3 is met."""
    id: str
    gap: str
    experiment: str
    strongest_alternative: str          # what a practitioner would claim
    strongest_alternative_tested: bool  # RULE 3
    result: str
    status: str
    boundary: str
    note: str = ""
    # How the gap may be presented. A gap whose specification survives the
    # counterfactual audit may be published as a measured mismatch. One whose
    # alternative specification is defensible may only be published as a formal
    # result about a property the paper still has to argue for.
    published_as: str = "measured-mismatch"

    @property
    def admissible(self) -> bool:
        return self.strongest_alternative_tested

    def words(self) -> int:
        return sum(len(getattr(self, f).split()) for f in
                   ("gap", "strongest_alternative", "result", "boundary"))


# ---------------------------------------------------------------------------
# Controls that held
# ---------------------------------------------------------------------------

HELD = [
    Held(
        "H1", "FI tolerance groups (per-document and per-line amount limits)",
        "A fraudulent posting whose value lies outside the range of ordinary "
        "business for the principal making it.",
        "400 credit memos of 20,000-50,000 each, interleaved with the "
        "legitimate workload in a single agent session — 1.2m of harm against "
        "a materiality threshold of 500,000.",
        "`ToleranceGroup.amount_per_document` and `amount_per_line`, evaluated "
        "per user per company code, refusing the document before it posts.",
        "action",
        "The limit must actually be set. The sweep's default of unbounded "
        "blocks nothing, and an unbounded tolerance group is a configuration a "
        "practitioner would recognise as wrong — which is the point: this "
        "control works and is routinely left open.",
        "None measured. 100% of the legitimate workload posted with the "
        "separating configuration in place.",
        "Holds only while the harmful amounts lie outside the legitimate "
        "distribution. When the two overlap, the same mechanism at its best "
        "setting retains 37.5% of legitimate throughput (X7). The control is "
        "not weak; the variable it ranges over stops matching the harm.",
        "In the modelled surface a control already governs the variable — "
        "document value — on which this autonomous sequence attempted to "
        "create harm, and no new security object is required for value-based "
        "fraud there. Whether the deployed mechanism has the same shape is "
        "the open question M2 names. What agents change is not whether value "
        "is governed but whether value is the variable the harm is expressed "
        "in.",
        "secondary_only",
        "`python3 verify.py` — the mutation test neuters "
        "`ToleranceGroup.permits` and the positive control stops separating.",
    ),

    Held(
        "H2", "PFCG organisational-level restriction (AUTHORITY-CHECK)",
        "An action taken against an organisational unit outside the authority "
        "the task was granted.",
        "The full legitimate workload posted into company code 1000 by a "
        "principal authorised only for 2000.",
        "`AUTHORITY-CHECK` on `F_BKPF_BUK`, evaluated per authorisation "
        "INSTANCE rather than by unioning field values across instances.",
        "action",
        "The per-instance semantics are load-bearing and easy to model wrongly. "
        "A union model — passing if BUKRS is permitted somewhere and ACTVT is "
        "permitted somewhere — is strictly more permissive than SAP and would "
        "have manufactured a finding. Tested explicitly.",
        "None. Zero legitimate documents refused.",
        "Ranges over the organisational unit and the activity. Says nothing "
        "about volume, sequence, or content, and is not weakened by agents in "
        "any way we could construct.",
        "This is the control the first book models as C2 and C10 together, "
        "and the modelled version is finer than either. Where the first book "
        "found verb-level scope insufficient and resource-level scope "
        "necessary, the reconstructed surface carries resource-level scope as "
        "a matter of course. That is a first-book recommendation arriving as "
        "a solved problem — in the reconstruction — and the held register "
        "should say so plainly.",
        "secondary_only",
        "`python3 verify.py` — neutering `Authorization.permits` unblocks the "
        "wrong company code; the real check blocks all 120 documents.",
    ),

    Held(
        "H3", "GRC Access Risk Analysis against an accumulating principal",
        "A single principal holding both sides of a conflicting duty pair.",
        "A technical user, `RFC_AGENT`, holding the AP clerk's vendor-master "
        "grant and treasury's payment-run grant simultaneously — the "
        "configuration an autonomous background agent most naturally gets.",
        "A static predicate over role assignments, evaluated per principal "
        "against a ruleset of conflicting function pairs.",
        "grant",
        "The ruleset must contain the pair, and the analysis must actually be "
        "run against technical and communication users. Secondary sources "
        "suggest those principals frequently do not appear as distinct "
        "identities in access-risk tooling, which makes this an assumption "
        "worth stating rather than a given.",
        "None at runtime; it is an offline analysis.",
        "Holds only where grants accumulate on one principal. X8 shows it does "
        "not see the same conflict composed across two propagated principals — "
        "so the control is correct and its scope is narrower than the harm.",
        "The counter-intuitive result, and the one the held register exists to protect: "
        "the architecture that looks worse on every checklist — a technical "
        "user hoarding grants — is the one the modelled control can see. "
        "Principal propagation, which any reviewer would prefer, is the one it "
        "cannot. A control is only as good as the shape of the principal it "
        "was designed to read.",
        "secondary_only",
        "`python3 verify.py` — the technical-user arm must be flagged, or the "
        "ruleset is inert and X8 proves nothing.",
    ),

    Held(
        "H4", "Content-ranging steps of the transport-governance surface "
        "(static check variant, peer review, quality-system exercise)",
        "A transport whose released objects change system behaviour in a way "
        "nobody authorised — here, a change to an FI validation exit that "
        "stops the tolerance predicate firing for a document class, which is "
        "the control this paper's own principal finding depends on.",
        "Forty harmful transports made identical at request level to forty "
        "legitimate ones: same owner, same target, same request class, same "
        "object types, same object count, same naming shape. The only "
        "difference is what an object does once it is active, which is the "
        "one thing a request-level predicate cannot read. The condition is "
        "enforced in code by `assert_transport_indistinguishable()`.",
        "A predicate evaluated against the transported objects themselves — "
        "a static check catalogue matching the object's content, a human "
        "reading the change, or a functional exercise of the affected path in "
        "the quality system before the production import.",
        "action",
        "Two assumptions, and the experiment refuses to hide either. The "
        "static check discriminates only if its catalogue contains a rule for "
        "this harm class, which is unverified for delivered SAP check "
        "variants and is swept as a parameter rather than assumed. Human "
        "review and quality-system exercise discriminate only in proportion "
        "to the coverage a team actually achieves, which no mechanism "
        "guarantees and which is therefore also swept.",
        "Not measurable from this model, and the attempt to report it as "
        "measured is loss L6. Cost here is set entirely by the rate at which "
        "a content step stops a benign transport, which is a swept parameter "
        "with no measured value: at five percent the surface still clears the "
        "95% bar X7 was held to and at ten percent nothing does. What the "
        "contrast with X7 establishes is a difference in KIND rather than in "
        "price — an extent mismatch makes the exchange rate a property of the "
        "control-property pair that no implementation can improve, while a "
        "subject match makes it a property of the implementation.",
        "Holds against the behavioural property. Against the narrower "
        "property that released code conforms to the change request that was "
        "approved, only the human steps retain the subject match — a "
        "pattern-matching catalogue cannot read a change request. That "
        "alternative specification is defensible and the pair is recorded as "
        "contested for exactly that reason.",
        "The result is close to definitional and is reported that way: a "
        "control that reads the property's own subject is not a surprising "
        "thing to find sufficient. What earns it a place is the contrast one "
        "step away. In the 800 configurations whose active steps range only "
        "over the request — release authorisation, approval — not one "
        "discriminates and all forty harmful transports reach production in "
        "every single one, at every setting of every parameter. Two decisions "
        "in the same governance surface, taken minutes apart by the same "
        "organisation, and only one of them is about the thing the property "
        "is about.",
        "secondary_only",
        "`python3 -c \"from sapsec.experiments import x11; r=x11(); "
        "print(r['n_discriminating'], r['request_only_discriminating'])\"` "
        "— 2512 and 0.",
    ),
]

# ---------------------------------------------------------------------------
# Gaps that survived
# ---------------------------------------------------------------------------

GAPS = [
    Gap(
        "G1",
        "An aggregate outcome produced by individually-authorised actions that "
        "are per-document indistinguishable from legitimate work.",
        "X7",
        "FI tolerance groups, purchasing release strategies, organisational "
        "level, document-type authorisation group — every value-carrying and "
        "scope-carrying mechanism we could identify, swept exhaustively.",
        True,
        "12,288 configurations. 10,398 hold the outcome below materiality; the "
        "best retains 37.5% of legitimate throughput and none retains 95%. The "
        "surface can throttle; it cannot discriminate.",
        "secondary_only",
        "Not a claim that SAP is insecure — a claim about where the control has "
        "to live. If SAP holds a per-principal cumulative mechanism we did not "
        "model, this result is about our model and is withdrawn.",
    ),

    Gap(
        "G2",
        "A duty conflict composed across two principals by one agent, where "
        "each principal is individually clean.",
        "X8",
        "Access Risk Analysis run per principal, and run against the technical "
        "user that would accumulate both grants.",
        True,
        "Both propagated principals clean; the composition completes; the "
        "technical-user variant IS flagged, which confirms the ruleset is not "
        "inert. The harm is pre-existing — two colluding humans produce it "
        "identically — so agents change the price, not the possibility.",
        "secondary_only",
        "Close to definitional and reported as such. The contribution is the "
        "location of the assumption, not a bypass. **The specification is "
        "contested**: SAP's delivered SoD control claims to detect conflicting "
        "access assigned to a user, and against that property it holds (H3). "
        "G2 exists because we substituted a decision-layer property the vendor "
        "never claimed, which is an argument the paper owes rather than a "
        "measurement it has.",
        published_as="formal-result-pending-argument",
    ),

    Gap(
        "G3",
        "Attribution of an action to a human or to an agent, from the evidence "
        "layer alone.",
        "X9",
        "The Security Audit Log's own correlates: terminal field, session "
        "identifier, timing density, and whatever change-document metadata "
        "carries alongside the user ID.",
        True,
        "**Tested in X12, which repairs loss L2.** 512 conditions over "
        "concurrent actors behind one propagated principal. Retention depth "
        "changed nothing in any of the 18 condition groups where no recorded "
        "field separated the actors, and the best accuracy reached in any of "
        "them is chance. Every condition that did attribute had a field that "
        "names the origin. For the practitioner's actual objection — an agent "
        "posting hundreds of documents in minutes is obviously not a person — "
        "the upper bound on ANY procedure reading principal, transaction, "
        "terminal and timestamp equals the accuracy of naming the busiest "
        "actor for every record without reading anything, at every agent "
        "action rate tested. The density signal establishes that machine-speed "
        "activity occurred. It attributes no individual action.",
        "not_found",
        "The rule-3 block is lifted and the gap is smaller than it was. What "
        "survives is a bound over one modelled evidence stream, not a claim "
        "about SAP's audit capability: change documents, table logging and "
        "read-access logging were not modelled, and a correlate in one of them "
        "would narrow this further. The honest status of an actor field "
        "remains 'not found by us', not 'absent'. **The property is still "
        "contested** — an audit trail that names the accountable principal may "
        "be doing exactly what audit trails are for, and the argument that "
        "autonomous mediation broke the assumption that made accountable and "
        "deciding the same entity is one the paper owes rather than has.",
        published_as="formal-result-pending-argument",
    ),
]


# ---------------------------------------------------------------------------
# The checks
# ---------------------------------------------------------------------------

def check() -> list[str]:
    problems = []

    for h in HELD:
        if h.stage not in STAGE:
            problems.append("%s: stage %r is not one of %s"
                            % (h.id, h.stage, ", ".join(STAGE)))
        if h.status not in STATUS:
            problems.append("%s: unknown evidence status %r" % (h.id, h.status))
        for f in ("failure_definition", "strongest_attack", "mechanism",
                  "config_assumptions", "operational_cost", "boundary",
                  "interpretation", "reproduce"):
            if not getattr(h, f).strip():
                problems.append("%s: %s is empty" % (h.id, f))
        # RULE 2, mechanically: an interpretation that only says the control
        # worked is not an interpretation.
        if h.words() and len(h.interpretation.split()) < 25:
            problems.append("%s: interpretation is a summary, not an "
                            "architectural reading (RULE 2)" % h.id)

    for g in GAPS:
        if g.status not in STATUS:
            problems.append("%s: unknown evidence status %r" % (g.id, g.status))
        # RULE 3
        if not g.strongest_alternative.strip():
            problems.append("%s: no strongest existing mechanism named "
                            "(RULE 3)" % g.id)

    # RULE 1 -- parity of resolution. The comparison is deliberately crude and
    # deliberately mechanical: the failure mode is a held control summarised in
    # two paragraphs beside a gap given twenty pages, and a word count catches
    # exactly that.
    if HELD and GAPS:
        h_mean = sum(x.words() for x in HELD) / len(HELD)
        g_mean = sum(x.words() for x in GAPS) / len(GAPS)
        if h_mean < 0.8 * g_mean:
            problems.append(
                "RULE 1: controls that held average %.0f words of evidence "
                "against %.0f for gaps. The held register is being under-written, "
                "which is precisely the direction the standing conflict of "
                "interest predicts." % (h_mean, g_mean))
    # RULE 5 -- the registers are named, never numbered.
    #
    # For most of this project's life the held record and the gap record were
    # referred to by chapter number in twenty-nine places across five modules,
    # while `manifest_sap.CHAPTERS` gave those same two numbers to "Story
    # three" and "The method". Both schemes were internally consistent and they
    # were not the same scheme. Nothing caught it, because every check here
    # compares generated text against a source, and both texts were generated
    # correctly from their own sources. A collision between two correct sources
    # is invisible to that whole family of checks.
    import glob
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    forbidden = ["chapter " + n for n in ("5", "6")]
    for f in sorted(glob.glob(os.path.join(here, "*.py"))):
        low = open(f).read().lower()
        for phrase in forbidden:
            if phrase in low:
                problems.append(
                    "%s refers to %r. The held and gap registers are named, "
                    "not numbered: that numbering collided with "
                    "manifest_sap.CHAPTERS once and no check could see it."
                    % (os.path.basename(f), phrase))
    return problems


def inadmissible() -> list[Gap]:
    return [g for g in GAPS if not g.admissible]


def _contested_ids():
    try:
        from counterfactual import contested
        return {c.pair for c in contested()}
    except Exception:
        return set()


def main():
    if "--check" in sys.argv:
        p = check()
        # A gap whose specification is contested may not be published as a
        # measured mismatch. This is a second gate on top of rule 3, and it
        # blocks a different gap: rule 3 stopped G3 for lack of testing, this
        # stops G2 for having substituted a property the vendor never claimed.
        for g in GAPS:
            if (g.id in _contested_ids()
                    and g.published_as == "measured-mismatch"):
                p.append("%s: its specification is CONTESTED (see "
                         "counterfactual.py) but it is still marked "
                         "'measured-mismatch'. A contested gap may only be "
                         "published as a formal result about a property the "
                         "paper argues for." % g.id)
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        h_mean = sum(x.words() for x in HELD) / len(HELD)
        g_mean = sum(x.words() for x in GAPS) / len(GAPS)
        print("   boundary map consistent: %d held, %d gaps, %d gap(s) "
              "blocked from the gap register by rule 3." % (len(HELD), len(GAPS),
                                                     len(inadmissible())))
        print("   resolution parity: %.0f words per held control, %.0f per "
              "gap." % (h_mean, g_mean))
        return

    print("# The boundary map")
    print()
    print("*Generated by `python3 boundary.py`. Where a reconstruction of "
          "four decades of deployed "
          "control engineering absorbed autonomous execution without needing a "
          "new security object, and where it did not.*")
    print()
    print("## The five rules")
    print()
    print("Referred to by number elsewhere in this paper, and printed here so "
          "the reference resolves. Every one of them is checked by the "
          "build.")
    print()
    print("| | rule | how it is enforced |")
    print("|:--|:---|:---|")
    for n, rule, how in RULES:
        print("| **%d** | %s | %s |" % (n, rule, how))
    print()

    print("## Controls that held")
    print()
    _con = _contested_ids()
    for h in HELD:
        mark = " — **CONTESTED SPECIFICATION**" if h.id in _con else ""
        print("### %s — %s%s" % (h.id, h.control, mark))
        print()
        print("| | |")
        print("|:---|:---|")
        print("| failure definition | %s |" % h.failure_definition)
        print("| strongest attack attempted | %s |" % h.strongest_attack)
        print("| mechanism that blocked it | %s |" % h.mechanism)
        print("| intervenes at | **%s** |" % h.stage)
        print("| configuration assumptions | %s |" % h.config_assumptions)
        print("| operational cost | %s |" % h.operational_cost)
        print("| generalisation boundary | %s |" % h.boundary)
        print("| evidence status | *%s* |" % STATUS[h.status])
        print("| reproduce | %s |" % h.reproduce)
        print()
        print("**What the success means.** %s" % h.interpretation)
        print()

    print("## Gaps that survived")
    print()
    print("A gap may not appear here until the strongest existing mechanism a "
          "practitioner would reasonably claim closes it has been named *and* "
          "tested.")
    print()
    for g in GAPS:
        mark = "" if g.admissible else " — **BLOCKED BY RULE 3**"
        if g.published_as != "measured-mismatch":
            mark += " — **CONTESTED SPECIFICATION**"
        print("### %s%s" % (g.id, mark))
        print()
        print("| | |")
        print("|:---|:---|")
        print("| gap | %s |" % g.gap)
        print("| experiment | %s |" % g.experiment)
        print("| strongest existing mechanism | %s |" % g.strongest_alternative)
        print("| was it tested? | **%s** |"
              % ("yes" if g.strongest_alternative_tested else "**NO**"))
        print("| result | %s |" % g.result)
        print("| evidence status | *%s* |" % STATUS[g.status])
        print()
        if g.note:
            print("> %s" % g.note)
            print()

    bad = inadmissible()
    print("---")
    print()
    print("*%d controls held (%d contested), %d gaps recorded, %d blocked from the gap register "
          "because the strongest existing mechanism has not been tested: %s.*"
          % (len(HELD), len([h for h in HELD if h.id in _contested_ids()]),
             len(GAPS), len(bad),
             ", ".join(g.id for g in bad) or "none"))


if __name__ == "__main__":
    main()
