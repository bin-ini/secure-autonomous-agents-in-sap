# Where this paper stands

*Secure Autonomous Agents in SAP Systems — A Control-Property Review Evaluated on a Reconstructed SAP FI Authorization Model*

*Draft 0.1, 31 July 2026.*

> **Not a study of SAP, and not a list of SAP control gaps. A reproducible method for mapping where a mature enterprise control set remains valid under autonomous execution and where the assumptions beneath it stop holding. SAP is the first completed instance, chosen because four decades of deployed audited control is the case most likely to refute the claim.**

| | Chapter | State | Experiment | Evidence |
|---|---|---|---|---|
| 1 | Why SAP? | **argued** | — | **a falsification chapter, not an overview** — and a **RETROSPECTIVE** one. If the gaps vanish here the first book's findings were a maturity artefact; if they remain they are probably structural. The frame was written after all three of its experiments had run (loss L1), the experiment that would have tested it prospectively has been moved out of this paper, and the frame is therefore not load-bearing: it organises the presentation and is not offered as validated |
| 2 | The control-property pair | **argued** | — | **the formal object.** Extent mismatch, subject mismatch, and compositional closure. H2 is the worked example: its property ranges over the whole workflow, the control observes one action, and the control still guarantees it — because the property is closed under the local predicate. Without that, the principle degenerates into *a broader property needs a broader control* |
| 3 | Story one — one control, two properties | **measured** | X7 | **the paper's spine.** The same FI tolerance group against a document-local property (H1, holds, 100% throughput) and a period-aggregate one (G1, cannot discriminate, best of 12,288 configurations retains 37.5%). The only uncontested mismatch in the paper, because materiality over a reporting period is the organisation's own property and not one we authored |
| 4 | Story two — when the property is ours | **measured** | X8 | **the method refusing a result.** H3 holds: per-principal analysis reports a technical user accumulating both grants. G2 exists only because we substituted a decision-layer property SAP never claimed. Published as a proposed property with an open measurement (S0c), never as a control failure |
| 5 | Story three — when the countermechanism was untested | **measured** | X9/X12 | **the method refusing a result twice over, and then clearing one of the two refusals by doing the work.** G3 was blocked by rule 3 — the attribution correlates its own pre-registration named were never tried — and by a contested property, since accountable principal and deciding actor are both legitimate audit objectives. X12 tested the correlates and they do not recover the actor; the bound over any procedure reading the modelled record equals the do-nothing baseline. The rule-3 block lifts, the property stays contested, and the gap survives smaller |
| 6 | Story four — the prediction that narrowed | **measured** | X11 | **the method losing an argument to its own audit.** P1 predicted that release authorisation cannot see what is released. The audit ruled the prediction unfairly specified before it was run and required it aimed at the whole transport-governance surface instead. Respecified and run: true at the authorisation object, irrelevant at the surface, and transport leaves the list of open mismatches. What it leaves behind is H4 and a distinction that cost a retraction to arrive at (loss L6): where the property outruns the control's extent the exchange rate is forced by the pair, and where the control reads the property's own subject it is set by that decision's false-positive rate instead |
| 7 | The method, and what it cost | **partial** | X7/X8/X11/X12 | the boundary map, the replication protocol, and the honest accounting: one uncontested gap, two refused, one prediction respecified before running and then narrowed by its own result, and a class claim that one instance cannot support |

## What one instance establishes

One completed instance cannot show that immaturity is an insufficient explanation for anything, and the finding's own bounds say so: no mechanism has reached SAP evidence level, so what was observed are gaps in a reconstruction. What one instance CAN show is that those gaps are derivable from the control-property specifications before any experiment runs, rather than from a judgement about how mature the surface is. It cannot establish that other enterprise control environments share them. That is a replication question, and the method is written to be replicable precisely because this paper cannot answer it alone.

## Standing conflict of interest

This paper's falsification condition is a statement about the first book, by the same author. The interest points towards finding gaps, and therefore towards under-writing the held register, which is the control on that interest, which is why it is load-bearing and why it is the chapter primary sources are mandatory for.

*4 of 7 chapters measured, 1 partial, 2 argued.*

## Deliberately out of scope

| | why |
|:---|:---|
| **LLM theory** | the results here do not depend on how the planner works, and a chapter explaining transformers would date faster than anything else in the paper |
| **Prompt-injection surveys** | well covered elsewhere, and none of the five experiments needs an injection: every harmful action is one the agent was authorised to take |
| **AI trends and market sizing** | has a shelf life measured in months and is not architecture |
| **The future of work** | not a security question, and the paper has no evidence about it |
| **Regulatory speculation** | the first book already carries a chapter on designing against a standard that does not exist; repeating it here would be padding |

## The blocker

**Nothing in this paper is yet verified against a deployed SAP mechanism.** The accurate description of the work is *tested against a reconstructed SAP authorisation model*, not *tested against SAP*. The subtitle says exactly that and is computed from the release state rather than chosen, so it changes by itself when at least M2 and M4 reach SAP level.

The dependency is not spread evenly. Chapter 3 is the paper's spine, and both of its verdicts rest on **M2 — FI tolerance groups being document-local**. If a tolerance field retains state across documents, G1 is wrong and the only uncontested gap in the paper goes with it. Exclusion **E2, the F110 payment program**, is the other place a cumulative FI limit could plausibly live and has not been examined at all.

Those two are publication-blocking in a way nothing else here is. 9 of 9 modelled mechanisms remain unverified against primary sources, and `help.sap.com` refuses automated retrieval even for exact document URLs — so this pass cannot be done from inside the toolchain that produced everything else in this repository.
