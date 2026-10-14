"""HACOF prototype and simulation.

Two parts, kept deliberately separate:

1. A working prototype of HACOF's enforcement plane (real logic, no randomness):
   authorization profiles, an in-path gateway that allows / denies / holds each
   action, delegation that can only narrow a parent's profile, an append-only
   hash-chained audit log, and the Step-3 fallback (an unanswered hold expires
   to "denied").

2. A Monte Carlo simulation around it. Supervisors B, C and D are simulated
   detectors whose accuracy and error correlation are model parameters, not
   measurements of any real AI system. Every reported rate is a property of the
   simulation under the stated parameters.

Standard library only. Deterministic for a given seed.
Usage:  python3 hacof_sim.py            (writes results/*.csv and results/summary.json)
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import statistics
from dataclasses import dataclass, field
from statistics import NormalDist

# ----------------------------------------------------------------------------
# Part 1 — enforcement-plane prototype (deterministic)
# ----------------------------------------------------------------------------

ALLOW, DENY, HOLD = "allow", "deny", "hold"


@dataclass(frozen=True)
class Profile:
    """Machine-readable authorization profile (Layer 2)."""
    agent_id: str
    may_call: frozenset          # tools the agent may invoke at all
    needs_approval: frozenset    # tools that are permitted only with a human approval
    clause: dict = field(default_factory=dict, hash=False, compare=False)

    def delegate(self, child_id: str, tools: set) -> "Profile":
        """A sub-agent's profile can only narrow its parent's (monotonic delegation)."""
        return Profile(child_id,
                       frozenset(tools) & self.may_call,
                       frozenset(tools) & self.needs_approval,
                       self.clause)


@dataclass
class Action:
    session: int
    step: int
    agent_id: str
    tool: str
    outbound: bool          # moves data across the deployment boundary
    high_impact: bool       # e.g. a funds transfer
    malicious: bool         # ground truth (simulation only; never seen by the gateway)
    injected: bool          # attempt caused by an injected instruction (ground truth)
    routed: bool            # passes through the in-path gateway (fraction phi)
    unusual_legit: bool = False


class AuditLog:
    """Append-only, hash-chained record (audit plane). Tampering breaks the chain."""

    def __init__(self) -> None:
        self.entries: list[dict] = []
        self._head = "0" * 64

    def append(self, record: dict) -> None:
        payload = json.dumps(record, sort_keys=True)
        digest = hashlib.sha256((self._head + payload).encode()).hexdigest()
        self.entries.append({"prev": self._head, "hash": digest, **record})
        self._head = digest

    def verify(self) -> bool:
        head = "0" * 64
        for e in self.entries:
            rec = {k: v for k, v in e.items() if k not in ("prev", "hash")}
            payload = json.dumps(rec, sort_keys=True)
            if e["prev"] != head or hashlib.sha256((head + payload).encode()).hexdigest() != e["hash"]:
                return False
            head = e["hash"]
        return True


class Gateway:
    """In-path policy enforcement point (Layer 3). Pure rule evaluation: Agent A."""

    def __init__(self, profiles: dict[str, Profile], log: AuditLog) -> None:
        self.profiles = profiles
        self.log = log
        self.revoked: set[str] = set()

    def decide(self, a: Action) -> str:
        p = self.profiles.get(a.agent_id)
        if p is None or a.agent_id in self.revoked:
            verdict, rule = DENY, "no-profile-or-revoked"
        elif a.tool not in p.may_call:
            verdict, rule = DENY, "tool-not-in-profile"
        elif a.tool in p.needs_approval:
            verdict, rule = HOLD, "approval-required"
        else:
            verdict, rule = ALLOW, "in-profile"
        self.log.append({"s": a.session, "t": a.step, "agent": a.agent_id,
                         "tool": a.tool, "verdict": verdict, "rule": rule})
        return verdict

    @staticmethod
    def resolve_hold(responded: bool, approved: bool) -> str:
        """Step-3 fallback: an unanswered hold expires to denied, never to approved."""
        if not responded:
            return DENY
        return ALLOW if approved else DENY


def selftest() -> dict:
    """Deterministic checks of the prototype; returned and written to the summary."""
    log = AuditLog()
    parent = Profile("recon", frozenset({"ledger_read", "report", "payment"}),
                     frozenset({"payment"}))
    child = parent.delegate("recon.sub", {"ledger_read", "email", "payment"})
    gw = Gateway({"recon": parent, "recon.sub": child}, log)
    mk = lambda agent, tool: Action(0, 0, agent, tool, False, False, False, False, True)
    checks = {
        "in_profile_allowed": gw.decide(mk("recon", "report")) == ALLOW,
        "out_of_profile_denied": gw.decide(mk("recon", "email")) == DENY,
        "high_impact_held": gw.decide(mk("recon", "payment")) == HOLD,
        "delegation_cannot_widen": gw.decide(mk("recon.sub", "email")) == DENY,
        "delegation_keeps_hold": gw.decide(mk("recon.sub", "payment")) == HOLD,
        "unanswered_hold_denied": Gateway.resolve_hold(False, True) == DENY,
        "audit_chain_valid": log.verify(),
    }
    gw.revoked.add("recon")
    checks["revoked_agent_denied"] = gw.decide(mk("recon", "report")) == DENY
    log.entries[1]["verdict"] = ALLOW            # tamper with one record
    checks["tamper_detected"] = not log.verify()
    return checks


# ----------------------------------------------------------------------------
# Part 2 — simulation
# ----------------------------------------------------------------------------

@dataclass
class Params:
    # Workload (per session of L agent actions). Defaults are assumptions, not data.
    sessions: int = 2000
    L: int = 20
    p_attacked: float = 0.15        # session receives an injected instruction
    p_cred_compromise: float = 0.03 # session runs on stolen credentials
    p_comply: float = 0.6           # model follows an injected instruction (same in all arms)
    campaign_len: int = 3           # malicious attempts per compromised session
    p_unusual_legit: float = 0.02   # legitimate but unusual action (a legitimate transfer)
    phi: float = 0.95               # fraction of actions routed through the gateway
    # Simulated detectors: (detection rate on malicious, false-positive rate on benign)
    dD: float = 0.85; fpD: float = 0.02   # Agent D, in-path, outbound content only
    dB: float = 0.60; fpB: float = 0.01   # Agent B, out-of-path anomaly
    dC: float = 0.70; fpC: float = 0.005  # Agent C, out-of-path injection signs
    dC_cred: float = 0.20                 # Agent C on credential compromise (no injection text)
    fpB_unusual: float = 0.30             # anomaly FP on unusual-but-legitimate actions
    rho: float = 0.2                      # latent error correlation among B, C, D
    # Humans and containment
    p_respond: float = 0.90; p_human_correct: float = 0.95
    detect_latency: float = 1.0           # mean actions between execution and an out-of-path alert
    contain_latency: float = 1.0          # mean actions between alert and effective containment
    scrutiny_window: int = 5              # actions under raised scrutiny after a single alert
    p_F_reverse: float = 0.8              # Agent F + reviewer lift a false containment at review
    review_delay: float = 5.0             # mean actions from containment to human review
    # Baseline arm
    baseline_review_every: int = 50       # actions between periodic manual log reviews
    baseline_review_frac: float = 0.10    # fraction of logs read at each review
    arm: str = "hacof"     # hacof | baseline | no_supervisors | homog_declared | homog_hidden


TOOLS_BENIGN = ["ledger_read", "ledger_read", "report", "report"]
MAL_TYPES = [("email", True, False), ("report", True, False), ("payment", False, True),
             ("admin_escalate", False, True)]  # (tool, outbound, high_impact)
MAL_WEIGHTS = [0.35, 0.25, 0.25, 0.15]


def correlated_hits(rng: random.Random, rates: list[float], rho: float) -> list[bool]:
    """Bernoulli outcomes with a shared latent factor (one-factor Gaussian copula)."""
    common = rng.gauss(0, 1)
    out = []
    for r in rates:
        if r <= 0:
            out.append(False); continue
        if r >= 1:
            out.append(True); continue
        z = math.sqrt(rho) * common + math.sqrt(1 - rho) * rng.gauss(0, 1)
        out.append(z < NormalDist().inv_cdf(r))
    return out


def gen_session(rng: random.Random, s: int, P: Params) -> list[Action]:
    acts: list[Action] = []
    attacked = rng.random() < P.p_attacked
    cred = (not attacked) and rng.random() < P.p_cred_compromise
    start = rng.randrange(2, P.L - P.campaign_len) if (attacked or cred) else None
    complies = attacked and rng.random() < P.p_comply
    t = 0
    while t < P.L:
        if start is not None and t == start and (complies or cred):
            for _ in range(P.campaign_len):
                tool, outb, hi = rng.choices(MAL_TYPES, MAL_WEIGHTS)[0]
                acts.append(Action(s, t, "recon", tool, outb, hi, True, attacked,
                                   rng.random() < P.phi))
                t += 1
            continue
        if rng.random() < P.p_unusual_legit:
            acts.append(Action(s, t, "recon", "payment", False, True, False, False,
                               rng.random() < P.phi, unusual_legit=True))
        else:
            tool = rng.choice(TOOLS_BENIGN)
            acts.append(Action(s, t, "recon", tool, tool == "report" and rng.random() < 0.3,
                               False, False, False, rng.random() < P.phi))
        t += 1
    return acts


def run(P: Params, seed: int) -> dict:
    """One arm, one seed.

    Arms: baseline | no_supervisors (Ablation 1) | hacof |
          homog_declared (Ablation 2a: B, C, D are one model and are declared as such, so
                          condition (ii) does not count their agreement as two methods) |
          homog_hidden   (Ablation 2b: per-supervisor rates unchanged, errors correlated at
                          rho=0.9, but declared as different methods -- (ii) met on paper only).
    """
    rng = random.Random(seed)                       # decisions (detectors, humans, latencies)
    wrng = random.Random(1_000_003 * (seed + 1))    # workload: identical across arms (paired design)
    profile = Profile("recon", frozenset({"ledger_read", "report", "payment"}),
                      frozenset({"payment"}))
    arm = P.arm
    supervisors_on = arm in ("hacof", "homog_declared", "homog_hidden")
    rho = 0.9 if arm in ("homog_declared", "homog_hidden") else P.rho
    one_method = arm == "homog_declared"
    m = dict(mal=0, prevented=0, detected=0, executed=0, ttd=[], ttc=[], decision_logged=0,
             evidence_logged=0, benign=0, fp_block=0, fp_contain_sessions=0, collateral=0,
             mal_hi=0, mal_hi_prevented=0, sessions=P.sessions, wrong_lifts=0)
    for s in range(P.sessions):
        log = AuditLog()
        gw = Gateway({"recon": profile}, log)
        acts = gen_session(wrng, s, P)
        session_mal = any(x.malicious for x in acts)
        c_start = c_end = None        # containment interval [c_start, c_end)
        scrutiny_until = -1           # V.G: a single alert raises scrutiny, it does not contain
        counted_false = False
        for a in acts:
            if a.malicious:
                m["mal"] += 1; m["mal_hi"] += a.high_impact
            else:
                m["benign"] += 1
            # ------------- containment in force (credential revoked / session isolated) -------------
            if c_start is not None and c_start <= a.step < c_end:
                if a.malicious:
                    m["prevented"] += 1; m["mal_hi_prevented"] += a.high_impact
                    m["detected"] += 1                          # part of an incident already detected
                    m["decision_logged"] += a.routed; m["evidence_logged"] += 1
                elif session_mal:
                    m["collateral"] += 1
                else:
                    m["fp_block"] += 1
                continue
            blocked = alert = False
            rD = P.dD if a.malicious else P.fpD
            rB = P.dB if a.malicious else (P.fpB_unusual if a.unusual_legit else P.fpB)
            rC = (P.dC if a.injected else P.dC_cred) if a.malicious else P.fpC
            hitD, hitB, hitC = correlated_hits(rng, [rD, rB, rC], rho)
            if arm == "baseline":
                # prompt-level rules + one content guard on outbound actions; no gateway, no
                # approvals; manual review of 10% of logs every 50 actions (> session length,
                # so the baseline never contains within a session)
                blocked = a.outbound and hitD
                if a.malicious:
                    m["decision_logged"] += a.outbound; m["evidence_logged"] += a.outbound
                    if blocked:
                        m["detected"] += 1; m["ttd"].append(0)
                    elif rng.random() < P.baseline_review_frac:
                        nxt = (a.step // P.baseline_review_every + 1) * P.baseline_review_every
                        m["detected"] += 1; m["ttd"].append(nxt - a.step)
            else:
                det_evidence = False
                if a.routed:
                    verdict = gw.decide(a)
                    if (supervisors_on and verdict == ALLOW and a.step <= scrutiny_until
                            and (a.outbound or a.high_impact)):
                        verdict = HOLD                          # narrowed privileges
                    if verdict == DENY:
                        blocked = True; det_evidence = True
                    elif verdict == HOLD:
                        responded = rng.random() < P.p_respond
                        correct = rng.random() < P.p_human_correct
                        approve = (not a.malicious) == correct
                        blocked = Gateway.resolve_hold(responded, approve) == DENY
                    if not blocked and supervisors_on and a.outbound and hitD:
                        blocked = True                          # Agent D holds outbound transfer
                d_fired = supervisors_on and a.routed and a.outbound and hitD
                fired = [x for x, h in (("B", hitB), ("C", hitC)) if supervisors_on and h]
                if d_fired:
                    fired.append("D")
                det_lat = None
                if supervisors_on and (hitB or hitC):
                    alert = True
                    det_lat = 1 + int(rng.expovariate(1 / P.detect_latency))
                n_methods = (1 if fired else 0) if one_method else len(fired)
                # Five conditions (V.G): (ii) deterministic evidence or >= 2 different methods;
                # (iii) serious harm; (i), (iv), (v) assumed met by an approved reversible playbook.
                serious = a.outbound or a.high_impact or det_evidence
                auto = supervisors_on and serious and (det_evidence or n_methods >= 2)
                if auto and c_start is None:
                    t_detect = a.step if (det_evidence or d_fired) else a.step + det_lat
                    lag = int(rng.expovariate(1 / P.contain_latency))
                    c_start = max(a.step + 1, t_detect + lag)
                    review = c_start + max(1, round(rng.expovariate(1 / P.review_delay)))
                    if session_mal:
                        m["ttc"].append(c_start - t_detect)
                        lift = rng.random() > P.p_human_correct     # reviewer wrongly lifts
                        m["wrong_lifts"] += lift
                    else:
                        lift = rng.random() < P.p_F_reverse        # false containment reversed
                        if not counted_false:
                            m["fp_contain_sessions"] += 1; counted_false = True
                    c_end = review if lift else 10 ** 9
                elif supervisors_on and fired:
                    scrutiny_until = max(scrutiny_until, a.step + P.scrutiny_window)
                if a.malicious:
                    m["decision_logged"] += a.routed
                    m["evidence_logged"] += a.routed or alert
                    if blocked:
                        m["detected"] += 1; m["ttd"].append(0)  # in-path: caught before execution
                    elif alert:
                        m["detected"] += 1; m["ttd"].append(det_lat)
            if a.malicious:
                if blocked:
                    m["prevented"] += 1; m["mal_hi_prevented"] += a.high_impact
                else:
                    m["executed"] += 1
            elif blocked:
                m["fp_block"] += 1
        if not log.verify():
            raise RuntimeError("audit chain broken")
    return m


def summarize(ms: list[dict]) -> dict:
    def ratio(num, den):
        vals = [x[num] / x[den] for x in ms if x[den]]
        return statistics.mean(vals), (1.96 * statistics.stdev(vals) / math.sqrt(len(vals))) if len(vals) > 1 else 0.0
    def meanlist(key):
        vals = [statistics.mean(x[key]) for x in ms if x[key]]
        return (statistics.mean(vals), 1.96 * statistics.stdev(vals) / math.sqrt(len(vals))) if len(vals) > 1 else (float("nan"), 0.0)
    out = {
        "detection_rate": ratio("detected", "mal"),
        "prevention": ratio("prevented", "mal"),
        "residual_harm_per_1000_sessions": (statistics.mean([1000 * x["executed"] / x["sessions"] for x in ms]),
                                            1.96 * statistics.stdev([1000 * x["executed"] / x["sessions"] for x in ms]) / math.sqrt(len(ms))),
        "false_block_rate": ratio("fp_block", "benign"),
        "false_containment_per_1000_sessions": (statistics.mean([1000 * x["fp_contain_sessions"] / x["sessions"] for x in ms]),
                                                1.96 * statistics.stdev([1000 * x["fp_contain_sessions"] / x["sessions"] for x in ms]) / math.sqrt(len(ms))),
        "audit_completeness": ratio("decision_logged", "mal"),
        "evidence_completeness": ratio("evidence_logged", "mal"),
        "collateral_per_1000_sessions": (statistics.mean([1000 * x["collateral"] / x["sessions"] for x in ms]),
                                         1.96 * statistics.stdev([1000 * x["collateral"] / x["sessions"] for x in ms]) / math.sqrt(len(ms))),
        "mttd_actions": meanlist("ttd"),
        "mttc_actions": meanlist("ttc"),
        "prevention_high_impact": ratio("mal_hi_prevented", "mal_hi"),
    }
    return {k: [round(v[0], 4), round(v[1], 4)] for k, v in out.items()}


# ---------------------------- experiments -----------------------------------

def e1(seeds: range) -> dict:
    res = {}
    for arm in ["baseline", "no_supervisors", "homog_declared", "homog_hidden", "hacof"]:
        res[arm] = summarize([run(Params(arm=arm), sd) for sd in seeds])
    return res


def e4(seeds: range) -> list[dict]:
    """Sensitivity of HACOF to approver responsiveness (Step-3 fallback cost)."""
    rows = []
    for pr in [0.70, 0.80, 0.90, 0.99]:
        s = summarize([run(Params(arm="hacof", p_respond=pr), sd) for sd in seeds])
        rows.append({"p_respond": pr, "false_block_rate": s["false_block_rate"][0],
                     "fbr_ci95": s["false_block_rate"][1], "prevention": s["prevention"][0],
                     "prev_ci95": s["prevention"][1]})
    return rows


def e2(seeds: range) -> list[dict]:
    """Prevention vs. routed fraction phi, single in-path detector of rate d, no out-of-path."""
    rows = []
    d = 0.85
    for phi in [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0]:
        for contain in (False, True):
            prev = []
            for sd in seeds:
                rng = random.Random(10_000 + sd)
                n = p = 0
                for _ in range(4000):                     # independent high-impact attempts
                    k = 3 if contain else 1               # campaign length
                    stopped_session = False
                    for _ in range(k):
                        n += 1
                        if stopped_session:
                            p += 1; continue
                        routed = rng.random() < phi
                        if routed and rng.random() < d:
                            p += 1
                            if contain:
                                stopped_session = True    # containment after an in-path catch
                        elif contain and rng.random() < 0.6:
                            stopped_session = True        # out-of-path alert contains the rest
                prev.append(p / n)
            rows.append({"phi": phi, "campaign_containment": contain, "d": d,
                         "bound_phi_d": round(phi * d, 4),
                         "prevention_mean": round(statistics.mean(prev), 4),
                         "ci95": round(1.96 * statistics.stdev(prev) / math.sqrt(len(prev)), 4)})
    return rows


def e3(seeds: range) -> list[dict]:
    """n supervisors, each detection d=0.7, latent correlation rho; any-of-n alarm."""
    rows = []
    n, d = 7, 0.7
    m_single = 1 - d
    for rho in [0.0, 0.2, 0.4, 0.6, 0.8, 0.9]:
        joint_miss, pair_r = [], []
        for sd in seeds:
            rng = random.Random(20_000 + sd)
            miss = 0; trials = 20000
            e1s, e2s = [], []
            for _ in range(trials):
                hits = correlated_hits(rng, [d] * n, rho)
                miss += not any(hits)
                e1s.append(0 if hits[0] else 1); e2s.append(0 if hits[1] else 1)
            joint_miss.append(miss / trials)
            pair_r.append(_pearson(e1s, e2s))
        jm = statistics.mean(joint_miss); rb = statistics.mean(pair_r)
        k_eff = math.log(jm) / math.log(m_single) if 0 < jm < 1 else float("inf")
        rows.append({"rho_latent": rho, "rho_binary_errors": round(rb, 4),
                     "joint_miss_rate": round(jm, 5),
                     "k_eff_detection": round(k_eff, 3),
                     "n_eff_formula_binary_rho": round(n / (1 + (n - 1) * rb), 3),
                     "independent_miss_rate": round(m_single ** n, 5)})
    return rows


def _pearson(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sxy / (sx * sy) if sx and sy else 0.0


def write_csv(path, rows):
    keys = list(rows[0].keys())
    with open(path, "w") as f:
        f.write(",".join(keys) + "\n")
        for r in rows:
            f.write(",".join(str(r[k]) for k in keys) + "\n")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "results"); os.makedirs(out, exist_ok=True)
    seeds = range(20)
    summary = {"selftest": selftest(), "params_default": Params().__dict__,
               "seeds": list(seeds)}
    summary["E1"] = e1(seeds)
    write_csv(os.path.join(out, "e1_arms.csv"),
              [{"arm": a, **{k: v[0] for k, v in d.items()}} for a, d in summary["E1"].items()])
    rows2 = e2(range(10)); summary["E2"] = rows2; write_csv(os.path.join(out, "e2_coverage.csv"), rows2)
    rows4 = e4(range(10)); summary["E4"] = rows4; write_csv(os.path.join(out, "e4_respond.csv"), rows4)
    rows3 = e3(range(5)); summary["E3"] = rows3; write_csv(os.path.join(out, "e3_neff.csv"), rows3)
    with open(os.path.join(out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({"selftest": summary["selftest"], "E1": summary["E1"]}, indent=1))
    for r in rows2: print("E2", r)
    for r in rows3: print("E3", r)
