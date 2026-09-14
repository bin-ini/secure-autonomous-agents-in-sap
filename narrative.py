"""
narrative.py -- the spine.

    python3 narrative.py            # the connective tissue
    python3 narrative.py --check    # the trajectory must match the artefacts

Everything else in this repository is an artefact. This is the thread that
makes seven correct artefacts feel like one discovery, and it is the last thing
written rather than the first, because the story is what the evidence turned
out to be and not what anyone hoped it would be.

Two rules hold it honest.

The opening incident ASKS. It ends on a question the reader cannot answer yet,
and `--check` fails if the scenario contains a verdict — because an opening
that has already decided the control failed is not a mystery, it is an
accusation with a preamble.

The claims trajectory is DERIVED. Every reversal in it is read from the
artefact that forced it — the counterfactual audit, the loss register — rather
than typed here. A narrative of how the argument changed is exactly the kind of
prose that quietly flatters its author, so it is generated like every other
number in this project.
"""
from __future__ import annotations

import sys

# ---------------------------------------------------------------------------
# 1. The opening incident. Fictional, technically bounded, no customer
#    material of any kind. It ends on a question.
# ---------------------------------------------------------------------------

INCIDENT = """
An autonomous finance agent is given authority to process ordinary customer
credit memos: dispute resolution, one company code, one document type, amounts
in the range the team has handled for years. It runs for a period.

Every individual document is inside the configured tolerance. Every
authorisation check succeeds. No company-code boundary is crossed. No
abnormal document is posted. Nothing in the audit log is out of order, and
nothing in it is false.

At the end of the period, the cumulative credited value exceeds the
organisation's materiality threshold.

**Did the control fail?**
""".strip()

# A verdict here would give the answer away and turn the mystery into an
# accusation. Checked.
VERDICT_WORDS = ("failed.", "the control was inadequate", "obviously",
                 "of course", "clearly the control", "sap failed",
                 "this proves", "demonstrates that the control")

# ---------------------------------------------------------------------------
# 2. The antagonist
# ---------------------------------------------------------------------------

ANTAGONIST = (
    "A mismatch between the unit a control evaluates and the unit over which "
    "the protected property is defined.")

ANTAGONIST_NOTE = """
Not SAP. Not legacy authorisation. Not even autonomy. The conflict this paper
is about is **local correctness against global protection**, and the evidence
says so in both directions: two of the controls examined were locally correct
*and* globally sufficient, one was locally correct and globally silent, and the
difference between them is derivable before any attack is run.
""".strip()

# ---------------------------------------------------------------------------
# 3. The turning point
# ---------------------------------------------------------------------------

TURN = """
The obvious reading of the incident is that a document-local control cannot
govern a period-level property, and that wider harms therefore need wider
controls. That reading is wrong, and the control that disproves it is
unremarkable.

Organisational-level authorisation observes one action. The property an
organisation actually wants is wider — that *no part of the workflow* touches a
unit outside the grant. The extents do not match. The control guarantees the
property anyway, because refusing every out-of-unit action means no sequence
assembled from permitted ones can leave the unit. The local predicate composes
into the global guarantee.

So an observation-boundary mismatch is a reason to *investigate*, never a
reason to *conclude*. The next question, and the one that does the work, is
whether the locally enforced predicate composes into the property being
claimed. Tolerance groups do not: no per-document allowance that admits the
legitimate population implies a bound on the sum of the population.

That is the whole difference between the two halves of the incident.
""".strip()

# ---------------------------------------------------------------------------
# 4. What autonomy actually changed
# ---------------------------------------------------------------------------

# The four axes, named once, in a data structure so the prose and the figure
# cannot drift apart. Each is (label, one-line effect).
AXES = [
    ("Action volume",
     "a mismatch a human would take a year to express is expressed in an "
     "afternoon"),
    ("State accumulation",
     "a property defined over a period is breached inside one"),
    ("Decision chaining across contexts",
     "one session, one principal, one company code at a time, so a constraint "
     "that ranges over the whole workflow is never in view at any single step"),
    ("Boundary exposure",
     "all of it stays inside every local boundary, so the limits of what a "
     "control observes are reached faster than any human workload would reach "
     "them"),
]

AUTONOMY_LEAD = (
    "The agent did not invent the possibility of cumulative harm. A sufficiently "
    "patient person with an ordinary authorisation could always post a great "
    "many ordinary documents. What autonomous action selection changes is not "
    "the ceiling of what is possible but the rate at which it is reached — and "
    "it does so along four axes at once:")

