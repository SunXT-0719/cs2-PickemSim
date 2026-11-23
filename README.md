# PGL Major Singapore 2026 Pick’Em simulator

[中文版](README_zh.md) · [Stage 1 picks and probabilities (Chinese)](STAGE1_PICKEM_zh.md)

Simulate a 16-team Swiss stage and find cards with a high modelled chance of getting at least five of the ten Pick’Em slots right.

## Run

From the repository root, use Python 3.10 or later. Only the standard library is required.

```bash
python3 main.py --stage 1
python3 main.py --stage 1 --sims 50000 --pick-sims 100000 --candidates 4000 --seed 20261124
python3 main.py --stage 2 --no-advancers
python3 win_probability.py
python3 -m unittest discover -v
```

| Option | Meaning |
| --- | --- |
| `--stage {1,2,3}` | Swiss stage to simulate |
| `--sims N` | Search tournaments for team probabilities and card selection (default 5,000) |
| `--pick-sims N` | Fresh tournaments for evaluating the three finalists (default 3,000) |
| `--candidates N` | Maximum cards to compare on the search tournaments (default 4,000) |
| `--seed N` | Reproducible random stream for the whole run (default 42) |
| `--no-advancers` | Draw all feeder stages from scratch, including those with configured results |

## Data and configuration

`config.py` contains the 32 teams, fixed event seeds, pre-match rating inputs, model parameters and an optional card filter. PGL set the initial seed order using the November 2 VRS. The strength model uses the November 16 HLTV world ranking and November 23 live VRS. Event names include PVISION (PARIVISION) and GOSH (BC.Game). [PGL stage schedule](https://www.pglesports.com/cs2/pgl-major-singapore-2026/) · [HLTV world ranking](https://www.hltv.org/ranking/teams/2026/november/16) · [Live VRS](https://www.hltv.org/valve-ranking/teams/2026/november/23)

The first eight entries of `STAGE2` and `STAGE3` are direct invites. When the preceding stage ends, enter all eight qualifiers in final seed order in slots 9–16. Until then the CLI draws the missing field once per run, prints it, and evaluates cards conditional on that field.

`rank_bias` adjusts perceived playing strength in ranking places. Positive values strengthen a team. The initial seed and official matchups stay fixed. The Singapore values and their source are described in the [Stage 1 reference](STAGE1_PICKEM_zh.md). Optional `HEAD_TO_HEAD` values represent a team's map win share against a particular opponent. The Singapore snapshot leaves these empty. To restrict picks, assign your own `pickem_filter(picks, teams)` function in the configuration.

## Draw and scoring

The opening round pairs seeds 1–8 with seeds 9–16 in order. For each later round, teams are grouped by record and ranked by their opponents’ current net wins (Buchholz), then by initial seed. Rounds 2–3 match high against low with backtracking to avoid rematches. Rounds 4–5 use Valve’s ordered six-team table. The final standings determine incoming seeds 9–16 for the next stage. [Valve Major rules](https://github.com/ValveSoftware/counter-strike_rules_and_regs/blob/main/major-supplemental-rulebook.md#swiss-bracket)

Three wins advance a team and three losses eliminate it. In Stages 1–2, advancement and elimination series are BO3 and the remaining series are BO1. Stage 3 uses BO3 throughout. [PGL event format](https://www.pglesports.com/cs2/pgl-major-singapore-2026/)

| Slot | Picks | Each scores one point for |
| --- | ---: | --- |
| 3–0 | 2 | Advancing undefeated |
| 3–1 / 3–2 | 6 | Advancing with one or two losses |
| 0–3 | 2 | Elimination without a win |

Each team can occupy one slot. Five correct picks complete the stage challenge. [Singapore Pick’Em card](https://blast.tv/major/pickems)

## Win probabilities and card search

`win_probability.py` blends an HLTV points ratio with an Elo-style probability from the VRS points difference. The default weights are 0.837 and 0.163 respectively. The BO1 adjustment shrinks the single-map edge by 20%. BO3 increases the per-map edge by 10% and converts the adjusted map probability `p` to a series probability `3p² − 2p³`. The model treats a team's map probability as constant within a series and does not simulate vetoes.

`swiss_simulator.py` draws all 33 series of each tournament. `main.py` considers pairs from each exact slot’s five highest-probability teams and six ordinary advancers from the next nine eligible teams ranked by 3–1 / 3–2 probability. It screens by expected points and compares the retained cards on the same tournaments, preserving the dependencies created by Swiss pairings. The three finalists are ordered by search-sample five-point pass rate, with expected points breaking ties. The displayed pass rates, expected points, score distribution and individual team rates come from held-out tournaments. This is a bounded search and its estimates depend on the strength model.
