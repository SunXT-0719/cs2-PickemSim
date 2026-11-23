"""PGL Major Singapore 2026 pre-event configuration.

PGL event names, stage seeds and first-round schedule:
https://www.pglesports.com/cs2/pgl-major-singapore-2026/
Invitations and stage seed order use the November 2 Valve release:
https://github.com/ValveSoftware/counter-strike_regional_standings/blob/main/live/2026/standings_global_2026_11_02.md

For match strength, vrs and rating_vrs are the November 23 HLTV live VRS
global rank and points. hltv_rank and hltv_pts use the November 16 HLTV
world ranking (the published edition at the time of this pre-match snapshot).
https://www.hltv.org/valve-ranking/teams/2026/november/23
https://www.hltv.org/ranking/teams/2026/november/16

Ranking names mapped to PGL event names: PARIVISION → PVISION, BC.Game →
GOSH, BETBOOM → BB TEAM, 1win → The One, and 9z → 9z Globant.
"""

# rank_bias is a subjective adjustment from the pre-event cards in COMMUNITY.md.
TEAMS = {
    # Stage 1
    "nip": {"name": "Ninjas in Pyjamas", "vrs": 21, "rating_vrs": 1475, "hltv_rank": 18, "hltv_pts": 93},
    "pv": {"name": "PVISION", "vrs": 13, "rating_vrs": 1570, "hltv_rank": 13, "hltv_pts": 188},
    "hero": {"name": "HEROIC", "vrs": 18, "rating_vrs": 1499, "hltv_rank": 23, "hltv_pts": 76, "rank_bias": 1},
    "faze": {"name": "FaZe Clan", "vrs": 25, "rating_vrs": 1447, "hltv_rank": 19, "hltv_pts": 90, "rank_bias": -1},
    "liqu": {"name": "Team Liquid", "vrs": 15, "rating_vrs": 1527, "hltv_rank": 16, "hltv_pts": 128, "rank_bias": -1},
    "ef": {"name": "Eternal Fire", "vrs": 23, "rating_vrs": 1449, "hltv_rank": 22, "hltv_pts": 76, "rank_bias": -1},
    "100t": {"name": "100 Thieves", "vrs": 17, "rating_vrs": 1517, "hltv_rank": 29, "hltv_pts": 55, "rank_bias": 2},
    "9z": {"name": "9z Globant", "vrs": 35, "rating_vrs": 1363, "hltv_rank": 21, "hltv_pts": 89},
    "m80": {"name": "M80", "vrs": 27, "rating_vrs": 1416, "hltv_rank": 24, "hltv_pts": 71, "rank_bias": -1},
    "den": {"name": "DENDELE", "vrs": 28, "rating_vrs": 1414, "hltv_rank": 33, "hltv_pts": 48, "rank_bias": -2},
    "imp": {"name": "Imperial Esports", "vrs": 37, "rating_vrs": 1353, "hltv_rank": 48, "hltv_pts": 27, "rank_bias": -1},
    "wc": {"name": "Wildcard", "vrs": 42, "rating_vrs": 1325, "hltv_rank": 42, "hltv_pts": 32, "rank_bias": -1},
    "gosh": {"name": "GOSH", "vrs": 46, "rating_vrs": 1286, "hltv_rank": 46, "hltv_pts": 29, "rank_bias": 2},
    "fly": {"name": "FlyQuest", "vrs": 44, "rating_vrs": 1294, "hltv_rank": 58, "hltv_pts": 15, "rank_bias": 2},
    "cw": {"name": "Chinggis Warriors", "vrs": 56, "rating_vrs": 1221, "hltv_rank": 59, "hltv_pts": 15},
    "lvg": {"name": "Lynn Vision Gaming", "vrs": 61, "rating_vrs": 1195, "hltv_rank": 44, "hltv_pts": 30, "rank_bias": 1},
    # Stage 2 direct invites
    "fut": {"name": "FUT ESPORTS", "vrs": 10, "rating_vrs": 1623, "hltv_rank": 9, "hltv_pts": 272},
    "nemi": {"name": "Nemiga Gaming", "vrs": 11, "rating_vrs": 1621, "hltv_rank": 11, "hltv_pts": 264},
    "g2": {"name": "G2 Esports", "vrs": 12, "rating_vrs": 1580, "hltv_rank": 12, "hltv_pts": 223},
    "one": {"name": "The One", "vrs": 16, "rating_vrs": 1521, "hltv_rank": 15, "hltv_pts": 141},
    "navi": {"name": "Natus Vincere", "vrs": 7, "rating_vrs": 1763, "hltv_rank": 8, "hltv_pts": 336},
    "astr": {"name": "Astralis", "vrs": 19, "rating_vrs": 1493, "hltv_rank": 20, "hltv_pts": 89},
    "mong": {"name": "The MongolZ", "vrs": 9, "rating_vrs": 1751, "hltv_rank": 10, "hltv_pts": 267},
    "mibr": {"name": "MIBR", "vrs": 20, "rating_vrs": 1488, "hltv_rank": 17, "hltv_pts": 115},
    # Stage 3 direct invites
    "mouz": {"name": "MOUZ", "vrs": 1, "rating_vrs": 1955, "hltv_rank": 2, "hltv_pts": 808},
    "vita": {"name": "Team Vitality", "vrs": 3, "rating_vrs": 1875, "hltv_rank": 4, "hltv_pts": 638},
    "furi": {"name": "FURIA", "vrs": 2, "rating_vrs": 1934, "hltv_rank": 1, "hltv_pts": 960},
    "auro": {"name": "Aurora Gaming", "vrs": 6, "rating_vrs": 1799, "hltv_rank": 6, "hltv_pts": 419},
    "spir": {"name": "Team Spirit", "vrs": 4, "rating_vrs": 1852, "hltv_rank": 3, "hltv_pts": 766},
    "betb": {"name": "BB TEAM", "vrs": 5, "rating_vrs": 1842, "hltv_rank": 7, "hltv_pts": 355},
    "falc": {"name": "Team Falcons", "vrs": 8, "rating_vrs": 1756, "hltv_rank": 5, "hltv_pts": 448},
    "lega": {"name": "Legacy", "vrs": 14, "rating_vrs": 1567, "hltv_rank": 14, "hltv_pts": 172},
}

