#!/usr/bin/env python3
"""PGL Major Singapore 2026 Swiss-stage Pick'Em simulator."""

import argparse
import heapq
import itertools
import random

from config import TEAMS, HEAD_TO_HEAD, STAGE1, STAGE2, STAGE3, pickem_filter, SIM as _SIM
from swiss_simulator import (
    StageSample, TeamState, generate_round_matches, simulate_swiss_stage, monte_carlo_simulate,
)
from win_probability import composite_strength, match_win_probability


# ── Simulation defaults ───────────────────────────────────────────
DEFAULT_TEAM_SIMS = _SIM["team_sims"]
DEFAULT_PICK_SIMS = _SIM["pick_sims"]
DEFAULT_CANDIDATES = _SIM["candidates"]


def _build_pool(codes, start_seed=1):
    """Convert a list of team codes into a {code: team_data_with_seed} dict."""
    pool = {}
    for i, code in enumerate(codes):
        if code is None:
            continue
        t = dict(TEAMS[code])
        t["code"] = code
        t["seed"] = start_seed + i
        pool[code] = t
    return pool


def get_teams_for_stage(stage, use_actual_s1=True):
    """Build one seeded field. Undecided feeder stages are drawn once for this scenario."""
    if stage not in (1, 2, 3):
        raise ValueError(f"Unknown stage: {stage}")
    codes = list({1: STAGE1, 2: STAGE2, 3: STAGE3}[stage])
    if stage > 1:
        qualifiers = codes[8:]
        if not use_actual_s1 or not any(qualifiers):
            prior = get_teams_for_stage(stage - 1, use_actual_s1)
            states = {code: TeamState(team) for code, team in prior.items()}
            codes = codes[:8] + simulate_swiss_stage(states, stage - 1)["advancers"]
    if len(codes) != 16 or None in codes or len(set(codes)) != 16:
        raise ValueError(f"Stage {stage} needs 16 distinct teams. Enter all eight qualifiers "
                         "in their final seed order, or leave all eight empty.")
    return _build_pool(codes)


def evaluate_pick(picks, teams_pool, stage_num, num_trials):
    states = {c: TeamState(t) for c, t in teams_pool.items()}
    return monte_carlo_simulate(states, stage_num, picks, num_simulations=num_trials)


def find_best_pickem(teams_pool, stage_num, num_team_sims, num_pick_sims, num_candidates):
    """Search plausible legal cards for P(score >= 5), then evaluate finalists on fresh draws."""
    if min(num_team_sims, num_pick_sims, num_candidates) < 1:
        raise ValueError("Trial and candidate counts must be positive")
    states = {code: TeamState(data) for code, data in teams_pool.items()}
    print(f"  Simulating {num_team_sims} tournaments to select cards...")
    search = StageSample(states, stage_num, num_team_sims)
    ordered = {
        category: sorted(teams_pool, key=lambda c: search.rates[category, c], reverse=True)
        for category in ("exact30", "advancers", "exact03")
    }

    def candidates():
        for unbeaten in itertools.combinations(ordered["exact30"][:5], 2):
            for winless in itertools.combinations(ordered["exact03"][:5], 2):
                special = set(unbeaten + winless)
                if len(special) != 4:
                    continue
                eligible = [code for code in ordered["advancers"] if code not in special]
                for advancing in itertools.combinations(eligible[:9], 6):
                    card = {"exact30": list(unbeaten), "advancers": list(advancing),
                            "exact03": list(winless)}
                    if pickem_filter(card, TEAMS):
                        expected = sum(search.rates[category, team]
                                       for category, teams in card.items() for team in teams)
                        yield expected, card

    # Screen by marginal expected points, then compare complete cards on the
    # same brackets to account for teams meeting one another in the Swiss.
    shortlist = heapq.nlargest(num_candidates, candidates(), key=lambda item: item[0])
    if not shortlist:
        raise ValueError("No candidate cards passed pickem_filter")
    print(f"  Comparing {len(shortlist)} legal cards on those same tournaments...")
    finalists = heapq.nlargest(
        3, shortlist,
        key=lambda item: (search.pass_count(search.card_mask(item[1])), item[0]),
    )

    print(f"  Evaluating the finalists on {num_pick_sims} independent tournaments...")
    holdout = StageSample(states, stage_num, num_pick_sims)
    results = []
    for _, card in finalists:
        result = holdout.evaluate(card)
        results.append((result["success_rate"], card, result))
    return results, holdout.team_probabilities


