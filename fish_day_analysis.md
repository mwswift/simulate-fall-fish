## Comparison — Perfect Catch Threshold

P(all 8 fish caught) on a single rainy Fall day attempt.

| Strategy              | Perfect ≤50   | Perfect ≤30   | No perfect    |
|-----------------------|---------------|---------------|---------------|
| Rush lvl 2 at beach   | **71.0%**     | **45.2%**     | **3.0%**      |
| Rush lvl 2            | **65.4%**     | **43.1%**     | **31.7%**     |
| Skip non-targets      | **36.5%**     | **36.6%**     | **36.3%**     |

Average finish time (successful runs only) and real-world minigame time per day:
  Perfect catch: 6.5s/fish | Non-perfect: 7.2s/fish | Skip identify: 0.5s

| Strategy (≤50 threshold) | Avg finish    | Minigame s/day | vs Skip       |
|-----------------------|---------------|---------------|---------------|
| Rush lvl 2 at beach   | 4:40PM        | 98s           | +44s          |
| Rush lvl 2            | 4:40PM        | 93s           | +38s          |
| Skip non-targets      | 5:20PM        | 55s           | +0s           |

---

# Fall Fish Day — CC% Route Analysis
(TheHaboo, SDV 1.6, Forest Farm, Remixed Mines, Year 1)

---

## Rush Fishing Level 2 at the Beach

Fall fish day requires catching 8 specific fish across 3 locations on a single rainy day.
The run-killer is the river phase: Tiger Trout and Walleye have low catch weights and
narrow time windows, so the number of fast Fiberglass Rod casts you get at the river
is the primary lever on success probability.

The Fiberglass Rod requires fishing level 2 and is purchased from Willy, who is on the
beach. Levelling up at the beach costs nothing — Willy's shop is right there. Levelling
up at the river costs a 60-game-minute round trip (~7 minutes real time).

Three strategies, all catching non-selectively pre-Lv2 for max XP:

**Rush lvl 2 at beach** — Fish non-selectively at the beach until Tilapia AND Lv2 are
both achieved, buying the Fiberglass Rod for free on the way out. River fishing starts
with fiber rod already in hand: avg 16 fiber casts at river,
0 bamboo casts. P(all 8 fish) = **71.0%**.

**Rush lvl 2** — Same aggressive beach fishing, but departs for the river as soon as
Tilapia is caught, using the bamboo rod until levelling up mid-river. The Willy round
trip eats into fiber-rod time: avg 3 bamboo + 12 fiber casts at river.
P(all 8 fish) = **65.4%** (–5.7% vs rush at beach).

**Skip non-targets** — Cast only for target fish throughout; almost never reaches Lv2
(15.8% of runs) and fishes the Eel phase with the slow bamboo rod.
Saves ~55s of minigame time per day but Tiger Trout and
Walleye kill runs at similar rates to the rush strategies.
P(all 8 fish) = **36.5%** (–34.6% vs rush at beach).

**Perfect catches matter for the XP model.** The ×2.4 XP multiplier on fish with
difficulty ≤ 50 (Tilapia, Shad, Walleye, etc.) is what makes Lv2 achievable at the
beach. If the runner isn't consistently clearing the minigame perfectly, level-up timing
shifts later and the Lv2-at-beach guarantee weakens — see the ≤30/no-perfect rows
in the comparison table above.

**Strategic considerations:**
- Run pacing well → prefer **rush lvl 2 at beach**: the risk-averse play that locks in
  a 71.0% success rate at a cost of only ~44s extra
  minigame time per day compared to skipping.
- Run pacing poorly → consider **skip non-targets**: save ~40s per reset to make more
  attempts, accepting the lower per-day probability.
- **Rush lvl 2** (no beach guarantee) is dominated by rush at beach: same time cost,
  lower success rate. Only prefer it if you're already Lv2 before Tilapia.

---

| Strategy | P(all 8 fish) | Got Fiberglass | Minigame s/day | Avg level-up |
|---|---|---|---|---|
| Rush lvl 2 at beach | **71.0%** | 100.0% | 98s | 10:10AM |
| Rush lvl 2 | **65.4%** | 100.0% | 93s | 10:40AM |
| Skip non-targets | **36.5%** | 15.8% | 55s | 5:40PM |