AUTONOMY_TAIL = (
    "None of these requires the agent to be intelligent, adversarial or wrong; "
    "they are properties of speed and composition, not of cognition. The "
    "security question is therefore not whether agents reach a new prohibited "
    "action, but whether autonomous composition makes a protected property "
    "depend on a unit larger than the unit the deployed control evaluates — and "
    "every one of the four axes makes that dependence more likely to bite in "
    "practice, sooner.\n\n"
    "*This is an architectural interpretation, not a measured claim, and it is "
    "labelled as one throughout.*")

# ---------------------------------------------------------------------------
# 4b. The same shape, arriving from the adversarial direction. A real,
#     documented incident -- offered as illustration of the structure, never
#     as evidence for the measurements that follow.
# ---------------------------------------------------------------------------

REALWORLD = """
The structure is not hypothetical, and it is not confined to finance. In July
2026 Hugging Face disclosed that an autonomous agentic framework had moved
through its production infrastructure over roughly four and a half days,
executing on the order of 17,600 individual actions grouped into some 6,280
clusters. For the argument here, the striking feature is not the breach but its
shape. Almost every individual action was benign in isolation — routine
reconnaissance, ordinary file reads, the kind of cluster-introspection query a
legitimate job makes — and the existing per-action controls passed each step:
an allow-list that correctly refused a remote fetch could not tell a legitimate
local file read from one that disclosed a secret. In the vendor's own account,
"most actions went nowhere. Together, however, they produced enough coverage to
find a viable chain across several independent systems." No single step was the
harm; the campaign was, and human analysts could not correlate thousands of
individually-unremarkable events in real time.

That is the structure the finance scenarios in this paper isolate, arriving
from the adversarial direction rather than the ordinary-operations one: harm
assembled from individually-permitted actions, each locally compliant,
composing into an outcome no single action would have been allowed to produce,
and invisible to any control that decides one action at a time. The incident is
offered as an illustration of the shape, not as evidence for the measurements
that follow — it is an adversarial intrusion, and the modelled scenarios are
non-adversarial. What the two share is the gap, and an autonomous agent is what
made the gap move fast enough, and compose across enough steps, to matter.

*Source: Hugging Face, "Security incident disclosure — July 2026," and the
accompanying technical timeline (huggingface.co/blog/security-incident-july-2026).*
""".strip()

# ---------------------------------------------------------------------------
# 5. The three stories, as escalating dramatic functions
# ---------------------------------------------------------------------------

STORIES = [
    ("Admit one",
     "The method accepts a failure",
     "The same tolerance control, unchanged, against two properties the "
     "organisation itself claims. Against the document-local one it separated "
     "completely and cost nothing. Against the period-aggregate one it could "
     "reduce harm only by refusing legitimate work drawn from the same "
     "distribution. Stated flatly, because it earned that."),

    ("Contest one",
     "The method catches the author moving the goalposts",
     "Segregation of duties looked like the next failure. It is not. SAP's "
     "control is stated around conflicting access assigned to a user, and the "
     "experiment confirms it detects exactly that — the technical user holding "
     "both grants is reported. The failure appears only after substituting a "
     "stronger property: that no single decision process should complete both "
     "sides. That may be an important property for autonomous systems. It is "
     "ours, and it is not evidence that SAP's claimed control failed."),

    ("Block one",
     "The method stops the paper publishing an unsupported result",
     "Attribution was going to be the easy chapter: the log names a principal, "
     "the principal is a human, the agent is invisible. The method refused it "
     "twice. The strongest reconstruction from existing correlates — timing "
     "density, session identifiers, terminal fields — was named in the "
     "experiment's own pre-registration and never attempted. And 'accountable "
     "principal' and 'deciding actor' are both defensible audit subjects, so "
     "the property is contested as well as the evidence. This is the climax of "
     "the method, because it is where the instrument says *this experiment is "
     "not entitled to a finding.*\n"
     "\n"
     "One of those two blocks has since been cleared, by doing the work rather "
     "than by arguing it away. The correlates were tested (X12) and they do "
     "not recover the actor: retention depth changed nothing wherever no "
     "recorded field separated the actors, and for the objection a "
     "practitioner would actually raise — an agent posting hundreds of "
     "documents in minutes is obviously not a person — the best accuracy "
     "available to any procedure equals the accuracy of naming the busiest "
     "actor without reading anything. A density signal can say that the "
     "period was busy. It cannot say which of the actions in it were the "
     "machine's, and the presence test written for this experiment fires even "
     "where neither actor exceeds human speed, so it is a load detector and "
     "is reported as one. The property remains contested and the gap survives "
     "smaller, which is what a block is supposed to lead to."),

    ("Narrow one",
     "The method makes a prediction, is told the prediction is unfair, and "
     "loses the argument",
     "The formalism predicted that transport release authorisation could not "
     "discriminate a harmful transport, because its predicate is about the "
     "request and the property is about what the request does. The "
     "specification-sensitivity audit refused it before it was ever run: "
     "release authorisation has never claimed behavioural safety, a reviewer "
     "would say so in one sentence, and testing it against that property was "
     "choosing the wrong pair. Respecified against the whole governance "
     "surface and run, the prediction held exactly where it was aimed — "
     "among the configurations whose decisions range only over the request, "
     "none discriminates and every harmful transport reaches production, at "
     "every setting of every parameter — and was made irrelevant by the same "
     "experiment, because the surface holds content-ranging decisions the "
     "prediction had ignored. Transport leaves the list of open mismatches.\n"
     "\n"
     "What it leaves behind is a distinction the paper did not have, and "
     "arriving at it cost a retraction. The first version of the experiment "
     "reported that the subject-matched control stopped the harm at no cost "
     "to legitimate work, and set that beside X7\'s one-to-one exchange rate "
     "as the strongest thing in the paper. It was a property of the model: "
     "nothing in it allowed a content-ranging step to stop a benign change, "
     "so of course nothing benign was stopped. That is loss L6. With a "
     "false-positive rate in the model and swept, what survives is smaller "
     "and is about kind rather than price. Where the property outruns the "
     "control\'s extent, the exchange rate is forced by the pair and no "
     "implementation can improve it. Where the control reads the property\'s "
     "own subject, nothing is forced — and a bad implementation can squander "
     "the whole advantage."),
]

