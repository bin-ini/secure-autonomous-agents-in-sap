# The Control-Property Review — the procedure in one page

*Apply this to one control against one protected property. It takes minutes, and it is built to return a refusal as readily as a finding.*

**Step 1 — Control.** Name the control, its enforcement point, and its type.

**Step 2 — Control specification.** State what it observes at decision time, what state it retains, and the local predicate it enforces.

**Step 3 — Protected property.** State the property, its extent across actions, principals and time, and — decisively — WHO claims it.

**Step 4 — Closure test.** Ask whether the local predicate, holding for every action, forces the property over the whole workflow.

**Step 5 — Specification-sensitivity audit.** Name the smallest defensible alternative specification. If it flips the verdict, the claim is contested.

**Step 6 — Countermechanism test.** Search, through more than one route, for the strongest existing mechanism that would close this — and test it before concluding.

**Step 7 — classify.** The verdict is one of:

| verdict | when |
|:---|:---|
| **holds directly** | the control observes the property |
| **holds by compositional closure** | the property is wider, and the local predicate composes into it |
| **cannot discriminate** | the property is outside the boundary and is not closed |
| **contested specification** | a defensible alternative specification changes the verdict |
| **countermechanism untested** | the strongest existing mechanism was never tried |
| **non-discriminating experiment** | the test could not have come out otherwise |
| **unsupported** | no evidence either way |

Four of the seven are refusals. A review that can only conclude *works* or *failed* cannot tell you that you moved the goalposts, or that you never tried the obvious countermeasure.

## When this review is wrong

The instrument makes claims, so it must say what would falsify it. The Control-Property Review would be inadequate if any of the following held:

- Independent reviewers, applying the instrument to the same case from the same evidence, reach systematically different verdicts. (This is what review R2 is for, and it is an open gate.)

- A small, defensible change to a specification produces an arbitrary rather than an explicable change of verdict — so the categories are not carving anything real.

- The instrument cannot separate a control everyone agrees enforces its property directly from one everyone agrees cannot, on cases whose answer is not in dispute.

- Adding the countermechanism test does not improve the accuracy of the verdicts over omitting it — in which case that step is ceremony, not method.

None of these is idle: the first is the open review gate R2, and the second and fourth are the reasons the specification-sensitivity audit and the countermechanism test are in the procedure at all.

---

# The Control-Property Review

*One control, one protected property, one verdict. Fill it in before claiming a control failed.*

## Control

- Control name

- Product, module and release — *'SAP' is not a scope*

- Enforcement point

- Preventive, detective, corrective, or evidentiary

## Control specification

- Control subject — what entity is the predicate about?

- Observation boundary — what can it see at decision time?

- Retained state — what history does it keep?

- Local predicate — what does it decide, per evaluation?

- Decision outputs

- Source of the specification

- Independent evidence for the specification *(primary documentation, vendor statement, or reconstruction)*

## Protected property

- Property statement

- Property subject — what entity is the property about?

- Extent across actions — single, sequence, aggregate

- Extent across principals — one, many

- Time horizon — instant, session, period

- Source of the property

- **Who claims this property — the organisation, the vendor, a regulator, or the researcher?**

## Closure test

- If the local predicate holds for every action, does the protected property necessarily hold for the complete workflow?

- If yes — state the closure argument

- If no — give the smallest counterexample

## Specification-sensitivity audit

- Smallest defensible alternative CONTROL specification

- Smallest defensible alternative PROPERTY specification

- Does either alternative change the verdict?

- What independent evidence prefers the specification chosen?

- Audit status — rejected, contested, not-yet-contested, replicated

- *Absence of an identified alternative does not certify uniqueness. The search is bounded by the imagination of whoever ran it.*

## Countermechanism test

- Strongest existing mechanism a practitioner would claim closes this

- Was it tested?

- Was it tested at the correct business-process scope?

- Is there an equivalent mechanism ELSEWHERE in the same product?

- **Through how many independent retrieval routes was the countermechanism search performed?** *A control-surface review is incomplete until the strongest countermechanisms have been searched through independent routes. This question exists because a single route missed Availability Control — the one mechanism capable of overturning this paper's principal finding. See loss L3.*

- What result would eliminate the claim?

## Verdict

| verdict | when |
|:---|:---|
| **holds directly** | the control observes the property |
| **holds by compositional closure** | the property is wider, and the local predicate composes into it |
| **cannot discriminate** | the property is outside the boundary and is not closed |
| **contested specification** | a defensible alternative specification changes the verdict |
| **countermechanism untested** | the strongest existing mechanism was never tried |
| **non-discriminating experiment** | the test could not have come out otherwise |
| **unsupported** | no evidence either way |

