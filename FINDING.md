# The finding

In the reconstructed FI scenario, the tolerance control did one job perfectly
and another not at all. It caught every document whose own value was anomalous,
and it did so without turning away a single piece of legitimate work. Then we
aimed the same control, unchanged, at a different harm: a materiality breach
assembled from documents that are each, on their own, completely ordinary. Here
it was helpless. Across 12,288 configurations, the only way to hold the period's
total under materiality was to start refusing legitimate work — and the best
setting still gave back most of it, keeping just 37.5%.

The reason is not that the control is weak. It is that the two harms live at
different scales. The first is settled one document at a time, which is exactly
what the control sees. The second is a running sum over every document in the
period, and no per-document limit that lets the legitimate work through can put
a ceiling on that sum. We read both verdicts off the specifications before the
sweep ran; the sweep then confirmed them.

So a control is not strong or weak on its own. What carries a guarantee is the
control-harm pair. The very same control can be complete against one harm and,
against another, unable even in principle to tell the good from the bad.

## What bounds it

Eight, and none of them is in the paragraph above. A reader cannot tell the difference between a careful claim and an abandoned one if every clause carries its own disclaimer, so the claim is stated first and bounded here.

**This is a reconstructed model, not deployed SAP.** Every mechanism is rebuilt from secondary sources. No entry in the control surface specification has reached SAP evidence level.

**The product and release scope is not yet fixed.** The reconstruction is shaped by S/4HANA on-premise FI, but no release was chosen, and the mechanisms differ across Cloud, ECC and ByDesign. Until it is fixed, a reader cannot tell which omission is a limitation and which invalidates the surface.

**M2 must be primary-sourced.** The finding rests on FI tolerance groups being document-local. If any tolerance field retains state across documents, the second half of the finding is wrong.

**F110 is unresolved.** The payment program is the other plausible location for a cumulative FI limit and has not been examined. Silence in the sources is not absence.

**The principle is not new, and the paper may not present it as new.** The related-work section, written last, records the works that anticipate part of it — Schneider 2000; Lunt 1989; Nash 1990; McCullough 1988 — and a further group that supplies the mechanism its repair recommendation amounts to. Extent mismatch is the aggregation problem. The principle specialises a published characterisation of enforceable security policies to controls whose observation boundary is narrower than the execution. The repair is history-based access control and usage control's mutable attributes. What is asserted above is a measurement of one reconstructed surface, and it is the measurement that is offered, not the phenomenon.

**Availability Control may narrow or eliminate the SAP-specific gap.** SAP evaluates accumulated consumption against a consumable budget per control object and can refuse a posting on that basis. Whether it binds the credit-memo path modelled here is unknown. If it does, this becomes a control-placement finding rather than a control gap — and 'SAP lacks aggregate-state control' is retired either way.

**The specification is not-yet-contested, which is not certification.** The specification-sensitivity audit found no defensible alternative for this pair. That reflects a bounded search. It can invalidate a verdict; it cannot establish that a specification is unique.

**One instance cannot support a class claim, and this instance does not yet support a deployment claim either.** Nothing here establishes that mature enterprise control environments in general share this shape. Nor — and this bound was itself over-reaching until a reviewer caught it — does it yet establish that immaturity is an insufficient explanation for the SAP instance, because no mechanism has reached SAP evidence level. What it establishes is narrower: **within the reconstructed FI control surface, immaturity is not required to produce the observed control-property mismatch.** Once M2 and the cumulative countermechanisms are resolved for a named product and release, that upgrades to: for the validated SAP path, immaturity is not a sufficient explanation.

