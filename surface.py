"""
surface.py -- the SAP Control Surface Specification.

    python3 surface.py            # the specification
    python3 surface.py --check    # refuse to overstate what was verified

This is the validity foundation of the whole paper, and right now it is mostly
empty. That is the honest state and the file is written so it cannot pretend
otherwise.

The objection this exists to survive is one sentence long: *you did not model
control X*. Because the paper's case-selection argument depends on SAP being the
strongest available counter-example, that objection does not damage one
experiment — it damages the claim that the case was hard, and therefore
everything the other chapters are supposed to mean.

Three things follow, and all three are enforced below.

1. EVERY entry names its product and release scope. "SAP" is not a scope.

2. Every entry carries a LEVEL, and the three levels may not be conflated:

     FORMAL   a result about the shape of the modelled control. True of any
              control with that observation boundary, including ones SAP does
              not have.
     IMPL     a result in our reference implementation. True of our code.
     SAP      a verified claim about a deployed SAP mechanism, with a primary
              source.

   Almost everything in this paper is currently FORMAL or IMPL. The title says
   "tested against SAP"; until some entries reach SAP level, the accurate
   phrase is "tested against a reconstructed SAP authorisation model", and the
   check below prints that verdict rather than leaving it to taste.

3. Every EXCLUSION states why it cannot trivially close a tested gap. An
   exclusion without that argument is an admission, not a scope statement.

`help.sap.com` and `community.sap.com` refuse automated retrieval, including
for exact document URLs. Every SAP-level entry therefore has to be filled by a
human with a browser, and the `source` field is where that citation goes.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

# ---------------------------------------------------------------------------

SCOPE = {
    "product": "**UNSPECIFIED — must be fixed before publication.** The "
               "reconstruction is shaped by S/4HANA on-premise FI and GRC "
               "Access Control, but no release was chosen, and the mechanisms "
               "differ across S/4HANA Cloud, ECC and Business ByDesign.",
    "release": "**UNSPECIFIED.**",
    "date": "31 July 2026",
}

LEVELS = {
    "FORMAL": "a result about the shape of the modelled control",
    "IMPL": "a result in the reference implementation",
    "SAP": "a verified claim about a deployed SAP mechanism, primary-sourced",
}


@dataclass
class Mechanism:
    id: str
    name: str
    modelled_as: str
    fields: str              # exactly what was modelled
    level: str
    source: str              # primary citation, or what is missing
    assumptions: str


@dataclass
class Exclusion:
    id: str
    name: str
    why_excluded: str
    # RULE: an exclusion must argue why it cannot trivially close a tested gap.
    cannot_close: str
    gap_at_risk: str


MECHANISMS = [
    Mechanism(
        "M1", "Authorization objects and AUTHORITY-CHECK",
        "`Authorization.permits()`; per-instance evaluation, no union of field "
        "values across instances",
        "F_BKPF_BUK (BUKRS, ACTVT), F_BKPF_BLA (BRGRU, ACTVT), "
        "F_LFA1_BUK (BUKRS, ACTVT), F_REGU_BUK (BUKRS, ACTVT), "
        "S_TRANSPRT (ACTVT)",
        "IMPL",
        "**No primary source read.** Object names and field semantics from "
        "secondary material. Needs: the authorization object documentation "
        "for each of the five, confirming field lists and check semantics.",
        "That SAP evaluates per instance rather than unioning fields. A union "
        "model is strictly more permissive and would have manufactured "
        "findings, so this assumption is conservative in our favour and still "
        "needs confirming."),

    Mechanism(
        "M2", "FI tolerance groups",
        "`ToleranceGroup.permits()`; per-document and per-line amount ceilings",
        "amount per document, amount per open-item line. Cash-discount "
        "percentage NOT modelled",
        "IMPL",
        "**No primary source read.** Needs: OBA4 documentation confirming "
        "which limits are per user, per company code, and whether any limit "
        "spans documents.",
        "That no tolerance field retains state across documents. **If one "
        "does, G1 is wrong and the gap register loses its principal claim.** This is "
        "the single most damaging thing that could be found in the primary "
        "sources, which is why it is listed first among the assumptions."),

    Mechanism(
        "M3", "GRC Access Risk Analysis",
        "`SodRuleset.violations()`; static predicate over one principal's "
        "grant set",
        "conflicting function pairs, each function a set of "
        "(object, activity)",
        "IMPL",
        "**No primary source read.** Secondary material reports that the "
        "delivered rule list is not exhaustive and that implementing every "
        "delivered rule does not guarantee compliance. That reading supports "
        "the paper's framing, which is a reason to be careful with it: it is "
        "used in the specification-sensitivity audit as independent evidence "
        "for what the vendor claims, and until the primary text is read that "
        "evidence is secondary and the audit entry says so.",
        "That analysis is per principal and static. If ARA offers a "
        "process- or workflow-scoped mode, G2 narrows sharply."),

    Mechanism(
        "M4", "Security Audit Log",
        "`SalLog`; user, transaction, message, terminal",
        "user ID, tcode, message, terminal, timestamp and clock granularity. "
        "Change-document metadata, table logging and read-access logging "
        "remain NOT modelled",
        "IMPL",
        "**No primary source read.** Needs: the SAL field list, and the "
        "change-document schema, to establish what correlates actually exist.",
        "That no MODELLED field distinguishes one actor from another. X12 "
        "tested that assumption rather than resting on it — terminal, "
        "transaction code, clock granularity, session gaps and retention "
        "depth are all swept — and the assumption held: retention changed "
        "nothing where no field separated the actors. Loss L2 is repaired. "
        "What remains unmodelled is the three other evidence streams above, "
        "and a correlate in any of them would narrow G3 further."),

    Mechanism(
        "M5", "Principal propagation (IAS to S/4HANA)",
        "each agent session holds exactly one principal's grants; nothing "
        "persists between sessions but world state",
        "the identity under which an agent-initiated action executes",
        "FORMAL",
        "**No primary source read.** Secondary material indicates Joule runs "
        "under the calling user and respects that user's authorisations. "
        "Needs confirmation, and needs the autonomous/background case, which "
        "may differ.",
        "That the propagated identity carries no marker of having been reached "
        "through an agent. If a marker exists, G3 changes entirely."),

    # X11 measured a surface that had no entry here at all. That is the same
    # defect as the numbering collision rule 5 catches: two artefacts each
    # internally consistent, describing different sets of mechanisms. The
    # count "N of N unverified" implied a completeness the specification did
    # not have.
    Mechanism(
        "M6", "CTS transport release authorisation (S_TRANSPRT, ACTVT 43)",
        "`Cts.release()` and `transport.run_one()` step T1; a predicate over "
        "the principal's grant and the request",
        "the request: owner, target system, request class. NOT the content",
        "IMPL",
        "**No primary source read.** Needs: the S_TRANSPRT field list and "
        "the activities defined for it in the named release.",
        "That release authorisation never inspects the transported objects. "
        "This is the assumption P1 rests on and X11 confirmed against the "
        "model; if a delivered release check reads content, P1 is wrong."),

    Mechanism(
        "M7", "Static check variant at release (ATC / Code Inspector)",
        "`transport.run_one()` step T2; a content-ranging predicate whose "
        "catalogue coverage of the harm class is a SWEPT PARAMETER",
        "the behaviour of a transported object, as matched against a rule "
        "catalogue",
        "FORMAL",
        "**No primary source read, and this is the largest open question in "
        "X11.** Needs: what the delivered check variants actually check, and "
        "whether any rule matches a change that disables a validation exit.",
        "That whether the catalogue carries this harm class is unknown. It is "
        "swept rather than assumed and the results are reported on both "
        "branches; 1,296 of the 2,512 discriminating configurations stop "
        "discriminating without it."),

    Mechanism(
        "M8", "Human review and quality-system exercise before import",
        "`transport.run_one()` steps T3 and T5; content-ranging preventive "
        "decisions whose coverage and false-positive rate are SWEPT",
        "the content of the change, and the behaviour of the change when "
        "exercised",
        "FORMAL",
        "Not a product mechanism and no primary source is possible. These are "
        "organisational practices the transport system creates a place for, "
        "and modelling them as steps with parameters rather than as "
        "guarantees is the only honest option.",
        "That neither coverage nor false-positive rate is a property of the "
        "system. Loss L6 records what happened when the false-positive "
        "channel was left out of the model entirely."),

    Mechanism(
        "M9", "Post-import comparison against the reviewed baseline",
        "`transport.run_one()` step T6; content-ranging and detective",
        "the transported object, after it is active in production",
        "FORMAL",
        "Not verified. Included so the experiment can distinguish 'no "
        "content-ranging decision exists' from 'none of them is preventive'.",
        "That a detective content check does not prevent. Trivially true of "
        "the model; the point of measuring it is that 40 of 40 flagged and "
        "40 of 40 in production is the cleanest statement of the "
        "preventive/detective distinction the paper has."),
]


EXCLUSIONS = [
    Exclusion(
        "E1", "Purchasing release strategies",
        "Modelled only as a per-document value threshold, not as the full "
        "release-code and release-group machinery.",
        "Release strategies are evaluated per purchasing document. Whatever "
        "the code structure, the predicate's observation boundary is one "
        "document, so by the mismatch principle it cannot range over a "
        "period-level aggregate. Modelling the machinery in full would change "
        "the fidelity and not the verdict — **unless** a release strategy can "
        "be driven by a cumulative value, which is the thing to check.",
        "G1"),

    Exclusion(
        "E2", "Payment program (F110) limits",
        "Not modelled at all.",
        "**This exclusion is not yet defensible.** The payment program is the "
        "most plausible location for a genuinely cumulative limit in FI, and "
        "if one exists that binds per run or per period, it is a direct "
        "counter-example to G1. Listed here so it cannot be quietly forgotten.",
        "G1"),

    Exclusion(
        "E6", "Availability Control (Funds Management / Budget Control System)",
        "Not modelled, and **not previously known to us**. Surfaced by the "
        "reviewer's primary-source pass, not by ours.",
        "**This is the most consequential exclusion in the file and it may not "
        "survive as one.** Availability Control evaluates total consumption "
        "against a consumable budget per control object and can refuse a "
        "posting when a configured threshold is exceeded. That is aggregate "
        "state, held at the decision point, enforced preventively — which is "
        "precisely the shape G1 asserts the authorisation surface does not "
        "carry, and precisely the control X7 proposed as the repair.\n\n"
        "It does not automatically defeat G1, because the question is whether "
        "AVC binds the FI credit-memo path, control object and product scope "
        "we model. But it destroys a framing the paper was carrying: **the "
        "cumulative control is not missing from SAP.** It exists, in another "
        "module, and is not on the path we tested. That is a better claim and "
        "a narrower one, and it must replace any sentence implying SAP lacks "
        "aggregate-state enforcement.",
        "G1 — and the repair argument that rests on it"),

    Exclusion(
        "E3", "SAP Enterprise Threat Detection / behavioural monitoring",
        "Not modelled; the paper studies authorisation, not detection.",
        "Detection systems hold aggregate state by construction, so they do "
        "not refute G1 — they relocate it. The paper's claim is that the "
        "AUTHORISATION surface cannot express the constraint, and that the "
        "enterprise's aggregate-state machinery sits in a detection layer not "
        "wired to the authorisation decision. That relocation is the argument "
        "of the gap register and must be made explicitly rather than by omission.",
        "G1"),

    Exclusion(
        "E4", "Firefighter / Emergency Access Management",
        "Not modelled.",
        "EAM's control is review of a logged elevated session. Review is a "
        "detective control over a session, so it does not close G1 or G2 "
        "preventively — but it is a real mechanism a practitioner would cite, "
        "and 'volume defeats review' is currently an assertion in this paper "
        "rather than a measurement.",
        "G1, G2"),

    Exclusion(
        "E5", "Workflow (SAP Business Workflow) approval steps",
        "Not modelled.",
        "**This exclusion is weak.** Workflow is the one SAP mechanism whose "
        "observation unit is the PROCESS rather than the document or the "
        "principal, which by the mismatch principle makes it the strongest "
        "candidate to close G2. It should be modelled before G2 is published.",
        "G2"),
]


def check() -> list[str]:
    problems = []
    for m in MECHANISMS:
        if m.level not in LEVELS:
            problems.append("%s: unknown level %r" % (m.id, m.level))
        if not m.source.strip():
            problems.append("%s: no source and no statement of what is "
                            "missing" % m.id)
        if m.level == "SAP" and "No primary source" in m.source:
            problems.append("%s: claims SAP level with no primary source"
                            % m.id)
    for e in EXCLUSIONS:
        if not e.cannot_close.strip():
            problems.append("%s: excluded with no argument that it cannot "
                            "close a tested gap" % e.id)
    if "UNSPECIFIED" in SCOPE["product"] and any(
            m.level == "SAP" for m in MECHANISMS):
        problems.append("a SAP-level claim exists but no product or release "
                        "scope has been fixed")
    return problems


def verdict() -> str:
    n_sap = sum(1 for m in MECHANISMS if m.level == "SAP")
    if n_sap == 0:
        return ("**Nothing in this paper is yet verified against a deployed "
                "SAP mechanism.** The accurate description of the work is "
                "*tested against a reconstructed SAP authorisation model*, "
                "not *tested against SAP*. The subtitle says exactly that "
                "and is computed from the release state rather than chosen, "
                "so it changes by itself when at least M2 and M4 reach SAP "
                "level.")
    return ("%d of %d mechanisms verified against primary sources."
            % (n_sap, len(MECHANISMS)))


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   surface spec consistent: %d mechanisms, %d exclusions, "
              "%d verified against SAP."
              % (len(MECHANISMS), len(EXCLUSIONS),
                 sum(1 for m in MECHANISMS if m.level == "SAP")))
        return

    print("# SAP Control Surface Specification")
    print()
    print("*Generated by `python3 surface.py`. The validity foundation of the "
          "paper, and currently its weakest artefact.*")
    print()
    print("| | |")
    print("|:---|:---|")
    for k, v in SCOPE.items():
        print("| %s | %s |" % (k, v))
    print()
    print("> %s" % verdict())
    print()
    print("## Levels")
    print()
    print("| level | meaning |")
    print("|:---|:---|")
    for k, v in LEVELS.items():
        print("| **%s** | %s |" % (k, v))
    print()
    print("## Mechanisms modelled")
    print()
    for m in MECHANISMS:
        print("### %s — %s  *(%s)*" % (m.id, m.name, m.level))
        print()
        print("| | |")
        print("|:---|:---|")
        print("| modelled as | %s |" % m.modelled_as)
        print("| fields modelled | %s |" % m.fields)
        print("| primary source | %s |" % m.source)
        print("| load-bearing assumption | %s |" % m.assumptions)
        print()
    print("## Mechanisms excluded")
    print()
    _weak = [e for e in EXCLUSIONS
             if any(w in (e.cannot_close + e.why_excluded).lower() for w in
                    ("not yet defensible", "weak", "may not survive"))]
    print("An exclusion must argue why it cannot trivially close a tested "
          "gap. %d below cannot yet make that argument, and say so: %s."
          % (len(_weak), ", ".join(e.id for e in _weak)))
    print()
    for e in EXCLUSIONS:
        print("### %s — %s  *(puts %s at risk)*" % (e.id, e.name, e.gap_at_risk))
        print()
        print("*Excluded because:* %s" % e.why_excluded)
        print()
        print("*Why it cannot trivially close the gap:* %s" % e.cannot_close)
        print()


if __name__ == "__main__":
    main()
