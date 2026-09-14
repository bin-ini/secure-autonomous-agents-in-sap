"""
prereg_sap.py -- pre-registration for the SAP arm.

WRITTEN AND COMMITTED BEFORE THE EXPERIMENT EXISTS. That is the whole point:
the outcomes that would strengthen, weaken or eliminate the claim, plus the
result that would show the test is non-discriminating, are fixed while the
answer is still unknown.

The book's own audit (Appendix D.2) records that its monotonicity sweep failed
exactly this test -- run first, interpreted afterwards -- and that the
reframing which followed happened to be the one the data supported. It was
still post-hoc. This file exists so that does not happen twice.

    python3 prereg_sap.py > PREREG_SAP.md
"""
from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass
class Prereg:
    id: str
    name: str
    claim: str
    strengthen: str
    weaken: str
    eliminate: str
    non_discriminating: str
    boundary: str
    instrument_check: str
    cost: str
    status: str = "not run"


# The admission rule, in the precise form it needs for this paper.
#
# The first book's rule was: a test that cannot cost the model anything is not
# a test of the model. That was well formed while the MODEL was the subject.
# Here a mature control environment is the subject, so "cost" has to mean
# something else, and stating it loosely would let the rule be applied as
# ritual.
ADMISSION = (
    "An experiment belongs in this paper only if at least one PRE-DECLARED "
    "outcome removes a chapter's principal claim, transfers it to the chapter "
    "on controls that held, or reduces it to configuration guidance."
)

# Which of those three terminal outcomes each experiment actually had
# available. Checked, because an experiment with none of them is decoration.
CHAPTER_EFFECT = {
    "X7": ("A clean separator retaining acceptable legitimate throughput would "
           "have REDUCED THE FIRST STORY TO CONFIGURATION GUIDANCE -- 'set the "
           "tolerance group properly' -- and the chapter would not have been "
           "written. The realised outcome cost the principal claim its "
           "territory: from 'cannot express' to 'can bound only at a "
           "one-to-one loss of legitimate work'."),
    "X8": ("Detection by the ruleset as stated would have REMOVED THE SECOND "
           "STORY's principal claim. Detection only via the technical user "
           "would have "
           "TRANSFERRED it to the held register as a control that held. Both were "
           "pre-declared; the second turned out to be half true and is now "
           "held record H3."),
    "X9": ("Reconstruction from correlates would have REDUCED THE THIRD STORY "
           "TO DEPLOYMENT GUIDANCE -- 'derive the actor from what you already "
           "log'. That outcome was pre-declared and then not tested, which is "
           "loss L2. X12 is the repair and has since run; the rule-3 block it "
           "caused on gap G3 is lifted."),
    "X11": ("A content-ranging preventive decision found anywhere in the "
            "transport-governance surface REDUCES the standing P1 prediction "
            "TO CONFIGURATION AND PLACEMENT GUIDANCE — 'the mismatch is real "
            "at the authorisation object and is covered elsewhere in the same "
            "surface' — which is a smaller claim than the one the formalism "
            "currently carries, and removes transport from the paper's list "
            "of open mismatches. If instead the surface's only preventive "
            "decision ranges over the request, the subject mismatch survives "
            "against the full surface and the prediction is confirmed at its "
            "stated strength. Both are pre-declared."),
    "X12": ("Reconstruction of the deciding actor from correlates already "
            "logged would REDUCE THE THIRD STORY TO DEPLOYMENT GUIDANCE and "
            "would "
            "falsify the formalism's subject-mismatch clause, which asserts "
            "that no amount of retained history repairs a non-injective "
            "subject map. That clause is load-bearing: it is the half of the "
            "principle that is not about extent. This is the experiment loss "
            "L2 records as pre-declared and then not run."),
    "X10": ("Bulk reversal covering the attacked session would TRANSFER the "
            "whole of the recovery material out of the gap register and into "
            "the held register. That is the predicted outcome, "
            "and it is the only experiment in this paper whose predicted result "
            "damages the book's preferred conclusion."),
}

EVIDENCE_AT_PREREGISTRATION = "secondary_only"

EVIDENCE_STATES = {
    "secondary_only": "no primary vendor documentation incorporated",
    "primary_partial": "an independent retrieval route has identified primary "
                       "material, and no modelled mechanism has yet been "
                       "verified against it",
    "primary_verified": "at least one modelled mechanism carries a primary "
                        "source",
}

