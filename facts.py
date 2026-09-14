"""
facts.py -- the numbers, in one place, plus a list of the ones that retired.

    python3 facts.py            # the table
    python3 facts.py --check    # no artefact may quote a retired figure

Every module in this repository generates its own prose from its own source,
which is what stops any single artefact drifting from the code behind it. It
does not stop a figure produced by ONE module being quoted in the prose of
another, and then going stale there when the experiment changes.

That is not hypothetical. When X11 gained a false-positive dimension its
configuration count went from 3,200 to 12,800 and its discriminating count from
1,256 to 2,512. The results section, the abstract, the boundary map and the
control-surface specification all followed, because all four read the numbers
from the experiment. The narrative, the related-work section, the
pre-registration status line and the chapter table did not, because all four
had the old numbers typed into their prose. Every check passed. A hostile
reader found them.

So there are two mechanisms here. `FACTS` is the single source any module may
quote from. `RETIRED` is a list of figures that were once correct and are not
any more, and `--check` fails the build if one of them appears in a generated
artefact. The second exists because the first cannot be enforced: nothing stops
someone typing a number, and the only way to catch a typed number is to know
which typed numbers are wrong.
"""
from __future__ import annotations

import functools
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


@functools.lru_cache(maxsize=1)
def facts() -> dict:
    from boundary import GAPS, HELD
    from counterfactual import CF, contested
    from losses_sap import LOSSES
    from mismatch import PAIRS
    from prereg_sap import PREREG
    from relatedwork import WORKS, anticipating
    from sapsec.experiments import x7, x11, x12
    from surface import EXCLUSIONS, MECHANISMS

    r7, r11, r12 = x7(), x11(), x12()
    p = r7["primary"]
    return {
        # X7
        "x7_configs": p.n_configs,
        "x7_hold": p.n_prevent_harm,
        "x7_best": 100 * p.best_legit_fraction,
        # X11
        "x11_configs": r11["n_configs"],
        "x11_disc": r11["n_discriminating"],
        "x11_needs_catalogue": r11["needs_catalogue"],
        "x11_request_only": r11["n_request_only"],
        "x11_detective_only": r11["n_detective_only"],
        "x11_no_atc": r11["n_no_atc"],
        "x11_no_atc_disc": r11["n_no_atc_discriminating"],
        "x11_arm": r11["n_arm"],
        # X12
        "x12_conditions": r12["n_conditions"],
        "x12_no_signal": r12["n_no_signal"],
        "x12_no_signal_moved": r12["n_no_signal_moved"],
        # the registers
        "pairs": len(PAIRS),
        "contested": len(contested()),
        "audited": len(CF),
        "held": len(HELD),
        "gaps": len(GAPS),
        "experiments": len(PREREG),
        "losses": len(LOSSES),
        "mechanisms": len(MECHANISMS),
        "exclusions": len(EXCLUSIONS),
        "works": len(WORKS),
        "anticipating": len(anticipating()),
    }


def n(key: str) -> str:
    """A figure, formatted with thousands separators. Quote this, never a
    literal."""
    v = facts()[key]
    return "{:,}".format(v) if isinstance(v, int) else "%.1f" % v


# Figures that were correct once and are not any more. Each entry is the
# retired value, the fact it used to be, and when it stopped being true.
RETIRED = [
    ("3,200 configurations", "x11_configs",
     "X11 gained a swept false-positive rate (loss L6)"),
    ("1,256 discriminating", "x11_disc", "same"),
    ("1,256 configurations", "x11_disc", "same"),
    ("200 configurations whose", "x11_request_only", "same"),
    ("952", "x11_needs_catalogue",
     "the catalogue share was computed by subtraction rather than "
     "counterfactually, and overstated it by half"),
    ("five-of-five", "pairs", "the formalism went from five pairs to eight"),
    ("three experiments", "experiments",
     "X11 and X12 were registered and run"),
    ("Three stories", "held", "a fourth story was added for X11"),
]


def check() -> list[str]:
    problems = []
    f = facts()
    for k, v in f.items():
        # Zero is a real result here -- `x12_no_signal_moved` being zero is
        # the finding -- so only a negative is impossible.
        if isinstance(v, int) and v < 0:
            problems.append("%s is %d, which cannot be right" % (k, v))

    # A retired figure appearing in a generated artefact, or in the one
    # module that writes prose of its own.
    #
    # Two things are deliberately not scanned. `FACTS.md` quotes every retired
    # figure by construction -- it is the register of them -- and forbidding
    # the register of forbidden numbers would be silly. `PAPER.md` is an
    # assembly of artefacts that have each been checked already, plus that
    # register, and it is written AFTER these checks run, so scanning it would
    # be judging the previous build. That was the defect the stale-ignorance
    # check took three attempts to shake off and it is not repeated here.
    # `paper.py` is scanned instead, because it is the only assembler that
    # contributes prose of its own.
    targets = [q for q in sorted(glob.glob(os.path.join(HERE, "*.md")))
               if os.path.basename(q) not in ("FACTS.md", "PAPER.md")]
    targets.append(os.path.join(HERE, "paper.py"))
    for path in targets:
        name = os.path.basename(path)
        text = open(path).read()
        for phrase, key, why in RETIRED:
            if phrase in text:
                problems.append(
                    "%s quotes the retired figure %r. It is now %s (%s). "
                    "Quote `facts.n(%r)` instead of typing it."
                    % (name, phrase, n(key), why, key))
    return problems


def main():
    if "--check" in sys.argv:
        p = check()
        for x in p:
            print("  " + x, file=sys.stderr)
        if p:
            sys.exit(1)
        print("   %d shared figures, %d retired figures, none quoted."
              % (len(facts()), len(RETIRED)))
        return

    print("# The figures, and where each comes from")
    print()
    print("*Generated by `python3 facts.py`. Do not edit by hand.*")
    print()
    print("Every module here generates its prose from its own source, which "
          "stops any one artefact drifting from the code behind it. It does "
          "not stop a figure produced by one module being typed into the "
          "prose of another and going stale there. This table is what a "
          "module quotes instead; the list beneath it is what the build "
          "refuses to let one quote.")
    print()
    print("| figure | value |")
    print("|:---|---:|")
    for k in facts():
        print("| `%s` | %s |" % (k, n(k)))
    print()
    print("## Retired")
    print()
    print("| was | is | why it changed |")
    print("|:---|---:|:---|")
    for phrase, key, why in RETIRED:
        print("| %s | %s | %s |" % (re.sub(r"\s+", " ", phrase), n(key), why))
    print()


if __name__ == "__main__":
    main()
