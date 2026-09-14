"""
abstract.py -- the abstract, and the one place a reader decides.

    python3 abstract.py            # the abstract, keywords, and the caveat
    python3 abstract.py --check    # the same discipline finding.py gets

An abstract is the highest-leverage paragraph in a paper and the easiest place
to overclaim, because nobody checks it against the body. So it gets the two
instruments `finding.py` already has -- no hedging words, no language exceeding
the evidence class -- plus a third that matters more here: **every number in it
is interpolated from the code that produced it.** A figure cannot be typed into
this file. If the sweep changes, the abstract changes with it or the build
fails.

The structural rule is the same as the finding's, and for the same reason.
ASSERT, then BOUND. A paper that has withdrawn two of its own verdicts and
narrowed a third has earned a plain first paragraph; lacing every clause with a
disclaimer would leave a reader unable to tell a careful claim from an
abandoned one. The bounds follow immediately and are not softened.
"""
from __future__ import annotations

import functools
import sys

from boundary import GAPS, HELD
from counterfactual import CF, contested
from losses_sap import LOSSES
from mismatch import PAIRS
from prereg_sap import PREREG
from relatedwork import WORKS, anticipating
from sapsec.experiments import x7, x11, x12
from sapsec.workload import MATERIALITY
from release import TITLE, open_blockers, releasable, subtitle

# The same two word lists finding.py enforces, imported rather than copied so
# they cannot drift apart.
from finding import ESCALATIONS, HEDGES


@functools.lru_cache(maxsize=1)
def _numbers() -> dict:
    r7, r11, r12 = x7(), x11(), x12()
    p = r7["primary"]
    c = lambda v: "{:,}".format(v)          # noqa: E731
    return {
        "n_cfg7": c(p.n_configs),
        "n_hold": c(p.n_prevent_harm),
        "best": 100 * p.best_legit_fraction,
        "materiality": MATERIALITY,
        "n_cfg11": c(r11["n_configs"]),
        "n_disc": c(r11["n_discriminating"]),
        "n_req": r11["n_request_only"],
        "n_req_disc": r11["request_only_discriminating"],
        "n_arm": r11["n_arm"],
        "n_det": r11["n_detective_only"],
        "det_flagged": r11["detective"]["flagged"],
        "det_prd": r11["detective"]["in_prd"],
        "n_cond12": r12["n_conditions"],
        "n_nosig": r12["n_no_signal"],
        "n_nosig_moved": r12["n_no_signal_moved"],
        "n_pairs": len(PAIRS),
        "n_tested": len([x for x in PAIRS if x.observed != "untested"]),
        "n_contested": len(contested()),
        "n_cf": len(CF),
        "n_held": len(HELD),
        "n_held_contested": len([h for h in HELD
                                 if h.id in {c.pair for c in contested()}]),
        "n_gaps": len(GAPS),
        "n_exp": len(PREREG),
        "n_losses": len(LOSSES),
        "n_works": len(WORKS),
        "n_ant": len(anticipating()),
        "ant_names": "; ".join(
            "%s %s" % (w.authors.split(" and ")[0].split()[-1], w.year)
            for w in anticipating()),
    }


TEMPLATE = """
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
a diagnostic instrument, the Control-Property Review, and {n_exp} pre-registered
experiments against a reconstructed SAP authorisation surface.

A control is neither strong nor weak. The unit that carries a guarantee is the
control-property pair, and a pair fails whenever the property is defined outside
the control's observation boundary — because it ranges over more actions,
principals or time than the control sees, or because it is about a different
entity than its predicate names. For all {n_pairs} specified pairs the
verdict derived from the specification agreed with the observed outcome. The
instrument refused as readily as it found: {n_contested} of {n_pairs} pairs are
contested — a defensible alternative specification flips the verdict — and one
cost result was retracted.

Three measurements. The same FI tolerance group separated a document-local
anomaly at full throughput yet could not discriminate a materiality breach built
from documents indistinguishable on every field it reads: of {n_cfg7}
configurations, {n_hold} held the outcome below materiality, the best retaining
{best:.1f}% of legitimate work — it can throttle the total, not tell the two
apart. A harmful transport identical at request level was discriminated only by
decisions ranging over its content, never by the request alone ({n_disc} of
{n_cfg11}). Under principal propagation, no procedure
reading the audit fields beats naming the busiest actor unread.

The first two differ in kind, not price: where the property outruns the
control's extent the exchange rate is forced by the pair; where it reads the
property's own subject, cost is a swept, unmeasured false-positive rate.
""".strip()

