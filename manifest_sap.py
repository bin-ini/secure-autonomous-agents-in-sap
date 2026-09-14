"""
manifest_sap.py -- the state of the second book, and the evidence each chapter
currently rests on.

    python3 manifest_sap.py            # the status table
    python3 manifest_sap.py --check    # refuse to build on an unstated gap

The first book learned this the hard way: it argued for mechanical consistency
between prose and evidence, did not apply the rule to its own metadata, and
opened chapter 9 with "STUB, and it is the largest hole in this paper"
immediately above four completed experiments. So the chapter list, the state of
each chapter and the experiment it rests on live here from the first day rather
than being reconstructed at the end.

One rule is enforced that the first book's manifest did not have: a chapter may
not be marked `measured` unless the experiment it names has a recorded result
in the pre-registration. A chapter cannot cite an experiment that has not
happened.
"""
from __future__ import annotations

import sys

# The previous title was "Where Enterprise Authorization Models Break". It was
# retired for a reason that belongs in the record rather than in a changelog:
# it pre-announced the gap register and said nothing about the held register,
# which makes the
# title itself an instance of the standing conflict of interest documented
# below. A paper whose result is a boundary map should not be named after one
# side of the boundary.
# Third title, and the last. "Where Mature Controls Hold, and Where They Stop"
# was symmetric and still named the wrong protagonist: the contribution is not
# a map of SAP, it is the procedure that decides what belongs on the map. The
# title now asks the question the instrument answers, and it stays true whether
# Availability Control eliminates the SAP-specific gap or converts it into a
# control-placement finding. Held in release.py, which refuses a title that
# asserts breakage.
from release import TITLE as _T, subtitle as _sub  # noqa: E402
TITLE = _T
# "tested against SAP" was in this subtitle while the surface specification's
# own generated verdict said nothing had been verified against a deployed SAP
# mechanism. A paper that enforces consistency between prose and evidence
# everywhere else may not carry that on its cover. It returns only when the
# SAP evidence level in surface.py is genuinely populated.
SUBTITLE = _sub()

# The thesis, fixed before the chapters are written, because it determines what
# chapter 1 has to establish and what the gap register has to prove.
#
# This paper is not a study of SAP. It is a study of whether mature enterprise
# control models remain complete under autonomous action selection. SAP is used
# because it supplies the strongest available counter-argument: four decades of
# deployed, audited enterprise controls. If the same gaps appear there, they
# are unlikely to be explained by immaturity alone.
#
# Two consequences follow, and both change the work:
#
#   Chapter 1 is not scene-setting. It has to establish CASE SELECTION -- that
#   SAP was chosen because it was most likely to refute the claim. A reader who
#   finishes chapter 1 believing SAP was chosen for convenience or familiarity
#   has been given no reason to care about chapters 2 to 5.
#
#   The gap register stops being a courtesy and becomes load-bearing. A paper
#   claiming
#   to have tested the hardest case must demonstrate that the case was hard. A
#   a thin gap register collapses the selection argument and, with it,
#   everything
#   the other chapters are supposed to mean.
THESIS = (
    "Not a study of SAP, and not a list of SAP control gaps. A reproducible "
    "method for mapping where a mature enterprise control set remains valid "
    "under autonomous execution and where the assumptions beneath it stop "
    "holding. SAP is the first completed instance, chosen because four decades "
    "of deployed audited control is the case most likely to refute the claim.")

# What a single instance can and cannot establish. Written down because the
# class-level inference is the one most likely to be quoted beyond its warrant.
INFERENCE = (
    "One completed instance cannot show that immaturity is an insufficient "
    "explanation for anything, and the finding's own bounds say so: no "
    "mechanism has reached SAP evidence level, so what was observed are gaps "
    "in a reconstruction. What one instance CAN show is that those gaps are "
    "derivable from the control-property specifications before any experiment "
    "runs, rather than from a judgement about how mature the surface is. It "
    "cannot establish that other enterprise control environments share them. "
    "That is a replication question, and the method is written to be "
    "replicable precisely because this paper cannot answer it alone.")
