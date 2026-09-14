"""
relatedwork.py -- what was already known, and what the paper may still claim.

    python3 relatedwork.py            # the section
    python3 relatedwork.py --check    # every entry must cost the paper something

This file exists because of a hole the project's own machinery could not see.

Rule 3 in `boundary.py` says a gap may not be published until the strongest
existing COUNTERMECHANISM has been named and tested. Loss L3 generalises it:
a control-surface review is incomplete until the strongest countermechanisms
have been searched through independent retrieval routes. Neither rule was ever
pointed at the literature. The paper carried a formal object, a principle, a
diagnostic instrument and five experiments, and cited nothing at all -- so the
question rule 3 asks about mechanisms had never once been asked about ideas.

That is the same defect one level up, and it is the one that decides whether
the paper is novel rather than merely correct.

---------------------------------------------------------------------------
THE RULE THIS FILE ENFORCES

An entry belongs here only if it CHANGES WHAT THE PAPER MAY CLAIM. Every
entry therefore carries a `narrows` field saying how the paper's claim shrinks
because the work exists, and `--check` refuses an entry whose `narrows` is
empty. A related-work section that does not cost the paper anything is a
courtesy list, and this project has a name for tests that cannot cost
anything.

At least one entry must be marked `anticipates`: if the search found nothing
that anticipates any part of the contribution, the search was not real.

---------------------------------------------------------------------------
WHAT THE SEARCH FOUND, STATED BEFORE THE DETAIL

The principle is not new. The Control-Property Mismatch Principle is a
specialisation of Schneider's characterisation of enforceable security
policies to controls whose observation boundary is narrower than the
execution. Its extent form is the aggregation problem, named in the
multilevel-security literature in 1989. Its repair -- give the control state
-- is history-based access control, dynamic separation of duty, and the
mutable attributes of UCON. Its closure refinement is an inductive invariant.
Even the agent-specific framing has a contemporary: an arXiv preprint from May
2026 names aggregation inference as one of three sub-problems of authorisation
propagation in multi-agent systems.

What survives is smaller than the paper was carrying, and it is stated in
`RESIDUAL` at the foot of this file.

---------------------------------------------------------------------------
ON THE STATUS OF THESE CITATIONS

Bibliographic fields were read from DBLP record pages, OpenAlex, publisher or
author-hosted PDFs, and arXiv abstract pages. Every entry records the URL its
fields were read from. Where a field could not be read from a fetched source
it says UNVERIFIED rather than carrying a remembered value, because a
reconstructed citation is exactly the failure this project exists to avoid.

Two publisher sites -- IEEE Xplore and the ACM Digital Library -- refused
automated retrieval, and so did `help.sap.com` and `community.sap.com`, which
is loss L3 arriving in the literature search. `UNREAD` at the foot of this
file lists what that cost.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

RELATIONS = {
    "anticipates": "states some part of this paper's contribution first",
    "supplies": "supplies the mechanism this paper's repair recommendation "
                "amounts to",
    "adjacent": "asks a related question with a different object",
    "instrument": "the method this paper borrows or should have borrowed",
    "contemporary": "concurrent work on the same problem",
}


@dataclass(frozen=True)
class Work:
    key: str
    authors: str
    title: str
    venue: str
    year: str
    pages: str
    doi: str
    verified_from: str
    says: str            # what the work claims, read from a fetched source
    relation: str
    narrows: str         # how THIS paper's claim shrinks because it exists


WORKS = [
    # -- the closest prior art -------------------------------------------
    Work(
        "Schneider2000",
        "Fred B. Schneider",
        "Enforceable security policies",
        "ACM Transactions on Information and System Security (TISSEC) 3(1)",
        "2000", "30–50", "10.1145/353323.353382",
        "https://www.cs.cornell.edu/fbs/publications/EnfSecPols.pdf",
        "Characterises exactly the class of security policies enforceable by "
        "mechanisms that monitor system execution, and gives security automata "
        "for specifying that class. Three conditions: the policy must be a "
        "PROPERTY, meaning membership is determined by each execution "
        "individually rather than by the set of executions; the allowed set "
        "must be prefix-closed in the safety sense, so a violated prefix "
        "cannot be repaired by any extension; and the violation must be "
        "detectable from a finite prefix. Information-flow policies are the "
        "named example of what falls outside, because they relate multiple "
        "executions.",
        "anticipates",
        "**This is the closest prior art in the paper and it takes a large "
        "piece of the contribution.** The vocabulary for saying that a "
        "monitor cannot enforce what it cannot decide from what it observes "
        "has existed since 2000, and it is sharper than ours.\n\n"
        "What is left after it is a difference of question rather than of "
        "answer. Schneider fixes the observation — an EM mechanism sees the "
        "whole execution prefix — and asks which policies are enforceable. "
        "This paper fixes the CONTROL, whose observation boundary was decided "
        "by whoever specified it and is usually far narrower than the "
        "execution, and asks which properties that particular boundary can "
        "decide. The distinction is not academic here: the period-aggregate "
        "materiality property of G1 is a safety property of the execution and "
        "is EM-enforceable in Schneider's sense. A monitor watching the whole "
        "period would enforce it without difficulty. The FI tolerance group "
        "cannot, because its predicate reads one document. So the paper may "
        "not claim to have found a class of unenforceable policies. It may "
        "claim, at most, to apply the enforceable-policy question to deployed "
        "controls one at a time, which is a specialisation."),

    Work(
        "ClarksonSchneider2010",
        "Michael R. Clarkson and Fred B. Schneider",
        "Hyperproperties",
        "Journal of Computer Security (JCS) 18(6)",
        "2010", "1157–1210", "10.3233/JCS-2009-0393",
        "https://api.openalex.org/works/doi:10.3233/JCS-2009-0393 "
        "(conference version: CSF 2008, 51–65, 10.1109/CSF.2008.7)",
        "Generalises trace properties to hyperproperties — sets of sets of "
        "traces — so that policies which are not predicates on individual "
        "traces, such as secure information flow and average-case service "
        "level agreements, become expressible. Safety and liveness both "
        "generalise, and every hyperproperty is the intersection of a safety "
        "hyperproperty and a liveness hyperproperty.",
        "adjacent",
        "Fixes the boundary of what this paper is entitled to say about its "
        "own two forms. Neither is a hyperproperty. Extent mismatch concerns "
        "a property of a single execution that a narrow control cannot see "
        "all of, and subject mismatch concerns a single execution whose "
        "record does not carry the field the property is about. The paper "
        "must not reach for the hyperproperty vocabulary to make its results "
        "sound deeper than they are — and the X12 bound is a plain "
        "indistinguishability argument of the kind this literature has used "
        "for decades, not a new instrument."),

    # -- extent mismatch was named in 1989 --------------------------------
    Work(
        "Lunt1989",
        "Teresa F. Lunt",
        "Aggregation and inference: facts and fallacies",
        "IEEE Symposium on Security and Privacy (S&P), Oakland",
        "1989", "102–109", "UNVERIFIED",
        "https://conferences.computer.org/sp/pdfs/sp/1989/00044312.pdf",
        "Examines inference and aggregation problems in multilevel relational "
        "database systems and argues that aggregation had been treated only "
        "superficially. The aggregation problem is that a collection of "
        "individually releasable items can require a classification higher "
        "than any item in it.",
        "anticipates",
        "**Extent mismatch, in its purest form, is the aggregation problem "
        "under another name and in another control domain.** A set of "
        "individually-permitted actions producing an outcome no individual "
        "action would be permitted to produce is what G1 measures and what "
        "this paper spent five thousand words describing as though it were "
        "structural news. It is thirty-seven years old. The paper may claim "
        "the measurement and the location — that a mature ERP authorisation "
        "surface exhibits it on a specific posting path, and at what cost to "
        "legitimate work — and may not claim the phenomenon."),

    # -- the repair is old too --------------------------------------------
    Work(
        "BrewerNash1989",
        "David F. C. Brewer and Michael J. Nash",
        "The Chinese Wall security policy",
        "IEEE Symposium on Security and Privacy (S&P), Oakland",
        "1989", "206–214", "10.1109/SECPRI.1989.36295",
        "https://www.cs.purdue.edu/homes/ninghui/readings/AccessControl/"
        "brewer_nash_89.pdf",
        "A mathematical theory for a commercial security policy in which "
        "access is history-dependent: datasets are grouped into "
        "conflict-of-interest classes and a subject's prior accesses "
        "determine what it may access next. Shows the policy cannot be "
        "correctly represented in a Bell–LaPadula model.",
        "supplies",
        "The recommendation this paper's G1 result leads to — give the "
        "control state that survives the individual action — is the shape "
        "Brewer and Nash formalised for commercial systems in 1989, in the "
        "same industry sector. The paper may not present a stateful control "
        "as a new proposal. It may report what a specific deployed surface "
        "does and does not offer on a specific path."),

    Work(
        "NashPoland1990",
        "Michael J. Nash and K. R. Poland",
        "Some conundrums concerning separation of duty",
        "IEEE Symposium on Research in Security and Privacy (S&P)",
        "1990", "201–209 (DBLP) / 201–207 (OpenAlex) — DISPUTED, verify "
        "against the printed proceedings before citing",
        "10.1109/RISP.1990.63851",
        "https://dblp.org/rec/conf/sp/NashP90.html",
        "Presents a dynamic separation-of-duty policy occurring in real "
        "commercial settings which can be implemented efficiently but cannot "
        "be implemented by mechanisms based solely on the TCSEC, and a "
        "financial-transaction-integrity product satisfying neither the TCSEC "
        "nor the Clark–Wilson rules.",
        "anticipates",
        "The observation that a real commercial integrity policy outruns the "
        "control model available to enforce it — which is this paper's whole "
        "argument shape — is stated here, in finance, in 1990. The page range "
        "disagrees between two sources and is recorded as disputed rather "
        "than picked."),

    Work(
        "SimonZurko1997",
        "Richard T. Simon and Mary Ellen Zurko",
        "Separation of duty in role-based environments",
        "IEEE Computer Security Foundations Workshop (CSFW)",
        "1997", "183–194", "10.1109/CSFW.1997.596811",
        "https://dblp.org/rec/conf/csfw/SimonZ97.html",
        "Surveys applications of separation of duty, notes that computing "
        "implementations diverge from traditional practice with no agreed "
        "definition, introduces history-based considerations, and describes "
        "an implementation in the Adage authorisation toolkit.",
        "adjacent",
        "G2 proposes a decision-layer separation property — that no single "
        "decision process should complete both sides of a conflicting duty "
        "pair. The observation that deployed separation of duty diverges from "
        "what practitioners mean by it, and that history is what closes the "
        "difference, is this paper. G2's contribution is therefore not the "
        "observation but the specific substitution the counterfactual audit "
        "caught us making."),

    Work(
        "FerraioloEtAl2001",
        "David F. Ferraiolo, Ravi Sandhu, Serban Gavrila, D. Richard Kuhn and "
        "Ramaswamy Chandramouli",
        "Proposed NIST standard for role-based access control",
        "ACM Transactions on Information and System Security (TISSEC) 4(3)",
        "2001", "224–274", "10.1145/501978.501980",
        "https://csrc.nist.gov/csrc/media/projects/role-based-access-control/"
        "documents/rbac-std-draft.pdf (NIST draft; TISSEC page proofs not "
        "fetched)",
        "Unifies prior RBAC models into a reference model plus functional "
        "specification. Dynamic separation of duty is a standard component: "
        "where static SSD constrains permanent user–role assignment, DSD "
        "constrains role ACTIVATION within and across a user's sessions and "
        "is enforced at activation time.",
        "supplies",
        "Sets the boundary of G2 precisely. DSD already constrains what one "
        "principal may activate across sessions, so the paper may not claim "
        "that deployed access-control standards ignore dynamic conflict. What "
        "X8 measures is narrower and survives: DSD is defined over a USER's "
        "sessions, and the composition in X8 is across two propagated "
        "principals in one agent workflow, which is not a user."),

    Work(
        "ParkSandhu2004",
        "Jaehong Park and Ravi Sandhu",
        "The UCON_ABC usage control model",
        "ACM Transactions on Information and System Security (TISSEC) 7(1)",
        "2004", "128–174", "10.1145/984334.984339",
        "https://profsandhu.com/journals/tissec/ucon-abc.pdf",
        "A family of core models unifying authorisations, obligations and "
        "conditions and subsuming MAC, DAC, RBAC, trust management and DRM. "
        "Two defining innovations, quoted from the authors: authorisations "
        "may be pre-authorisations or ONGOING authorisations evaluated while "
        "a right is being exercised; and subject and object attributes may be "
        "MUTABLE, changed as a consequence of access through pre-, ongoing- "
        "and post-updates.",
        "supplies",
        "**The repair this paper recommends for G1 already has a model, and "
        "it is twenty-two years old.** A cumulative credited-value limit is a "
        "UCON ongoing authorisation over a mutable accumulated-value "
        "attribute; that is what mutability was introduced for. The paper's "
        "recommendation is therefore not 'add a new kind of control' but 'the "
        "control model that expresses this has existed since 2004 and this "
        "posting path does not use it'. That is a weaker claim and a more "
        "useful one."),

    Work(
        "AbadiFournet2003",
        "Martín Abadi and Cédric Fournet",
        "Access control based on execution history",
        "Network and Distributed System Security Symposium (NDSS)",
        "2003", "UNVERIFIED (no page range in the NDSS or DBLP record)",
        "none assigned",
        "https://www.ndss-symposium.org/wp-content/uploads/2017/09/"
        "Access-Control-Based-on-Execution-History-Martin-Abadi.pdf",
        "Argues that stack-inspection mechanisms for determining the runtime "
        "rights of code are inherently partial, and proposes a history-based "
        "model in which rights are determined by the attributes of all code "
        "that has run, together with explicit requests to augment rights.",
        "supplies",
        "The enforcement mechanism for an extent-mismatched control — carry "
        "the history rather than the current step — with an argument for why "
        "the narrower alternative is inherently partial. The paper's "
        "structural claim is a restatement of that argument in an "
        "authorisation surface rather than a language runtime."),

    Work(
        "EdjlaliEtAl1998",
        "Guy Edjlali, Anurag Acharya and Vipin Chaudhary",
        "History-based access control for mobile code",
        "ACM Conference on Computer and Communications Security (CCS)",
        "1998", "38–48", "10.1145/288090.288102",
        "https://dblp.org/rec/conf/ccs/EdjlaliAC98.html",
        "A history-based access-control mechanism maintaining a selective "
        "history of each program's access requests, so that what a program "
        "may do depends on its own prior behaviour rather than only on its "
        "origin. Implemented in the Deeds system.",
        "supplies",
        "The same repair, implemented, five years earlier, and with the "
        "'selective history' problem — which history is worth keeping — "
        "already identified as the hard part. This paper does not address "
        "that question at all and should not imply it has."),

    # -- the repair, instantiated in industry ------------------------------
    Work(
        "NextLabs2024",
        "NextLabs, Inc.",
        "Data Access Enforcer for SAP ERP — dynamic authorization and "
        "attribute-based access control",
        "Vendor product documentation and datasheet",
        "2024", "n/a", "none assigned",
        "https://www.nextlabs.com/products/data-access-enforcer/"
        "dynamic-data-protection-using-attribute-based-access-control-abac/",
        "A commercial enforcement product for SAP that evaluates access at "
        "runtime against attribute-based policies every time data or an "
        "application is accessed, and filters, masks or blocks the result at "
        "the application and database layers accordingly. The same direction "
        "is taken by other enterprise ISVs — Saviynt and comparable "
        "identity-governance and fine-grained-entitlement platforms — moving "
        "enforcement from static SAP roles to conditional, per-request "
        "decisions on individual data items.",
        "supplies",
        "The repair direction this paper points to — relocate the control so "
        "that it observes the entity the property is about — is already "
        "instantiated in industry, so the paper may not present runtime, "
        "content-ranging, per-data-item authorization as a new idea. What "
        "survives, and what the existence of these products sharpens rather "
        "than removes, is the cumulative-over-time case. These enforcers "
        "evaluate each request on its own attributes, so they address the "
        "extent-over-content and extent-over-principal mismatches while a "
        "per-request decision that retains no accumulated state still cannot "
        "bound the G1 period aggregate. The one uncontested gap in this paper "
        "therefore survives even the strongest deployed tooling of this class "
        "unless that tooling is given state over the horizon the guarantee is "
        "defined on — which is the paper's actual recommendation, now "
        "expressible against a concrete product rather than in the abstract."),

    # -- composition -------------------------------------------------------
    Work(
        "McCullough1988",
        "Daryl McCullough",
        "Noninterference and the composability of security properties",
        "IEEE Symposium on Security and Privacy (S&P)",
        "1988", "177–186", "10.1109/SECPRI.1988.8110",
        "https://api.openalex.org/works/doi:10.1109/SECPRI.1988.8110",
        "Shows that noninterference and several generalisations do not "
        "compose — two individually secure systems can be connected so that "
        "the composite is insecure — and introduces restrictiveness, a "
        "property that is composable, so that legally connected restrictive "
        "systems yield a restrictive system.",
        "anticipates",
        "The compositional-closure refinement in `mismatch.py` — that an "
        "extent difference is a mismatch only where the property is not "
        "closed under the control's local predicate — is the "
        "access-control shadow of this result. Composability is a property "
        "systems have to be designed to have, and cannot be assumed from the "
        "security of the parts. H2 is an instance of a closed case and the "
        "paper presented it as a refinement it had found. It is an "
        "instantiation."),

    Work(
        "McLean1994",
        "John McLean",
        "A general theory of composition for trace sets closed under "
        "selective interleaving functions",
        "IEEE Symposium on Research in Security and Privacy (S&P)",
        "1994", "79–93", "10.1109/RISP.1994.296590",
        "https://api.openalex.org/works/doi:10.1109/RISP.1994.296590",
        "A general theory of composition for possibilistic security "
        "properties, observing that they fall outside the Alpern–Schneider "
        "safety/liveness domain and are therefore not subject to the "
        "Abadi–Lamport composition principle. Closure under selective "
        "interleaving functions is generally preserved by product and "
        "cascading but not by feedback, internal composition or refinement.",
        "adjacent",
        "Supplies the warning this paper needs about its own closure test. "
        "Closure is preserved by some compositions and not by others, so "
        "`closed_under_composition` as a single boolean is coarser than the "
        "literature it echoes, and the paper must say so rather than let the "
        "field's simplicity imply the question is simple."),

    Work(
        "Mantel2002",
        "Heiko Mantel",
        "On the composition of secure systems",
        "IEEE Symposium on Security and Privacy (S&P)",
        "2002", "88–101", "10.1109/SECPRI.2002.1004364",
        "https://api.openalex.org/works/doi:10.1109/SECPRI.2002.1004364",
        "Compositionality results for security properties, including a "
        "composable property weaker than forward correctability, and a "
        "demonstration that certain non-trivial properties emerge under "
        "composition. All results derive from one general lemma which also "
        "re-proves and classifies earlier compositionality results.",
        "adjacent",
        "That properties can EMERGE under composition is the mirror image of "
        "this paper's argument and it is not addressed anywhere in these "
        "experiments. The sweep asks only whether a harm survives; it never "
        "asks whether composing two controls creates a guarantee neither has "
        "alone. That is an omission and belongs in the research programme."),

    # -- obligations, and the preventive/detective split -------------------
    Work(
        "BettiniEtAl2002",
        "Claudio Bettini, Sushil Jajodia, X. Sean Wang and Duminda "
        "Wijesekera",
        "Provisions and obligations in policy management and security "
        "applications",
        "International Conference on Very Large Data Bases (VLDB)",
        "2002", "502–513", "10.1016/B978-155860869-6/50051-2",
        "https://dblp.org/rec/conf/vldb/BettiniJWW02.html "
        "(bibliographic fields only; the VLDB PDF refused retrieval and the "
        "abstract is UNREAD)",
        "UNVERIFIED — the abstract was not fetched, so no claim is made here "
        "about what the paper argues. The entry is carried for the "
        "distinction its title names, not for its content.",
        "adjacent",
        "X11 forced this paper to separate preventive from detective coverage "
        "for the first time, and the provision/obligation distinction is the "
        "policy-language vocabulary for exactly that split. The paper should "
        "not present the separation as one it invented. Because the abstract "
        "is unread, this entry may be cited for the existence of the "
        "distinction and for nothing else."),

    Work(
        "NiBertinoLobo2008",
        "Qun Ni, Elisa Bertino and Jorge Lobo",
        "An obligation model bridging access control policies and privacy "
        "policies",
        "ACM Symposium on Access Control Models and Technologies (SACMAT)",
        "2008", "133–142", "10.1145/1377836.1377857",
        "https://api.openalex.org/works/doi:10.1145/1377836.1377857",
        "An obligation model for privacy-aware RBAC supporting pre-, post-, "
        "conditional and repeating obligations, with algorithms to detect "
        "undesired interactions between permissions and obligations.",
        "adjacent",
        "Obligations that must be discharged after an action are the formal "
        "counterpart of the detective step T6 in X11, whose measured result "
        "is forty of forty flagged and forty of forty in production. The "
        "paper may report that measurement; it may not imply that the "
        "preventive/detective asymmetry is a new observation."),

    # -- the contemporary work ---------------------------------------------
    Work(
        "Tallam2026",
        "Krti Tallam",
        "Authorization propagation in multi-agent AI systems: identity "
        "governance as infrastructure",
        "arXiv preprint arXiv:2605.05440",
        "2026", "n/a", "arXiv:2605.05440",
        "https://arxiv.org/abs/2605.05440",
        "Formalises authorisation propagation as a workflow-level property "
        "not reducible to prompt injection and not covered by RBAC, ABAC or "
        "ReBAC, and names three sub-problems: transitive delegation, "
        "AGGREGATION INFERENCE, and temporal validity, from which seven "
        "structural requirements are derived.",
        "contemporary",
        "**The closest contemporary work, and it names the aggregate problem "
        "for agent systems three months before this paper.** The paper may "
        "not claim to be first to identify aggregate authorisation as an "
        "agent-specific structural problem. What is not in it, as far as this "
        "search can tell, is measurement: no control surface is swept, no "
        "harm predicate reads world state, and no verdict is withdrawn under "
        "audit. This paper's claim narrows to the empirical half."),

    Work(
        "LiEtAl2025",
        "Xinfeng Li, Dong Huang, Jie Li, Hongyi Cai, Zhenhong Zhou, Wei Dong, "
        "XiaoFeng Wang and Yang Liu",
        "A vision for access control in LLM-based agent systems",
        "arXiv preprint arXiv:2510.11108",
        "2025", "n/a", "arXiv:2510.11108",
        "https://arxiv.org/abs/2510.11108",
        "A position paper arguing that static rule-based access control is "
        "ill-equipped for agentic information flows, and proposing Agent "
        "Access Control: dynamic, context-aware information-flow governance "
        "with adaptive responses such as redaction and summarisation rather "
        "than binary allow/deny.",
        "contemporary",
        "Establishes that 'static access control is the wrong shape for "
        "agents' is a position already in the literature and already argued "
        "generically. This paper's difference is that it names one deployed "
        "surface, sweeps it exhaustively, and reports the exchange rate. The "
        "difference is evidence, not thesis."),

    Work(
        "BoothEtAl2026",
        "Harold Booth, Bill Fisher, Ryan Galluzzo and Joshua Roberts",
        "Accelerating the adoption of software and AI agent identity and "
        "authorization",
        "NIST National Cybersecurity Center of Excellence, concept paper "
        "(draft)",
        "2026", "n/a", "none assigned",
        "https://www.nccoe.nist.gov/sites/default/files/2026-02/"
        "accelerating-the-adoption-of-software-and-ai-agent-identity-and-"
        "authorization-concept-paper.pdf",
        "Proposes a NIST project applying existing identity standards — "
        "OAuth 2.0, SPIFFE/SPIRE, NGAC — to identification, authentication, "
        "authorisation and logging for AI agents in enterprise environments "
        "with human oversight. Does not mention ERP.",
        "adjacent",
        "Fixes what 'enterprise' currently means in standards work on agent "
        "authorisation: identity infrastructure, not the business-application "
        "control surface an agent actually acts through. The paper's choice "
        "of object is defensible against this and should be argued rather "
        "than assumed."),
]


# ---------------------------------------------------------------------------
# The absence, stated as a search result rather than as a claim
# ---------------------------------------------------------------------------

ABSENCE = (
    "A search of arXiv, OpenAlex, DBLP, Semantic Scholar and the open web "
    "found no peer-reviewed or preprint work on the security or authorisation "
    "of autonomous agents acting specifically in ERP or SAP systems. The "
    "agent-authorisation work that exists is domain-generic; the "
    "ERP-plus-agents work that exists is about capability and architecture "
    "rather than control. **This is reported as the result of one bounded "
    "search, not as an absence.** The same asymmetry the "
    "specification-sensitivity audit insists on applies here: finding nothing "
    "is evidence about the search."
)

# What could not be read, and what that costs. Loss L3 in the literature.
UNREAD = [
    ("IEEE Xplore and the ACM Digital Library",
     "refused automated retrieval, so abstracts for several entries were read "
     "from OpenAlex reconstructions or author-hosted preprints rather than "
     "from the publisher's page of record. Where the two disagreed the "
     "disagreement is recorded in the entry."),
    ("`help.sap.com` and `community.sap.com`",
     "refuse automated retrieval, which is loss L3 unchanged. Two SAP-authored "
     "community posts on securing agentic AI and on propagating user identity "
     "from Joule into S/4HANA were found by title and could not be read. They "
     "are the highest-value unread sources for this paper and they bear "
     "directly on whether the modelled surface resembles the current one."),
    ("Workflow authorisation models",
     "were not searched systematically. G2's decision-layer property is a "
     "workflow-level separation constraint, and there is a literature on "
     "workflow authorisation this file does not cover. That is a known hole, "
     "named here rather than left for a reviewer."),
    ("Bettini et al. 2002",
     "is carried on bibliographic fields alone; its abstract was not fetched, "
     "and the entry says so."),
]


# ---------------------------------------------------------------------------
# What is left
# ---------------------------------------------------------------------------

RESIDUAL = [
    ("The instrument, not the principle",
     "The Control-Property Review is a decision procedure a practitioner can "
     "run against a named control and a named property, and four of its seven "
     "verdicts are refusals. Schneider's characterisation tells you what a "
     "monitor can enforce; it does not tell a security architect holding a "
     "PFCG role and a materiality threshold what to do on a Tuesday. Whether "
     "an instrument is a contribution is a fair question, and it is the "
     "question the paper should be defending."),

    ("The specification-sensitivity audit",
     "Naming, for every verdict, the smallest defensible alternative "
     "specification that would flip it — and marking the verdict CONTESTED "
     "when that alternative is consistent with independent evidence. Four of "
     "eight pairs come back contested, including two the paper wanted to "
     "publish. This search found no precedent for it as a stated protocol. "
     "That is a bounded search and the asymmetry applies: no precedent found "
     "is not no precedent."),

    ("The measurement, and the exchange rate",
     "The aggregation problem is old; what it costs on a specific posting "
     "path in a specific reconstructed authorisation surface is not recorded "
     "anywhere this search could find. 12,288 configurations, 10,398 holding "
     "the outcome below materiality, best legitimate throughput 37.5%, and a "
     "one-to-one exchange between harm reduction and refused work. Numbers "
     "are what this paper has that the prior art does not."),

    ("The distinction between the two forms, and what claiming it cost",
     "X7 and X11 measure one organisation's controls against harms of the two "
     "different shapes, and the difference between them is not that one "
     "control is cheap and the other expensive. Where the property outruns "
     "the control's extent, the exchange rate between harm and refused "
     "legitimate work is forced by the pair: the workloads are identical on "
     "the dimension the control reads, so every predicate over it removes the "
     "same proportion of each, and no implementation can do better. Where the "
     "control reads the property's own subject, nothing is forced and the "
     "cost is set by that decision's false-positive rate. Arriving at that "
     "distinction cost a retraction — the first version of X11 had no "
     "false-positive channel at all and reported zero cost as a measurement, "
     "which is loss L6 — and the surviving claim is narrower than the one it "
     "replaced."),

    ("The negative results",
     "Two verdicts withdrawn under audit, one prediction respecified before "
     "running and then narrowed by its own result, one experiment whose "
     "procedure produced two rounds of artefacts before it produced a result, "
     "and a loss register that grew during the writing. Reporting these is "
     "not a contribution to knowledge about SAP. It is the reason the rest "
     "should be believed."),
]


def anticipating() -> list[Work]:
    return [w for w in WORKS if w.relation == "anticipates"]


def check() -> list[str]:
    problems = []
    keys = set()
    for w in WORKS:
        if w.key in keys:
            problems.append("%s appears twice" % w.key)
        keys.add(w.key)
        if w.relation not in RELATIONS:
            problems.append("%s: unknown relation %r" % (w.key, w.relation))
        for f in ("authors", "title", "venue", "year", "verified_from",
                  "says", "narrows"):
            if not getattr(w, f).strip():
                problems.append("%s: %s is empty" % (w.key, f))
        # The rule this file exists for.
        if len(w.narrows.split()) < 25:
            problems.append(
                "%s: `narrows` is a sentence, not a statement of what the "
                "paper may no longer claim. An entry that costs the paper "
                "nothing is a courtesy citation." % w.key)
        if not w.verified_from.startswith("http"):
            problems.append("%s: no URL the fields were read from. A citation "
                            "reconstructed from memory is the failure this "
                            "project exists to avoid." % w.key)
    if not anticipating():
        problems.append(
            "no entry is marked `anticipates`. Either the contribution is "
            "unprecedented, which is not credible, or the search was not "
            "real.")
    if not UNREAD:
        problems.append("nothing is recorded as unread, which has never once "
                        "been true of a literature search")
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   %d works, %d anticipating some part of the contribution, "
              "%d gaps in the search recorded."
              % (len(WORKS), len(anticipating()), len(UNREAD)))
        return

    print("# Related work, and what it costs this paper")
    print()
    print("*Generated by `python3 relatedwork.py`. Do not edit by hand.*")
    print()
    print("This section is placed before the results rather than after them, "
          "because it changes what the results are allowed to mean.")
    print()
    print("Rule 3 of the boundary map says a gap may not be published until "
          "the strongest existing countermechanism has been named and tested. "
          "Loss L3 generalises it: a control-surface review is incomplete "
          "until the strongest countermechanisms have been searched through "
          "independent retrieval routes. Neither rule had ever been pointed "
          "at the literature. The paper carried a formal object, a principle, "
          "an instrument and five experiments, and cited nothing — so the "
          "question rule 3 asks about mechanisms had never once been asked "
          "about ideas. This section is that question, asked late.")
    print()
    print("**Every entry below states how the paper's claim shrinks because "
          "the work exists.** An entry that costs the paper nothing is not "
          "carried; the build refuses it.")
    print()
    print("## The short version")
    print()
    print("The principle is not new. It is a specialisation of Schneider's "
          "characterisation of enforceable security policies to controls "
          "whose observation boundary is narrower than the execution. Its "
          "extent form is the aggregation problem, named in 1989. Its repair "
          "— give the control state — is history-based access control, "
          "dynamic separation of duty, and the mutable attributes of UCON. "
          "Its closure refinement is the access-control shadow of the "
          "composability literature. Even the agent framing has a "
          "contemporary: an arXiv preprint from May 2026 names aggregation "
          "inference as one of three sub-problems of authorisation "
          "propagation in multi-agent systems.")
    print()
    print("%d of the %d works below are marked as anticipating some part of "
          "what this paper was carrying as a contribution."
          % (len(anticipating()), len(WORKS)))
    print()

    order = ["anticipates", "supplies", "adjacent", "contemporary",
             "instrument"]
    for rel in order:
        group = [w for w in WORKS if w.relation == rel]
        if not group:
            continue
        print("## %s — %s" % (rel.capitalize(), RELATIONS[rel]))
        print()
        for w in group:
            print("### %s. *%s.* %s, %s." % (w.authors, w.title, w.venue,
                                             w.year))
            print()
            print("| | |")
            print("|:---|:---|")
            print("| pages | %s |" % (w.pages or "—"))
            print("| doi | %s |" % (w.doi or "—"))
            print("| fields read from | %s |" % w.verified_from)
            print()
            print("**What it says.** %s" % w.says)
            print()
            print("**What it costs this paper.** %s" % w.narrows)
            print()

    print("## What was not found")
    print()
    print(ABSENCE)
    print()
    print("## What was not read")
    print()
    print("| source | what it costs |")
    print("|:---|:---|")
    for what, cost in UNREAD:
        print("| %s | %s |" % (what, cost))
    print()
    print("## What is left")
    print()
    print("After all of the above, this is what the paper may still claim.")
    print()
    for title, body in RESIDUAL:
        print("**%s.** %s" % (title, body))
        print()


if __name__ == "__main__":
    main()