def show_round1(teams_pool, stage_num=1):
    """Display the opening opponents and win chances for this stage's match format."""
    states = [TeamState(team) for team in teams_pool.values()]
    matches, _ = generate_round_matches(states)
    bo3 = stage_num == 3
    print(f"\n  Round 1 matchups ({'BO3' if bo3 else 'BO1'})")
    for a, b in matches:
        prob = match_win_probability(a.data, b.data, bo3, HEAD_TO_HEAD)
        print(f"    #{a.data['seed']:2} {a.name:<22} vs #{b.data['seed']:2} {b.name:<22} "
              f"  {a.name} {prob:.1%}")


def print_results(top_results, probs, teams_pool):
    """
    Print the top Pick'em combinations (up to 3).
    top_results is a list of (score, picks_dict, result).
    """
    for rank, (score, picks, result) in enumerate(top_results, 1):
        labels = {1: "1st", 2: "2nd", 3: "3rd"}
        label = labels.get(rank, f"{rank}th")

        print(f"\n{'=' * 70}")
        print(f"{label} PICK'EM  (ranked on search trials)")
        print(f"{'=' * 70}")

        print(f"\n  Held-out pass (>=5pts):   {score:.1%}")
        print(f"  Chance of >=4pts:         {result['success_rate_4plus']:.1%}")
        print(f"  Expected points:          {result.get('expected_points', 0):.2f} / 10")

        print(f"\n  Exact 3-0 Picks (2 slots):")
        for code in picks["exact30"]:
            p = probs[code]
            print(f"    {TEAMS[code]['name']:<22} advance={p['advance_rate']:.1%}  3-0={p['exact30_rate']:.1%}")

        print(f"\n  Advancers Picks (6 slots):")
        for code in picks["advancers"]:
            p = probs[code]
            a_3x = p['advancers_3x_rate']
            print(f"    {TEAMS[code]['name']:<22} advance={p['advance_rate']:.1%}  3-0={p['exact30_rate']:.1%}"
                  f"  3-1/3-2={a_3x:.1%}")

        print(f"\n  Exact 0-3 Picks (2 slots):")
        for code in picks["exact03"]:
            p = probs[code]
            print(f"    {TEAMS[code]['name']:<22} 0-3={p['exact03_rate']:.1%}")

    # Point distribution from the best result
    best_result = top_results[0][2]
    print(f"\n  Point Distribution (best):")
    for pts in range(11):
        prob = best_result["point_distribution"].get(pts, 0)
        if prob > 0.001:
            bar = "=" * int(prob * 100)
            marker = " <-- pass" if pts == 5 else ""
            print(f"    {pts:2d} pts: {prob:6.1%} {bar}{marker}")

    print(f"\n{'=' * 70}")
    print(f"ALL TEAM PROJECTIONS (sorted by advance rate)")
    print(f"{'=' * 70}")
    print(f"{'Team':<22} {'Advance':>8} {'3-0':>8} {'3-1/3-2':>8} {'0-3':>8} {'Str':>6} {'Seed':>4}")
    print("-" * 72)
    for code, p in sorted(probs.items(), key=lambda x: x[1]["advance_rate"], reverse=True):
        t = teams_pool[code]
        s = composite_strength(t)
        print(f"{t['name']:<22} {p['advance_rate']:>7.1%} {p['exact30_rate']:>7.1%}"
              f" {p['advancers_3x_rate']:>7.1%} {p['exact03_rate']:>7.1%} {s:>6.4f} {t['seed']:>4}")


