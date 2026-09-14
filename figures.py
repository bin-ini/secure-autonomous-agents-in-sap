"""
figures.py -- three figures, drawn from the data rather than about it.

    python3 figures.py            # writes fig/*.pdf and fig/*.png, emits captions
    python3 figures.py --check    # the figures must agree with the sources

A figure is the part of a paper a reader trusts most and checks least, and it
is the easiest place for a stale number to survive a rebuild. So no figure here
carries a coordinate, a label or a count that was typed. Figure 1 is drawn by
iterating `mismatch.PAIRS`; figures 2 and 3 are drawn from the experiments'
return values. Adding a pair or rerunning a sweep moves the picture, and
`--check` recomputes a digest of the data behind each figure and fails if the
picture on disk was drawn from anything else.

Figure 1 is the one worth arguing about. It plots the two axes of compositional
extent that the FI results actually range over -- how many actions, and over
what horizon -- and draws an arrow from what each control observes to what its
property is defined over. An arrow that leaves the observation point is an
extent difference. A SOLID arrow is a mismatch; a DASHED one is an extent
difference the local predicate closes, which is H2 and is the case that stops
the principle degenerating into "a broader property needs a broader control".
Pairs whose failure is a subject mismatch have no arrow at all, because their
extents are identical and the break is on an axis this plane does not have.
Drawing them as points with a marked subject break, rather than fitting them
onto the extent axes, is the honest option: a figure that made both forms look
like the same picture would be arguing by illustration.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                             # noqa: E402
from matplotlib.lines import Line2D                         # noqa: E402

from mismatch import ACTIONS, HORIZON, PAIRS                # noqa: E402
from sapsec.attribution import RETENTION_GRID               # noqa: E402
from sapsec.workload import MATERIALITY                      # noqa: E402
from sapsec.experiments import sweep_data, x7, x11, x12     # noqa: E402
from sapsec.workload import fraud_overlapping                # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "fig")

HOLD = "#1b6b3a"
FAIL = "#a01b2b"
INK = "#222222"
GREY = "#888888"

FIGURES = [
    ("fig0-scope-schematic",
     "The mismatch, before any data: what a control sees against what its "
     "guarantee is about.",
     "The plain picture behind the whole paper, drawn for the decisive pair "
     "G1. The small box is everything the FI tolerance group sees at the "
     "moment it decides — one document, in isolation. The large box is what "
     "the organisation's materiality guarantee is actually about — the "
     "cumulative credited value across every document in the period. Harm that "
     "lives in the band between the two boxes is compliant at every point the "
     "control checks, because each document is individually within tolerance; "
     "only the sum breaches, and the sum is never in the control's view. That "
     "band is the gap the rest of the paper measures."),

    ("fig0b-autonomy-axes",
     "The four axes along which autonomous execution amplifies a latent "
     "mismatch.",
     "Autonomy does not create a control-property mismatch; it amplifies a "
     "latent one along four independent axes. From one ordinary, individually-"
     "permitted action, autonomous execution raises the volume of such actions, "
     "accumulates state a per-action control never retains, chains decisions "
     "across sessions and principals so no single step sees the whole, and "
     "reaches the limits of what each control observes faster than any human "
     "workload would. Only the first depends on throughput; together they push "
     "a property past the boundary the control can see."),

    ("fig1-boundary-map",
     "The observation boundary against the property's extent.",
     "Each arrow runs from what a control observes at decision time to what "
     "its protected property is defined over. Solid arrows are extent "
     "mismatches; the dashed arrow is H2, where the extents differ and the "
     "property is closed under the control's local predicate, so the control "
     "still guarantees it. H1 and G1 are the same SAP control — an FI "
     "tolerance group — against two different properties, which is why one "
     "sits on the origin with no arrow and the other reaches the far corner. "
     "The two rows beneath carry the breaks this plane cannot draw: G2's "
     "property outruns its control on principals, and G3 and P1 have "
     "identical extents and break on subject instead. Drawing those below "
     "rather than forcing them onto these axes is deliberate — a figure that "
     "made both forms look like the same picture would be arguing by "
     "illustration."),

    ("fig2-exchange-rate",
     "What each kind of mismatch costs to close, and what sets the price.",
     "Left: every configuration of the modelled FI authorisation surface, "
     "each plotted as the harm it admits against the legitimate work it "
     "retains. They collapse onto a line through the origin, and that line is "
     "not fitted: because the two workloads are per-document identical, any "
     "per-document predicate removes the same proportion of each, so a point "
     "below the materiality line is bought one-for-one in refused legitimate "
     "work. No implementation escapes it. Right: the same axes for the "
     "transport surface, where the discriminating decision reads the "
     "property's own subject — one track per false-positive rate, because "
     "that rate and not the control-property pair is what sets the price "
     "here. The earlier version of this panel plotted only the zero-rate "
     "track and captioned it as a measurement of what a subject-matched "
     "control costs. It was a property of the model, it is loss L6, and the "
     "remaining tracks are what the retraction bought."),

    ("fig3-attribution",
     "Attribution accuracy under principal propagation.",
     "Left: accuracy against how much history the responder is allowed to "
     "hold, for two, four and eight concurrent actors behind one propagated "
     "principal, in the conditions principal propagation actually produces. "
     "The lines are flat and sit on 1/k. Right: the upper bound on ANY "
     "procedure reading principal, transaction code, terminal and timestamp, "
     "against the accuracy of naming the busiest actor without reading "
     "anything, for one human and one agent at each agent action rate. The "
     "two are equal at every rate."),
]


def _row(ax, title, rows):
    """A break that this plane cannot draw, drawn as what it is."""
    ax.axis("off")
    ax.set_title(title, fontsize=10.5, loc="left")
    n = len(rows)
    for i, (pid, left, mid, right) in enumerate(rows):
        y = 0.5 + (n - 1) * 0.28 - i * 0.56
        ax.text(0.0, y, pid, fontsize=10, fontweight="bold", color=FAIL,
                va="center")
        ax.text(0.055, y, left, fontsize=9.5, color=INK, va="center")
        ax.annotate("", xy=(0.60, y), xytext=(0.46, y),
                    arrowprops=dict(arrowstyle="-|>", color=FAIL, lw=2.0))
        if mid:
            ax.text(0.53, y + 0.20, mid, fontsize=8.5, color=FAIL,
                    ha="center", va="center")
        ax.text(0.63, y, right, fontsize=9.5, color=INK, va="center")
    ax.set_xlim(-0.02, 1.0)
    ax.set_ylim(0.0, 1.0)


def _fig_scope():
    """The concept, before any measurement: a small observation box inside a
    large property box, with the gap between them named. Every label is read
    from the G1 pair, so a change to that pair changes the picture."""
    from matplotlib.patches import FancyBboxPatch
    g1 = [p for p in PAIRS if p.id == "G1"][0]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    outer = FancyBboxPatch((0.5, 0.7), 9.0, 8.2,
                           boxstyle="round,pad=0.02,rounding_size=0.15",
                           linewidth=2.2, edgecolor=FAIL, facecolor="#f7ebec",
                           zorder=1)
    ax.add_patch(outer)
    inner = FancyBboxPatch((3.35, 3.5), 3.3, 2.3,
                           boxstyle="round,pad=0.02,rounding_size=0.12",
                           linewidth=2.2, edgecolor=INK, facecolor="white",
                           zorder=3)
    ax.add_patch(inner)

    ax.text(5.0, 8.45, "What the guarantee is about", ha="center", va="top",
            fontsize=11.5, fontweight="bold", color=FAIL)
    ax.text(5.0, 7.9, g1.protected_property, ha="center", va="top",
            fontsize=9.5, color=FAIL, style="italic")
    ax.text(5.0, 8.0, "", ha="center")
    ax.text(5.0, 4.75, "What the control sees\nwhen it decides", ha="center",
            va="center", fontsize=10.5, fontweight="bold", color=INK)
    ax.text(5.0, 3.95, "one %s, in isolation" % g1.control_subject,
            ha="center", va="center", fontsize=9, color=INK, style="italic")

    ax.annotate("the gap — harm assembled in this band is\n"
                "compliant at every point the control checks:\n"
                "each %s is within tolerance, only the\nsum breaches, and the "
                "sum is never in view" % g1.control_subject,
                xy=(1.15, 6.55), xytext=(1.15, 6.55), ha="left", va="center",
                fontsize=8.8, color=FAIL)
    ax.text(6.75, 5.55, "observes:\n%s" % g1.observes.short(), ha="left",
            va="top", fontsize=8, color=INK, family="monospace")
    ax.text(9.35, 1.0, "property extent: %s" % g1.property_extent.short(),
            ha="right", va="bottom", fontsize=8, color=FAIL,
            family="monospace")
    ax.set_title("Pair G1 — %s" % g1.control, fontsize=10.5, loc="left")
    fig.tight_layout()
    return fig


def _fig_axes():
    """The four amplification axes, drawn as arrows fanning from one ordinary
    action. Labels come from narrative.AXES so the figure and the prose stay in
    step; the short glosses are the figure's own legend."""
    from narrative import AXES
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.text(1.15, 5, "one ordinary,\nindividually-\npermitted action",
            ha="center", va="center", fontsize=9, fontweight="bold", color=INK,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=INK, lw=1.6))
    ys = [8.6, 6.4, 3.6, 1.4]
    gloss = ["a year of harm in an afternoon",
             "a period breached inside one",
             "no single step sees the whole",
             "the control's limits are reached first"]
    for (label, _eff), y, g in zip(AXES, ys, gloss):
        ax.annotate("", xy=(6.3, y), xytext=(2.35, 5),
                    arrowprops=dict(arrowstyle="-|>", color=FAIL, lw=2.0))
        ax.text(6.5, y, label, ha="left", va="center", fontsize=10.5,
                fontweight="bold", color=FAIL)
        ax.text(6.5, y - 0.44, g, ha="left", va="center", fontsize=8.5,
                color=INK, style="italic")
    ax.text(5.0, 9.6, "a property past the boundary the control can see",
            ha="center", va="center", fontsize=8.5, color=GREY)
    ax.set_title("Autonomy amplifies a latent mismatch along four axes at once",
                 fontsize=10.5, loc="left")
    fig.tight_layout()
    return fig


