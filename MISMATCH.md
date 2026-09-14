# The Control-Composition Mismatch Principle

> **A control cannot discriminate harmful from legitimate execution when the protected property lies outside its observation boundary, the executions are indistinguishable on the control's inputs, and the locally enforced predicate does not compose into the property.**

The final clause is not decoration. An extent difference alone is insufficient: compositional closure must first be excluded, which is exactly what H2 below demonstrates — a property wider than the boundary that the local predicate nonetheless guarantees.

Two forms. **Extent mismatch:** the property ranges over more actions, more principals, or a longer horizon than the control observes and retains. **Subject mismatch:** the property is about a different entity than the control's predicate, and the map between them is not injective — which no amount of retained history repairs.

Each row's verdict is derived from its specification alone. In every tested pair the observed outcome matched that derived verdict, so the summary table below carries only what a reader needs to follow the argument; the full observation boundary, subject and extent for each pair are drawn in Figure 1 and set out in the per-pair discussion.

| pair | control | the property it is asked to guarantee | mismatch | verdict |
|:--|:---|:---|:---|:---|
| **H1** | FI tolerance group (per-document / per-line amount) | no posting of anomalous value | none | **holds** |
| **G1** | FI tolerance group (per-document / per-line amount) | cumulative credited value in the period below materiality | extent | **cannot-discriminate** |
| **H2** | PFCG organisational-level restriction (AUTHORITY-CHECK) | no part of the workflow touches an org unit outside the grant | none | **holds** |
| **H3** | GRC Access Risk Analysis (static, per principal) | no principal holds both sides of a conflicting duty pair | none | **holds** |
| **G2** | GRC Access Risk Analysis (static, per principal) | no single decision process completes both sides of a conflicting duty pair | extent | **cannot-discriminate** |
| **G3** | Security Audit Log record | attribution of the action to the entity that SELECTED it | subject | **cannot-discriminate** |
| **P1** | CTS transport release (S_TRANSPRT, ACTVT 43) | released code does not change system behaviour in an unauthorised way | subject | **cannot-discriminate** |
| **H4** | Static check and pre-release review of the transported objects (ATC check variant, peer review, quality-system exercise) | released code does not change system behaviour in an unauthorised way | none | **holds** |

*(The paired detail — what each control observes at decision time versus what its property ranges over — is the substance of Figure 1 and the sections that follow; collapsing it into one ten-column table made it unreadable, so it is shown where there is room to see it.)*

## The decisive pair

**H1 and G1 are the same SAP control.** FI tolerance groups, unchanged, against two different harms.

| | H1 | G1 |
|:---|:---|:---|
| harm | no posting of anomalous value | cumulative credited value in the period below materiality |
| property extent | `single/one/instant` | `aggregate/one/period` |
| control outrun on | — | actions aggregate>single, horizon period>instant |
| derived verdict | **holds** | **cannot-discriminate** |
| experiment | X7 positive control: clean separation, 100% legitimate throughput | X7 primary: 12,288 configurations, best retains 37.5% throughput |

This is why the paper is not a list of SAP defects. A control is not strong or weak; a control-harm pair either matches or it does not. The same tolerance group is a correct and sufficient control against a document-local harm and cannot discriminate at all against a period-aggregate one, and the difference is derivable before any experiment runs.

## What the experiments become

| experiment | pair | form | where the boundary is crossed |
|:---|:--|:---|:---|
| **X7** | G1 | extent mismatch | actions aggregate>single, horizon period>instant |
| **X8** | G2 | extent mismatch | principals many>one |
| **X9/X12** | G3 | subject mismatch | the control's predicate is about authenticated principal; the property is about the deciding actor, and the map between them is not injective |
| **X11** | P1 | subject mismatch | the control's predicate is about the transport request; the property is about the behaviour of the transported objects, and the map between them is not injective |
| **X11** | H4 | no mismatch — the pair holds | nowhere — the control's subject IS the property's subject |

They are not observations that happened to sit near each other. Two are the same failure along different axes of one extent, two are the other form of the same boundary, and the last is what the boundary looks like from the inside — a control in the same governance surface whose predicate is about the property's own subject.

## The prediction that was made before the experiment

**P1 — CTS transport release (S_TRANSPRT, ACTVT 43).** **PREDICTION MADE BEFORE THE EXPERIMENT, THEN TESTED.** X11: across every configuration whose active steps range only over the request, none discriminates and all forty harmful transports reach production in every one of them, at every setting of every parameter. The prediction held at the pair it names — and X11 also found what the counterfactual audit said it would, which is that the same surface contains content-ranging decisions the prediction had ignored. See H4.
