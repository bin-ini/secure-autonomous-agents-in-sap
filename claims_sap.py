"""
claims_sap.py -- the claim ledger for book two.

    python3 claims_sap.py > CLAIMS_SAP.md

Same rule as the first book: every claim carries a date, a source class, a
confidence, and whether the argument fails if it is wrong. One addition, and it
is the reason this file exists on day one rather than at the end.

S0 is a claim about a CLASS -- mature enterprise control models in general --
supported by evidence from a single instance. The first book had no entry of
that shape and did not need one; every one of its measured claims was about the
thing it had measured. A class claim is a different object, it is the one most
likely to be quoted, and it is the one this project's own standards would
otherwise let through unexamined. So it is written down as a conjecture, with
the instance that supports it and the instance that appears to contradict it
both named.
"""
from __future__ import annotations

from dataclasses import dataclass

AS_OF = "8 August 2026"


@dataclass
class Claim:
    id: str
    claim: str
    source: str
    confidence: str
    load_bearing: bool
    falsifier: str


LEDGER = [
    Claim(
        "S0-Extent",
        "Autonomous execution can compose individually permitted actions "
        "across more actions, more principals, or a longer horizon than a "
        "deployed control observes and retains.",
        "our-argument; instantiated by X7 (actions, horizon) and X8 "
        "(principals)",
        "conjecture — two instances, one system, and G2 is contested",
        True,
        "A composition an autonomous workflow can perform that no control's "
        "observation boundary is outrun by. Note the honest weakness: the only "
        "UNCONTESTED instance is G1 (see `counterfactual.py`)."),

    Claim(
        "S0-Subject",
        "Autonomous mediation can separate the identity or object a control "
        "names from the actor or behaviour the protected property is about, "
        "so that the map from the control's subject to the property's subject "
        "stops being injective.",
        "our-argument; both instances now measured (X12, X11) and both still "
        "**contested on their specifications**",
        "conjecture, and the weaker half: measured, and with no uncontested "
        "instance",
        True,
        "Either instance surviving its counterfactual. G3's alternative — that "
        "an audit trail's objective is the accountable principal, not the "
        "deciding actor — is defensible and unanswered; the countermechanism "
        "has now been tested and the gap survives smaller. P1 was misspecified "
        "and has been respecified against the complete transport-governance "
        "surface, run, and confirmed at the authorisation object while being "
        "made irrelevant at the surface."),

    Claim(
        "S0-Amplifier",
        "Human throughput was an implicit rate limiter, and removing it "
        "amplifies extent mismatch on the action and horizon axes.",
        "our-argument; the mechanism behind X7 specifically",
        "medium — and deliberately demoted",
        False,
        "An earlier draft made this the universal explanation for every "
        "finding, which was wrong: only X7 is fundamentally about throughput. "
        "X8 arises from a principal boundary and X9 from a subject boundary, "
        "and both occur at low volume. One explanation was being made to carry "
        "several distinct mechanisms. It is now an amplifier of one axis, not "
        "the theory."),

    Claim(
        "S0a",
        "**Proposition.** A decision procedure whose inputs are limited to "
        "the current principal's grants and the current action's required "
        "rights cannot discriminate two executions that are identical over "
        "those inputs and differ only in an aggregate outcome.",
        "our-argument; a statement about a decision procedure's inputs, "
        "verified by X7's sweep",
        "high — but note it is a proposition about inputs, not a claim about "
        "SAP",
        True,
        "Not falsifiable as stated; it follows from the definition of the "
        "input set. The value is in what it forbids us from saying. The "
        "earlier phrasing — *permission-shaped authorisation cannot express "
        "aggregate constraints* — invited a definitional argument and, worse, "
        "let 'permission-shaped' stand in for SAP authorisation as a whole. "
        "An enterprise decision engine may consult history, workflow state or "
        "a policy information point and still produce an authorisation "
        "decision; card payment velocity checks (S0b) are exactly that. The "
        "proposition binds only procedures with the stated input set, and "
        "whether SAP's is one of those is an empirical question the surface "
        "specification has not yet answered."),

    Claim(
        "S0b",
        "Aggregate-state authorisation is not an unsolved problem. Card "
        "payment authorisation has performed velocity and cumulative checks "
        "inside the authorisation decision for decades.",
        "our-argument from general knowledge of payment systems, now "
        "**second-sourced twice over** by the related-work section: Brewer and "
        "Nash formalised history-dependent access for commercial systems in "
        "1989, and UCON gave cumulative constraints a model in 2004",
        "high, and load-bearing in the wrong direction: it constrains S0",
        True,
        "This is no longer at risk of being wrong; it is at risk of having "
        "been understated. The framing that survives is not that the control "
        "must be borrowed from another industry — loss L3 retired that when "
        "Availability Control turned out to be native to SAP, and the "
        "related-work section retired what was left of it. It is that the "
        "required control shape has been available in the access-control "
        "literature for decades and is not on this posting path."),

    Claim(
        "S0c",
        "**Logical concentration under credential separation.** An autonomous "
        "workflow can preserve every credential boundary an organisation has "
        "established while concentrating action SELECTION in a single decision "
        "process. Duties remain separated at the credential layer and are "
        "unified at the decision layer, which is the layer no deployed control "
        "in the reviewed surface reads.",
        "our-argument, from X8; the paper's least measured object, and its "
        "originality is **not established** — the related-work section records "
        "that the workflow-authorisation literature, which is where a prior "
        "statement of this would live, was not searched systematically",
        "conjecture — the concept is defined, the distinguishing measurement "
        "is not yet designed",
        True,
        "The obvious objection is that this is ordinary collusion, and it must "
        "be answered with a measurement rather than a definition. The "
        "distinguishing questions: does the composed sequence require "
        "agreement between two accountable people? How many separately "
        "accountable decision-makers does the workflow contain? Does one "
        "policy select both steps? Can an investigator attribute the composed "
        "intent to a single controller? Until at least one of those is "
        "measured, S0c is a name for something, not a finding about it. The "
        "architect's review question it yields — *are duties separated only at "
        "the credential layer, or also at the decision layer?* — is usable "
        "today and is not thereby evidence."),

    Claim(
        "S1",
        "**Proposition, with the sweep as verification.** Let legitimate and "
        "harmful documents be drawn from the same distribution F, and let the "
        "control be any predicate π on a single document. The expected value "
        "admitted from a population of n documents is n·E_F[V·1{π(D)}], so the "
        "FRACTION of value admitted, E_F[V·1{π}]/E_F[V], is identical for both "
        "populations and independent of n. Harm and legitimate work are "
        "therefore reduced in the same proportion: the exchange rate is one to "
        "one, exactly, in expectation. This is a consequence of "
        "exchangeability, not an empirical law of SAP or of workloads in "
        "general.",
        "formal consequence of the constructed condition; X7's sweep verifies "
        "it (best legitimate throughput 37.5% against a materiality/session "
        "ratio of 36.1%, agreeing to within the amount grid)",
        "high as a proposition; **the empirical contribution is elsewhere**",
        True,
        "The proposition cannot fail; what can fail is its applicability. The "
        "real empirical claims are four, and each is separately attackable: "
        "(i) the reconstructed SAP surface is transaction-local in the tested "
        "scenario; (ii) no identified SAP mechanism supplies the missing "
        "aggregate state — at risk from exclusions E2 and E5; (iii) "
        "configuration-only mitigation produces measured business denial; "
        "(iv) a cumulative control changes the failure mode from silent "
        "financial harm to visible partial outage, refusing 80 of 120 "
        "legitimate documents. Do not quote the exchange rate as a discovery. "
        "It is the arithmetic that makes (iii) inevitable once (i) holds."),

    Claim(
        "S2",
        "A segregation-of-duties ruleset evaluated as a static predicate over "
        "role assignments cannot see a conflict composed across two principals "
        "by one agent.",
        "own testbed (X8), with a collusion control confirming the harm "
        "pre-exists agents",
        "high, and close to definitional — reported as such",
        False,
        "A static per-principal analysis that reports the composed sequence. "
        "By construction it cannot, which is why the contribution is the "
        "location of the assumption and not the bypass."),

    Claim(
        "S2b",
        "Principal propagation — the architecture a reviewer would prefer, "
        "because the agent holds no standing authority of its own — is the one "
        "that renders the composition invisible. A technical user "
        "accumulating both grants IS reported.",
        "own testbed (X8); this outcome was not among the three "
        "pre-registered ones",
        "high, within the reconstruction",
        True,
        "An access-risk analysis that flags the propagated case. Ours does "
        "not, and the technical-user arm confirms the ruleset is not inert."),

    Claim(
        "S3",
        "An audit record keyed on principal identity correctly names the "
        "authenticated principal but, under the deciding-actor property "
        "examined here, attributes no separate identity to the autonomous "
        "process that selected the action; read as naming the decider rather "
        "than the accountable principal, it assigns the selection to a named "
        "employee.",
        "own testbed (X9) — **declared definitional before it was run**",
        "certain and uninformative: this is arithmetic, not measurement",
        False,
        "Not falsifiable as an empirical matter. Its value is the size of the "
        "repair — one field — and it may not be cited in support of S0, S1 "
        "or S2."),

    Claim(
        "S4",
        "The remediation path has the same per-document shape as the "
        "authorisation that permitted the harm, so recovery cost scales with "
        "attack volume while attack cost does not.",
        "**not yet measured** — X10 is pre-registered, with an advance "
        "prediction that it will weaken",
        "unknown; do not quote this until X10 has run",
        True,
        "Bulk reversal covering the attacked session cleanly at realistic "
        "detection latencies. See PREREG_SAP.md."),
]