# A standing conflict of interest, recorded because it does not go away and
# because it points at exactly one chapter.
#
# Chapter 1's falsification condition is a statement about the FIRST paper: if
# the gaps vanish here, that book's findings were a maturity artefact. The two
# books therefore cannot be independent. They have the same author, and that
# author has an interest in the first one surviving.
#
# The mitigation is not to claim neutrality, which would be false. It is to
# notice that the interest points in a single direction -- towards finding gaps
# -- and therefore towards writing the held register badly. It is where the
# controls held. It is the chapter that damages the first book. It is the one
# the author is motivated to keep short, and it is the one that must be the
# longest and the best sourced.
#
# The second guard is structural and already in place: every result in chapters
# 2 to 4 was produced under a pre-registration written before its own code
# existed, so the individual measurements could not be steered. What could be
# steered is emphasis, and emphasis lives in the held register.
CONFLICT = (
    "This paper's falsification condition is a statement about the first book, "
    "by the same author. The interest points towards finding gaps, and "
    "therefore towards under-writing the held register, which is the control on "
    "that interest, which is why it is load-bearing and why it is the chapter "
    "primary sources are mandatory for."
)

EDITION = "Draft 0.1"
DATE = "31 July 2026"

# THREE STORIES, ONE PAPER -- and the reason it works.
#
# The counterfactual audit left one uncontested gap and two contested ones. The
# obvious response is three papers: the rigorous one, the original one, the
# evidence one. That response is wrong, and the reason is worth stating.
#
# Split apart, each contested story becomes a weak paper. "Static SoD misses a
# composed workflow" is adjacent to published work. "Audit logs should record
# the actor" is obvious. Neither survives alone, because what makes them
# interesting is not the observation but the frame that produced it.
#
# Kept together, they change ROLE rather than status. The paper's contribution
# is a method for deciding whether a control failure is real. G1 is the proof
# the method can produce a positive result. G2 and G3 are the proof it can
# REFUSE one -- and an author publishing the audit that killed two of their own
# three results is the rarest thing in this literature.
#
# So the evidence asymmetry stops being a weakness and becomes the structure.
# The condition, enforced below: G2 and G3 may appear only as demonstrations of
# the method refusing a result. The moment either is presented as a finding,
# the paper is weaker than the three-paper split would have been.
CHAPTERS = [
    ("1", "Why SAP?", "argued", "—",
     "**a falsification chapter, not an overview** — and a **RETROSPECTIVE** "
     "one. If the gaps vanish here the first book's findings were a maturity "
     "artefact; if they remain they are probably structural. The frame was "
     "written after all three of its experiments had run (loss L1), the "
     "experiment that would have tested it prospectively has been moved out of "
     "this paper, and the frame is therefore not load-bearing: it organises "
     "the presentation and is not offered as validated"),

    ("2", "The control-property pair", "argued", "—",
     "**the formal object.** Extent mismatch, subject mismatch, and "
     "compositional closure. H2 is the worked example: its property ranges "
     "over the whole workflow, the control observes one action, and the "
     "control still guarantees it — because the property is closed under the "
     "local predicate. Without that, the principle degenerates into *a broader "
     "property needs a broader control*"),

    ("3", "Story one — one control, two properties", "measured", "X7",
     "**the paper's spine.** The same FI tolerance group against a "
     "document-local property (H1, holds, 100% throughput) and a "
     "period-aggregate one (G1, cannot discriminate, best of 12,288 "
     "configurations retains 37.5%). The only uncontested mismatch in the "
     "paper, because materiality over a reporting period is the organisation's "
     "own property and not one we authored"),

    ("4", "Story two — when the property is ours", "measured", "X8",
     "**the method refusing a result.** H3 holds: per-principal analysis "
     "reports a technical user accumulating both grants. G2 exists only "
     "because we substituted a decision-layer property SAP never claimed. "
     "Published as a proposed property with an open measurement (S0c), never "
     "as a control failure"),

    ("5", "Story three — when the countermechanism was untested", "measured",
     "X9/X12",
     "**the method refusing a result twice over, and then clearing one of the "
     "two refusals by doing the work.** G3 was blocked by rule 3 — the "
     "attribution correlates its own pre-registration named were never tried "
     "— and by a contested property, since accountable principal and deciding "
     "actor are both legitimate audit objectives. X12 tested the correlates "
     "and they do not recover the actor; the bound over any procedure reading "
     "the modelled record equals the do-nothing baseline. The rule-3 block "
     "lifts, the property stays contested, and the gap survives smaller"),

    ("6", "Story four — the prediction that narrowed", "measured", "X11",
     "**the method losing an argument to its own audit.** P1 predicted that "
     "release authorisation cannot see what is released. The audit ruled the "
     "prediction unfairly specified before it was run and required it aimed "
     "at the whole transport-governance surface instead. Respecified and run: "
     "true at the authorisation object, irrelevant at the surface, and "
     "transport leaves the list of open mismatches. What it leaves behind is "
     "H4 and a distinction that cost a retraction to arrive at (loss L6): "
     "where the property outruns the control's extent the exchange rate is "
     "forced by the pair, and where the control reads the property's own "
     "subject it is set by that decision's false-positive rate instead"),

    ("7", "The method, and what it cost", "partial", "X7/X8/X11/X12",
     "the boundary map, the replication protocol, and the honest accounting: "
     "one uncontested gap, two refused, one prediction respecified before "
     "running and then narrowed by its own result, and a class claim that one "
     "instance cannot support"),
]