Four of the seven are refusals. That is the point of the instrument: a review that can only conclude *the control works* or *the control failed* has no way to tell you that you moved the goalposts, or that you never tried the obvious countermeasure.

---

# Worked examples

Our own four pairs, filled in. One admits a mismatch, one is held by closure, one is refused because the property was ours, one is refused twice.

## H1/G1 — One control, two properties — the method admitting a mismatch

| | |
|:---|:---|
| Control name | FI tolerance group (per-document / per-line amount) |
| Product, module and release | S/4HANA on-premise FI — **release unspecified; blocking** |
| Enforcement point | document posting |
| Type | preventive |
| Control subject | one document |
| Observation boundary | single action / one principal / instant |
| Retained state | none |
| Local predicate | document total ≤ limit, and every line ≤ line limit |
| Property A | no posting of anomalous value (document-local) |
| Property B | cumulative credited value in the period below materiality |
| Who claims them | both the organisation. Materiality is an audit concept defined over a reporting period; neither property was authored here |
| Closure | A: boundary aligned. B: **not closed** — no per-document predicate admitting the legitimate population implies a bound on the sum |
| Audit status | not-yet-contested (bounded search) |
| Countermechanism | tolerance groups, release strategies, org level, document type — swept exhaustively. **Availability Control was missed and may be fatal** |
| Verdict | A holds directly · B cannot discriminate |
| Result | A: clean separation, 100% legitimate throughput. B: 12,288 configurations, best retains 37.5%, none 95% |

## H2 — A wider property a local control still guarantees — the case that stops the principle degenerating

| | |
|:---|:---|
| Control name | PFCG organisational-level restriction |
| Product, module and release | S/4HANA on-premise — unspecified |
| Enforcement point | AUTHORITY-CHECK, per action |
| Type | preventive |
| Control subject | one action against one org unit |
| Observation boundary | single action / one principal / instant |
| Retained state | none |
| Local predicate | the action's org unit is in the grant |
| Property A | no part of the workflow touches an org unit outside the grant |
| Property B | — |
| Who claims them | the organisation |
| Closure | **closed.** If every out-of-unit action is refused, no sequence of permitted actions can leave the unit. The property is wider than the boundary and holds anyway |
| Audit status | not-yet-contested |
| Countermechanism | n/a — the control holds |
| Verdict | holds by compositional closure |
| Result | all 120 documents refused for the wrong company code |

## H3/G2 — The method refusing a result because the property was ours

| | |
|:---|:---|
| Control name | GRC Access Risk Analysis (static, per principal) |
| Product, module and release | GRC Access Control — unspecified |
| Enforcement point | offline analysis of role assignments |
| Type | detective |
| Control subject | one principal's grant set |
| Observation boundary | sequence / one principal / period |
| Retained state | the grant set |
| Local predicate | no principal spans both sides of a conflicting pair |
| Property A | no principal holds both sides — **the vendor's own stated property** |
| Property B | no single decision process completes both sides — **ours** |
| Who claims them | A: SAP. B: the researcher. That difference is the whole finding |
| Closure | not applicable to B; the property ranges over principals the analysis never considers together |
| Audit status | **contested** — keeping property A is defensible and is what SAP claims |
| Countermechanism | ARA per principal and against the accumulating technical user, both tested. SAP Business Workflow **not** tested and is process-scoped |
| Verdict | A holds directly · B contested specification |
| Result | A: the technical user accumulating both grants is flagged. B: both propagated principals clean, composition completes — published as a proposed property, never as a failure |

## G3 — The method refusing a result twice

| | |
|:---|:---|
| Control name | Security Audit Log record |
| Product, module and release | S/4HANA — unspecified |
| Enforcement point | after the fact |
| Type | evidentiary |
| Control subject | authenticated principal |
| Observation boundary | single action / one principal / instant |
| Retained state | the log |
| Local predicate | record the principal, transaction and time |
| Property A | name the accountable principal |
| Property B | attribute the action to the entity that SELECTED it |
| Who claims them | A: conventional audit practice. B: the researcher |
| Closure | not applicable — this is a subject mismatch, and no retained history repairs a non-injective map |
| Audit status | **contested** — A is a legitimate audit objective |
| Countermechanism | **tested, late.** Timing density, session identifiers and terminal fields were named in the pre-registration, left untried for eight days (loss L2), and finally measured in X12: retained history changes nothing where no recorded field separates the actors, and the best accuracy available to any procedure over the modelled record equals the do-nothing baseline |
| Verdict | contested specification |
| Result | blocked on two grounds — *contested specification* and *countermechanism untested* — one of which has since been cleared by doing the work rather than by arguing it away. What survives is a bound over one modelled evidence stream and a property nobody has agreed on |