def main():
    parser = argparse.ArgumentParser(
        description="PGL Major Singapore 2026 Pick'em Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py --stage 1
  python3 main.py --stage 2 --sims 10000
  python3 main.py --stage 3 --no-advancers

Customize team strength: edit config.py, set rank_bias per team.
  rank_bias = +2  → team treated as 2 ranks better
  rank_bias = -1  → team treated as 1 rank worse
        """)
    parser.add_argument("--stage", type=int, required=True, choices=[1, 2, 3],
                        help="Which Swiss stage to simulate (1/2/3)")
    parser.add_argument("--sims", type=int, default=DEFAULT_TEAM_SIMS,
                        help=f"Number of Monte Carlo trials (default: {DEFAULT_TEAM_SIMS})")
    parser.add_argument("--pick-sims", type=int, default=DEFAULT_PICK_SIMS,
                        help=f"Independent trials to evaluate the finalists (default: {DEFAULT_PICK_SIMS})")
    parser.add_argument("--candidates", type=int, default=DEFAULT_CANDIDATES,
                        help=f"Max Pick'em combinations to test (default: {DEFAULT_CANDIDATES})")
    parser.add_argument("--no-advancers", action="store_true",
                        help="For stage 2/3: simulate prior stages from scratch "
                             "(ignore configured qualifier lists)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility (default: 42)")
    args = parser.parse_args()

    if min(args.sims, args.pick_sims, args.candidates) < 1:
        parser.error("--sims, --pick-sims and --candidates must be positive")
    random.seed(args.seed)
    use_actual = not args.no_advancers

    # ── Stage info ──────────────────────────────────────────────
    print("=" * 70)
    print(f"PGL MAJOR SINGAPORE 2026 — STAGE {args.stage}")
    print("=" * 70)

    # ── Build team pool ─────────────────────────────────────────
    print(f"\n  Building team pool...")
    teams_pool = get_teams_for_stage(args.stage, use_actual_s1=use_actual)

    if args.stage > 1:
        configured = STAGE2 if args.stage == 2 else STAGE3
        if not use_actual or not all(configured[8:]):
            print("  Projections are conditional on the qualifier field simulated for this run.")

    # Count rank_bias overrides
    bias_count = sum(1 for t in teams_pool.values() if t.get("rank_bias", 0) != 0)
    if bias_count > 0:
        print(f"  ({bias_count} team(s) with custom rank_bias)")

    print(f"\n  Stage {args.stage} — {len(teams_pool)} teams:")
    for code in sorted(teams_pool.keys(), key=lambda c: teams_pool[c]["seed"]):
        t = teams_pool[code]
        s = composite_strength(t)
        bias = t.get("rank_bias", 0)
        bias_str = f" bias={'+' if bias > 0 else ''}{bias}" if bias != 0 else ""
        print(f"    Seed{t['seed']:>2}: {t['name']:<22} VRS#{t['vrs']}"
              f" HLTV#{t['hltv_rank']} s={s:.4f}{bias_str}")

    # ── Verify Round 1 pairings ─────────────────────────────────
    show_round1(teams_pool, args.stage)

    # ── Find optimal Pick'em ────────────────────────────────────
    top_results, probs = find_best_pickem(
        teams_pool, args.stage, args.sims, args.pick_sims, args.candidates
    )

    # ── Print results ───────────────────────────────────────────
    print_results(top_results, probs, teams_pool)

    # ── Show next-stage context ─────────────────────────────────
    if args.stage < 3:
        invited = STAGE2 if args.stage == 1 else STAGE3
        names = ", ".join(TEAMS[code]["name"] for code in invited[:8])
        print(f"\n  Top 8 advance to Stage {args.stage + 1} and join {names}.")
    else:
        print("\n  Top 8 advance to the playoffs.")


if __name__ == "__main__":
    main()
