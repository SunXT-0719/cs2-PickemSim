import unittest
from unittest.mock import patch

from config import MODEL
from win_probability import _effective_ratings, match_win_probability


class WinProbabilityTests(unittest.TestCase):
    def setUp(self):
        self.team = {
            "code": "a", "vrs": 20, "rating_vrs": 1550,
            "hltv_rank": 20, "hltv_pts": 120,
        }
        self.opponent = dict(self.team, code="b")

    def test_bias_moves_measured_ratings_in_the_requested_direction(self):
        unbiased = _effective_ratings(self.team)
        self.assertEqual(unbiased[0], 1550)
        for bias in (-1, 1):
            shifted = _effective_ratings(dict(self.team, rank_bias=bias))
            for before, after in zip(unbiased, shifted):
                self.assertGreater((after - before) * bias, 0)

    def test_head_to_head_takes_either_order_and_uses_config_weight(self):
        history = {("b", "a"): 0.25}
        with patch.dict(MODEL, h2h_weight=0.4):
            self.assertAlmostEqual(match_win_probability(self.team, self.opponent,
                                                        head_to_head=history), 0.60)
            for bo3 in (False, True):
                forward = match_win_probability(self.team, self.opponent, bo3, history)
                reverse = match_win_probability(self.opponent, self.team, bo3, history)
                self.assertAlmostEqual(forward + reverse, 1.0)


if __name__ == "__main__":
    unittest.main()
