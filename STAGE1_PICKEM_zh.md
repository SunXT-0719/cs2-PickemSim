# 新加坡 Major 第一阶段 Pick’Em 参考

赛前版，2026 年 11 月 24 日。首场 HEROIC 对 Imperial、9z 对 Lynn Vision 均定于北京时间 12:00 开始。交作业请以游戏内倒计时为准。[PGL 官方赛程](https://www.pglesports.com/cs2/pgl-major-singapore-2026/)

| 栏位 | 建议填写 |
| --- | --- |
| **3–0** | **PVISION、Team Liquid** |
| **3–1 / 3–2 晋级** | **HEROIC、Ninjas in Pyjamas、100 Thieves、FaZe Clan、Eternal Fire、M80** |
| **0–3** | **Chinggis Warriors、Lynn Vision Gaming（LVG）** |

这张卡在 100,000 届独立模拟中有 **33.7%** 达到五分，平均 **3.92 / 10**。五分过关，普通晋级格只对 3–1 或 3–2 给分。[新加坡 Pick’Em 卡面](https://blast.tv/major/pickems)

## 三个值得斟酌的位置

- **3–0 首选 PVISION，第二格给 Liquid。** PVISION 首轮打 DENDELE，模型给出 64.9% 的首胜率、31.6% 的全胜率，81 张社区卡中也有 41 张选它 3–0。Liquid 首轮对 GOSH，模型给出 23.7% 的全胜率，略高于 HEROIC 的 20.5% 和 NiP 的 20.1%。社区更喜欢把 Liquid 放普通晋级格，81 张里有 66 张这么填。把 HEROIC 和 NiP 留在普通格，两队各有约 49% 的对应命中率。[5EPlay 赛前作业汇总](https://csgo.5eplay.com/article/article-1795079861-0148)
- **第六个晋级名额，M80 和 9z 几乎打平。** 只看普通晋级率，9z 是 43.0%，M80 是 42.7%。把主卡的 M80 换成 9z，在同一批赛果上过线率为 33.6%，与主卡的 33.7% 只差约 0.1 个百分点。
- **第二个 0–3 最容易换。** Chinggis Warriors 在 81 张卡里拿到 71 张 0–3 票，首轮就要打 100 Thieves。另一个位置，社区里有 35 张押 Imperial，18 张押 LVG，10 张押 FlyQuest。模型给三队的 0–3 率分别是 18.1%、25.2%、24.6%。保留其余九格，只换这一格，填 **LVG / FlyQuest / Imperial** 的整卡过线率依次为 **33.7% / 33.5% / 31.6%**。想支持 LVG，可以直接换 FlyQuest。[社区统计及意向分](COMMUNITY.md)

## 赛前模拟概率

按任意战绩晋级的概率排序。填写中间六格时看「3–1 / 3–2」列。百分比经过四舍五入。

| 队伍 | 任意晋级 | 3–0 | 3–1 / 3–2 | 0–3 |
| --- | ---: | ---: | ---: | ---: |
| PVISION | 84.7% | 31.6% | 53.1% | 2.5% |
| Team Liquid | 76.1% | 23.7% | 52.4% | 3.8% |
| HEROIC | 70.2% | 20.5% | 49.7% | 4.7% |
| Ninjas in Pyjamas | 69.1% | 20.1% | 49.0% | 5.1% |
| 100 Thieves | 67.0% | 18.5% | 48.5% | 5.5% |
| FaZe Clan | 63.7% | 16.7% | 47.0% | 5.6% |
| Eternal Fire | 60.5% | 14.9% | 45.5% | 6.2% |
| 9z Globant | 55.5% | 12.6% | 43.0% | 7.5% |
| M80 | 52.7% | 10.0% | 42.7% | 9.5% |
| DENDELE | 43.0% | 6.8% | 36.2% | 13.3% |
| Imperial Esports | 31.3% | 4.8% | 26.4% | 18.1% |
| Wildcard | 30.6% | 4.9% | 25.7% | 19.1% |
| GOSH | 29.3% | 4.5% | 24.8% | 20.7% |
| Lynn Vision Gaming | 24.0% | 4.0% | 20.0% | 25.2% |
| FlyQuest | 23.6% | 3.4% | 20.2% | 24.6% |
| Chinggis Warriors | 18.6% | 3.0% | 15.6% | 28.7% |

## 输入、验证与复现

赛事种子固定为 PGL 采用的 11 月 2 日顺序。对局实力使用 11 月 16 日 HLTV 世界排名积分及 11 月 23 日实时 VRS 积分。根据中文社区整理的 81 张国内外赛前作业，对 12 队的实力做了 −2 至 +2 个排名位次的微调。沿用项目原有胜率模型权重，关闭了科隆的选队过滤条件。整卡通过率是这些假设下的模型估计，地图 BP、临场阵容和单日状态会影响实战结果。[HLTV 世界排名](https://www.hltv.org/ranking/teams/2026/november/16) · [赛前 VRS](https://www.hltv.org/valve-ranking/teams/2026/november/23) · [社区样本与计算方法](COMMUNITY.md)

先用 50,000 届完整瑞士轮搜索 4,000 张候选卡，再用 100,000 届独立模拟评估前三套。换随机种子重新搜索，第一名仍是上面这张。另用 50,000 届将所有意向分设为零，同卡过线率为 34.2%，只把 LVG 换成 FlyQuest 为 34.3%。两个 0–3 方案的差距小于模型假设带来的变化。

```bash
python3 main.py --stage 1 --sims 50000 --pick-sims 100000 --candidates 4000 --seed 20261124
```
