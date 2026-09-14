"""
impact.py -- who this lands on, and what it asks of them.

    python3 impact.py            # the implications section
    python3 impact.py --check    # implications, framed as implications

The paper's unit is deliberately narrow -- one control against one property --
and a reader can finish it thinking the consequence is narrow too. It is not.
This section states, per role, what the result implies and what it asks of
them. It is the highest-leverage way to raise the paper's reach without
inflating a single claim: everything here is framed as an implication that
holds to the extent the reconstruction reflects a deployed system, which is the
validation this edition leaves open. `--check` fails if the framing disclaimer
is missing, if fewer than five roles are addressed, or if the section slips into
claiming the implications as proven.
"""
from __future__ import annotations

import sys

DISCLAIMER = (
    "*These are implications the study points to, not results it establishes. "
    "They hold to the extent a reconstruction reflects a deployed system — the "
    "validation this edition leaves open — so read them as where to look, not "
    "as findings about your own landscape.*")

ROLES = [
    ("Security and enterprise architects (control owners)",
     "Map the controls you rely on by what they observe at decision time and "
     "what state they retain, not by whether they exist. A control catalogue "
     "is an inventory of controls, not of guarantees. Before an agent is given "
     "authority over a process, run the Control-Property Review over each "
     "control it will touch: does this control observe the thing we are "
     "claiming it protects? Where the answer is no, the fix is usually to "
     "relocate or fund a control, not to patch one."),

    ("CISOs, risk and internal audit",
     "A control matrix that is green for human operators does not stay "
     "equivalent to assurance once an agent is the operator. The sharpest "
     "exposure is attribution: under a propagated identity the record names a "
     "person, not the deciding agent, and that bears directly on financial "
     "attestation and on insurer and regulator conversations. Ask, for each "
     "agent-operated process, which controls hold state and which decide one "
     "action at a time."),

    ("SAP Basis and security administration",
     "Transport-release authorization decides on the request and the "
     "principal, not on the content, so it is not a content control; place the "
     "content-ranging check preventively at release rather than as a "
     "post-import reconciliation. And the audit log attributes to the "
     "authenticated principal — retention does not repair the agent-versus-"
     "human gap, because it is a schema gap, not a volume one."),

    ("Project and service process owners",
     "Project and service processes accrue value across many individually "
     "ordinary postings, which is precisely the shape a per-document control "
     "cannot bound. The control that matters is the stateful one — availability "
     "control, project budget, contract-value caps — not the per-line "
     "tolerance. And because the compensating control can hand most of the "
     "automation benefit back, the benefits case and the control case are one "
     "conversation, not two."),

    ("Auditors, assurance and regulators",
     "\"Compliant at each transaction\" is not the same statement as "
     "\"compliant process,\" and autonomous execution widens the distance "
     "between them. The question to ask of any agent-operated process is where "
     "the control's observation boundary sits relative to the property being "
     "certified — and whether anything in the path watches the property at the "
     "scope the certification is about."),

    ("Platform and agent builders",
     "The controls that survive agent operation share four properties: they "
     "range over content rather than the request, they act preventively rather "
     "than after the fact, they retain the state the property is defined over, "
     "and they distinguish the deciding actor from the identity it runs under. "
     "Build for those four, not for per-action permission alone."),
]

CLOSING = (
    "The through-line is one sentence: autonomous execution does not create "
    "these gaps, it reveals where local compliance has been standing in for "
    "global assurance. The instrument in this paper is a way for any of the "
    "roles above to find that line for a control they own, before an agent is "
    "switched on — and, as often, to find that it does not apply, which is the "
    "point.")

FIRST_DIRECTION = (
    "A first direction — stated as direction, not as a finished solution. The "
    "controls that survive agent operation in this study share four "
    "properties: they range over content rather than the request, they act "
    "preventively rather than after the fact, they retain the state the "
    "property is defined over, and they distinguish the deciding actor from "
    "the identity it runs under. A migration from human-intended controls to "
    "agent-ready ones can be organised around those four, applied control by "
    "control to the processes an agent will touch. Part of this is already "
    "industry practice: enterprise enforcement products such as NextLabs and "
    "Saviynt move authorization from static roles to runtime, per-request "
    "decisions on individual data items, which supplies the first two "
    "properties. The property most current tooling still lacks is the third — "
    "accumulated state over the horizon the guarantee is about — which is "
    "exactly where the one uncontested gap in this study lives. So the "
    "direction is not a new control to buy but a question to put to each "
    "control an agent will operate under: does it hold the state its guarantee "
    "is defined over, or does it decide one action at a time and trust the "
    "sum?")


def check() -> list[str]:
    problems = []
    if len(ROLES) < 5:
        problems.append("fewer than five roles are addressed; the section is "
                        "meant to establish breadth of impact")
    if "implications the study points to, not results it establishes" \
            not in DISCLAIMER:
        problems.append("the implications disclaimer is missing or altered")
    body = " ".join(b for _, b in ROLES).lower() + " " + CLOSING.lower()
    for overclaim in (" we prove", " proves ", " proven ", "demonstrates that",
                      "guaranteed to", "for the first time"):
        if overclaim in body:
            problems.append("the impact section overclaims (%r); implications "
                            "must not be stated as proven" % overclaim.strip())
    for _t, b in ROLES:
        if len(b.split()) < 25:
            problems.append("a role implication is too short to be useful")
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   impact section: %d roles, framed as implications, no "
              "overclaim." % len(ROLES))
        return

    print("# Why this matters")
    print()
    print(DISCLAIMER)
    print()
    print("The paper's unit is narrow — one control against one property — but "
          "the pattern it exposes is not. Wherever an autonomous agent is given "
          "authority inside an enterprise system, the same question applies: "
          "does each control you rely on actually observe the thing you are "
          "claiming it protects? Here is who that lands on, and what it asks of "
          "them.")
    print()
    for title, body in ROLES:
        print("**%s.** %s" % (title, body))
        print()
    print(CLOSING)
    print()
    print("## A first direction")
    print()
    print(FIRST_DIRECTION)
    print()


if __name__ == "__main__":
    main()
