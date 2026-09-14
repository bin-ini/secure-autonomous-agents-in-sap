"""
verify.py -- adversarial checks on the SAP arm, run before any result is
written up.

Three of this project's worst moments came from measurements that could not
have come out any other way: a harm predicate that was a hardcoded string, a
control whose whole body could be deleted without failing a test, and an
approval gate that "worked" by substring-matching a tool's own name. So every
gate here is mutation-tested -- delete or neuter its body, and a test must fail
-- and every harm predicate has a negative control that turns the harm off.

    python3 verify.py
"""
from __future__ import annotations

import sys

from sapsec import experiments as E
from sapsec import model as M
from sapsec import workload as W

FAILS: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print("  %-58s %s" % (name, "ok" if ok else "FAIL"))
    if not ok:
        FAILS.append("%s %s" % (name, detail))


# ---------------------------------------------------------------------------
print("construction")

# The pre-registered non-discriminating condition must be enforced, not
# assumed. If the guard cannot fire, it is not a guard.
try:
    W.assert_indistinguishable(W.legitimate(), W.fraud_above_band())
    fired = False
except AssertionError:
    fired = True
check("indistinguishability guard fires on the above-band arm", fired)

try:
    W.assert_indistinguishable(W.legitimate(), W.fraud_overlapping())
    ok = True
except AssertionError as e:
    ok, _ = False, print("     ", e)
check("...and passes on the primary arm", ok)

# AUTHORITY-CHECK is per instance, not unioned across instances. A union model
# is strictly more permissive than SAP and would manufacture findings.
p = M.Principal("U", roles=(M.Role("R", (
    M.Authorization("F_BKPF_BUK", {"BUKRS": frozenset({"1000"}),
                                   "ACTVT": frozenset({"02"})}),
    M.Authorization("F_BKPF_BUK", {"BUKRS": frozenset({"2000"}),
                                   "ACTVT": frozenset({"01"})}),)),))
check("authority check does not union fields across instances",
      not p.has("F_BKPF_BUK", BUKRS="1000", ACTVT="01"))
check("...and still passes a genuinely covered combination",
      p.has("F_BKPF_BUK", BUKRS="2000", ACTVT="01"))

# ---------------------------------------------------------------------------
print("\nnegative controls -- the harm must be caused by the attack")

cfg_open = E.SapConfig(frozenset({"*"}), frozenset({"*"}), frozenset({"*"}),
                       float("inf"), float("inf"))
legit_only = E.run_workload(cfg_open, W.legitimate()).credited_total(W.DOC_TYPE)
attacked = E.run_workload(
    cfg_open, W.interleave(W.legitimate(), W.fraud_overlapping())
).credited_total(W.DOC_TYPE)
check("legitimate workload alone is BELOW materiality",
      legit_only < W.MATERIALITY, "%.0f" % legit_only)
check("attacked session is ABOVE materiality",
      attacked > W.MATERIALITY, "%.0f" % attacked)

# The budget must actually bind, or the proposed repair is decoration.
capped = E.run_workload(
    E.SapConfig(frozenset({"*"}), frozenset({"*"}), frozenset({"*"}),
                float("inf"), float("inf"), 400_000.),
    W.interleave(W.legitimate(), W.fraud_overlapping()))
check("cumulative budget changes the outcome",
      capped.credited_total(W.DOC_TYPE) < attacked)

# ---------------------------------------------------------------------------
print("\nmutation tests -- neuter a gate, a result must move")

_real_tol = M.ToleranceGroup.permits
M.ToleranceGroup.permits = lambda self, doc: True
try:
    ctrl = E.sweep(W.fraud_above_band)
    check("neutering the tolerance gate breaks the positive control",
          not ctrl.clean_separation,
          "still separates at legit=%.3f" % ctrl.best_legit_fraction)
finally:
    M.ToleranceGroup.permits = _real_tol

ctrl_real = E.sweep(W.fraud_above_band)
check("...and the real tolerance gate does separate it",
      ctrl_real.clean_separation,
      "legit=%.3f" % ctrl_real.best_legit_fraction)

_real_auth = M.Authorization.permits
M.Authorization.permits = lambda self, checked: True
try:
    wrong_cc = E.run_workload(
        E.SapConfig(frozenset({"01"}), frozenset({"2000"}), frozenset({"DG"}),
                    float("inf"), float("inf")), W.legitimate())
    check("neutering the authority check unblocks a wrong company code",
          wrong_cc.posted_count() > 0)
finally:
    M.Authorization.permits = _real_auth

right = E.run_workload(
    E.SapConfig(frozenset({"01"}), frozenset({"2000"}), frozenset({"DG"}),
                float("inf"), float("inf")), W.legitimate())
check("...and the real authority check blocks it",
      right.posted_count() == 0)

# ---------------------------------------------------------------------------
print("\nX8 -- the test must not be rigged")

r8 = E.x8()
check("neither propagated principal violates the ruleset",
      all(v == [] for v in r8["ara"].values()), str(r8["ara"]))
check("the composed sequence produces the harm", r8["harm"])
check("the same sequence by two colluding humans produces the same harm",
      r8["collusion_harm"])
check("a technical user holding BOTH grants IS flagged",
      r8["tech_violations"] != [],
      "if this were empty the ruleset would be inert")

# ---------------------------------------------------------------------------
print("\nbook stack -- confirm no control fires, rather than assuming it")

try:
    bs = E.book_stack()
    check("every posting executes with all controls enabled",
          bs["executed"] == bs["n"] and bs["blocked"] == 0,
          str(bs["blockers"]))

    E._load_agentsec()
    from agentsec.controls import Controls  # noqa: E402
    _default = Controls()
    check("Controls() carries no field naming rate, budget or accumulation",
          not any(k in f for f in _default.__dataclass_fields__
                  for k in ("rate", "budget", "quota", "cumul", "limit")),
          "a field like that would mean the book already had the answer")
except E.CompanionTestbedMissing as exc:
    print("  SKIPPED: %s" % exc)

# ---------------------------------------------------------------------------
print()
if FAILS:
    print("%d FAILED:" % len(FAILS))
    for f in FAILS:
        print("  " + f)
    sys.exit(1)
print("all checks passed.")