# What this paper is deliberately not about. Written down because every one of
# these is a thing a reader would expect, and a paper that quietly omits them
# reads as having forgotten rather than having decided.
OUT_OF_SCOPE = [
    ("LLM theory",
     "the results here do not depend on how the planner works, and a chapter "
     "explaining transformers would date faster than anything else in the "
     "paper"),
    ("Prompt-injection surveys",
     "well covered elsewhere, and none of the five experiments needs an "
     "injection: "
     "every harmful action is one the agent was authorised to take"),
    ("AI trends and market sizing",
     "has a shelf life measured in months and is not architecture"),
    ("The future of work",
     "not a security question, and the paper has no evidence about it"),
    ("Regulatory speculation",
     "the first book already carries a chapter on designing against a "
     "standard that does not exist; repeating it here would be padding"),
]

DONE = {"measured", "partial"}


def status_table() -> str:
    out = ["| | Chapter | State | Experiment | Evidence |",
           "|---|---|---|---|---|"]
    for n, t, s, x, e in CHAPTERS:
        out.append("| %s | %s | **%s** | %s | %s |"
                   % (n, t, s, x or "—", e))
    return "\n".join(out)


def check() -> list[str]:
    """A chapter may not claim an experiment that has not produced a result,
    and a contested gap may not be presented as a finding."""
    from prereg_sap import PREREG
    by_id = {p.id: p for p in PREREG}
    problems = []
    for n, t, s, x, _e in CHAPTERS:
        if s == "measured":
            if x is None:
                problems.append("chapter %s is 'measured' and names no "
                                "experiment" % n)
                continue
            for xid in x.split("/"):
                p = by_id.get(xid)
                if p is None:
                    problems.append("chapter %s cites %s, which is not "
                                    "pre-registered" % (n, xid))
                elif not p.status.startswith("RUN"):
                    problems.append("chapter %s is 'measured' but %s has not "
                                    "run (status: %s)" % (n, xid, p.status))
        if s == "stub" and x and by_id.get(x) is None:
            problems.append("chapter %s names %s, which is not pre-registered "
                            "-- write the pre-registration before the chapter"
                            % (n, x))
    # X10 left the register, so chapter 1 must carry the retrospective label.
    # Holding both positions -- the frame needs a prospective test, and that
    # test is not required -- is the defect this check exists to prevent.
    try:
        from prereg_sap import FUTURE, PREREG
        ch1 = [c for c in CHAPTERS if c[0] == "1"][0]
        here = any(x.id == "X10" for x in PREREG)
        future = any(x.id == "X10" for x in FUTURE)
        if future and not here and "RETROSPECTIVE" not in ch1[4]:
            problems.append(
                "X10 has moved to the research programme, so chapter 1's frame "
                "has no prospective test and must be labelled RETROSPECTIVE. "
                "Either label it, or put X10 back and make it a release "
                "blocker -- both positions cannot be held at once.")
        if here and "RETROSPECTIVE" in ch1[4]:
            problems.append(
                "X10 is registered for this paper but chapter 1 is still "
                "labelled retrospective.")
    except Exception as e:                       # noqa: BLE001
        problems.append("could not cross-check the frame label: %s" % e)

    # The three-stories structure only works while the contested stories stay
    # demonstrations of the method. If either is relabelled a measured
    # mismatch, the paper is weaker than the three-paper split would have been.
    try:
        from boundary import GAPS
        from counterfactual import contested
        con = {c.pair for c in contested()}
        for g in GAPS:
            if g.id in con and g.published_as == "measured-mismatch":
                problems.append(
                    "%s is contested but marked 'measured-mismatch'. Chapters "
                    "4 and 5 exist to show the method REFUSING a result; a "
                    "contested gap presented as a finding removes the only "
                    "reason to keep the three stories in one paper." % g.id)
    except Exception as e:                      # noqa: BLE001
        problems.append("could not cross-check the contested gaps: %s" % e)
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        if p:
            print("manifest drift -- %d problem(s):" % len(p), file=sys.stderr)
            for x in p:
                print("  " + x, file=sys.stderr)
            sys.exit(1)
        print("   chapter states match the experiment register.")
        return
    print("# Where this paper stands")
    print()
    print("*%s — %s*" % (TITLE, SUBTITLE))
    print()
    print("*%s, %s.*" % (EDITION, DATE))
    print()
    print("> **%s**" % THESIS)
    print()
    print(status_table())
    print()
    print("## What one instance establishes")
    print()
    print(INFERENCE)
    print()
    print("## Standing conflict of interest")
    print()
    print(CONFLICT)
    print()
    n_meas = len([c for c in CHAPTERS if c[2] == "measured"])
    n_part = len([c for c in CHAPTERS if c[2] == "partial"])
    print("*%d of %d chapters measured, %d partial, %d argued.*"
          % (n_meas, len(CHAPTERS), n_part,
             len([c for c in CHAPTERS if c[2] == "argued"])))
    print()
    print("## Deliberately out of scope")
    print()
    print("| | why |")
    print("|:---|:---|")
    for topic, why in OUT_OF_SCOPE:
        print("| **%s** | %s |" % (topic, why))
    print()
    print("## The blocker")
    print()
    # The blocker used to be named by chapter. It is now named by MECHANISM,
    # because the three-stories restructure distributed the held controls
    # across chapters 2, 3 and 4 and left a chapter reference pointing at a
    # heading that no longer exists -- the third stale cross-reference this
    # project has produced by hardcoding one.
    from surface import MECHANISMS, verdict
    unverified = [x for x in MECHANISMS if x.level != "SAP"]
    print(verdict())
    print()
    print("The dependency is not spread evenly. Chapter 3 is the paper's "
          "spine, and both of its verdicts rest on **M2 — FI tolerance "
          "groups being document-local**. If a tolerance field retains state "
          "across documents, G1 is wrong and the only uncontested gap in the "
          "paper goes with it. Exclusion **E2, the F110 payment program**, is "
          "the other place a cumulative FI limit could plausibly live and has "
          "not been examined at all.")
    print()
    print("Those two are publication-blocking in a way nothing else here is. "
          "%d of %d modelled mechanisms remain unverified against primary "
          "sources, and `help.sap.com` refuses automated retrieval even for "
          "exact document URLs — so this pass cannot be done from inside the "
          "toolchain that produced everything else in this repository."
          % (len(unverified), len(MECHANISMS)))


if __name__ == "__main__":
    main()