# Present-tense claims of ignorance that stop being true once the state moves.
STALE_IGNORANCE = ("no primary vendor documentation was read",
                   "no primary vendor documentation has been read",
                   "no primary source has been read",
                   "no primary sources have been read",
                   "nothing primary has been read")


def current_evidence_state() -> str:
    """Derived, never typed. At registration nothing primary had been read and
    that remains permanently true of X7-X9; the CURRENT state is a different
    fact and has already advanced."""
    try:
        from surface import MECHANISMS
        if any(m.level == "SAP" for m in MECHANISMS):
            return "primary_verified"
    except Exception:                            # noqa: BLE001
        pass
    try:
        from losses_sap import LOSSES
        if any("primary-source review" in l.how for l in LOSSES):
            return "primary_partial"
    except Exception:                            # noqa: BLE001
        pass
    return "secondary_only"


PREREG = [
    Prereg(
        "X7", "The missing rate limiter",

        "An authorisation model that decides per action and holds no aggregate "
        "state cannot express a constraint on outcome. A sequence of "
        "individually-authorised actions can therefore produce a harm that no "
        "configuration of that model prevents, and this is a property of the "
        "model rather than of any particular configuration of it. "
        "(New ledger entry S1.)",

        "The exhaustive sweep finds NO configuration of the modelled "
        "authorisation surface -- activity, organisational level, document "
        "type, per-document tolerance, per-line tolerance -- that permits the "
        "legitimate workload while denying the harmful sequence; and a control "
        "holding cumulative state does separate them. The gap is structural "
        "and the recommendation is to add state, not to configure better.",

        "Some configurations separate the two, but only by also denying a "
        "material fraction of the legitimate workload. The model can express "
        "the constraint, badly. The claim then becomes one about the cost of "
        "the available separation rather than about expressiveness, which is a "
        "weaker and much more ordinary finding.",

        "Some configuration separates them cleanly -- full legitimate "
        "throughput, harmful sequence denied. The claim is simply wrong: the "
        "authorisation model already covers the case and the correct advice is "
        "'configure it properly', which is the answer SAP practitioners have "
        "been giving for thirty years and would deserve to keep giving. The "
        "SAP thesis collapses and the chapter is not written.",

        "The harmful and legitimate sequences differ in any field the "
        "authorisation model ranges over -- a different transaction, company "
        "code, document type, or an amount distribution that does not overlap. "
        "If they do, the sweep separates them trivially and the experiment has "
        "measured how we constructed the attack, not what the model can "
        "express. The two workloads must be drawn from the SAME amount "
        "distribution, in the same company code, with the same document type, "
        "differing ONLY in count.",

        "SAP being unable to express the constraint is not a claim that SAP is "
        "insecure. It is a claim about where the control has to live. Nor may "
        "a falsification of this model be reported as a falsification of SAP: "
        "the authorisation surface here is reconstructed from SECONDARY "
        "sources, because help.sap.com and community.sap.com block automated "
        "retrieval. If SAP holds an aggregate mechanism we did not model, this "
        "result is about our model and must be withdrawn, not defended. The "
        "known aggregate-ish mechanisms -- FI tolerance groups, purchasing "
        "release strategies -- ARE modelled precisely so this defence is not "
        "available to us later.",

        "POSITIVE CONTROL. The same sweep is run against a second harmful "
        "sequence whose amounts lie ABOVE the legitimate distribution. The "
        "sweep MUST find a separating tolerance for that arm. If it does not, "
        "the instrument is broken and the primary result is uninterpretable -- "
        "not evidence for the claim. This is the check the monotonicity sweep "
        "did not have, and it is why that sweep spent an afternoon treating "
        "128 of its own bugs as a finding.",

        "a day",
        "RUN, 31 July 2026 -- matched the WEAKENING outcome, the second of the "
        "three branches. 12,288 configurations; 10,398 hold the outcome below "
        "materiality; the best of those retains 37.5% of legitimate "
        "throughput and none retains 95%. So the model CAN bound the outcome "
        "and the claim as written -- 'cannot express' -- is withdrawn. What "
        "replaces it is narrower: because the two workloads are per-document "
        "identical, any per-document predicate removes the same proportion of "
        "each, so harm can be reduced only by reducing the work at a one-to-one "
        "exchange rate. The surface can throttle; it cannot discriminate. "
        "Positive control passed (clean separation at 100% throughput when the "
        "harmful amounts lie above the legitimate band), so the null is about "
        "the arm and not the instrument."),

    Prereg(
        "X8", "Composed authority across propagated principals",

        "A segregation-of-duties ruleset that is a static predicate over role "
        "assignments cannot see a duty conflict composed across two principals "
        "by one agent, because the conflict exists in the workflow and not in "
        "either principal's grant. (New ledger entry S2.)",

        "Each propagated principal passes the SoD ruleset individually and in "
        "every pairwise combination the ruleset examines, while the composed "
        "sequence executed by the agent completes the conflicting pair of "
        "duties and produces the harm the rule exists to prevent.",

        "The ruleset catches it, but only because the technical user under "
        "which the agent runs accumulates both grants -- i.e. it is caught as "
        "an ordinary SoD violation on a service account, which is a known "
        "finding and needs no new argument. The contribution shrinks to "
        "'remember to run ARA against technical users'.",

        "The conflict is visible to the ruleset as stated, with no change to "
        "how SoD is evaluated. S2 is wrong and the SoD material is dropped.",

        "The agent is modelled as holding both roles at once. Then the result "
        "is a restatement of ordinary SoD and says nothing about composition. "
        "Each session must hold exactly one principal's grants and nothing "
        "must persist between them except the world state.",

        "Demonstrating that a static analysis misses a dynamic composition is "
        "close to a definitional result, and it must be reported as one. The "
        "contribution, if any, is not the discovery but the location: that the "
        "control which enterprises rely on most heavily for this exact class "
        "of harm is the one whose assumption agents break.",

        "The composed sequence must also be shown to be harmful when executed "
        "by two HUMANS in collusion -- i.e. the harm is real and pre-existing. "
        "If it is not, we have invented a harm to fit the control.",

        "half a day",
        "RUN, 31 July 2026 -- matched the STRENGTHENING outcome, but the "
        "result that matters was not among the three. Both propagated "
        "principals pass the ruleset; the composition completes; the payment "
        "reaches the attacker account. The instrument check confirms two "
        "colluding humans produce the identical harm, so agents introduce no "
        "new harm and the contribution is about price, not possibility. The "
        "unanticipated finding: the technical user -- which every checklist "
        "marks as the worse architecture because it accumulates grants -- IS "
        "flagged by the ruleset, while principal propagation, the design a "
        "reviewer would prefer, is the one that renders the composition "
        "invisible. The control rewards the architecture that gives it "
        "something to look at. That inversion was not in any of the three "
        "pre-registered outcomes, which is the second time in this project a "
        "pre-registration has been bounded by its author's imagination."),

    Prereg(
        "X9", "Attribution from the evidence layer alone",

        "An audit record keyed on principal identity cannot answer whether an "
        "action was taken by a human or by an agent, and therefore cannot "
        "support the first question of an incident response. (New ledger "
        "entry S3.)",

        "A responder reconstructing the incident from the log alone attributes "
        "0 of N agent actions correctly; adding a single actor field takes it "
        "to N of N.",

        "Partial reconstruction is possible from correlates -- timing density, "
        "session identifiers, terminal fields -- so the gap is real but "
        "narrower than stated, and the recommendation becomes 'derive the "
        "actor' rather than 'record it'.",

        "The existing record already distinguishes them reliably. S3 is wrong.",

        "We define both the log format and the reconstruction procedure, so a "
        "0-to-N result is arithmetic, not measurement. This experiment CANNOT "
        "produce a discovery and is not being run as one.",

        "This is stated in advance to be a DEFINITIONAL result and will be "
        "reported as such. Its value is entirely in the size of the repair -- "
        "one field -- and it may not be presented as evidence for anything "
        "else. If the write-up leans on X9 to support S1 or S2, the write-up "
        "is wrong.",

        "Not applicable; nothing here can fail informatively. Included in the "
        "register for completeness and to fix its status before anyone is "
        "tempted to describe it as a finding.",

        "an hour",
        "RUN, 31 July 2026 -- 0 of 520 actions attributable as logged, 520 of "
        "520 with one added field. Exactly the arithmetic predicted, exactly "
        "as uninformative as declared. Recorded here so that the number cannot "
        "later be cited as evidence for anything."),

    # -----------------------------------------------------------------------
    # X11 and X12 were registered on 8 August 2026, after X7-X9 had run and
    # after the frame was fixed. Two things follow and both are stated rather
    # than left to be noticed.
    #
    # First, they inherit loss L1: the frame was already in hand when they were
    # written, so neither is a prospective test OF the frame. They are
    # prospective tests of two specific clauses of the formalism, which is a
    # smaller and different thing.
    #
    # Second, the ordering is checkable rather than asserted. This block was
    # committed before either experiment's code existed, and `git log` on
    # `prereg_sap.py` against `sapsec/transport.py` and `sapsec/attribution.py`
    # shows it. That is the only form of pre-registration a single-author
    # repository can actually offer, and it is offered here instead of a
    # promise.
    # -----------------------------------------------------------------------

    Prereg(
        "X11", "The transport-governance surface (P1, respecified)",

        "The standing prediction P1 says release authorisation cannot "
        "discriminate a harmful transport, because its predicate is about the "
        "request while the property is about the behaviour of what the request "
        "contains. The counterfactual audit ruled that prediction "
        "MISSPECIFIED: release authorisation never claimed behavioural safety, "
        "and a reviewer would dismiss it in one sentence. This experiment "
        "tests the respecified question instead — **does the complete modelled "
        "transport-governance surface contain a content-ranging decision "
        "capable of discriminating the defined harmful transport BEFORE "
        "release?** The claim under test is that only content-ranging "
        "preventive decisions can do it, and that their coverage of a given "
        "harm is a parameter a deployment sets rather than a property the "
        "surface guarantees.",

        "No decision anywhere in the modelled surface — preventive or "
        "detective — ranges over the behaviour of the transported object. "
        "Every gate is about the request, its owner, its target, or the "
        "identity of an approver. The subject mismatch survives against the "
        "full surface and P1 stands at the strength the formalism gives it.",

        "The surface contains a content-ranging preventive decision that "
        "separates the harmful transport from the legitimate ones. P1 narrows "
        "to the authorisation object alone — which is where the counterfactual "
        "audit said it should always have been aimed — and transport leaves "
        "the paper's list of open mismatches, becoming a control-placement "
        "finding of the same shape as Availability Control.",

        "Release authorisation ITSELF discriminates: some configuration of "
        "`S_TRANSPRT` separates harmful from legitimate transports without "
        "reading their content. The formalism's subject-mismatch derivation is "
        "then wrong, and `mismatch.py --check` fails by construction rather "
        "than by anyone's judgement.",

        "The harmful and legitimate transports differ in any request-level "
        "field — owner, target system, object type, object count, request "
        "class. If they do, a metadata rule separates them and the experiment "
        "has measured how we built the transport, not what the surface can "
        "decide. Enforced in code by `assert_transport_indistinguishable()`. "
        "A second and subtler form: if the harmful behaviour is chosen to "
        "match a rule the modelled static-check catalogue contains by "
        "construction, the weakening outcome is manufactured. Catalogue "
        "coverage must be swept as a parameter and the result reported on both "
        "branches.",

        "The modelled surface is a reconstruction. Whether SAP's delivered ATC "
        "check variants contain a rule matching this harm class is NOT "
        "answered here and may not be reported as if it were. What the "
        "experiment can establish is the SHAPE of the surface — which "
        "decisions range over content, which are preventive, which are "
        "advisory — and how the outcome depends on parameters a deployment "
        "sets. Nor may a human review step be assigned a detection rate: "
        "coverage is swept across its whole range and reported as a surface, "
        "the discipline the materiality figure got in X7. A finding that "
        "'review catches it' at an assumed rate would be a finding about the "
        "assumption.",

        "POSITIVE CONTROL. The same surface is run against a transport whose "
        "release is attempted by a principal WITHOUT `S_TRANSPRT ACTVT 43`. "
        "Authorisation MUST refuse it, in every configuration. If it does not, "
        "the modelled surface is broken and nothing it says about "
        "content-ranging decisions is interpretable.",

        "half a day",
        "RUN, 8 August 2026 -- matched the WEAKENING outcome, and the third "
        "branch fired as well. Of the configurations whose active steps range "
        "only over the request, none discriminates and every harmful "
        "transport reaches production in every one of them, so the prediction "
        "held at the pair it names. But a fifth of the space does "
        "discriminate and every configuration in it has a content-ranging "
        "preventive step active, so P1 narrows to the authorisation object "
        "and transport leaves the list of open mismatches. The third branch: "
        "wherever the only content-ranging step is detective, forty of forty "
        "harmful transports are flagged and forty of forty are in production, "
        "so the paper now has to separate preventive from detective coverage. "
        "The exact counts are in the results section and are not repeated "
        "here, because the first version of this line repeated them and they "
        "went stale within a day. **The experiment also produced a "
        "retraction**: its first version had no channel through which a "
        "content-ranging step could stop a benign change, so it reported zero "
        "cost as a measurement. That is loss L6, and the surviving claim is "
        "about kind rather than price. Positive control passed."),

    Prereg(
        "X12", "Attribution from correlates (the repair for loss L2)",

        "The formalism's SUBJECT-MISMATCH clause, which is the half of the "
        "principle that is not about extent. G3 says the Security Audit Log's "
        "subject — the authenticated principal — maps non-injectively onto the "
        "property's subject, the deciding actor, and that this is a projection "
        "failure rather than a memory failure: no depth of retained history "
        "repairs it. X9 measured only whether an actor field exists, which was "
        "arithmetic. This measures whether the actor can be RECONSTRUCTED from "
        "correlates that are already recorded.",

        "Attribution accuracy is invariant to retention depth — a responder "
        "holding one record does no worse than one holding the whole period — "
        "and rises only when a field that distinguishes the actors is present. "
        "The subject/extent distinction is doing real work, and G3 becomes a "
        "measured result rather than a definitional one.",

        "Accuracy rises materially with retention depth under some conditions "
        "and not others. The clause is then true only where the correlates do "
        "not separate, and must be restated with those conditions attached. G3 "
        "narrows to interleaved execution under a shared session identity, "
        "which is a smaller claim than the one the formalism now makes.",

        "Accuracy approaches certainty from retained correlates alone, with no "
        "distinguishing field added. The subject-mismatch clause is false as "
        "written, the repair is deployment guidance — derive the actor from "
        "what you already log — and the attribution material shrinks to a "
        "note. This is the outcome pre-declared for X9 and never tested, and "
        "it is the reason L2 is recorded as a loss.",

        "The actors are made distinguishable by construction — different "
        "terminals, different transaction codes, disjoint object ranges, or "
        "timestamps fine enough that no two actions collide. Correlation then "
        "succeeds trivially and the experiment has measured the construction. "
        "The baseline condition must be the one principal propagation actually "
        "produces: one technical user, one terminal, interleaved actions. "
        "Every distinguishing field is a swept parameter, never a default.",

        "This is a reconstruction of one evidence stream's record shape, not a "
        "measurement of SAP's audit capability. SAP writes several — change "
        "documents, table logging, application logs, read-access logging — and "
        "only the modelled correlates are available to the procedure. A "
        "negative result is a result about the modelled evidence surface and "
        "must be labelled so. A positive result may not be reported as 'SAP "
        "can attribute': it would establish that one correlation procedure "
        "over one record shape recovers the actor, which is a statement about "
        "the procedure and the schema together.",

        "POSITIVE CONTROL. The same procedure is run on a single-actor "
        "session. It MUST attribute every action correctly. A procedure that "
        "cannot name the actor when there is only one candidate is broken, and "
        "the multi-actor accuracies from it would mean nothing.",

        "half a day",
        "RUN, 8 August 2026 -- matched the STRENGTHENING outcome. 512 "
        "conditions. Retention depth changed nothing in any of the 18 "
        "condition groups where no recorded field separated the actors, and "
        "the best accuracy reached in any of them is chance. Of the 264 "
        "conditions that did attribute at 95% or better, every one had a "
        "field naming the origin. Retention moved the result in 28 of 96 "
        "groups and in every one of those a separating field was already "
        "present, so retention improves how well an existing signal is used "
        "and does not create one. The practitioner's objection was answered "
        "with a bound rather than a classifier: the best accuracy available "
        "to ANY procedure reading principal, transaction code, terminal and "
        "timestamp equals the do-nothing majority baseline at every agent "
        "action rate tested. Positive control passed on all 128 single-actor "
        "conditions. The procedure itself produced two rounds of artefactual "
        "results before this one; that is loss L4."),
]

