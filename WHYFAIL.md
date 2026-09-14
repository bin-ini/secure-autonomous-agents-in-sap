# Why existing control evaluations misclassify

A control catalogue is an inventory of controls, not an inventory of guarantees, and the ordinary way of auditing one reaches the wrong verdict in four recurring ways. Each is a specific mistake, each produces a specific misclassification, and each is the reason a particular step of the Control-Property Review exists. Naming them first is what makes the instrument that follows necessary rather than merely orderly.

## 1. Property inflation

*The mistake.* The evaluator quietly replaces the property the control actually claims to enforce with a stronger one the control was never asked to guarantee, then reports the control as failing against the substituted property.

*What it does.* A control that correctly enforces its stated property is recorded as a failure, and the report cannot distinguish a real gap from a moved goalpost. In this work it is the difference between what SAP's segregation-of-duties control claims and the stronger decision-layer property a researcher can substitute for it.

*What catches it.* The specification-sensitivity audit, which forces the smallest defensible alternative property into view and marks the verdict *contested* when a substitution is what produced it.

## 2. Comparator omission

*The mistake.* The evaluation runs the harmful workload through the control and observes harm, without ever running an equally ordinary but legitimate workload through the same control to see what it costs to stop.

*What it does.* A control that cannot tell the two workloads apart looks exactly like one that can, because only one side was measured. The exchange rate between harm prevented and legitimate work refused — the whole commercial question — is invisible.

*What catches it.* The paired positive control in every sweep, which measures the legitimate workload beside the harmful one and reports the throughput a control gives back to buy its coverage.

## 3. Countermechanism neglect

*The mistake.* The evaluator concludes that a control cannot address a harm without searching, through more than one route, for the strongest existing mechanism a practitioner would actually reach for — often in a different module of the same product.

*What it does.* A mismatch is declared structural when the product already ships the missing control shape somewhere else. This nearly happened here: a single retrieval route missed SAP Availability Control, the one native mechanism capable of overturning this paper's principal finding.

*What catches it.* The countermechanism test, which owes no verdict until the strongest existing mechanism has been searched through independent routes and tested at the correct process scope.

## 4. Observation-boundary confusion

*The mistake.* The evaluator treats every case where a property is wider than what a control observes as a failure, without asking whether the control's local predicate nonetheless composes into the wider property.

*What it does.* The category collapses two opposite situations: a control that is locally correct and globally sufficient, and one that is locally correct and globally silent. They look identical in a control matrix and require opposite responses — fund the control, or relocate it.

*What catches it.* The closure test, which asks whether local enforcement forces the global property before any mismatch is concluded, and is the case that stops the principle degenerating into 'a wider property needs a wider control'.

Across the 8 control-property pairs specified in this paper, and the 9 SAP mechanisms modelled, every misclassification the review prevented is one of these four. That is the argument for the instrument: not that it is elegant, but that without an explicit control-property analysis, documentation of individual controls does not by itself establish which wider properties follow under autonomous execution.

## What this review contributes

Stated plainly, and in the order of what survives longest:

1. **The Control-Property Review** — a structured method for deciding whether a named control can enforce a named property at all, with seven verdicts of which four are refusals.

2. **The specification-sensitivity audit** — a general test that marks a claim *contested* when a small, defensible change of specification would flip its verdict. This is the most portable idea here and works far outside SAP.

3. **Countermechanism review** — a discipline that owes no conclusion of structural failure until the strongest existing mechanism has been searched through independent routes and tested.

4. **A reconstructed autonomous-agent case study** in SAP FI that applies the three above and, in doing so, eliminates, narrows or reclassifies most of the findings its own author set out to make.

The first three are the durable contribution: they stand even if every SAP-specific result in the case study is eventually overturned. The case study is how they were earned, not what they depend on.

