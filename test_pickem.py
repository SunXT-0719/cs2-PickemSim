import random
import unittest
from unittest.mock import patch

from config import STAGE1, STAGE2
from main import get_teams_for_stage
from swiss_simulator import StageSample, TeamState, score_pickem


class PickEmTest(unittest.TestCase):
    def test_score_and_accuracy_use_the_same_slots(self):
        pool = get_teams_for_stage(1)
        states = {code: TeamState(team) for code, team in pool.items()}
        draw = {"exact30": STAGE1[:2], "advancers_3x": STAGE1[2:8],
                "advancers": STAGE1[:8], "exact03": STAGE1[8:10]}
        card = {"exact30": STAGE1[:2], "advancers": STAGE1[2:8], "exact03": STAGE1[8:10]}
        with patch("swiss_simulator.simulate_swiss_stage", return_value=draw):
            sample = StageSample(states, 1, 2)
        self.assertEqual(score_pickem(card, draw), 10)
        self.assertEqual(sample.evaluate(card)["point_distribution"][10], 1)
        misplaced = {"advancers": STAGE1[:2]}
        self.assertEqual(score_pickem(misplaced, draw), 0)
        wrong = sample.evaluate(misplaced)
        self.assertEqual(wrong["pick_accuracy"]["advancers"][STAGE1[0]], 0)
        self.assertEqual(wrong["team_probabilities"][STAGE1[0]]["advance_rate"], 1)
        with self.assertRaises(ValueError):
            sample.evaluate({"exact30": STAGE1[:2], "advancers": STAGE1[:1]})

    def test_simulated_qualifiers_keep_their_finishing_order(self):
        qualifiers = list(reversed(STAGE1[:8]))
        with patch("main.simulate_swiss_stage", return_value={"advancers": qualifiers}):
            stage2 = get_teams_for_stage(2, use_actual_s1=False)
        self.assertEqual([stage2[c]["seed"] for c in qualifiers], list(range(9, 17)))

    def test_partial_qualifier_list_does_not_shift_seeds(self):
        partial = STAGE2[:8] + [STAGE1[0]] + [None] * 7
        with patch("main.STAGE2", partial), self.assertRaises(ValueError):
            get_teams_for_stage(2)

    def test_simulation_respects_the_callers_seed(self):
        pool = get_teams_for_stage(1)
        states = {code: TeamState(team) for code, team in pool.items()}
        def draws(seed):
            random.seed(seed)
            return StageSample(states, 1, 10).outcomes
        self.assertEqual(draws(3), draws(3))
        self.assertNotEqual(draws(3), draws(4))


if __name__ == "__main__":
    unittest.main()
