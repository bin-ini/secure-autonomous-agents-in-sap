# Secure Autonomous Agents in SAP Systems

### A Control-Property Review, evaluated on a reconstructed SAP FI authorization model

**Bindiya Priyadarshini · Martin Pankraz · Version 1.0**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22747364.svg)](https://doi.org/10.5281/zenodo.22747364)

*Text CC BY 4.0 · Code MIT · doi: [10.5281/zenodo.22747364](https://doi.org/10.5281/zenodo.22747364)*

---

Enterprises are beginning to let AI agents *act* inside their ERP — post the
credit memo, change the vendor's bank detail, release the transport into
production — rather than merely suggest that a person do it. Almost every one of
those decisions travels with the same reassurance:

> *the agent runs under a named user, with the same authorisations that user
> already had, so it inherits the same controls.*

That sentence is doing an enormous amount of load-bearing work in deployment
decisions right now. It is not obviously wrong. It is also, mostly, untested.

This study tests it — one named control against one named property at a time, on
a reconstructed SAP FI authorization surface, with every experiment registered
*before* the code existed so the goalposts cannot move. The instrument is the
**Control-Property Review**: for a named control and a named property, can that
control decide that property at all?

Three of the results were not what the reassurance predicts:

- A value limit that reads **one document at a time** is complete against a
  single bad posting — and blind to the same harm assembled from individually
  ordinary ones. The only compensating control hands the automation benefit back
  almost one-for-one.
- A governance step can flag **40 of 40** harmful transport releases and prevent
  **0** of them, because it runs *after* the import. Perfect detection, zero
  prevention — and both look green in a control matrix.
- When an agent acts under a person's identity, the record names the **person,
  not the decider**. No amount of log retention repairs that; it is the wrong
  field, not too little history.

Underneath the three is one idea, and it is bigger than SAP:

> **Autonomous execution does not *create* these gaps. It reveals where local
> compliance has been standing in for global assurance** — the assumption every
> control environment leans on, that if each transaction is individually
> compliant, the process built from them must be compliant too.

The agent doesn't break that assumption so much as move fast enough, and compose
enough decisions across enough sessions, to make a gap that was always there
suddenly visible.

## What this repository is

Every numeric result and every narrative summary in the paper is **generated
from, or checked against, the sources here.** The build runs 20 consistency
checks and writes nothing if any of them fails, so the prose cannot quietly
disagree with the code: the central assertion is checked for hedging and for
language exceeding its evidence class; the abstract may not be more confident
than the release state; every figure carries a digest of the data it was drawn
from; and the claims trajectory is derived from the audit and loss registers
rather than written from memory.

## Status — read this first

This is **version 1.0: a complete, self-contained independent study**, reported
honestly on a *reconstructed* model of an SAP FI authorization surface. That
framing is deliberate. No modelled mechanism has yet been verified against
primary vendor documentation, the exact product and release scope is not yet
fixed, and independent practitioner review and replication are planned. Its
scope, the limits of what it establishes, and the external validation still to
come are set out in full in the paper's final part, *Scope, Limitations and
Future Validation* (`python3 release.py` prints the current state). Read the
results as results about the reconstruction.

The review procedure was built to be hard to please, and it was turned on this
work first: of eight control-property pairs examined, four held, two are
contested, one was withdrawn as misspecified and re-run, and exactly one
survived as an uncontested gap. The negative results are the point.

> **No customer, proprietary or vendor-licensed material appears anywhere in
> this work. Every scenario is synthetic.**

## Requirements

- Python 3.10 or newer (the sources use `X | None` and built-in generics).
- `matplotlib` for the figures only; every experiment and check runs on the
  standard library alone.

```
python3 -m pip install -r requirements.txt
```

## Reproduce everything

```
python3 figures.py     # render fig/*.png and fig/*.pdf from the experiment data
bash build.sh          # run all 20 checks, then regenerate every .md artefact
```

`build.sh` exits non-zero if any check fails and writes nothing in that case. A
clean run regenerates the per-section artefacts, the full results
(`RESULTS_SAP.md`) and the assembled paper source (`PAPER.md`).

Run a single experiment or check directly:

```
python3 run.py                 # the results, machine-generated
python3 <module>.py            # that section's artefact
python3 <module>.py --check    # that section's consistency check
python3 verify.py              # cross-checks over the experiment outputs
```

The three headline sweeps (X7, X11, X12) run standalone with no external
dependency.

## The companion cross-check

One supporting negative control — "does the generic agent-security control stack
close the SAP path?" — runs the same session through a fully-enabled generic
agent-security stack, to confirm that stack does not close the cumulative-value
path (it does not: every posting executes, none is blocked). That control
library comes from the companion work *AI Security Principles for the Autonomous
Enterprise* and is **vendored in `agentsec_testbed/`**, so the check runs as part
of the ordinary build with no external dependency. It is not part of the SAP
argument, which stands on X7–X12 alone; see `agentsec_testbed/NOTE.md`.

## What each source is

| file | what it produces |
|:---|:---|
| `sapsec/` | the reconstructed SAP model, workloads and experiments (X7–X12) |
| `mismatch.py` | the Control-Property Mismatch formalism — 8 pairs, each predicted from its specification |
| `counterfactual.py` | the specification-sensitivity (counterfactual) audit |
| `boundary.py` | the held/gap boundary map |
| `surface.py` | the SAP control-surface specification (mechanisms M1–M9, exclusions) |
| `review.py` | the Control-Property Review instrument (7 verdicts) |
| `finding.py`, `abstract.py` | the finding and abstract, with anti-overclaim checks |
| `whymature.py`, `whyfail.py`, `impact.py` | the thesis, the failure modes it corrects, and who the result lands on |
| `narrative.py` | the narrative spine and closing |
| `relatedwork.py` | the literature review |
| `prereg_sap.py` | the pre-registrations |
| `losses_sap.py` | the loss register — what the work stopped believing |
| `claims_sap.py` | the claim ledger |
| `figures.py` | the three figures, each digest-checked against its data |
| `release.py` | the release-gate state, scope and limitations |
| `facts.py` | the shared figures and the retired-figure guard |
| `run.py` | the assembled results (`RESULTS_SAP.md`) |
| `paper.py` | assembles the full paper source (`PAPER.md`) |
| `buildreg.py`, `build.sh` | the build registry and driver |
| `verify.py` | independent cross-checks |

## Citing this work

See `CITATION.cff`, or cite as:

> Priyadarshini, B., & Pankraz, M. (2026). *Secure Autonomous Agents in SAP
> Systems: A Control-Property Review Evaluated on a Reconstructed SAP FI
> Authorization Model* (Version 1.0). doi: [pending].

Fifth in a series on enterprise AI agent security, following *Calibrated to Act*
(10.5281/zenodo.21157411), *Proven Exploitable* (10.5281/zenodo.21159028),
*Ghost in the Stack* (10.5281/zenodo.21499947) and *No One Signs*.

## Licence

Code: MIT (see `LICENSE`). Paper text: CC BY 4.0. You may share and adapt this
work, including commercially, with attribution.

---

*Gödel proved that any system powerful enough to be worth trusting will always
hold at least one true statement it cannot prove from within itself. Control
frameworks are such systems. This study is, in the end, one small map of where a
control's boundary sits relative to the truth it is trusted to guarantee — and of
how to find that line for a control you own, before an agent is switched on.*
