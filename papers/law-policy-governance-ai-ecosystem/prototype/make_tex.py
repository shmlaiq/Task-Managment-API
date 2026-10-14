"""Builds the LaTeX results table and pgfplots coordinates from results/summary.json."""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
s = json.load(open(os.path.join(here, "results", "summary.json")))
E1 = s["E1"]
arms = [("baseline", "Baseline"), ("no_supervisors", "Gates only (Abl.~1)"),
        ("homog_declared", "Abl.~2a"), ("homog_hidden", "Abl.~2b"), ("hacof", "Full \\hacof{}")]
rows = [("Detection rate", "detection_rate", 2, 1), ("Prevention (all)", "prevention", 2, 1),
        ("Prevention (high-impact)", "prevention_high_impact", 2, 1),
        ("Residual harm / 1000 sessions", "residual_harm_per_1000_sessions", 0, 1),
        ("False-block rate (\\%)", "false_block_rate", 2, 100),
        ("False containments / 1000 sessions", "false_containment_per_1000_sessions", 1, 1),
        ("Decision-record completeness", "audit_completeness", 2, 1),
        ("Evidence-record completeness", "evidence_completeness", 2, 1),
        ("Mean time to containment (actions)", "mttc_actions", 2, 1),
        ("Mean time to detection (actions)", "mttd_actions", 2, 1)]
def cell(arm, key, nd, scale):
    v, ci = E1[arm][key]
    if v != v:  # nan
        return "n/a"
    if arm == "baseline" and key == "prevention_high_impact":
        return f"{v*scale:.{nd}f}$^\\ddagger$"
    return f"{v*scale:.{nd}f}\\,{{\\tiny$\\pm${ci*scale:.{nd}f}}}"
lines = []
for i, (label, key, nd, sc) in enumerate(rows):
    tint = "\\rowcolor{darkblue!5}" if i % 2 == 0 else ""
    lines.append(tint + label + " & " + " & ".join(cell(a, key, nd, sc) for a, _ in arms) + " \\\\")
table = "\n".join(lines)
e2 = s["E2"]
c_iso = " ".join(f"({r['phi']},{r['prevention_mean']})" for r in e2 if not r["campaign_containment"])
c_cam = " ".join(f"({r['phi']},{r['prevention_mean']})" for r in e2 if r["campaign_containment"])
c_bnd = " ".join(f"({r['phi']},{r['bound_phi_d']})" for r in e2 if not r["campaign_containment"])
e3 = s["E3"]
c_k = " ".join(f"({r['rho_binary_errors']},{r['k_eff_detection']})" for r in e3)
c_n = " ".join(f"({r['rho_binary_errors']},{r['n_eff_formula_binary_rho']})" for r in e3)
out = {"TABLE_ROWS": table, "E2_ISO": c_iso, "E2_CAMP": c_cam, "E2_BOUND": c_bnd, "E3_K": c_k, "E3_N": c_n}
json.dump(out, open(os.path.join(here, "results", "tex_snippets.json"), "w"), indent=1)
print(table); print(c_iso); print(c_cam); print(c_k); print(c_n)
