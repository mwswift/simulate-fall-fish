# Fall Fish Simulation

Simulating the Fall Fish day from [TheHaboo's 1.6 CC% route](https://docs.google.com/document/d/1xSc32FW5lmvpM0WAm3d4B9OcmwVnq1DuUCLEEa3MEpg).

## Takeaway

Runners should consider rushing fishing level 2 at the beach before moving to the river.  This strategy saves a round trip back to the beach to buy the fibereglass rod, resulting in several more casts at the river even though the river phase starts later.

Compared to only catching needed fish, rushing level 2 at the beach costs 6-7 extra fishing minigames (~44 seconds), but it almost doubles the likelihood of success for the day (36% to 72%).  This option could be particularly useful if the run is going well and you'd be willing to sacrifice a bit of extra time to increase the chances it succeeds.

However, this strategy is very dependent on getting lots of perfect catches.  Runners should practice perfect catches for all beach morning fish (especially sardine, anchovy, red snapper, and tilapia) and aim for level 2 around 10:10-10:40am.  If level 2 is slower than that, the strategy *reduces* your chances of success compared to only catching needed fish.

## What did I simulate?

I simulated 100,000 fall fish days with three strategies: rush level 2 at the beach, rush level 2 but move to the river after catching the ocean fish, and skip all unneeded fish.  I also tested three different cutoffs for perfect catches: no perfect catches, perfect catches on fish with difficulty <=30 (notably anchovy, sardine, red snapper), and perfect catches on everything with difficulty <=50 (notably adds tilapia and sea cucumber).  Here are the probabilities of successfully getting all 8 target fish:

| Strategy              | Perfect ≤50   | Perfect ≤30   | No perfect    |
|-----------------------|---------------|---------------|---------------|
| Rush lvl 2 at beach   | **71.1%**     | **45.6%**     | **2.9%**      |
| Rush lvl 2            | **65.4%**     | **43.5%**     | **31.7%**     |
| Skip non-targets      | **36.6%**     | **36.5%**     | **36.0%**     |

The code is `simulate_fish.py` and more details of the results can be found in `fish_day_analysis.md`.

## Completion Time Analysis

Very good luck on Fall Fish days is quite useful, because it allows an early try at lake fish and an early CC turn-in.  To get a sense of how often this ocurrs, we see how many runs complete the river fish early.  Rushing lvl 2 at the beach increases these odds as well.  In the three strategies, 22% / 14% / 9% of runs have river targets done by 1PM, allowing a meaningful lake window.

**River targets** (Shad, Catfish, Tiger Trout, Walleye) — cumulative % of all runs
where all four were caught by each time:

| Time | Rush at beach | Rush lvl 2 | Skip |
|---|---|---|---|
| 11AM | 0% | 0% | 0% |
| 12PM | 0% | 0% | 0% |
| 1PM | 22% | 14% | 9% |
| 2PM | 51% | 42% | 23% |
| 3PM (depart) | 71% | 66% | 38% |
| **Avg (done runs)** | 1:20PM | 1:30PM | 1:30PM |



## Acknowledgments

Thanks to Anthropic Sonnet 4.6 in Claude Code for writing most of the code, and for Dannode36 for the decompiled game source code as found in [StardewValleyDecompiled](https://github.com/Dannode36/StardewValleyDecompiled).