# ---------------------------------------------------------------------------
# 6. The reversal
# ---------------------------------------------------------------------------

REVERSAL = """
By this point the argument had a shape: a document-local control, a
period-level harm, no aggregate-state enforcement anywhere in the authorisation
surface, and a repair borrowed from card payment authorisation, which has done
velocity and cumulative checks for decades.

Then a reviewer, reading the primary documentation this project's own toolchain
could not reach, found Availability Control: accumulated consumption evaluated
against a consumable budget per control object, with configurable thresholds,
raising an error while a document is being checked or posted. Aggregate state,
at the decision point, enforced preventively — inside SAP.

Two sentences died. *SAP lacks aggregate-state control* is false. *The repair
must be borrowed from another industry* is unnecessary. Whether Availability
Control binds the credit-memo path modelled here is unresolved, and the honest
position is that it may narrow the surviving finding to a control-placement
problem.

Either way the question got better. It is no longer *why did SAP never build
this*. It is **why is the control shape available in one SAP domain and absent,
unavailable or unconfigured on another path with the same cumulative-risk
shape** — a question an architect can answer, and this paper cannot.
""".strip()

# ---------------------------------------------------------------------------
# 7. The ending
# ---------------------------------------------------------------------------

CLOSING_LINE = ("The purpose of the review is not to find more control "
                "failures. It is to make false claims of control failure "
                "harder to publish.")

# The coda. Where the arc actually ends: not on the finding, not on SAP, not on
# the instrument, but on the assumption the whole investigation stresses. Framed
# as the lens the work adopts and the question it sharpens -- not as a proven law
# about every enterprise, which the claim ledger (S0) forbids.
CODA_TITLE = "What this was actually about"

CODA = """
This work began as a search for SAP control failures under autonomous
execution. It ended somewhere else. Most of the failures it went looking for
dissolved the moment their protected properties were stated precisely; the one
that survived did not arise because a control was missing, but because the
property being defended lived at a larger observational scope than the control
evaluating it.

That reframes the concern. The assumption under stress is one every control
environment quietly relies on — that if each action is individually compliant,
the process built from those actions is compliant too. Autonomous execution
does not create the gap. It widens the distance between the scope a control
observes and the scope over which a guarantee is claimed, until a gap that was
always present becomes visible.

The lesson is therefore not that autonomous agents break enterprise controls.
It is that they reveal where **local compliance has been standing in for global
assurance** — and, for any one control-property pair, the review in this paper
is a way to tell whether it has. What one reconstructed instance offers is not
proof that every enterprise carries that gap, but the means to find out.
""".strip()


_NUMBER = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}


def _stories_heading() -> str:
    return "%s stories" % _NUMBER.get(len(STORIES), str(len(STORIES)))