# X10 IS NOT IN THIS PAPER, and the decision is recorded rather than implied.
#
# X10 was designed as the repair for loss L1: the only experiment registered
# after chapter 1's maturity-versus-structure frame was fixed, and therefore
# the only prospective test of that frame. Keeping it made the frame's
# validation a release blocker for a paper whose contribution is not the frame.
#
# The fork was real and both halves could not be held at once. Resolved by
# taking the narrower paper: the frame is admitted as RETROSPECTIVE and
# non-load-bearing here, chapter 1 may not claim prospective validation, and
# X10 moves to the research programme. `manifest_sap.check()` enforces the
# label; if X10 ever returns to PREREG, that check must be revisited.
FUTURE = [
    Prereg(
        "X10", "Recovery and financial reversibility (the held register)",

        "The remediation path has the same per-document shape as the "
        "authorisation that permitted the harm. Reversal cost therefore scales "
        "with the volume of the attack while the attack's own cost does not, "
        "and a fraction of the harm crosses an irreversibility boundary that "
        "grows with detection latency. (New ledger entry S4.)",

        "Bulk reversal fails to cover a material fraction of the attacked "
        "session -- documents blocked because they are cleared, because the "
        "period has closed, or because the payment medium has already been "
        "transmitted -- and the reversible fraction falls steeply with "
        "detection latency across ordinary payment-run cadences.",

        "Mass reversal covers most of it and the residue is small and "
        "predictable. The chapter shrinks from a finding to a practitioner "
        "note: use F.80, watch the clearing status, reconcile the remainder. "
        "Worth two pages, not a chapter.",

        "SAP's bulk reversal handles the entire attacked session cleanly at "
        "every realistic detection latency. S4 is wrong, financial recovery is "
        "a solved problem in this system, and the material is dropped rather than "
        "rewritten. This would be a good outcome for anyone running SAP and a "
        "bad one for the book, which is the correct asymmetry.",

        "The irreversibility is manufactured by choosing a payment cadence "
        "that guarantees clearing before detection. Cadence and latency must "
        "both be swept and the result reported as a surface, not asserted at "
        "one convenient point -- the same discipline the materiality figure "
        "got in X7.",

        "A reversal that restores the BALANCE is not a reversal that restores "
        "the WORLD. If the argument comes to rest on the vendor having already "
        "shipped or the customer having already spent the credit, that is a "
        "claim about business process and not about SAP, and must be labelled "
        "as such rather than counted as evidence for S4. Separately: this is "
        "the first book's recovery edge arriving in a second system. If the "
        "result reduces to a restatement of R1-R4, it is a replication and "
        "must be reported as a replication, which is worth something and is "
        "not worth a chapter.",

        "POSITIVE CONTROL. The same machinery is run against a small harm "
        "caught immediately -- a handful of documents, same period, nothing "
        "cleared. It MUST reverse completely and leave the ledger balance "
        "where it started. If the model cannot reverse even that, the model is "
        "broken and no conclusion about SAP is available from it.",

        "a day or two"),
]

