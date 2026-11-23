# PGL 新加坡 Major 2026 Pick’Em 模拟器

[English](README.md) · [第一阶段作业与概率](STAGE1_PICKEM_zh.md)

这个模拟器为 16 队瑞士轮挑选竞猜卡，目标是让十个位置至少猜对五个。每次试验都从首轮开始，上一场的胜负会改变下一场的对手。

## 运行

在仓库根目录使用 Python 3.10 或更新版本，仅需标准库。

```bash
python3 main.py --stage 1
python3 main.py --stage 1 --sims 50000 --pick-sims 100000 --candidates 4000 --seed 20261124
python3 main.py --stage 2 --no-advancers
python3 win_probability.py
python3 -m unittest discover -v
```

| 参数 | 用途 |
| --- | --- |
| `--stage {1,2,3}` | 指定瑞士轮阶段 |
| `--sims N` | 搜索用的模拟届数，默认 5,000 |
| `--pick-sims N` | 独立评估前三套作业的模拟届数，默认 3,000 |
| `--candidates N` | 参与整卡比较的组合数上限，默认 4,000 |
| `--seed N` | 控制整次运行的随机种子，默认 42 |
| `--no-advancers` | 从头模拟前置阶段，忽略已填写的晋级名单 |

## 数据与配置

`config.py` 保存 32 支队伍、赛事种子、赛前实力数据、模型参数和选队过滤器。初始种子使用赛事采用的 11 月 2 日 VRS 顺序，实力估计使用 11 月 16 日 HLTV 世界排名和 11 月 23 日实时 VRS。PVISION 对应 HLTV 的 PARIVISION，GOSH 对应 BC.Game。[PGL 赛程](https://www.pglesports.com/cs2/pgl-major-singapore-2026/) · [HLTV 世界排名](https://www.hltv.org/ranking/teams/2026/november/16) · [实时 VRS](https://www.hltv.org/valve-ranking/teams/2026/november/23)

`STAGE2` 和 `STAGE3` 的前八位是直邀队。上一阶段结束后，把八支晋级队按最终名次填进第 9–16 位。名单待定时，每次运行会先模拟出一套参赛阵容，随后显示的概率均以这套阵容为条件。

意向分 `rank_bias` 按排名位数微调实力，正值表示看好，官方种子与首轮对手固定。新加坡使用的分值与依据见[一阶段参考](STAGE1_PICKEM_zh.md)。`HEAD_TO_HEAD` 可录入两队的地图交手胜率，本次快照留空。需要限制某些选择时，可在配置中指定自己的 `pickem_filter(picks, teams)`。

## 配对与计分

首轮由 1–8 号种子分别对阵 9–16 号种子。以后各轮在同战绩组内，以所有已交手对手当前的净胜场之和（Buchholz）排序，再用本阶段初始种子破同分。第 2、3 轮优先高种子打低种子，遇到会迫使剩余队伍重赛的组合时回溯。第 4、5 轮按 Valve 的六队配对表依次检索。下一阶段的晋级种子按上一阶段最终战绩、最终 Buchholz、原种子排序。[Valve Major 补充规则](https://github.com/ValveSoftware/counter-strike_rules_and_regs/blob/main/major-supplemental-rulebook.md#swiss-bracket)

三胜晋级，三负淘汰。第一、二阶段的晋级战和淘汰战打 BO3，其余打 BO1。第三阶段全部打 BO3。[PGL 赛制](https://www.pglesports.com/cs2/pgl-major-singapore-2026/)

| 栏位 | 队数 | 每队得 1 分的条件 |
| --- | ---: | --- |
| 3–0 | 2 | 全胜晋级 |
| 3–1 / 3–2 | 6 | 恰好输一场或两场后晋级 |
| 0–3 | 2 | 三连败出局 |

每支队伍只能填一个位置，十个位置命中五个即完成该阶段挑战。[新加坡 Pick’Em 卡面与任务](https://blast.tv/major/pickems)

## 胜率与选卡方法

`win_probability.py` 将 HLTV 积分比值与 VRS 积分差折算为单图胜率，两项默认权重分别为 0.837 和 0.163。BO1 将基础胜率偏离 50% 的幅度收窄 20%。BO3 将单图优势放大 10%，再用 `3p² − 2p³` 将单图胜率换算为系列赛胜率。模型把同一系列赛各地图的胜率视为相同，未模拟地图 BP。

`swiss_simulator.py` 每届完整模拟 33 个系列赛。`main.py` 分别从 3–0 和 0–3 概率最高的五队中各选两队，再从剩余队伍里普通晋级概率最高的九队中选六队。程序按期望得分初筛，让保留的候选卡在同一批赛果上比较，以保留瑞士轮对手之间的相关性。前三套按搜索样本中达到五分的概率排序，同分时比较期望得分。显示的通过率、期望分、得分分布和各队命中率使用另一批独立模拟估算。搜索范围和模型假设都会影响结果。