def trajectory():
    """DERIVED from the artefacts that forced each change, not typed here."""
    from counterfactual import BY_PAIR, contested
    from losses_sap import LOSSES
    rows = []
    rows.append((
        "SAP lacks aggregate-state authorisation.",
        "**rejected** — Availability Control (loss %s)"
        % next(l.id for l in LOSSES if "Availability Control" in l.what),
        "The modelled FI tolerance path is document-local. Whether SAP's "
        "aggregate-state machinery governs the tested path is unresolved."))
    con = {c.pair for c in contested()}
    if "G2" in con:
        rows.append((
            "Static segregation of duties fails under agent composition.",
            "**rejected as stated** — retaining SAP's per-principal "
            "segregation-of-duties property (H3) changes the verdict to holds",
            "Decision-layer separation is a proposed stronger property "
            "requiring its own measurement."))
    if "G3" in con:
        rows.append((
            "SAP logs cannot attribute an action to an agent.",
            "**narrowed, and the block lifted** — the correlates named in "
            "loss %s were finally tested (X12) and do not recover the actor; "
            "the intended audit subject remains contested"
            % next(l.id for l in LOSSES if "attribution" in l.what),
            "The countermechanism is now settled and the property is not. "
            "What survives is a bound, not a claim about SAP's audit "
            "capability."))
    if "P1" in con:
        rows.append((
            "Transport release authorisation cannot see what is released.",
            "**withdrawn, respecified, run** — the comparator was one "
            "authorisation object, not the transport-governance surface (X11)",
            "True at the object and irrelevant at the surface: the same "
            "surface holds content-ranging decisions the prediction ignored."))
    if "H4" in con:
        rows.append((
            "The transport-governance surface closes what the authorisation "
            "object cannot.",
            "**admitted narrowly** — %s"
            % BY_PAIR["H4"].alternative.split(", rather than")[0].rstrip("."),
            "It holds against the behavioural property. Against conformance "
            "to a stated intent, only the human step retains the subject "
            "match, and its coverage is a parameter."))
    return rows


def check() -> list[str]:
    problems = []
    low = INCIDENT.lower()
    for w in VERDICT_WORDS:
        if w in low:
            problems.append("the opening incident contains a verdict (%r). It "
                            "must end on the question, not the answer." % w)
    if not INCIDENT.rstrip().endswith("?**"):
        problems.append("the incident does not end on its question")
    rows = trajectory()
    from counterfactual import contested
    if len(rows) < 1 + len(contested()):
        problems.append("the claims trajectory has %d rows for %d contested "
                        "pairs plus the reversal -- it is not being derived"
                        % (len(rows), len(contested())))
    if len(STORIES) != 4:
        problems.append("admit one, contest one, block one, narrow one -- "
                        "there are %d" % len(STORIES))
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   narrative consistent: incident ends on its question, "
              "%d stories, %d trajectory rows derived from the artefacts."
              % (len(STORIES), len(trajectory())))
        return

    print("# The argument, as a reader meets it")
    print()
    print("## The incident")
    print()
    print(INCIDENT)
    print()
    print("The answer is not obviously yes. The document-local control "
          "enforced, completely, the property it observes. The property that "
          "was breached is a different one.")
    print()
    print("## What the paper is actually against")
    print()
    print("> **%s**" % ANTAGONIST)
    print()
    print(ANTAGONIST_NOTE)
    print()
    print("## The turn")
    print()
    print(TURN)
    print()
    print("## What autonomy changed, and what it did not")
    print()
    print(AUTONOMY_LEAD)
    print()
    for label, effect in AXES:
        print("- **%s.** %s." % (label, effect[0].upper() + effect[1:]))
    print()
    print(AUTONOMY_TAIL)
    print()
    print("## The same shape, in the wild")
    print()
    print(REALWORLD)
    print()
    print("## %s" % _stories_heading())
    print()
    for i, (beat, function, body) in enumerate(STORIES, 1):
        print("### %d. %s — *%s*" % (i, beat, function))
        print()
        print(body)
        print()
    print("**%s.**" % ". ".join(b for b, _f, _x in STORIES))
    print()
    print("## The reversal")
    print()
    print(REVERSAL)
    print()
    print("## How the argument changed")
    print()
    print("*Derived from the audit and the loss register, not written from "
          "memory. This is the attrition the opening promised: the claims the "
          "author set out to make, and what the review left of each.*")
    print()
    print("| the claim we started with | what happened | what replaced it |")
    print("|:---|:---|:---|")
    for a, b, c in trajectory():
        print("| %s | %s | %s |" % (a, b, c))
    print()
    print("## What to do before you say a control failed")
    print()
    print("Specify what the control observes, what state it retains, and what "
          "local predicate it enforces. Then specify the protected property "
          "and say **who claims it** — the organisation, the vendor, a "
          "regulator, or you. Ask whether local enforcement composes into the "
          "wider property. Ask whether a defensible alternative specification "
          "changes the verdict. Ask whether the strongest existing "
          "countermechanism was tested, through more than one retrieval route.")
    print()
    print("The instrument is the deliverable. It is blank, and four of its "
          "seven verdicts are refusals.")
    print()
    print("> **%s**" % CLOSING_LINE)
    print()
    print("## %s" % CODA_TITLE)
    print()
    print(CODA)


if __name__ == "__main__":
    main()
