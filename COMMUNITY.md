# 新加坡 Major 一阶段意向分

原劫色和三米七七在北京时间 2026 年 11 月 21 日 18:45 发布的三张汇总图中，列出了国内外解说、选手、创作者及账号的 81 张赛前作业。下表按卡片逐格统计。三页各列出 30、30、21 张卡，每页右下角重复展示的汇总行均已剔除。每张卡各有 2、6、2 格，三栏总票数分别为 162、486、162。[5EPlay 原帖](https://csgo.5eplay.com/article/article-1795079861-0148) · [图一](https://oss.5eplay.com/cloudx/p/admin5e/home/dc1c0lsconkip2fe9280.png) · [图二](https://oss.5eplay.com/cloudx/p/admin5e/home/dc1c0o4conkip2fe928g.png) · [图三](https://oss.5eplay.com/cloudx/p/admin5e/home/dc1c0ssconkip2fe9290.png)

| 队伍 | 3–0 票 | 3–1 / 3–2 票 | 0–3 票 | 零偏置实力顺位 | 卡片顺位 | 意向分 |
|---|---:|---:|---:|---:|---:|---:|
| Ninjas in Pyjamas | 31 | 43 | 0 | 3 | 2 | 0 |
| PVISION | 41 | 37 | 0 | 1 | 1 | 0 |
| HEROIC | 28 | 47 | 0 | 5 | 3 | +1 |
| FaZe Clan | 9 | 68 | 0 | 4 | 6 | −1 |
| Team Liquid | 13 | 66 | 0 | 2 | 5 | −1 |
| Eternal Fire | 1 | 31 | 0 | 7 | 9 | −1 |
| 100 Thieves | 22 | 53 | 0 | 9 | 4 | +2 |
| 9z Globant | 9 | 40 | 0 | 6 | 7 | 0 |
| M80 | 1 | 29 | 3 | 8 | 10 | −1 |
| DENDELE | 0 | 3 | 12 | 10 | 14 | −2 |
| Imperial Esports | 0 | 2 | 35 | 12 | 15 | −1 |
| Wildcard | 1 | 3 | 11 | 11 | 13 | −1 |
| GOSH | 3 | 41 | 2 | 13 | 8 | +2 |
| FlyQuest | 2 | 10 | 10 | 15 | 11 | +2 |
| Chinggis Warriors | 0 | 0 | 71 | 16 | 16 | 0 |
| Lynn Vision Gaming | 1 | 13 | 18 | 14 | 12 | +1 |
| **合计** | **162** | **486** | **162** | | | |

**如何得到意向分**。先把一阶段所有队伍的 `rank_bias` 设为 0，按 `win_probability.composite_strength` 从高到低排出 16 队的实力顺位。模型输入采用 11 月 16 日 HLTV 世界排名积分和 11 月 23 日全球 VRS 积分。另将每支队伍的卡片得分算作「2 × 3–0 票 + 普通晋级票 − 0–3 票」，从高到低排序，得到卡片顺位。两组顺位都是场内顺位。[HLTV 世界排名](https://www.hltv.org/ranking/teams/2026/november/16) · [全球 VRS](https://www.hltv.org/valve-ranking/teams/2026/november/23)

```python
rank_bias = max(-3, min(3, int((model_rank - card_rank) / 2)))
```

折半、截断和各栏权重是本次模拟的主观设置。例如 100 Thieves 在卡片中排第 4，领先模型 5 位，折半向零取整后加 2 个世界排名位次。Chinggis Warriors 虽有 71 张 0–3 票，两个顺位都在第 16，模型已反映这项判断，因此维持 0。这些作业存在相互参考、出线签位与槽位策略等影响，投票频率只能描述这 81 张卡片。实际赛事种子始终由赛前官方名单决定。[PGL 官方赛事页](https://www.pglesports.com/cs2/pgl-major-singapore-2026/)

**分歧集中在第二个 0–3**。Imperial 的 35 票约占四成，Lynn Vision 得到 18 票。5EPlay 的首轮前瞻则看好 Lynn Vision 战胜 9z，也看好 FlyQuest 从 Eternal Fire 手里拿下首场 BO1。虎扑赛前讨论里，也有玩家把两个 0–3 给了 Chinggis Warriors 和 Imperial。这些观点给出了看好不同队伍的具体理由，仅 81 张汇总卡进入上表计数。[5EPlay 首轮预测](https://csgo.5eplay.com/article/article-1795358599-6639) · [虎扑赛前讨论](https://bbs.hupu.com/644144106.html)