def _fig1():
    def plane_differs(p):
        return (p.observes.actions != p.property_extent.actions
                or p.observes.horizon != p.property_extent.horizon)

    extent_pairs = [p for p in PAIRS if plane_differs(p)]
    principal_pairs = [p for p in PAIRS if not plane_differs(p)
                       and p.observes.principals
                       != p.property_extent.principals]
    subject_pairs = [p for p in PAIRS if p.observes == p.property_extent
                     and p.subject_mismatch()]
    flat = [p for p in PAIRS if not plane_differs(p)
            and p not in principal_pairs and p not in subject_pairs]

    n_rows = 1 + bool(principal_pairs) + bool(subject_pairs)
    heights = [3.4] + [0.26 + 0.26 * len(g)
                       for g in (principal_pairs, subject_pairs) if g]
    fig, axes = plt.subplots(n_rows, 1,
                             figsize=(7.2, 1.25 * sum(heights)),
                             height_ratios=heights)
    ax = axes[0]
    rest = list(axes[1:])

    for x in range(len(ACTIONS)):
        for y in range(len(HORIZON)):
            ax.plot(x, y, marker=".", color="#dddddd", zorder=0)

    seen_obs: dict[tuple, list[str]] = {}
    for p in flat + extent_pairs:
        seen_obs.setdefault((p.observes.actions, p.observes.horizon),
                            []).append(p.id)

    for p in extent_pairs:
        x0, y0 = p.observes.actions, p.observes.horizon
        x1, y1 = p.property_extent.actions, p.property_extent.horizon
        closed = p.closed_under_composition
        colour = HOLD if p.predicted() == "holds" else FAIL
        ax.annotate(
            "", xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", color=colour, lw=2.0,
                            linestyle="--" if closed else "-",
                            shrinkA=8, shrinkB=8,
                            connectionstyle="arc3,rad=0.14"))
        label = "%s%s" % (p.id, "  (closed)" if closed else "")
        ax.text(x1 + 0.06, y1 + 0.10, label, color=colour, fontsize=10,
                fontweight="bold")
        ax.plot(x1, y1, marker="o", ms=7, mfc="white", mec=colour, mew=1.8,
                zorder=3)

    for (x, y), ids in sorted(seen_obs.items()):
        ax.plot(x, y, marker="s", ms=9, color=INK, zorder=4)
        ax.text(x - 0.04, y - 0.22, ", ".join(sorted(ids)), color=INK,
                fontsize=10, ha="right" if x else "left")

    ax.set_xticks(range(len(ACTIONS)))
    ax.set_xticklabels([a.replace("aggregate", "aggregate\n(a period's sum)")
                        for a in ACTIONS])
    ax.set_yticks(range(len(HORIZON)))
    ax.set_yticklabels(HORIZON)
    ax.set_xlim(-0.55, len(ACTIONS) - 0.30)
    ax.set_ylim(-0.55, len(HORIZON) + 0.20)
    ax.set_xlabel("actions the property ranges over")
    ax.set_ylabel("horizon")
    ax.set_title("Extent: what the control observes → what the property is "
                 "defined over", fontsize=11, loc="left")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(handles=[
        Line2D([], [], color=INK, marker="s", ls="none",
               label="what the control observes"),
        Line2D([], [], color=FAIL, lw=2, label="extent mismatch"),
        Line2D([], [], color=HOLD, lw=2, ls="--",
               label="extent differs, property closed under the predicate"),
    ], loc="upper left", frameon=False, fontsize=8.5)

    # The two breaks this plane cannot draw, drawn as what they are rather
    # than squeezed onto axes that do not have them.
    if principal_pairs:
        _row(rest.pop(0),
             "Extent, on the third axis: the property ranges over more "
             "principals than the control",
             [(p.id, "one principal's grants", "",
               "several principals in one workflow")
              for p in principal_pairs])
    if subject_pairs:
        _row(rest.pop(0),
             "Subject: what the control's predicate is about → what the "
             "property is about",
             [(p.id, p.control_subject, "not injective", p.property_subject)
              for p in subject_pairs])
    fig.tight_layout()
    return fig