# ---------------------------------------------------------------------------
# D1 -- the countermechanism determination.
#
# Not an experiment. A determination against primary sources, and it is
# pre-registered for exactly the same reason the experiments are: the answer is
# unknown, four interpretations are available, and choosing between them after
# the documentation has been read is how a project talks itself into the
# reading it prefers.
#
# The question is path-binding, not a general survey of SAP's capabilities:
#
#     Can F110, Availability Control, or another standard SAP mechanism
#     PREVENTIVELY evaluate cumulative credited value for the exact
#     credit-memo process, control object, product and release used in X7?
#
# All four outcomes below are committed before the determination is made. Note
# that two of them remove the paper's surviving finding, and the project would
# be better off if one of those turned out to be true -- an organisation that
# can already configure this control is in a better position than one that
# cannot.
DETERMINATION = [
    ("Availability Control directly governs the tested path",
     "G1 ceases to be a control gap and becomes a **control-placement or "
     "configuration finding**: the mechanism exists, binds this path, and was "
     "not switched on. The paper's principal empirical claim is withdrawn and "
     "replaced by a smaller, more actionable one."),

    ("Availability Control can be bound to the path through supported "
     "composition",
     "Same conclusion, with the implementation dependencies stated explicitly. "
     "The finding becomes about the cost and the prerequisites of binding it, "
     "not about absence."),

    ("Availability Control exists but cannot govern that path or that "
     "protected property",
     "G1 survives **narrowly**, as a path-specific mismatch — and SAP itself "
     "supplies the strongest evidence that the required control shape is "
     "feasible, which makes the repair recommendation far harder to dismiss "
     "than a mechanism borrowed from another industry."),

    ("F110 or another standard mechanism closes the tested path",
     "G1 is revised or eliminated as a SAP-path mismatch. The formal result "
     "about control-property pairs is untouched; the SAP instantiation of it "
     "is not."),
]

