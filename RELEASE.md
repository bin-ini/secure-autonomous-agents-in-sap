# Scope, Limitations and Future Validation

*Secure Autonomous Agents in SAP Systems — A Control-Property Review Evaluated on a Reconstructed SAP FI Authorization Model*

## A Control-Property Review Evaluated on a Reconstructed SAP FI Authorization Model

*Release state at commit `unknown`.*

| | |
|:---|:---|
| product and release scope | **to be fixed — validation item B1** |
| evidence cutoff | **to be frozen at the validated edition** |
| accurate wording | *Evaluated on a reconstructed SAP FI authorization model* |
| build | 20 checks, 22 generated artefacts |

## Validation still to complete

*This edition (v1.0) is a complete independent study. The four items below are the external validation still to be done before a validated edition; none is a conceptual gap in the study itself.*

| gate | state | |
|:---|:---|:--|
| Evidence blockers | 3 open / 3 total | **pending** |
| Required independent reviews | 0 complete / 2 required | **pending** |
| Evidence cutoff | not frozen | **pending** |
| Frozen release build | not created | **pending** |

> **Validation status — v1.0.** This edition is complete as an independent study. Still pending before a validated edition: evidence blockers, required independent reviews, evidence cutoff, frozen release build. None of it is a conceptual gap in the study.

## Validation items — the primary-source pass

### B1 — Fix the precise SAP scope  *(**pending**)*

Product, deployment model, module and release. 'SAP' is not a scope and neither is 'S/4HANA'. Choose the release the reconstructed mechanisms actually represent — not the one whose documentation is easiest to reach — then rebuild or annotate every mismatch.

### B2 — Verify M2 from primary documentation  *(**pending**)*

For the named release: exact configuration name, exact field semantics, enforcement point, whether each limit binds per document, per line, per clearing transaction, per run, per account or per period, and whether ANY state persists across documents. If one does, the second half of the finding is wrong.

### B3 — Resolve the cumulative countermechanisms against the exact path  *(**pending**)*

Path-binding, not a survey. Can F110, Availability Control or another standard mechanism preventively evaluate cumulative credited value for the exact credit-memo process, control object, product and release used in X7? The four interpretations are pre-registered as D1 — committed before the sources are read, and two of them remove the finding.

## Independent review (planned)

Neither can be performed by the toolchain that built this repository, and that is the point of both.

**R1 — An SAP FI/GRC practitioner reviews the control-surface specification only.** *(**planned**)* Not the prose, not the finding. The question is whether the surface is faithfully described. Showing them the conclusion first would measure their agreement with us rather than the fidelity of the model.

**R2 — Inter-rater reliability — independent researchers reproduce the Control-Property Review for the decisive H1/G1 pair, in two stages: verdict reproducibility under fixed specifications (R2A) and specification-sensitivity reproducibility (R2B).** *(**planned**)* If the instrument only works in the hands of the person who wrote it, it is not an instrument; if two careful readers reach different verdicts on the same case, the categories are not carving anything real. Agreement across independent raters is the first real test of the paper's actual contribution, and it is what would falsify the method rather than a claim. Scope, stated so it cannot be overgeneralised: this covers the H1/G1 decisive pair only. A successful outcome establishes that independent reviewers reproduced the analysis for that pair and independently evaluated its specification sensitivity — not that CPR has demonstrated reliability across all seven verdict classes. A full instrument study (compositional closure via H2, a contested specification via G2 or G3, misspecification via P1, and a genuinely unsupported case) belongs to the research programme, not this release.

## Statements for the paper

**Artifacts.** The pre-registrations, control-surface specification,
experiment implementation, configuration manifest, generated results, loss
register, specification-sensitivity audit, claim ledger, narrative spine and
Control-Property Review instrument are released with the paper. Every reported
numeric result and every narrative summary is generated from, or checked
against, the same manifests that produced the experimental artefacts: the
build runs 20 consistency checks and writes nothing if any of them
fails.

**Evidence cutoff.** *Not yet frozen.* No evidence-cutoff date or fixed product-and-release scope is asserted while the gates above are open — asserting either before the primary-source pass would be a fiction. Both are frozen at release, and this line states them once they are.

## Until the blockers close

| may not appear | why |
|:---|:---|
| any title or subtitle saying *tested against SAP* | no mechanism has reached SAP evidence level |
| any deployment-level conclusion | the surface is a reconstruction |
| any claim that the tested path lacks cumulative enforcement | Availability Control is unresolved against that path |
| any claim that a deployed SAP control environment has failed this test | it has not been tested; a model of it has |