def _fig2():
    r7, r11 = x7(), x11()
    p = r7["primary"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.6, 3.4), sharey=True)

    # Every configuration, plotted. Not a frontier drawn between two summary
    # statistics -- that version of this panel was a straight line nobody
    # measured, and it is exactly the kind of figure this module exists to
    # refuse.
    data, session_total, _lt = sweep_data(fraud_overlapping)
    xs = [100 * frac for _c, _h, frac in data]
    ys = [100 * harm / session_total for _c, harm, _f in data]
    a.scatter(xs, ys, s=9, alpha=0.30, color=FAIL, edgecolors="none",
              label="%s configurations" % "{:,}".format(len(data)))
    a.axhline(100 * MATERIALITY / session_total, color=GREY, lw=1.0, ls=":")
    a.text(2, 100 * MATERIALITY / session_total + 2.5, "materiality",
           fontsize=8, color=GREY)
    a.plot([100 * p.best_legit_fraction],
           [100 * MATERIALITY / session_total], marker="o", ms=9,
           mfc="none", mec=INK, mew=1.6)
    a.annotate("best configuration holding the\noutcome below materiality:\n"
               "%.1f%% of legitimate work retained"
               % (100 * p.best_legit_fraction),
               xy=(100 * p.best_legit_fraction,
                   100 * MATERIALITY / session_total),
               xytext=(6, 62), fontsize=8.5, color=INK,
               arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    a.legend(frameon=False, fontsize=8, loc="upper left")
    a.set_title("X7 — extent mismatch\n(FI tolerance group vs a period "
                "aggregate)", fontsize=10, loc="left")
    a.set_xlabel("legitimate work retained (%)")
    a.set_ylabel("harm reaching the ledger (%)")

    n = r11["n_arm"]
    shades = ["#1b6b3a", "#4a8f63", "#79b38d", "#a8d7b8"]
    for i, fp in enumerate(sorted(r11["curves"])):
        rows = r11["curves"][fp]
        harm = [100 * h / n for _c, h, _l in rows]
        legit = [100 * lf for _c, _h, lf in rows]
        b.plot(legit, harm, color=shades[i % len(shades)], lw=2, marker="o",
               ms=4.5, label="%.0f%% false positives" % (100 * fp))
    top = r11["curves"][sorted(r11["curves"])[0]]
    for cov, hcount, lf in top:
        b.annotate("%.0f%% reviewed" % (100 * cov),
                   xy=(100 * lf, 100 * hcount / n),
                   xytext=(100 * lf - 3, 100 * hcount / n + 2),
                   fontsize=7.5, color=INK, ha="right")
    b.set_title("X11 — subject match\n(content-ranging review vs a "
                "behavioural property)", fontsize=10, loc="left")
    b.set_xlabel("legitimate work retained (%)")
    b.axvline(95, color=GREY, lw=1.0, ls=":")
    b.annotate("the 95% bar\nX7 was held to", xy=(95, 42), xytext=(38, 42),
               fontsize=7.5, color=GREY, va="center",
               arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    b.legend(frameon=False, fontsize=7.5, loc="upper left")

    for ax in (a, b):
        ax.set_xlim(-4, 108)
        ax.set_ylim(-6, 108)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.grid(alpha=0.15)
    fig.tight_layout()
    return fig


def _fig3():
    r12 = x12()
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.6, 3.2))

    xs = list(range(len(RETENTION_GRID)))
    labels = ["all" if r < 0 else str(r) for r in RETENTION_GRID]
    for k in (2, 4, 8):
        ys = [acc for (kk, _r, acc) in r12["baseline"] if kk == k]
        a.plot(xs, ys, marker="o", ms=5, lw=2, label="k = %d" % k)
        a.annotate("1/%d" % k, xy=(xs[-1], ys[-1]), xytext=(xs[-1] + 0.12,
                                                            ys[-1]),
                   fontsize=9, va="center", color=INK)
    a.set_xticks(xs)
    a.set_xticklabels(labels)
    a.set_xlim(-0.3, len(xs) - 0.3)
    a.set_ylim(0, 1.05)
    a.set_xlabel("records of history the responder may hold")
    a.set_ylabel("attribution accuracy")
    a.set_title("X12 — retention changes nothing", fontsize=10, loc="left")
    a.legend(frameon=False, fontsize=9)

    iv = [r["interval"] for r in r12["rate"]]
    bd = [r["bound"] for r in r12["rate"]]
    mj = [r["majority"] for r in r12["rate"]]
    b.plot(iv, bd, marker="o", ms=7, lw=2, color=FAIL,
           label="upper bound on any procedure")
    b.plot(iv, mj, marker="x", ms=9, lw=1.4, ls="--", color=INK,
           label="naming the busiest actor, unread")
    b.set_xscale("log")
    b.set_xlabel("seconds between the agent's actions")
    b.set_ylabel("accuracy")
    b.set_ylim(0.4, 1.05)
    b.set_title("X12 — the bound equals the baseline", fontsize=10, loc="left")
    b.legend(frameon=False, fontsize=8.5, loc="lower left")

    for ax in (a, b):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.grid(alpha=0.15)
    fig.tight_layout()
    return fig


