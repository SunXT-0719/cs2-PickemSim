"""Simulate the 16-team Swiss stages of the PGL Singapore Major 2026."""

import random
from collections import defaultdict
from config import HEAD_TO_HEAD
from win_probability import win_probability, bo3_win_probability

WINS_TO_ADVANCE = 3
LOSSES_TO_ELIMINATE = 3
TOTAL_ROUNDS = 5

# One-based positions within the reseeded six-team pool, in Valve priority order.
# https://github.com/ValveSoftware/counter-strike_rules_and_regs/blob/main/major-supplemental-rulebook.md#swiss-bracket
LATE_ROUND_PAIRINGS = (
    ((1, 6), (2, 5), (3, 4)),
    ((1, 6), (2, 4), (3, 5)),
    ((1, 5), (2, 6), (3, 4)),
    ((1, 5), (2, 4), (3, 6)),
    ((1, 4), (2, 6), (3, 5)),
    ((1, 4), (2, 5), (3, 6)),
    ((1, 6), (2, 3), (4, 5)),
    ((1, 5), (2, 3), (4, 6)),
    ((1, 3), (2, 6), (4, 5)),
    ((1, 3), (2, 5), (4, 6)),
    ((1, 4), (2, 3), (5, 6)),
    ((1, 3), (2, 4), (5, 6)),
    ((1, 2), (3, 6), (4, 5)),
    ((1, 2), (3, 5), (4, 6)),
    ((1, 2), (3, 4), (5, 6)),
)


class TeamState:
    """Tracks a team's state during a Swiss tournament simulation."""

    def __init__(self, team_data):
        self.code = team_data["code"]
        self.name = team_data["name"]
        self.data = team_data
        self.reset()

    def reset(self):
        self.wins = 0
        self.losses = 0
        self.opponents = []
        self.buchholtz = 0
        self.eliminated = False
        self.advanced = False


def get_pools(teams):
    """Group active teams by record, starting with the highest win count."""
    pools = defaultdict(list)
    for team in teams:
        if not team.advanced and not team.eliminated:
            pools[(team.wins, team.losses)].append(team)
    return [(f"{w}-{l}", pools[w, l]) for w, l in sorted(pools, reverse=True)]


def calculate_buchholtz(teams):
    """Use the current wins minus losses of *all* previous opponents."""
    records = {team.code: team.wins - team.losses for team in teams}
    for team in teams:
        team.buchholtz = sum(records[opponent] for opponent in team.opponents)


def _seed_key(team, stage):
    return -team.wins, team.losses, -team.buchholtz if stage else 0, team.data["seed"]


def compare_teams(a, b, stage):
    """Three-way comparison by current record, Buchholz, then initial seed."""
    key_a, key_b = _seed_key(a, stage), _seed_key(b, stage)
    return (key_a > key_b) - (key_a < key_b)


def sort_teams(teams, stage):
    return sorted(teams, key=lambda team: _seed_key(team, stage))


def has_played(a, b):
    return b.code in a.opponents or a.code in b.opponents


def _high_low_pairs(teams):
    """Try the lowest seed first, backing up if the remaining draw is blocked."""
    if not teams:
        return []
    first = teams[0]
    for i in range(len(teams) - 1, 0, -1):
        opponent = teams[i]
        if not has_played(first, opponent):
            rest = _high_low_pairs(teams[1:i] + teams[i + 1:])
            if rest is not None:
                return [(first, opponent)] + rest
    return None


def pair_pool(pool_teams, stage):
    """Pair one record group. stage is the number of rounds already completed."""
    if not pool_teams:
        return []
    teams = sort_teams(pool_teams, stage)
    if len(teams) % 2:
        raise ValueError("Cannot draw an odd-sized Swiss record group")
    if stage == 0:
        half = len(teams) // 2
        return list(zip(teams[:half], teams[half:]))
    if stage <= 2:
        matches = _high_low_pairs(teams)
        if matches is None:
            raise ValueError("No complete rematch-free draw for Swiss round 2 or 3")
        return matches

    if len(teams) != 6:
        raise ValueError("Swiss rounds 4 and 5 require six teams per record group")
    # If every table row requires a rematch, minimize repeats, then use table order.
    fewest_rematches = 4
    for row in LATE_ROUND_PAIRINGS:
        matches = [(teams[a - 1], teams[b - 1]) for a, b in row]
        rematches = sum(has_played(a, b) for a, b in matches)
        if rematches == 0:
            return matches
        if rematches < fewest_rematches:
            fewest_rematches = rematches
            best_matches = matches
    return best_matches


def generate_round_matches(teams):
    """Draw a whole round using the same completed-round standings for all pools."""
    pools = get_pools(teams)
    if not pools:
        return [], 0
    first = pools[0][1][0]
    stage = first.wins + first.losses
    if stage:
        calculate_buchholtz(teams)
    matches = []
    for _, pool in pools:
        if pool[0].wins + pool[0].losses != stage:
            raise ValueError("Cannot draw the next Swiss round before this round ends")
        matches.extend(pair_pool(pool, stage))
    return matches, stage


def is_bo3(match_record):
    """Advancement and elimination matches in Stages 1 and 2 are BO3."""
    wins, losses = match_record
    return wins >= 2 or losses >= 2


def simulate_match(team_a, team_b, stage_info, is_stage3=False, *, rng=None,
                   probability_cache=None):
    """Draw the winner using the series format for these teams' current record."""
    use_bo3 = is_stage3 or is_bo3((team_a.wins, team_a.losses))
    key = (team_a.code, team_b.code, use_bo3)
    if probability_cache is not None and key in probability_cache:
        probability = probability_cache[key]
    else:
        model = bo3_win_probability if use_bo3 else win_probability
        probability = model(team_a.data, team_b.data, HEAD_TO_HEAD)
        if probability_cache is not None:
            probability_cache[key] = probability
    if (rng or random).random() < probability:
        return team_a, team_b
    return team_b, team_a


