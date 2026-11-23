import random
import unittest
from unittest.mock import patch

from swiss_simulator import TeamState, has_played, is_bo3, pair_pool, simulate_swiss_stage


def seeded_teams(codes):
    return {code: TeamState({"name": code, "code": code, "seed": seed})
            for seed, code in enumerate(codes, 1)}


class SwissDrawTest(unittest.TestCase):
    def test_round_three_backtracks_instead_of_repeating_a_match(self):
        teams = seeded_teams(range(1, 9))
        teams[4].opponents = [5]
        teams[5].opponents = [4]
        pairs = pair_pool(list(teams.values()), stage=2)
        self.assertEqual([(a.code, b.code) for a, b in pairs],
                         [(1, 8), (2, 7), (3, 5), (4, 6)])

    def test_late_round_uses_first_legal_table_row(self):
        teams = seeded_teams(range(1, 7))
        teams[5].opponents = [2, 3]
        teams[2].opponents = teams[3].opponents = [5]
        # Row 7 retains 1v6, but row 3 is the higher-priority complete draw.
        for stage in (3, 4):
            pairs = pair_pool(list(teams.values()), stage)
            self.assertEqual([(a.code, b.code) for a, b in pairs],
                             [(1, 5), (2, 6), (3, 4)])

    def test_replay_previous_major_and_qualifier_seeding(self):
        # Historical fixture. Check every pairing against HLTV, then use the
        # published Stage 2 openers to verify the incoming seeds 9 to 16.
        # https://www.hltv.org/results?event=9028
        # https://www.hltv.org/news/44809/iem-cologne-major-stage-2-opening-matchups-set
        teams = seeded_teams("gl b8 hero bb big m80 mibr sinn nrg tylo shks gg liqu lvg tdu fly".split())
        rounds = (
            "gl/nrg b8/tylo shks/hero bb/gg liqu/big m80/lvg tdu/mibr fly/sinn",
            "bb/liqu big/gg gl/fly m80/shks mibr/tylo nrg/sinn b8/tdu lvg/hero",
            "b8/m80 hero/gg tylo/sinn bb/gl mibr/liqu big/tdu nrg/fly lvg/shks",
            "liqu/hero m80/nrg mibr/lvg gl/big tylo/shks fly/tdu",
            "big/nrg fly/liqu tylo/lvg",
        )
        fixtures = []
        for match_list in rounds:
            fixtures.append({frozenset((w, l)): w for w, l in
                             (pair.split("/") for pair in match_list.split())})

        def replay(a, b, *args, **kwargs):
            self.assertEqual((a.wins, a.losses), (b.wins, b.losses))
            self.assertFalse(has_played(a, b))
            winner = fixtures[a.wins + a.losses].pop(frozenset((a.code, b.code)))
            return (a, b) if a.code == winner else (b, a)

        with patch("swiss_simulator.simulate_match", side_effect=replay):
            result = simulate_swiss_stage(teams, 1)
        self.assertFalse(any(fixtures))
        self.assertEqual(result["advancers"], "b8 bb gl m80 mibr tylo big fly".split())
        self.assertEqual([teams[c].buchholtz for c in result["advancers"]],
                         [1, -2, 4, -1, -3, -1, -5, -5])

    def test_series_format_by_stage(self):
        teams = seeded_teams(range(1, 17))
        for stage, expected_bo1 in ((1, 20), (2, 20), (3, 0)):
            with patch("swiss_simulator.win_probability", return_value=0.5) as bo1, \
                 patch("swiss_simulator.bo3_win_probability", return_value=0.5) as bo3:
                result = simulate_swiss_stage(teams, stage, rng=random.Random(1))
            self.assertEqual(bo1.call_count, expected_bo1)
            self.assertEqual(bo3.call_count, 33 - expected_bo1)
            self.assertEqual([len(result[k]) for k in ("exact30", "advancers_3x", "exact03")],
                             [2, 6, 2])
        self.assertTrue(is_bo3((2, 0)))
        self.assertTrue(is_bo3((0, 2)))
        self.assertFalse(is_bo3((1, 1)))


if __name__ == "__main__":
    unittest.main()