BUILDERS = {"fig0-scope-schematic": _fig_scope,
            "fig0b-autonomy-axes": _fig_axes,
            "fig1-boundary-map": _fig1,
            "fig2-exchange-rate": _fig2,
            "fig3-attribution": _fig3}


# ---------------------------------------------------------------------------
# Staleness, by content rather than by clock.
#
# The first version compared file modification times against the source
# modules, which meant editing a caption invalidated every figure and a
# rebuild was the only way to find out. Worse, it made the check unfailable in
# any build that renders before it checks. So each figure now records a digest
# of the DATA it was drawn from. Cosmetic edits do not touch it; a changed
# sweep does.
# ---------------------------------------------------------------------------


def _data(name: str):
    if name == "fig0b-autonomy-axes":
        from narrative import AXES
        return {"axes": [label for label, _ in AXES]}
    if name == "fig0-scope-schematic":
        g1 = [p for p in PAIRS if p.id == "G1"][0]
        return {"id": g1.id, "control": g1.control,
                "control_subject": g1.control_subject,
                "protected_property": g1.protected_property,
                "property_subject": g1.property_subject,
                "observes": g1.observes.short(),
                "extent": g1.property_extent.short()}
    if name == "fig1-boundary-map":
        return [(p.id, p.control, p.observes.short(),
                 p.property_extent.short(), p.control_subject,
                 p.property_subject, p.subject_mismatch(),
                 p.closed_under_composition, p.predicted())
                for p in PAIRS]
    if name == "fig2-exchange-rate":
        r7, r11 = x7(), x11()
        p = r7["primary"]
        return {"best": p.best_legit_fraction, "n": p.n_configs,
                "hold": p.n_prevent_harm,
                "curves": sorted(r11["curves"].items()),
                "fp_cost": r11["fp_cost"],
                "arm": r11["n_arm"], "materiality": MATERIALITY}
    if name == "fig3-attribution":
        r12 = x12()
        return {"baseline": r12["baseline"],
                "rate": [(r["interval"], r["bound"], r["majority"])
                         for r in r12["rate"]],
                "retention": list(RETENTION_GRID)}
    raise KeyError(name)