# Each list position determines its event seed. Qualifier slots are
# filled in final standings order when the preceding stage is complete.
STAGE1 = [
    "nip", "pv", "hero", "faze", "liqu", "ef", "100t", "9z",
    "m80", "den", "imp", "wc", "gosh", "fly", "cw", "lvg",
]
# Set the eight Stage 1 qualifiers in published seed order when available.
STAGE1_ADVANCERS = []
STAGE2 = ["fut", "nemi", "g2", "one", "navi", "astr", "mong", "mibr"] + (STAGE1_ADVANCERS or [None] * 8)
STAGE3 = ["mouz", "vita", "furi", "auro", "spir", "betb", "falc", "lega"] + [None] * 8

# 3. WIN PROBABILITY MODEL PARAMETERS
# ═══════════════════════════════════════════════════════════════════

MODEL = {
    # --- Elo / Ratio weights ---
    "sigma_vrs": 89.0,       # Elo sigma for VRS component
    "hltv_exp": 0.432,       # exponent for HLTV ratio component
    "w_hltv": 0.837,         # HLTV weight (dominant)
    "w_vrs": 0.163,          # VRS weight

    # --- Upset factors ---
    # Formula: adj = 0.5 + (p - 0.5) * (1 - upset)
    #   upset > 0  -> pulls toward 50% (more randomness)
    #   upset = 0  -> no change
    #   upset < 0  -> pushes away from 50% (amplifies favorite)
    #   upset = 2  -> exchange
    "upset_bo1": 0.20,       # BO1: high variance, single-map randomness
    "upset_bo3": -0.10,      # BO3: multi-map amplifies skill gap

    # --- H2H adjustment ---
    "h2h_weight": 0.12,      # max H2H adjustment (±6% for extreme records)
}

# ═══════════════════════════════════════════════════════════════════
# 4. SIMULATION DEFAULTS
# ═══════════════════════════════════════════════════════════════════

SIM = {
    "team_sims": 5000,       # shared trials for team rates and candidate search
    "pick_sims": 3000,       # independent evaluation trials for shortlisted cards
    "candidates": 4000,      # max Pick'em combinations to test
}

# ═══════════════════════════════════════════════════════════════════
# Optional map-level head-to-head inputs. No Singapore-specific history configured.
HEAD_TO_HEAD = {}

# 6. PICK'EM FILTER (user-customizable)
# ═══════════════════════════════════════════════════════════════════
# Define rules to reject invalid Pick'em combinations before evaluation.
# Receives picks dict and TEAMS dict; return True to keep, False to skip.
#
# picks = {
#     "exact30": ["code1", "code2"],       # 2 team codes
#     "advancers": ["c1","c2",...,"c6"],   # 6 team codes
#     "exact03": ["code1", "code2"],       # 2 team codes
# }

def pickem_filter_default(picks, teams):
    """
    User-customizable Pick'em validation.
    Return True if the combination is acceptable, False to skip it.
    """
    return True  # default: accept all

# --- Example rules (uncomment and edit) ---
def pickem_filter_custom(picks, teams):
    # Example preference: keep TYLOO out of 0-3
    if "tylo" in picks["exact03"]:
        return False

    # Example preference: keep these teams out of 3-0
    excluded = {"furi", "mibr", "pain", "lega", "9z"}
    for code in picks["exact30"]:
        if code in excluded:
            return False

    return True

pickem_filter = pickem_filter_default