def main():
    print("# Claim ledger — book two")
    print()
    print("*Generated by `python3 claims_sap.py`. All claims as of %s.*" % AS_OF)
    print()
    print("Every mechanism behind S1–S4 is reconstructed from secondary "
          "sources. `help.sap.com` and `community.sap.com` refused automated "
          "retrieval, and no modelled mechanism has yet been verified against "
          "primary vendor documentation — see loss L3 for what a later manual "
          "pass found, and the control surface specification for the current "
          "evidence level of each mechanism. Claims are about the "
          "reconstruction until that changes.")
    print()
    print("| | claim | source class | confidence | load-bearing |")
    print("|:--|:---|:---|:---|:--|")
    for c in LEDGER:
        print("| **%s** | %s | %s | %s | %s |"
              % (c.id, c.claim, c.source, c.confidence,
                 "**yes**" if c.load_bearing else "no"))
    print()
    print("## Falsification criteria")
    print()
    for c in LEDGER:
        print("**%s.** %s" % (c.id, c.falsifier))
        print()
    n_lb = sum(1 for c in LEDGER if c.load_bearing)
    n_unmeasured = sum(1 for c in LEDGER if "not yet measured" in c.source
                       or "not yet second-sourced" in c.source)
    print("---")
    print()
    print("*%d claims, %d load-bearing, %d of those resting on nothing "
          "measured yet.*" % (len(LEDGER), n_lb, n_unmeasured))


if __name__ == "__main__":
    main()