BOUNDS = [
    ("The principle is not new and the paper does not claim it is.",
     "The related-work section records {n_ant} of {n_works} works that "
     "anticipate part of it — {ant_names} — and a further group that supplies "
     "the mechanism its repair recommendation amounts to. Extent mismatch is "
     "the aggregation problem; the principle specialises a published "
     "characterisation of enforceable security policies to controls whose "
     "observation boundary is narrower than the execution; the repair is "
     "history-based access control and usage control's mutable attributes. "
     "What is offered is the instrument, the specification-sensitivity audit, "
     "the measurements, and the negative results."),

    ("This is a reconstruction, not deployed SAP.",
     "No modelled mechanism has been verified against primary vendor "
     "documentation, the product and release scope is not fixed, and the "
     "results are results about the reconstruction. The study states its "
     "scope and the external validation still to be completed."),

    ("The second experiment's cost figures are conditional and its first "
     "version was wrong.",
     "The transport model originally contained no channel through which a "
     "content-ranging step could stop a benign change, so it reported zero "
     "cost as a measurement. That is recorded as a loss. The false-positive "
     "rate is now swept across four values, none of which is measured, and no "
     "claim rests on any particular one."),

    ("The audit refuses more than it grants.",
     "{n_contested} of the {n_cf} audited pairs are CONTESTED — a defensible "
     "alternative specification changes their verdict — and they are "
     "published as formal results awaiting an argument rather than as "
     "measured control failures. One prediction was withdrawn as misspecified "
     "before it was run, respecified, run, and then narrowed by its own "
     "result."),

    ("One instance establishes nothing about a class.",
     "{n_held} controls held — {n_held_contested} of them against a "
     "specification the audit contests — and {n_gaps} gaps survived, in one "
     "reconstructed surface, on a small number of paths. The register of "
     "{n_losses} recorded losses includes the one that matters most here: the "
     "paper was written to a complete manuscript before the literature was "
     "searched at all."),
]

KEYWORDS = [
    "enterprise resource planning", "SAP", "autonomous agents", "agentic AI",
    "access control", "authorisation", "separation of duties",
    "aggregation problem", "usage control", "audit and attribution",
    "security evaluation", "pre-registration",
]


def text() -> str:
    return TEMPLATE.format(**_numbers())


def bounds() -> list[tuple[str, str]]:
    n = _numbers()
    return [(t, b.format(**n)) for t, b in BOUNDS]


def check() -> list[str]:
    problems = []
    n = _numbers()
    body = text()

    low = body.lower()
    for h in HEDGES:
        if h in low:
            problems.append("the abstract hedges: %r" % h)
    for e in ESCALATIONS:
        if e in low:
            problems.append("the abstract exceeds its evidence class: %r" % e)

    # Every number in the abstract must come from the interpolation, never
    # from the keyboard. A literal digit in the template is a figure that can
    # drift, and this project has spent a lot of effort on that exact failure.
    import re
    stray = re.findall(r"(?<![\w.{])\d[\d,]*", TEMPLATE)
    if stray:
        problems.append("the abstract template contains typed numbers %s -- "
                        "every figure must be interpolated from the code that "
                        "produced it" % stray)

    # The abstract may not be more confident than the release state.
    if not releasable():
        if "reconstruct" not in low:
            problems.append("the release state is not releasable and the "
                            "abstract does not say the surface is "
                            "reconstructed")
        if "validation" not in " ".join(b for _, b in bounds()).lower():
            problems.append("the bounds do not carry the validation status")

    # It must not claim novelty the related-work section has taken away.
    for phrase in ("we introduce the principle", "novel principle",
                   "for the first time", "we are the first",
                   "a new class of", "previously unrecognised"):
        if phrase in low:
            problems.append("the abstract claims novelty the related-work "
                            "section removed: %r" % phrase)
    if n["n_ant"] and "not new" not in " ".join(t for t, _ in bounds()).lower():
        problems.append("%d works anticipate part of the contribution and no "
                        "bound says so" % n["n_ant"])

    if n["n_tested"] != n["n_pairs"] and "All {n_pairs}" in TEMPLATE:
        problems.append("the abstract says every pair has been tested and "
                        "%d of %d have" % (n["n_tested"], n["n_pairs"]))
    if len(body.split()) > 400:
        problems.append("the abstract is %d words; a reader decides in one "
                        "screen" % len(body.split()))
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   abstract: %d words, 0 hedges, 0 escalations, %d bounds, "
              "every figure interpolated." % (len(text().split()),
                                              len(BOUNDS)))
        return

    print("# %s" % TITLE)
    print()
    print("### %s" % subtitle())
    print()
    print("## Abstract")
    print()
    print(text())
    print()
    print("### What bounds it")
    print()
    for t, b in bounds():
        print("**%s** %s" % (t, b))
        print()
    if open_blockers():
        print("> This is **version 1.0**, a complete independent study on a "
              "reconstructed model, with %d primary-source validation items "
              "still to complete before a validated edition. Its scope and the "
              "external validation still to be done are set out in full in the "
              "final part." % len(open_blockers()))
        print()
    print("**Keywords:** %s." % "; ".join(KEYWORDS))
    print()


if __name__ == "__main__":
    main()
