# HACOF prototype and simulation (supplementary material, Section VII.D)

`hacof_sim.py` has two parts:

1. **Enforcement-plane prototype (deterministic, real logic).** It contains authorization profiles, an in-path gateway (allow / deny / hold), monotonic delegation, a hash-chained append-only audit log, and the Step-3 fallback (an unanswered hold expires to deny). `selftest()` runs nine checks.
2. **Monte Carlo simulation (assumed parameters).** Supervisors B, C and D are Bernoulli detectors with assumed detection and false-positive rates and a latent error correlation. **No language model is run.** Every reported rate is a property of the model, not a field measurement.

## Run
```bash
python3 -I hacof_sim.py     # ~70 s, standard library only, fixed seeds; writes results/
python3 -I make_tex.py      # regenerates the LaTeX table rows and pgfplots coordinates used in the paper
```

## Experiments
| ID | What | Output |
|---|---|---|
| E1 | Baseline vs. gates-only (Abl. 1) vs. one-model supervisors declared (Abl. 2a) vs. one-model hidden behind declared diversity (Abl. 2b) vs. full HACOF; paired workloads, 20 seeds × 2,000 sessions × 20 actions | `results/summary.json` (E1), `results/e1_arms.csv` |
| E2 | Prevention vs. routed fraction φ against the bound P ≤ φd; isolated actions vs. 3-step campaigns with containment | `results/e2_coverage.csv` |
| E3 | Seven supervisors with correlated errors: detection-equivalent k_eff vs. n/(1+(n−1)ρ) | `results/e3_neff.csv` |
| E4 | False-block rate and prevention vs. how often approvers answer holds | `results/e4_respond.csv` |

Default parameters are recorded in `results/summary.json` (`params_default`) and in the paper's Section VII.D.

## Modeling notes
- Human approvers and reviewers are modeled by fixed accuracy rates. They are the only components that see ground truth, and they see it only through those rates.
- Containment runs as an interval: a human review follows after a delay, false containments are lifted with probability 0.8, and correct ones are wrongly lifted with probability 0.05.
- Detection counts in-path blocks (at time 0) and attempts stopped inside an already-detected incident.
- A containment that a false alarm triggers before a compromised session's attack begins is judged correct by the reviewer, so it is not counted as a false containment. `false_containment_undercount` in `results/summary.json` (E1) reports the share of all false-alarm containments this rule hides: about 0.07 for full HACOF. It is a pure counter with no extra random draws, so all other outputs are identical to runs without it.

## Limitations
- The detectors are not language models.
- The attacker does not adapt to the supervisors.
- There is one agent type and one profile.
- Parameter values are assumptions, not estimates.