---

## Where Runs Die

Days where that fish was the sole reason the run failed:

**Rush lvl 2 at beach**
```
  Tiger Trout       12.7%     █████
  Walleye           4.8%      █
  Shad              3.4%      █
  Catfish           3.2%      █
  Red Snapper       0.1%      
  Sardine           0.0%      
  Tilapia           0.0%      
  Eel               0.0%      
```

**Rush lvl 2**
```
  Tiger Trout       14.0%     █████
  Walleye           6.2%      ██
  Shad              4.1%      █
  Catfish           3.6%      █
  Red Snapper       0.3%      
  Sardine           0.0%      
  Tilapia           0.0%      
  Eel               0.0%      
```

**Skip non-targets**
```
  Tiger Trout       15.0%     ██████
  Walleye           12.3%     ████
  Shad              5.1%      ██
  Catfish           4.6%      █
  Red Snapper       1.3%      
  Sardine           0.2%      
  Eel               0.0%      
  Tilapia           0.0%      
```

---

## Completion Time Analysis

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

**All non-Eel targets** (7 fish: all except Eel) — cumulative % of all runs
where all seven were caught by each time:

| Time | Rush at beach | Rush lvl 2 | Skip |
|---|---|---|---|
| 12PM | 0% | 0% | 0% |
| 1PM | 17% | 9% | 5% |
| 2PM | 41% | 26% | 13% |
| 4PM | 68% | 59% | 30% |
| 6PM | 71% | 65% | 35% |
| 7PM | 71% | 65% | 36% |
| **Avg (done runs)** | 1:50PM | 2:20PM | 2:30PM |

Non-Eel totals step up after 4PM: Sardine and Red Snapper can be caught during
the beach PM mop-up phase (4PM–7PM) if missed earlier.
**Avg (done runs)** is conditional on that set being completed (excludes failed runs).

---

## Catches per Phase

Average casts per phase per day (including junk; all strategies):

| Phase | Rush at beach | Rush lvl 2 | Skip |
|---|---|---|---|
| Beach 7–9AM | 5.6 | 5.6 | 5.6 |
| Beach 9AM–2PM | 5.6 | 2.7 | 2.5 |
| River (bamboo) | — | 3.4 | 12.6 |
| River (fiberglass) | 16.5 | 12.2 | — |
| Ocean 4PM–2AM | 11.2 | 10.3 | 6.6 |
| **Total** | **38.9** | **34.2** | **27.3** |

Fraction of minigames that were perfect catches (difficulty ≤ 50):

| Phase | Rush at beach | Rush lvl 2 | Skip |
|---|---|---|---|
| Beach 7–9AM | 88% | 88% | 100% |
| Beach 9AM–2PM | 88% | 90% | 100% |
| River (bamboo) | — | 68% | 51% |
| River (fiberglass) | 51% | 56% | — |
| Ocean 4PM–2AM | 17% | 30% | 27% |
| **Overall** | 72% | 71% | 64% |

---

## How the Day Is Routed

One real second ≈ 1.4 in-game minutes. One tick = 10 in-game minutes = 7 real seconds.

**Phase 1a — Beach, 7AM–9AM** (Bamboo Rod, no bait, Lv1)
  Targets: Sardine, Red Snapper, Tilapia
  Avg cast: 14.2s (~20 game-min)
  Sunfish caught at farm pond first (Training Rod, guaranteed); arrive beach 7AM.

  **9AM — Willy's for Trout Soup** (+1 effective fishing level)

**Phase 1b — Beach, 9AM–2PM** (Bamboo or Fiberglass*, Lv2*)
  Rush at beach: stay until Tilapia caught AND Lv2 reached; buy rod free at Willy's.
  Rush lvl 2:    depart as soon as Tilapia is caught (or 2PM if Tilapia not found).
  Skip:          depart as soon as Tilapia is caught.
  Avg cast (Bamboo Lv2): 14.1s

  **Walk to river: 30 game-min (3 ticks)**

**Phase 2a — River bamboo** (Bamboo Rod, no bait, Lv2*)
  Skipped entirely if Fiberglass already obtained (rush at beach).
  Rush lvl 2 avg: 3 bamboo casts here before levelling up.
  Skip avg: 13 bamboo casts (targets only; rarely hits Lv2).

  **Level 2 at river → Willy's round-trip: 60 game-min (6 ticks)**