# X10 now carries a second job, and it is the more important one.
#
# Loss L1 records that chapter 1's falsification frame was written after X7, X8
# and X9 had already run. Every one of those had its own pre-registration, so
# no individual result was shaped to fit -- but the FRAME was chosen with the
# results in hand, which is the defect the first book records against its own
# monotonicity sweep.
#
# X10 is the repair. It is the first experiment pre-registered while the frame
# is already fixed and public, and its expected outcome -- that SAP's reversal
# machinery largely holds -- is a gap VANISHING, which is precisely chapter 1's
# falsification condition. An experiment whose predicted result weakens the
# book's own thesis, registered in advance, is the only thing that makes the
# frame a test rather than a description.
FRAME_TEST = (
    "X10 was the only experiment registered AFTER chapter 1's frame was fixed, "
    "and therefore the only prospective test of it available. It has been "
    "moved out of this paper. The consequence is stated rather than softened: "
    "**chapter 1's maturity-versus-structure frame is retrospective and is not "
    "load-bearing for this paper's contribution.** It organises the "
    "presentation; it is not offered as validated, and no artefact here may "
    "describe it as tested."
)

# ---------------------------------------------------------------------------
# A prediction, recorded before X10 is built.
#
# The first book attacked one recovery edge and it lost half of itself: two of
# four recovery attacks turned out to be closed by controls that already
# existed, and the edge survived at reduced size. That is the only prior
# available, it is drawn from one observation, and it points at the WEAKENING
# outcome above rather than the strengthening one.
#
# Writing it down costs nothing now and costs something later, which is the
# point. If X10 comes back strengthening, this note says the prediction was
# wrong. If it comes back weakening, this note stops the result being narrated
# afterwards as though it had been obvious.
# ---------------------------------------------------------------------------
PREDICTION = (
    "X10 will match the WEAKENING outcome: bulk reversal will cover most of "
    "the attacked session, and what survives will be a narrower claim about "
    "the fraction that has crossed a payment boundary. Confidence: low. One "
    "prior observation, in a different system, about a differently shaped "
    "control."
)


