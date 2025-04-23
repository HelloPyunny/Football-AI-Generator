
import os
import sys
from typing import List

import numpy as np
from scipy.optimize import linear_sum_assignment

# make parent folder import‑able (e.g. formation_gernerator/…)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .select_eleven import select_eleven_players  # 이 파일에서 돌리려면 . 빼야함
from prediction_model.predict_ovr import predict_ovr_by_position 
from formation_algo.formation import FORMATIONS 

# ---------------------------------------------------------------------------
# 1. Static data
# ---------------------------------------------------------------------------
selected_features = [
    "PAC", "SHO", "PAS", "DRI", "DEF", "PHY", "Acceleration", "Sprint Speed", "Positioning",
    "Finishing", "Shot Power", "Long Shots", "Volleys", "Penalties", "Vision", "Crossing",
    "Free Kick Accuracy", "Short Passing", "Long Passing", "Curve", "Dribbling", "Agility",
    "Balance", "Reactions", "Ball Control", "Composure", "Interceptions", "Heading Accuracy",
    "Def Awareness", "Standing Tackle", "Sliding Tackle", "Jumping", "Stamina", "Strength",
    "Aggression", "Skill moves", "Weak foot", "Height", "GK Diving", "GK Handling",
    "GK Kicking", "GK Positioning", "GK Reflexes",
]

POSITION_LIST = [
    "CB", "LB", "RB", "CDM", "CM", "LM", "RM", "CAM", "LW", "RW", "ST", "GK",
]

# ---------------------------------------------------------------------------
# 2. Helpers
# ---------------------------------------------------------------------------

def dedup_players(rows):
    """Remove duplicate player rows by name while preserving order."""
    seen = {}
    for row in rows:
        name = row[0]
        if name not in seen:
            seen[name] = row
    return list(seen.values())


def compute_player_ovrs(players):
    """Return a list[dict] with per‑position OVRs for each player."""
    out = []
    for row in players:
        name, original_position, *feature_values = row

        raw_stats = dict(zip(selected_features, feature_values))
        stats = {feat: float(raw_stats.get(feat, 0.0)) for feat in selected_features}

        ovr_dict = {}
        for pos in POSITION_LIST:
            try:
                ovr = predict_ovr_by_position(stats, pos)
            except ValueError as err:
                print(f"[ERROR] {name} – {pos}: {err}")
                ovr = 0.0
            ovr_dict[pos] = ovr

        out.append({"name": name, "position": original_position, "ovr": ovr_dict})
    return out

# ---------------------------------------------------------------------------
# 3. Core algorithms
# ---------------------------------------------------------------------------

def optimal_formation(player_ovrs, formations):
    """Evaluate *one* formation dict and return the best assignment within it."""
    best_form = None
    best_assignment = None
    best_total = -1.0

    for form_name, form in formations.items():
        positions = [p for line in form["lines"] for p in line]
        if "GK" not in positions:
            continue  # safety check

        # 1) pick the best GK first (greedy) ---------------------------------
        gk_candidates = [p for p in player_ovrs if p["ovr"].get("GK", 0)]
        if not gk_candidates:
            continue
        best_gk = max(gk_candidates, key=lambda p: p["ovr"]["GK"])
        gk_ovr = best_gk["ovr"]["GK"]

        # 2) assign out‑field players with Hungarian algorithm ---------------
        outfield_players = [p for p in player_ovrs if p is not best_gk]
        outfield_positions = [pos for pos in positions if pos != "GK"]
        if len(outfield_players) < len(outfield_positions):
            continue  # not enough players

        cost = [[-pl["ovr"].get(pos, 0) for pos in outfield_positions] for pl in outfield_players]
        row_idx, col_idx = linear_sum_assignment(cost)

        assignment = [("GK", best_gk["name"], gk_ovr, "GK", gk_ovr)]
        total = gk_ovr

        for r, c in zip(row_idx, col_idx):
            pl = outfield_players[r]
            pos = outfield_positions[c]
            ovr = pl["ovr"].get(pos, 0)
            best_pos = max(pl["ovr"], key=pl["ovr"].get)
            best_ovr = pl["ovr"][best_pos]
            assignment.append((pos, pl["name"], ovr, best_pos, best_ovr))
            total += ovr

        if total > best_total:
            best_total = total
            best_form = form_name
            best_assignment = assignment

    return {"formation": best_form, "assignment": best_assignment, "total_ovr": best_total}


def evaluate_all_formations(player_ovrs, formations):
    results = []
    for name, form in formations.items():
        best = optimal_formation(player_ovrs, {name: form})
        if best["formation"]:
            results.append((name, round(best["total_ovr"], 2)))
    return sorted(results, key=lambda x: -x[1])

# ---------------------------------------------------------------------------
# 4. Public API
# ---------------------------------------------------------------------------

def main_optimized(player_names: List[str]):
    if len(player_names) != len(set(player_names)):
        raise ValueError("player_names contains duplicates.")

    raw = select_eleven_players(player_names)
    players = dedup_players(raw)

    if len(players) != 11:
        raise ValueError(f"Need 11 unique players, got {len(players)}")

    player_ovrs = compute_player_ovrs(players)
    formation_scores = evaluate_all_formations(player_ovrs, FORMATIONS)

    best_name = formation_scores[0][0]
    best_detail = optimal_formation(player_ovrs, {best_name: FORMATIONS[best_name]})

    return {
        "formation": best_name,
        "total_OVR": round(best_detail["total_ovr"], 2),
        "assignments": [
            [pos, name, round(ovr, 2)] for pos, name, ovr, _, _ in best_detail["assignment"]
        ],
        "all_formations": formation_scores,
    }

# ---------------------------------------------------------------------------
# 5. CLI usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    EXAMPLE_PLAYERS = [
        "Julia Magerl", "Aoife Mannion", "Laura Martínez", "Amanda Mbadi", "Paula Monteagudo",
        "Juliette Mossard", "Marjolen Nekesa Wafula", "Nina Ngueleu", "Bárbara Olivieri",
        "Cristina Roque", "Mar Segarra",
    ]

    result = main_optimized(EXAMPLE_PLAYERS)

    print("\nAll Formation Evaluations:")
    for name, score in result["all_formations"]:
        print(f"{name:10} → Total OVR: {score:.2f}")

    print("\nBest Formation:", result["formation"])
    print("Total Team OVR:", result["total_OVR"])

    print("\nAssignments:")
    for pos, name, ovr in result["assignments"]:
        print(f"{pos:4} - {name:20} (OVR: {ovr:.2f})")