**Phase 2b — River fiberglass** (Fiberglass Rod, bait, Lv3*)
  Avg cast: 7.0s (~10 game-min, WR observed exactly 10)
  Rush at beach avg: 16 fiber casts | Rush lvl 2 avg: 12 | Skip: 0
  Fish remaining river targets until caught or 3PM departure.

  **Leave river → coffee stop → beach: 60 game-min (6 ticks)**

**Phase 3 — Beach, 4PM–2AM** (Fiberglass or Bamboo*, Lv3)
  Targets: Eel (4PM–2AM, rain only); Sardine + Red Snapper until 7PM if missed earlier.
  Rush strategies: Fiberglass in 100.0%/100.0% of runs → avg 7.0s/cast
  Skip: Fiberglass in 15.8% of runs; Bamboo in remaining → avg 14.1s/cast

  * effective level = natural level + Trout Soup (+1)

---

## Assumptions in Plain English

### Timing

All timings from TheHaboo's world record run.

- **7AM beach start.** Sunfish caught at farm pond (guaranteed via Training Rod), then walk to beach.
- **9AM Willy's visit.** Buys Trout Soup (+1 fishing). Willy's is on the beach; no travel cost.
- **Extended Tilapia window.** If Tilapia not caught by 9AM, continue at beach until it appears
  or 2PM (when Tilapia's window closes). Sardine and Red Snapper caught opportunistically.
- **River arrival.** 30-min walk from beach after leaving. Worst case: depart 2PM → arrive 2:30PM.
- **Level-up at river → 60-min round trip to Willy's.** Only if rod not already obtained.
- **River departure: 3PM.** 60-min walk to beach (includes coffee purchase). Beach 4PM.

### Bite Time and Rod Mechanics

Two cast functions fitted to WR observed real-time timestamps (n=14 casts):
```
  Bamboo Pole (no bait):   bite = U(0.6, 30−0.25×level) × 0.75
    0.75 first-cast bonus universal (FishingRod.cs line 427; WR n=14 consistent)
    + 0.4 tick overhead (cast animation + pickup)
    Level 2: avg 14.1s per cast (~20 game-min)

  Fiberglass Rod + bait:   bite = U(0.6, 30−0.25×level) × 0.75 × 0.5
    + 0.2 tick overhead
    Level 3: avg 7.0s per cast (~10 game-min, WR observed exactly 10)
```
Cast distance does not affect bite time (confirmed: GameLocation.calculateTimeUntilFishingBite
uses only fishing level, tackle, and bait — bobberTile checked only for fish ponds).
Game clock is frozen during the fishing minigame; only bite wait advances the clock.

### XP and Level-Up

XP formula (FishingRod.cs doPullFishFromWater lines 1091-1104):
  base_xp = floor((quality+1)×3 + difficulty/3)   [pre-boost quality]
  if perfect: xp = base_xp + floor(base_xp × 1.4)   [≈ ×2.4 total]
  Quality from fishSize = (depth/5) × (Skill+2)/10 × Random/100
    depth: ocean=5, river=3 | Skill ~ U(even from floor_even(level) to 10)
    fishSize < 0.33 → normal (0); 0.33–<0.66 → silver (1); ≥0.66 → gold (2)
  Perfect catch assumed for difficulty ≤ 50. XP uses pre-boost quality.
  Normal-quality fish (quality=0) do not receive an inventory quality boost on perfect
  catch (FishingRod.cs lines 1077-1084: boost only if quality >= 1), but still earn ×2.4 XP.
  Starting XP: 31 from Sunfish (Training Rod → quality always normal).

Expected XP per fish by phase (quality distribution from fishSize formula):
```
  Fish                diff  Lv1 beach  Lv2 river  Lv3 ocean
  Super Cucumber        80       33.0       31.9       33.8
  Catfish               75       32.0       30.9       32.8
  Eel                   70       30.0       28.9       30.8
  Albacore              60       27.0       25.9       27.8
  Tiger Trout           60       27.0       25.9       27.8
  Tilapia*              50       54.9       52.0       56.9
  Salmon*               50       54.9       52.0       56.9
  Shad*                 45       52.4       49.8       54.3
  Walleye*              45       52.4       49.8       54.3
  Red Snapper*          40       47.4       44.8       49.3
  Sea Cucumber*         40       47.4       44.8       49.3
  Bream*                35       42.9       40.0       44.9
  Sunfish*              30                                   → 31 XP (Training Rod, always normal quality)
  Sardine*              30       40.4       37.8       42.3
  Anchovy*              30       40.4       37.8       42.3
  Smallmouth Bass*      28       38.2       35.6       40.3
  * = perfect catch assumed (difficulty ≤ 50)
```
SDV fishing XP thresholds (cumulative): Lv1=100, Lv2=380, Lv3=770

**catch_all / rush_beach** catch Smallmouth Bass, Salmon, Bream, etc. for XP pre-Lv2,
accelerating the level-up. **skip** only catches target fish — non-target casts cost
the same game-clock time (bite wait) but yield 0 XP.

### Fish Pools and Catch Weights

Rainy Fall day, SDV 1.6 game data (GameLocation.cs lines 13950-13961).
Catch weight formula: chance = baseRate − max(0, maxDepth−depth)×depthMult×baseRate + level/50
  capped at 0.90. Ocean depth=5 (no penalties); river depth=3 (Catfish penalty: −0.04).
```
Phase 1 — Beach AM (depth 5, Lv1):
  Sardine            0.67  6AM–7PM  ← target
  Anchovy            0.27  6AM–2AM
  Red Snapper        0.47  6AM–7PM  ← target
  Tilapia            0.42  6AM–2PM  ← target
  Sea Cucumber       0.27  6AM–7PM
  Albacore           0.32  6AM–11AM, 6PM–2AM
  Seaweed            0.32  6AM–2AM
  Sea Jelly          0.12  6AM–2AM

Phase 2 — River (depth 3, Lv2 bamboo / Lv3 fiber):
  Smallmouth Bass    0.49/0.51  6AM–2AM
  Salmon             0.44/0.46  6AM–7PM
  Catfish            0.40/0.42  6AM–12AM  ← target
  Shad               0.39/0.41  9AM–2AM  ← target
  Tiger Trout        0.24/0.26  6AM–7PM  ← target
  Walleye            0.44/0.46  12PM–2AM  ← target
  Green Algae        0.34/0.36  6AM–2AM
  River Jelly        0.14/0.16  6AM–2AM

Phase 3 — Beach PM (depth 5, Lv3):
  Sardine            0.71  6AM–7PM  ← target
  Anchovy            0.31  6AM–2AM
  Red Snapper        0.51  6AM–7PM  ← target
  Sea Cucumber       0.31  6AM–7PM
  Albacore           0.36  6AM–11AM, 6PM–2AM
  Seaweed            0.36  6AM–2AM
  Eel                0.61  4PM–2AM  ← target
  Super Cucumber     0.16  6PM–2AM
  Sea Jelly          0.16  6AM–2AM
```

### The Catch Algorithm

Each cast: shuffle the eligible fish list, roll each fish independently against its
weight, catch the first one that passes. Not a proportional draw — any fish can win
if it draws position #1 in the shuffle, regardless of weight.

### What This Model Doesn't Include

- **Fishing bubbles.** Halve bite time. Not modelled; makes simulation slightly pessimistic.
- **No escapes.** Assumes the runner clears the minigame on every cast.
- **Constant river cast depth.** The simulation fishes at depth 3 throughout the river
  phase. Experienced runners adjust depth mid-session: shallow casting (depth 1–2) once
  short-window fish are caught suppresses them and raises the relative odds of remaining
  targets. The current model may slightly understate success probability for runners who
  apply this technique.

---

## Sample Day Logs (perfect catch threshold ≤50)

One randomly sampled day per strategy. Seed per strategy: Rush lvl 2 at beach=0, Rush lvl 2=1, Skip non-targets=2.

Column layout:
```
  [time]   bite_s  Fish name             event  quality  XP  flags  [cumulative XP / level]
```
Events: CATCH = minigame played and won | SKIP = minigame declined | JUNK = auto-received

### Rush lvl 2 at beach (seed=0) — SUCCESS
```
[7:10AM] Phase 1a — Beach (Bamboo, no bait, natural Lv0)
  Starting XP: 31 (Sunfish caught at farm pond)
  7:10AM      3.5s  Sardine               CATCH  silver   38XP perfect          [total 69XP Lv0]
  7:10AM     13.9s  Sardine               CATCH  gold     45XP perfect          [total 114XP Lv1]
  *** Level 1! ***
  7:40AM      0.5s  Anchovy               CATCH  gold     45XP perfect (XP only)  [total 159XP Lv1]
  7:40AM      5.7s  Sea Cucumber          CATCH  gold     52XP perfect (XP only)  [total 211XP Lv1]
  7:50AM     12.4s  Sardine               CATCH  silver   38XP perfect          [total 249XP Lv1]
  8:20AM      6.8s  Sardine               CATCH  gold     45XP perfect          [total 294XP Lv1]
  8:30AM     17.0s  Sea Jelly             JUNK   3XP                    [total 297XP Lv1]
[9AM] Willy's — Trout Soup purchased (+1 effective level)
[9AM] Phase 1b — Beach (Bamboo→Fiber*, soup, effective Lv2)
  9AM        18.3s  Anchovy               CATCH  silver   38XP perfect (XP only)  [total 335XP Lv1]
  9:30AM     11.0s  Sardine               CATCH  gold     45XP perfect          [total 380XP Lv2]
  *** Level 2! Fiberglass Rod purchased (effective Lv3 with soup) ***
  9:50AM      8.8s  Tilapia               CATCH  silver   52XP perfect          [total 432XP Lv2]
[10AM] Depart beach → walk to river (30 min)
[10:30AM] Phase 2a — skipped (Fiberglass already in hand)
[10:30AM] Phase 2b — River (Fiberglass+bait, effective Lv3)
  10:30AM     6.4s  Salmon                SKIP
  10:40AM     0.6s  Shad                  CATCH  silver   50XP perfect          [total 482XP Lv2]
  10:50AM     7.5s  Shad                  SKIP
  11AM        4.9s  Catfish               CATCH  silver   31XP                  [total 513XP Lv2]
  11:10AM     9.9s  Catfish               SKIP
  11:20AM     2.9s  Catfish               SKIP
  11:30AM     7.3s  Salmon                SKIP
  11:40AM     3.2s  Green Algae           JUNK   3XP                    [total 516XP Lv2]
  11:50AM     8.3s  Tiger Trout           CATCH  silver   26XP                  [total 542XP Lv2]
  12PM        7.9s  Walleye               CATCH  silver   50XP perfect          [total 592XP Lv2]
[12:20PM] Depart river → coffee stop → beach (60 min)
[1:20PM] Phase 3 — Beach PM (Fiberglass+bait, effective Lv3)
  1:20PM      0.9s  Anchovy               SKIP
  1:20PM      3.6s  Sardine               SKIP
  1:30PM      0.5s  Seaweed               JUNK   3XP                    [total 595XP Lv2]
  1:30PM      9.1s  Sea Cucumber          SKIP
  1:50PM     10.7s  Red Snapper           CATCH  silver   45XP perfect          [total 640XP Lv2]
  2PM         3.0s  Red Snapper           SKIP
  2:10PM      0.5s  Anchovy               SKIP
  2:10PM      8.3s  Red Snapper           SKIP
  2:30PM      4.2s  Sardine               SKIP
  2:30PM      1.8s  Sardine               SKIP
  2:40PM      0.7s  Sardine               SKIP
  2:40PM      1.5s  Sea Cucumber          SKIP
  2:50PM      9.2s  Seaweed               JUNK   3XP                    [total 643XP Lv2]
  3PM         5.4s  Sardine               SKIP
  3:10PM      7.6s  Red Snapper           SKIP
  3:20PM      1.1s  Seaweed               JUNK   3XP                    [total 646XP Lv2]
  3:30PM      6.2s  Red Snapper           SKIP
  3:40PM     10.8s  Sardine               SKIP
  3:50PM      9.5s  Sardine               SKIP
  4:10PM      4.5s  Anchovy               SKIP
  4:20PM      5.2s  Sea Cucumber          SKIP
  4:30PM      4.6s  Sea Cucumber          SKIP
  4:40PM      7.8s  Eel                   CATCH  gold     32XP                  [total 678XP Lv2]
  *** All 8 targets caught! ***
[4:40PM] Run complete — all 8 fish caught.
```

### Rush lvl 2 (seed=1) — FAILED
```
[7:10AM] Phase 1a — Beach (Bamboo, no bait, natural Lv0)
  Starting XP: 31 (Sunfish caught at farm pond)
  7:10AM     20.1s  Anchovy               CATCH  gold     45XP perfect (XP only)  [total 76XP Lv0]
  7:40AM      0.9s  Albacore              CATCH  silver   26XP         (XP only)  [total 102XP Lv1]
  *** Level 1! ***
  7:40AM     20.7s  (trash)               JUNK   3XP                    [total 105XP Lv1]
  8:20AM     20.9s  Albacore              CATCH  silver   26XP         (XP only)  [total 131XP Lv1]
  8:50AM      9.5s  Red Snapper           CATCH  silver   45XP perfect          [total 176XP Lv1]
[9AM] Willy's — Trout Soup purchased (+1 effective level)
[9:10AM] Phase 1b — Beach (Bamboo→Fiber*, soup, effective Lv2)
  9:10AM      1.4s  Sardine               CATCH  silver   38XP perfect          [total 214XP Lv1]
  9:10AM     21.1s  Sardine               CATCH  gold     45XP perfect          [total 259XP Lv1]
  9:50AM     12.5s  Sardine               CATCH  gold     45XP perfect          [total 304XP Lv1]
  10:10AM     4.3s  Anchovy               CATCH  gold     45XP perfect (XP only)  [total 349XP Lv1]
  10:20AM     0.8s  Anchovy               CATCH  silver   38XP perfect (XP only)  [total 387XP Lv2]
  *** Level 2! Fiberglass Rod purchased (effective Lv3 with soup) ***
  10:30AM     1.9s  Sea Jelly             JUNK   3XP                    [total 390XP Lv2]
  10:30AM     1.5s  Sardine               SKIP
  10:30AM     8.1s  Albacore              SKIP
  10:50AM     7.9s  Red Snapper           SKIP
  11AM        7.7s  Sardine               SKIP
  11:10AM     8.1s  Red Snapper           SKIP
  11:30AM    10.3s  Seaweed               JUNK   3XP                    [total 393XP Lv2]
  11:40AM     2.6s  Sardine               SKIP
  11:50AM     2.4s  Red Snapper           SKIP
  12PM        5.6s  Sardine               SKIP
  12:10PM     9.4s  Seaweed               JUNK   3XP                    [total 396XP Lv2]
  12:20PM    10.2s  Tilapia               CATCH  silver   52XP perfect          [total 448XP Lv2]
[12:40PM] Depart beach → walk to river (30 min)
[1:10PM] Phase 2a — skipped (Fiberglass already in hand)
[1:10PM] Phase 2b — River (Fiberglass+bait, effective Lv3)
  1:10PM      0.7s  Salmon                SKIP
  1:10PM      3.4s  Shad                  CATCH  silver   50XP perfect          [total 498XP Lv2]
  1:20PM      9.1s  Catfish               CATCH  silver   31XP                  [total 529XP Lv2]
  1:30PM      6.0s  Shad                  SKIP
  1:40PM      4.7s  Green Algae           JUNK   3XP                    [total 532XP Lv2]
  1:50PM      8.2s  Walleye               CATCH  silver   50XP perfect          [total 582XP Lv2]
  2:10PM      3.6s  Walleye               SKIP
  2:10PM      0.9s  Green Algae           JUNK   3XP                    [total 585XP Lv2]
  2:20PM      6.0s  Salmon                SKIP
  2:30PM      3.7s  Salmon                SKIP
  2:30PM      0.5s  Salmon                SKIP
  2:40PM      0.5s  Salmon                SKIP
  2:40PM     10.4s  River Jelly           JUNK   3XP                    [total 588XP Lv2]
[3PM] Depart river → coffee stop → beach (60 min)
[4PM] Phase 3 — Beach PM (Fiberglass+bait, effective Lv3)
  4PM         5.8s  Sardine               SKIP
  4:10PM      7.4s  Sardine               SKIP
  4:20PM      0.7s  Sardine               SKIP
  4:20PM      9.4s  Sardine               SKIP
  4:40PM      7.7s  Sea Jelly             JUNK   3XP                    [total 591XP Lv2]
  4:50PM      6.3s  Sea Cucumber          SKIP
  5PM         3.6s  Red Snapper           SKIP
  5:10PM     10.5s  Sardine               SKIP
  5:30PM      1.0s  Anchovy               SKIP
  5:30PM      9.3s  Sardine               SKIP
  5:40PM      2.6s  Eel                   CATCH  gold     32XP                  [total 623XP Lv2]
[2AM] Run failed. Missing: Tiger Trout
```

### Skip non-targets (seed=2) — FAILED
```
[7:10AM] Phase 1a — Beach (Bamboo, no bait, natural Lv0)
  Starting XP: 31 (Sunfish caught at farm pond)
  7:10AM      5.1s  Albacore              SKIP
  7:20AM      6.4s  Tilapia               CATCH  gold     60XP perfect          [total 91XP Lv0]
  7:30AM      4.4s  Anchovy               SKIP
  7:40AM     20.2s  Seaweed               JUNK   3XP                    [total 94XP Lv0]
  8:10AM     14.9s  Sardine               CATCH  gold     45XP perfect          [total 139XP Lv1]
  *** Level 1! ***
  8:40AM     15.7s  Tilapia               SKIP
[9AM] Willy's — Trout Soup purchased (+1 effective level)
[9AM] Phase 1b — Beach (Bamboo→Fiber*, soup, effective Lv2)
[9AM] Depart beach → walk to river (30 min)
[9:30AM] Phase 2a — River (Bamboo, no bait, effective Lv2)
  9:30AM      5.0s  Salmon                SKIP
  9:50AM     12.9s  Shad                  CATCH  normal   43XP perfect          [total 182XP Lv1]
  10:10AM     6.2s  River Jelly           JUNK   3XP                    [total 185XP Lv1]
  10:20AM     8.3s  Green Algae           JUNK   3XP                    [total 188XP Lv1]
  10:40AM    16.3s  River Jelly           JUNK   3XP                    [total 191XP Lv1]
  11AM       17.7s  Tiger Trout           CATCH  silver   26XP                  [total 217XP Lv1]
  11:30AM     7.1s  Catfish               CATCH  silver   31XP                  [total 248XP Lv1]
  11:50AM    14.8s  Green Algae           JUNK   3XP                    [total 251XP Lv1]
  12:10PM    19.4s  Salmon                SKIP
  12:40PM     3.3s  Shad                  SKIP
  12:50PM     2.2s  River Jelly           JUNK   3XP                    [total 254XP Lv1]
  1PM        16.7s  Smallmouth Bass       SKIP
  1:30PM      4.4s  River Jelly           JUNK   3XP                    [total 257XP Lv1]
  1:40PM     15.3s  Catfish               SKIP
  2PM         8.4s  Walleye               CATCH  normal   43XP perfect          [total 300XP Lv1]
[2:20PM] Depart river → coffee stop → beach (60 min)
[3:20PM] Phase 3 — Beach PM (Bamboo, no bait, effective Lv2)
  3:20PM      7.1s  Sea Cucumber          SKIP
  3:30PM      1.0s  Sardine               SKIP
  3:40PM      8.5s  Sea Jelly             JUNK   3XP                    [total 303XP Lv1]
  4PM        13.8s  Sardine               SKIP
  4:20PM     14.7s  Seaweed               JUNK   3XP                    [total 306XP Lv1]
  4:40PM      8.6s  Eel                   CATCH  gold     32XP                  [total 338XP Lv1]
  5PM         3.8s  Sardine               SKIP
  5:10PM      8.2s  Eel                   SKIP
  5:30PM      6.9s  Eel                   SKIP
  5:40PM     12.2s  Seaweed               JUNK   3XP                    [total 341XP Lv1]
  6PM        22.0s  Sardine               SKIP
  6:40PM      6.4s  Albacore              SKIP
  6:50PM     18.2s  Sea Jelly             JUNK   3XP                    [total 344XP Lv1]
[2AM] Run failed. Missing: Red Snapper
```