def check() -> list[str]:
    """Every experiment must have a declared chapter-level adverse outcome,
    and no artefact may assert an ignorance the project has outgrown."""
    problems = []
    # Scan the SOURCES, not the generated markdown.
    #
    # Three earlier versions of this check were defective and each defect
    # hid the next. It exempted `PREREG_SAP.md`, which concealed a second
    # copy of the phrase inside that very file -- surfaced only when the
    # assembler pulled it into the manuscript. It read generated markdown,
    # which `build.sh` rewrites AFTER the checks run, so it was always
    # judging the previous build. And it reported the file that declares the
    # forbidden list. Reading the sources with the declaration stripped fixes
    # all three: prose lives in the sources, the sources are what a person
    # edits, and nothing is exempt.
    if current_evidence_state() != EVIDENCE_AT_PREREGISTRATION:
        import glob
        import os
        here = os.path.dirname(os.path.abspath(__file__))
        for f in sorted(glob.glob(os.path.join(here, "*.py"))):
            src = open(f).read()
            for phrase in STALE_IGNORANCE:
                src = src.replace('"%s"' % phrase, "")
                src = src.replace("'%s'" % phrase, "")
            low = src.lower()
            for phrase in STALE_IGNORANCE:
                if phrase in low:
                    problems.append(
                        "%s asserts %r in the present tense while the "
                        "evidence state is %r -- say what was true at "
                        "registration, in the past tense"
                        % (os.path.basename(f), phrase,
                           current_evidence_state()))
    for x in PREREG:
        if x.id not in CHAPTER_EFFECT:
            problems.append("%s declares no chapter-level adverse outcome -- "
                            "it cannot cost the book anything and does not "
                            "belong in it" % x.id)
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   %d experiments, all with a declared chapter-level adverse "
              "outcome." % len(PREREG))
        return
    print("# Pre-registration — SAP arm")
    print()
    print("*Generated by `python3 prereg_sap.py`. Do not edit by hand.*")
    print()
    print("> **%s**" % ADMISSION)
    print()
    print("The first book's rule -- *a test that cannot cost the model "
          "anything is not a test of the model* -- was well formed while the "
          "model was the subject. Here a mature control environment is the "
          "subject, so a chapter surviving with a smaller claim is a real "
          "adverse outcome, and so is a claim moving into the chapter on "
          "controls that held.")
    print()
    print("| experiment | the adverse outcome that was available |")
    print("|:---|:---|")
    for _x in PREREG:
        print("| **%s** | %s |" % (_x.id, CHAPTER_EFFECT.get(_x.id, "—")))
    print()
    _run = [x for x in PREREG if x.status.startswith("RUN")]
    print("**%d experiments are registered for this paper; %d have run.** D1 "
          "below is a pre-registered countermechanism determination, not an "
          "experiment. %d further experiment (X10) is registered for the "
          "research programme and is deliberately NOT a blocker for this "
          "paper — see the note beside `FUTURE`."
          % (len(PREREG), len(_run), len(FUTURE)))
    print()
    print("One of them — X9 — is declared in advance to be incapable of "
          "failing informatively, and is registered anyway so that its status "
          "is fixed before the results make it tempting to describe it as a "
          "discovery.")
    print()
    print("Every claim below rests on an authorisation model reconstructed "
          "from secondary sources. `help.sap.com` and `community.sap.com` "
          "refused automated retrieval, so at the time these experiments were "
          "registered and run no primary vendor material had been "
          "incorporated. That remains permanently true of X7 to X9. The "
          "project's evidence state has since advanced and is tracked in loss "
          "L3 and determination D1; the current state is **%s**. Where the "
          "reconstruction is wrong, the results are about the "
          "reconstruction." % EVIDENCE_STATES[current_evidence_state()])
    print()
    for x in PREREG:
        print("## %s — %s" % (x.id, x.name))
        print()
        print("*Cost: %s · Status: %s*" % (x.cost, x.status))
        print()
        print("**Claim under test.** %s" % x.claim)
        print()
        print("| outcome | means |")
        print("|:---|:---|")
        print("| strengthens | %s |" % x.strengthen)
        print("| weakens | %s |" % x.weaken)
        print("| eliminates | %s |" % x.eliminate)
        print("| non-discriminating | %s |" % x.non_discriminating)
        print()
        print("**Interpretation boundary.** %s" % x.boundary)
        print()
        print("**Instrument check.** %s" % x.instrument_check)
        print()
    print("## D1 — the countermechanism determination")
    print()
    print("*Committed before the primary sources are read.* The question is "
          "path-binding, not a survey: **can F110, Availability Control, or "
          "another standard SAP mechanism preventively evaluate cumulative "
          "credited value for the exact credit-memo process, control object, "
          "product and release used in X7?**")
    print()
    print("| if | then |")
    print("|:---|:---|")
    for cond, then in DETERMINATION:
        print("| %s | %s |" % (cond, then))
    print()
    print("Two of the four remove the paper's surviving finding. The project "
          "would be better off if one of those were true: an organisation that "
          "can already configure this control is in a better position than one "
          "that cannot, and a paper is a worse reason to prefer an answer than "
          "that is.")
    print()
    print("## The frame, and what it is not")
    print()
    print("> " + FRAME_TEST)
    print()
    print("## A prediction, recorded before X10 is built")
    print()
    print("> " + PREDICTION)
    print()
    print("The first book attacked one recovery edge and it lost half of "
          "itself. That is the only prior available, it rests on a single "
          "observation in a different system, and it points at the weakening "
          "outcome rather than the strengthening one. Recording it costs "
          "nothing now and costs something later, which is the point.")
    print()


if __name__ == "__main__":
    main()
