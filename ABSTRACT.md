# Secure Autonomous Agents in SAP Systems

### A Control-Property Review Evaluated on a Reconstructed SAP FI Authorization Model

## Abstract

Autonomous agents are being given authority to act inside enterprise resource
planning systems, whose authorisation models were built for human operators and
are among the most mature in commercial software. Autonomous execution does not
create the underlying harms; it reveals where local compliance has been standing
in for global assurance — the assumption that individually-compliant actions
compose into a compliant process. It changes harm's reach in three ways:
amplifying aggregate harm, so that what a human would take a year to express an
agent expresses in an afternoon; composing a duty conflict across sessions or
principals that no per-principal check ever considers together; and separating
the deciding process from the principal the record names. Only the first depends
on throughput. This paper asks one narrow question — for a named control and a
named property, can that control decide that property at all? — and answers with
a diagnostic instrument, the Control-Property Review, and 5 pre-registered
experiments against a reconstructed SAP authorisation surface.

A control is neither strong nor weak. The unit that carries a guarantee is the
control-property pair, and a pair fails whenever the property is defined outside
the control's observation boundary — because it ranges over more actions,
principals or time than the control sees, or because it is about a different
entity than its predicate names. For all 8 specified pairs the
verdict derived from the specification agreed with the observed outcome. The
instrument refused as readily as it found: 4 of 8 pairs are
contested — a defensible alternative specification flips the verdict — and one
cost result was retracted.

Three measurements. The same FI tolerance group separated a document-local
anomaly at full throughput yet could not discriminate a materiality breach built
from documents indistinguishable on every field it reads: of 12,288
configurations, 10,398 held the outcome below materiality, the best retaining
37.5% of legitimate work — it can throttle the total, not tell the two
apart. A harmful transport identical at request level was discriminated only by
decisions ranging over its content, never by the request alone (2,512 of
12,800). Under principal propagation, no procedure
reading the audit fields beats naming the busiest actor unread.

The first two differ in kind, not price: where the property outruns the
control's extent the exchange rate is forced by the pair; where it reads the
property's own subject, cost is a swept, unmeasured false-positive rate.

### What bounds it

**The principle is not new and the paper does not claim it is.** The related-work section records 4 of 19 works that anticipate part of it — Schneider 2000; Lunt 1989; Nash 1990; McCullough 1988 — and a further group that supplies the mechanism its repair recommendation amounts to. Extent mismatch is the aggregation problem; the principle specialises a published characterisation of enforceable security policies to controls whose observation boundary is narrower than the execution; the repair is history-based access control and usage control's mutable attributes. What is offered is the instrument, the specification-sensitivity audit, the measurements, and the negative results.

**This is a reconstruction, not deployed SAP.** No modelled mechanism has been verified against primary vendor documentation, the product and release scope is not fixed, and the results are results about the reconstruction. The study states its scope and the external validation still to be completed.

**The second experiment's cost figures are conditional and its first version was wrong.** The transport model originally contained no channel through which a content-ranging step could stop a benign change, so it reported zero cost as a measurement. That is recorded as a loss. The false-positive rate is now swept across four values, none of which is measured, and no claim rests on any particular one.

**The audit refuses more than it grants.** 4 of the 8 audited pairs are CONTESTED — a defensible alternative specification changes their verdict — and they are published as formal results awaiting an argument rather than as measured control failures. One prediction was withdrawn as misspecified before it was run, respecified, run, and then narrowed by its own result.

**One instance establishes nothing about a class.** 4 controls held — 1 of them against a specification the audit contests — and 3 gaps survived, in one reconstructed surface, on a small number of paths. The register of 6 recorded losses includes the one that matters most here: the paper was written to a complete manuscript before the literature was searched at all.

> This is **version 1.0**, a complete independent study on a reconstructed model, with 3 primary-source validation items still to complete before a validated edition. Its scope and the external validation still to be done are set out in full in the final part.

**Keywords:** enterprise resource planning; SAP; autonomous agents; agentic AI; access control; authorisation; separation of duties; aggregation problem; usage control; audit and attribution; security evaluation; pre-registration.