def apply_result(winner, loser):
    winner.wins += 1
    loser.losses += 1
    winner.opponents.append(loser.code)
    loser.opponents.append(winner.code)
    winner.advanced = winner.wins == WINS_TO_ADVANCE
    loser.eliminated = loser.losses == LOSSES_TO_ELIMINATE


def simulate_swiss_stage(teams_dict, stage_num, random_seed=None, *, rng=None,
                         probability_cache=None):
    """Return team records and the eight advancers in final Swiss seed order.

    Reuse an RNG and an initially empty probability_cache across trials with the
    same team data and model parameters. A single random_seed isolates a trial.
    """
    if stage_num not in (1, 2, 3):
        raise ValueError("Swiss stage must be 1, 2 or 3")
    teams = list(teams_dict.values())
    if len(teams) != 16 or {t.data["seed"] for t in teams} != set(range(1, 17)):
        raise ValueError("A Swiss stage requires 16 teams with seeds 1 through 16")
    if random_seed is not None:
        if rng is not None:
            raise ValueError("Pass either rng or random_seed")
        rng = random.Random(random_seed)
    for team in teams:
        team.reset()

    for _ in range(TOTAL_ROUNDS):
        matches, _ = generate_round_matches(teams)
        for a, b in matches:
            winner, loser = simulate_match(a, b, None, stage_num == 3,
                                           rng=rng, probability_cache=probability_cache)
            apply_result(winner, loser)

    calculate_buchholtz(teams)
    standings = sort_teams(teams, TOTAL_ROUNDS)
    advancers = [t for t in standings if t.advanced]
    return {
        "exact30": [t.code for t in advancers if t.losses == 0],
        "advancers": [t.code for t in advancers],
        "advancers_3x": [t.code for t in advancers if t.losses > 0],
        "exact03": [t.code for t in standings if t.eliminated and t.wins == 0],
        "eliminated": [t.code for t in standings if t.eliminated],
        "all_results": {t.code: f"{t.wins}-{t.losses}" for t in standings},
    }


# Each team can score in only one of the three Pick'Em categories.
PICK_SLOTS = {"exact30": 2, "advancers": 6, "exact03": 2}
RESULT_KEYS = {"exact30": "exact30", "advancers": "advancers_3x", "exact03": "exact03"}


def _selections(picks):
    """Accept partial cards for analysis, enforcing slot limits and one slot per team."""
    seen = set()
    for category, limit in PICK_SLOTS.items():
        teams = picks.get(category, ())
        if len(teams) > limit:
            raise ValueError(f"At most {limit} picks allowed in {category}")
        for team in teams:
            if team in seen:
                raise ValueError(f"Team {team} was picked more than once")
            seen.add(team)
            yield category, team


def score_pickem(picks, results):
    """One point per correct slot, for a maximum of ten."""
    return sum(team in results[RESULT_KEYS[category]]
               for category, team in _selections(picks))


class StageSample:
    """Shared tournament outcomes for comparing cards against the same brackets."""

    def __init__(self, teams_dict, stage_num, num_simulations):
        if num_simulations < 1:
            raise ValueError("The number of simulations must be positive")
        # One bit per (slot category, team). A card and a stage result use the
        # same layout, so counting their shared bits gives the exact score.
        self.bits = {}
        hit_counts = {}
        for category in PICK_SLOTS:
            for code in teams_dict:
                key = (category, code)
                self.bits[key] = 1 << len(self.bits)
                hit_counts[key] = 0

        self.outcomes = []
        probability_cache = {}
        for _ in range(num_simulations):
            result = simulate_swiss_stage(teams_dict, stage_num, probability_cache=probability_cache)
            outcome = 0
            for category, result_key in RESULT_KEYS.items():
                for code in result[result_key]:
                    key = (category, code)
                    hit_counts[key] += 1
                    outcome |= self.bits[key]
            self.outcomes.append(outcome)

        self.rates = {key: hits / num_simulations for key, hits in hit_counts.items()}
        self.team_probabilities = {}
        for code, team in teams_dict.items():
            exact30 = self.rates["exact30", code]
            ordinary = self.rates["advancers", code]
            self.team_probabilities[code] = {
                "name": team.name, "advance_rate": exact30 + ordinary,
                "advancers_3x_rate": ordinary, "exact30_rate": exact30,
                "exact03_rate": self.rates["exact03", code],
            }

    def card_mask(self, picks):
        mask = 0
        for key in _selections(picks):
            mask |= self.bits[key]
        return mask

    def pass_count(self, mask):
        return sum((outcome & mask).bit_count() >= 5 for outcome in self.outcomes)

    def evaluate(self, picks):
        mask = self.card_mask(picks)
        counts = [0] * 11
        for outcome in self.outcomes:
            counts[(outcome & mask).bit_count()] += 1
        n = len(self.outcomes)
        return {
            "success_rate": sum(counts[5:]) / n,
            "success_rate_4plus": sum(counts[4:]) / n,
            "expected_points": sum(points * hits for points, hits in enumerate(counts)) / n,
            "point_distribution": {points: hits / n for points, hits in enumerate(counts)},
            "team_probabilities": self.team_probabilities,
            "pick_accuracy": {category: {code: self.rates[category, code]
                                        for code in picks.get(category, ())}
                             for category in PICK_SLOTS},
        }


def monte_carlo_simulate(teams_dict, stage_num, picks, num_simulations=10000):
    """Simulate one stage and evaluate a card, including category-specific accuracy."""
    return StageSample(teams_dict, stage_num, num_simulations).evaluate(picks)