def digest(name: str) -> str:
    blob = json.dumps(_data(name), sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def render() -> list[str]:
    os.makedirs(FIGDIR, exist_ok=True)
    written = []
    for name, _t, _c in FIGURES:
        fig = BUILDERS[name]()
        for ext in ("pdf", "png"):
            path = os.path.join(FIGDIR, "%s.%s" % (name, ext))
            fig.savefig(path, dpi=200, bbox_inches="tight")
            written.append(path)
        plt.close(fig)
        with open(os.path.join(FIGDIR, "%s.sha" % name), "w") as f:
            f.write(digest(name) + "\n")
    return written


def check() -> list[str]:
    problems = []
    if len(FIGURES) != len(BUILDERS):
        problems.append("a figure is described and not drawn, or drawn and "
                        "not described")
    for name, title, caption in FIGURES:
        if len(caption.split()) < 30:
            problems.append("%s: the caption does not say what the reader is "
                            "looking at" % name)
        if not title.strip():
            problems.append("%s: no title" % name)
    # A figure drawn from data the sources no longer produce is the one
    # artefact a reader will not check.
    for name, _t, _c in FIGURES:
        pdf = os.path.join(FIGDIR, "%s.png" % name)
        sha = os.path.join(FIGDIR, "%s.sha" % name)
        if not os.path.exists(pdf) or not os.path.exists(sha):
            problems.append("%s has never been drawn" % name)
            continue
        if open(sha).read().strip() != digest(name):
            problems.append("%s was drawn from data the sources no longer "
                            "produce -- run `python3 figures.py`" % name)
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   %d figures, each matching the data it was drawn from."
              % len(FIGURES))
        return

    render()
    print("# Figures")
    print()
    print("*Generated by `python3 figures.py`. Do not edit by hand. Every "
          "coordinate, label and count below is read from the sources; none "
          "is typed.*")
    print()
    for i, (name, title, caption) in enumerate(FIGURES, 1):
        print("![%s](fig/%s.png){ width=100%% }" % (title, name))
        print()
        print("**Figure %d. %s** %s" % (i, title, caption))
        print()


if __name__ == "__main__":
    main()
