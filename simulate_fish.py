#!/usr/bin/env python3
"""
Fall Fish Day — standalone simulation for TheHaboo's CC% speedrun (SDV 1.6, Forest Farm).

Simulates catching 8 required fish in a single rainy Fall day (Year 1, Fall 2–14).
Compares three strategies:
  catch_all  ("Rush lvl 2")          — complete every minigame; max XP; reach Lv2 fastest
  rush_beach ("Rush lvl 2 at beach") — same, but stay beach until BOTH Tilapia caught AND Lv2
                                        reached; Fiberglass picked up at Willy's for free (0 ticks)
  skip       ("Skip non-targets")    — quit minigame for non-targets; saves real time, slower XP

Output: fish_day_analysis.md

Route (reconstructed from WR run):
  7:10–9:10   Ocean     Bamboo, no bait, Lv1    Sardine / Red Snapper / Tilapia
  9:10        Willy's   Buy Trout Soup (+1 effective fishing level)
  9:40        River start
  9:40–LvUp   River     Bamboo, no bait, Lv2*   fish for XP + targets
  LvUp+60min  River     Fiberglass, bait, Lv3*  remaining targets
  ~3:10       Leave river (coffee stop); 60-min walk to beach
  ~4:10       Ocean     Fiberglass, bait, Lv3*  Eel (+ any missed Sardine/Snapper)

* effective level = natural level + Trout Soup (+1); soup confirmed active throughout river phase

Source data: Data/Fish.xnb + Data/Locations.xnb via brokencygnus/stardew-fishing-calc (SDV 1.6).
Fish difficulty: fish data.xlsx "sell price/difficulty" sheet.
"""

import random
import sys


# ══════════════════════════════════════════════════════════════════════════════
# GAME TIME CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# 1 tick = 10 game-minutes = 7 real seconds. tick = (game_time − 600) × 0.06
TICK_6AM         =   0
TICK_BEACH_START =   7   # 7:10 AM (WR: arrive after farm-pond Sunfish)
TICK_9_10AM      =  19   # 9:10 AM (WR: enter Willy's for Trout Soup)
TICK_9AM         =  18
TICK_11AM        =  30
TICK_12PM        =  36
TICK_2PM         =  48
TICK_4PM         =  60
TICK_6PM         =  72
TICK_7PM         =  78
TICK_12AM        = 108
TICK_2AM         = 120

# WR-verified transitions (ticks = 10 game-minutes each):
TRANS_SOUP_TO_RIVER  = 3   # Willy's soup purchase + walk to Town river = 30 min
TRANS_LEVELUP_WILLY  = 6   # river → Willy's fiberglass purchase → river  = 60 min (WR)
TRANS_RIVER_TO_OCEAN = 6   # river → coffee purchase → beach = 60 min (WR)

# River departure and ocean arrival (simplified to clean round times).
RIVER_DEPART = 54   # tick 54 = 3:00 PM  (WR was 3:10; simplified 1 tick)


# ══════════════════════════════════════════════════════════════════════════════
# FISH POOLS
# ══════════════════════════════════════════════════════════════════════════════

TARGET_FISH = frozenset({"Sardine", "Red_Snapper", "Tilapia", "Eel",
                          "Shad", "Catfish", "Tiger_Trout", "Walleye"})

# Format: (name, depth_adjusted_baseRate, [(window_start_tick, window_end_tick)])
# Weight formula (GameLocation.cs lines 13950-13961):
#   dropOff = depthMultiplier × baseRate
#   chance  = baseRate − max(0, maxDepth − waterDepth) × dropOff + fishingLevel/50
#   capped at 0.90
# Ocean depth=5: all target fish have maxDepth ≤ 5 → no depth penalty → rate = baseRate
# River depth=3: Catfish has maxDepth=4 → penalty = (4−3)×0.1×0.40 = 0.04 → rate = 0.36
# Depth also affects fishSize factor (distance/5) → quality → XP; see CAST_DISTANCE constants.
# Rainy Fall day only; fountain-area items excluded.
BEACH_FISH = [
    ("Sardine",        0.65, [(TICK_6AM,  TICK_7PM)]),
    ("Anchovy",        0.25, [(TICK_6AM,  TICK_2AM)]),
    ("Red_Snapper",    0.45, [(TICK_6AM,  TICK_7PM)]),   # rain only
    ("Tilapia",        0.40, [(TICK_6AM,  TICK_2PM)]),
    ("Sea_Cucumber",   0.25, [(TICK_6AM,  TICK_7PM)]),
    ("Albacore",       0.30, [(TICK_6AM,  TICK_11AM), (TICK_6PM, TICK_2AM)]),
    ("Seaweed",        0.30, [(TICK_6AM,  TICK_2AM)]),
    ("Eel",            0.55, [(TICK_4PM,  TICK_2AM)]),   # rain only
    ("Super_Cucumber", 0.10, [(TICK_6PM,  TICK_2AM)]),
    ("Sea_Jelly",      0.10, [(TICK_6AM,  TICK_2AM)]),   # SDV 1.6 junk, any season/weather
]

TOWN_FISH = [
    ("Smallmouth_Bass", 0.45, [(TICK_6AM,  TICK_2AM)]),
    ("Salmon",          0.40, [(TICK_6AM,  TICK_7PM)]),
    ("Catfish",         0.36, [(TICK_6AM,  TICK_12AM)]),  # rain only; 0.36 = depth-3 adjusted (maxDepth=4 penalty: −0.04)
    ("Shad",            0.35, [(TICK_9AM,  TICK_2AM)]),   # rain only
    ("Tiger_Trout",     0.20, [(TICK_6AM,  TICK_7PM)]),
    ("Walleye",         0.40, [(TICK_12PM, TICK_2AM)]),   # rain only
    ("Green_Algae",     0.30, [(TICK_6AM,  TICK_2AM)]),
    ("Bream",           0.45, [(TICK_6PM,  TICK_2AM)]),
    ("River_Jelly",     0.10, [(TICK_6AM,  TICK_2AM)]),   # SDV 1.6 junk, any season/weather
]


# ══════════════════════════════════════════════════════════════════════════════
# FISHING LEVEL MODEL
# ══════════════════════════════════════════════════════════════════════════════

# Effective levels — used for writeup/display only; simulation uses dynamic natural_level.
# Soup (+1 effective fishing level) is active from 9AM through end of day.
# Simulation: effective = natural_level (Phase 1a, no soup) or natural_level+1 (Phase 1b+).
LEVEL_OCEAN_AM     = 1   # typical natural Lv1 by mid-Phase 1a (display only)
LEVEL_BAMBOO_RIVER = 2   # typical natural Lv1 + soup = Lv2 effective (display only)
LEVEL_FIBER_RIVER  = 3   # typical natural Lv2 + soup = Lv3 effective (display only)
LEVEL_OCEAN_PM     = 3   # same as fiberglass phase (display only)


# ══════════════════════════════════════════════════════════════════════════════
# XP MODEL
# ══════════════════════════════════════════════════════════════════════════════

# Fish difficulty from "fish data.xlsx" → "sell price/difficulty" sheet.
# Used only for XP calculation; does not affect catch weights.
FISH_DIFFICULTY: dict[str, int] = {
    "Sunfish":        30,   # caught at farm pond before beach phase (starting XP only)
    "Sardine":        30,
    "Anchovy":        30,
    "Red_Snapper":    40,
    "Tilapia":        50,
    "Sea_Cucumber":   40,
    "Albacore":       60,
    "Eel":            70,
    "Super_Cucumber": 80,
    "Smallmouth_Bass":28,
    "Salmon":         50,
    "Catfish":        75,
    "Shad":           45,
    "Tiger_Trout":    60,
    "Walleye":        45,
    "Bream":          35,
    # Junk items (Seaweed, Green_Algae, Sea_Jelly, River_Jelly) → JUNK_XP via JUNK_ITEMS set
}

# Junk items: auto-received (no minigame, can't skip), each gives JUNK_XP = 3.
# FishingRod.cs junk branch passes difficulty=-1 → max(1,(0+1)*3+(-1)/3) = max(1,3) = 3 XP.
# Sea_Jelly (Beach) and River_Jelly (Town river): SDV 1.6 additions, Chance=0.10, any season.
# "Other": fallback when no fish passes its weight roll → trash (Category=-20) in-game → 3 XP.
JUNK_ITEMS = frozenset({"Seaweed", "Green_Algae", "Sea_Jelly", "River_Jelly", "Other"})
JUNK_XP    = 3

# SDV fishing XP thresholds (cumulative). Lv1=100, Lv2=380 (user-confirmed).
XP_THRESHOLDS = [0, 100, 380, 770, 1300]

# Cast distance: max tiles of clear water from shore.
# Beach/ocean: 5+ tiles available; river (Town): max 3 tiles (user-confirmed).
CAST_DISTANCE       = 5   # ocean/beach phases
RIVER_CAST_DISTANCE = 3   # town river — affects fishSize → quality → XP only


def _fish_size_factor(effective_level: int, cast_distance: int = CAST_DISTANCE) -> float:
    """fishSize ∈ [0,1]: (Distance/5) × (Skill+2)/10 × Random/100."""
    floor_even = (effective_level // 2) * 2
    skill = random.choice(range(floor_even, 11, 2))
    rnd = random.randint(90, 110)
    fs = (cast_distance / 5) * ((skill + 2) / 10.0) * (rnd / 100.0)
    return min(1.0, max(0.0, fs))


def _base_quality(size_factor: float) -> int:
    """0 = normal, 1 = silver, 2 = gold (pre-perfect-catch-boost value)."""
    if size_factor < 0.33:
        return 0
    elif size_factor < 0.66:
        return 1
    return 2


def _display_quality(base_quality: int, perfect: bool) -> int:
    """Inventory quality after perfect-catch boost (doPullFishFromWater lines 1077-1084).
    Only silver+ fish are boosted; normal (0) stays normal even on a perfect catch."""
    if base_quality >= 2 and perfect:
        return 4   # iridium
    if base_quality >= 1 and perfect:
        return 2   # gold
    return base_quality  # normal stays normal; no boost


def _fish_xp(name: str, quality: int, perfect: bool) -> float:
    """
    XP for one catch (doPullFishFromWater lines 1091-1104).
    quality = pre-boost base quality (local param, not this.fishQuality after boost).
    perfect = True if minigame was perfect; adds ×2.4 multiplier regardless of quality.
    Note: a normal-quality perfect catch still earns ×2.4 XP even though the inventory
    quality is not boosted (_display_quality returns 0 for normal+perfect).
    """
    diff = FISH_DIFFICULTY.get(name, 0)
    if diff <= 0:
        return 0.0
    base_xp = int((quality + 1) * 3 + diff / 3.0)  # floor truncation
    if perfect:
        return float(int(base_xp * 2.4))            # floor truncation
    return float(base_xp)


def _expected_xp(name: str, effective_level: int, cast_distance: int = CAST_DISTANCE) -> float:
    """Analytical expected XP for a fish at the given effective fishing level."""
    diff = FISH_DIFFICULTY.get(name, 0)
    if diff <= 0:
        return 0.0
    perfect = diff <= 50
    floor_even = (effective_level // 2) * 2
    skills = list(range(floor_even, 11, 2))
    total, count = 0.0, 0
    for skill in skills:
        for rnd in range(90, 111):
            fs = min(1.0, (cast_distance / 5) * ((skill + 2) / 10.0) * (rnd / 100.0))
            total += _fish_xp(name, _base_quality(fs), perfect)
            count += 1
    return total / count


def _level_from_xp(xp: float) -> int:
    lv = 0
    for i, threshold in enumerate(XP_THRESHOLDS[1:], start=1):
        if xp >= threshold:
            lv = i
        else:
            break
    return lv


# ══════════════════════════════════════════════════════════════════════════════
# CAST TIME
# ══════════════════════════════════════════════════════════════════════════════

# Bite-time formula: FishingRod.cs calculateTimeUntilFishingBite.
# raw_ms ~ U[600, 30000−250×level) ms; if isFirstCast: raw_ms *= 0.75; if bait: *= 0.5.
# Code (both StardewValley/ and StardewValleyDecompiled/) passes isFirstCast=true on
# EVERY cast, no rod-type check — 0.75 applies universally to bamboo and fiberglass alike.
# WR real-time bite-wait analysis, n=14 bamboo casts (ocean AM + river):
#   ocean AM (n=4): observed mean 11.1s; with-0.75 E=11.5s → z=−0.13, p=0.89 ✓
#   river Lv2 (n=10, incl 2.01s point): observed mean 13.2s; with-0.75 E=11.3s → z=+0.97, p=0.33 ✓
#   no-0.75 model requires +4.2s overhead at ocean but only +1.8s at river — implausible.
# Both models pass the p>0.05 threshold; 0.75 is supported by code, wiki, and ocean data.
# Simulation applies 0.75 to bamboo.
#
# Minigame real-time (BobberBar.cs): distanceFromCatching starts at 0.3, fills at
# 1/500 per frame → needs 350 frames = 5.83s at 60fps.
# Fade-in/out: 20 frames × 0.05/frame × 2 = 0.67s. Total perfect minigame ≈ 6.5s.
# Game clock is frozen during the fishing minigame; only bite wait advances the clock.
SECS_PER_TICK           = 7.0
BAMBOO_OVERHEAD_TICKS   = 0.4    # cast animation + pickup, Bamboo Pole
FIBER_OVERHEAD_TICKS    = 0.2    # cast animation + pickup, Fiberglass Rod
MINIGAME_PERFECT_SECS   = 6.5   # BobberBar.cs: perfect-catch minigame real time
MINIGAME_IMPERFECT_SECS = 6.5 * 1.1  # non-perfect ~1.1× longer
SKIP_IDENTIFY_SECS      = 0.5   # time to read fish pattern before deciding to skip


def _cast_bamboo(level: int) -> tuple:
    """Bamboo Pole (no bait, 0.75 first-cast bonus). Returns (ticks, bite_secs)."""
    max_raw = 30.0 - 0.25 * level
    bite = max(0.5, random.uniform(0.6, max_raw) * 0.75)
    return bite / SECS_PER_TICK + BAMBOO_OVERHEAD_TICKS, bite


def _cast_fiber(level: int) -> tuple:
    """Fiberglass Rod + bait (0.75 × 0.5 bite reduction). Returns (ticks, bite_secs)."""
    max_raw = 30.0 - 0.25 * level
    bite = max(0.5, random.uniform(0.6, max_raw) * 0.75 * 0.5)
    return bite / SECS_PER_TICK + FIBER_OVERHEAD_TICKS, bite


# ══════════════════════════════════════════════════════════════════════════════
# CORE FISHING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _build_pool(fish_data: list, tick: int, level: int) -> list:
    pool = []
    for name, base_rate, windows in fish_data:
        if any(s <= tick < e for s, e in windows):
            pool.append((name, min(0.90, base_rate + 0.02 * level)))
    return pool


def _draw_fish_sdv(pool: list) -> str:
    shuffled = list(pool)
    random.shuffle(shuffled)
    for name, w in shuffled:
        if random.random() < w:
            return name
    return "Other"


# ══════════════════════════════════════════════════════════════════════════════
# SIMULATION
# ══════════════════════════════════════════════════════════════════════════════

def _sim_fish_day(strategy: str, perfect_threshold: int = 50,
                  log: list | None = None) -> dict:
    """
    Simulate one rainy Fall fish day.

    strategy = "catch_all"  : catch all fish pre-Lv2 for max XP; targets only after
    strategy = "rush_beach" : same, but Phase 1b extends until BOTH Tilapia caught AND
                               Lv2 reached; Fiberglass obtained free at Willy's on beach
    strategy = "skip"       : targets only throughout (no XP fishing)

    log: if a list is passed, verbose per-cast entries are appended to it.

    Returns dict: caught, got_fiber, levelup_tick, xp, minigame_secs, finish_tick, phase_stats
    """
    uncaught      = set(TARGET_FISH)
    caught        = set()
    xp            = _fish_xp("Sunfish", 0, 30 <= perfect_threshold)
    natural_level = 0
    got_fiber     = False
    levelup_tick  = None
    finish_tick   = None
    minigame_secs = 0.0

    PHASES = ("beach_am", "beach_ext", "river_bamboo", "river_fiber", "ocean_pm")
    pc = {ph: {"casts": 0, "minigames": 0, "perfect": 0} for ph in PHASES}

    # ── Logging helpers ───────────────────────────────────────────────────
    def _log(msg: str) -> None:
        if log is not None:
            log.append(msg)

    _QUAL = {-1: "     ", 0: "normal", 1: "silver", 2: "gold  "}

    def _log_cast(fish: str, tick: float, bite_s: float, event: str,
                  q: int, gained: float) -> None:
        if log is None:
            return
        t  = _tick_to_time(tick)
        nm = "(trash)" if fish == "Other" else fish.replace("_", " ")
        if event == "JUNK":
            _log(f"  {t:<8}  {bite_s:5.1f}s  {nm:<20}  JUNK   {int(gained)}XP"
                 f"                    [total {int(xp)}XP Lv{natural_level}]")
        elif event == "CATCH":
            diff     = FISH_DIFFICULTY.get(fish, 0)
            perf_tag = " perfect" if diff <= perfect_threshold else "        "
            tgt_tag  = "        " if fish in TARGET_FISH else " (XP only)"
            _log(f"  {t:<8}  {bite_s:5.1f}s  {nm:<20}  CATCH  {_QUAL[q]}  "
                 f"{int(gained):3}XP{perf_tag}{tgt_tag}  [total {int(xp)}XP Lv{natural_level}]")
        else:
            _log(f"  {t:<8}  {bite_s:5.1f}s  {nm:<20}  SKIP")

    # ── Core closures ─────────────────────────────────────────────────────
    def do_catch(name: str, tick: float, effective_level: int,
                 cast_distance: int = CAST_DISTANCE) -> tuple:
        """Process one catch. Returns (quality, xp_gained); quality=-1 for junk.
        Does NOT log — callers log level-up / all-caught after the cast line."""
        nonlocal xp, natural_level, got_fiber, levelup_tick, finish_tick

        if name in JUNK_ITEMS:
            xp    += JUNK_XP
            new_lv = _level_from_xp(xp)
            if new_lv > natural_level:
                if natural_level < 2 <= new_lv:
                    levelup_tick = tick
                    got_fiber    = True
                natural_level = new_lv
            return -1, JUNK_XP

        if name in uncaught:
            caught.add(name)
            uncaught.discard(name)
            if not uncaught:
                finish_tick = tick

        diff = FISH_DIFFICULTY.get(name, 0)
        if diff <= 0:
            return 0, 0.0

        perfect = diff <= perfect_threshold
        orig_q  = _base_quality(_fish_size_factor(effective_level, cast_distance))
        gain    = _fish_xp(name, orig_q, perfect)
        xp     += gain
        new_lv  = _level_from_xp(xp)
        if new_lv > natural_level:
            if natural_level < 2 <= new_lv:
                levelup_tick = tick
                got_fiber    = True
            natural_level = new_lv
        return orig_q, gain

    def _log_events(lv_before: int, finish_before) -> None:
        """Log level-up and all-caught events that happened during the last do_catch."""
        if log is None:
            return
        if finish_tick is not None and finish_before is None:
            _log(f"  *** All 8 targets caught! ***")
        if natural_level > lv_before:
            if natural_level == 2:
                _log(f"  *** Level 2! Fiberglass Rod purchased"
                     f" (effective Lv{natural_level + 1} with soup) ***")
            else:
                _log(f"  *** Level {natural_level}! ***")

    def want(name: str) -> bool:
        if name in JUNK_ITEMS:
            return False
        if strategy in ("catch_all", "rush_beach") and not got_fiber:
            return True
        return name in uncaught

    def track_cast(fish: str, tick: float, lv: int, cast_fn,
                   cast_distance: int = CAST_DISTANCE, ctr: dict = None) -> float:
        nonlocal minigame_secs
        if ctr is not None:
            ctr["casts"] += 1

        lv_before     = natural_level
        finish_before = finish_tick

        if fish in JUNK_ITEMS:
            q, gained = do_catch(fish, tick, lv, cast_distance)
            event = "JUNK"
        elif want(fish):
            q, gained = do_catch(fish, tick, lv, cast_distance)
            diff    = FISH_DIFFICULTY.get(fish, 0)
            is_perf = diff <= perfect_threshold
            minigame_secs += (MINIGAME_PERFECT_SECS if is_perf else MINIGAME_IMPERFECT_SECS)
            if ctr is not None:
                ctr["minigames"] += 1
                if is_perf:
                    ctr["perfect"] += 1
            event = "CATCH"
        else:
            minigame_secs += SKIP_IDENTIFY_SECS
            q, gained = 0, 0.0
            event = "SKIP"

        dt, bite_s = cast_fn(lv)
        _log_cast(fish, tick, bite_s, event, q, gained)
        _log_events(lv_before, finish_before)
        return tick + dt

    # ── Phase 1a: Ocean AM (Bamboo, no soup) ─────────────────────────────
    tick = float(TICK_BEACH_START)
    ocean_am_targets = {"Sardine", "Red_Snapper", "Tilapia"}
    _log(f"[{_tick_to_time(tick)}] Phase 1a — Beach (Bamboo, no bait, natural Lv{natural_level})")
    _log(f"  Starting XP: {int(xp)} (Sunfish caught at farm pond)")

    while tick < TICK_9AM and (uncaught & ocean_am_targets):
        lv   = natural_level
        pool = _build_pool(BEACH_FISH, int(tick), lv)
        tick = track_cast(_draw_fish_sdv(pool), tick, lv, _cast_bamboo, ctr=pc["beach_am"])

    tick = max(tick, float(TICK_9AM))
    _log(f"[{_tick_to_time(float(TICK_9AM))}] Willy's — Trout Soup purchased (+1 effective level)")

    # ── Phase 1b: Extended beach (soup active) ────────────────────────────
    _log(f"[{_tick_to_time(tick)}] Phase 1b — Beach (Bamboo→Fiber*, soup,"
         f" effective Lv{natural_level + 1})")
    while tick < TICK_2PM:
        if strategy == "rush_beach":
            if "Tilapia" not in uncaught and got_fiber:
                break
        else:
            if "Tilapia" not in uncaught:
                break
        lv      = natural_level + 1
        cast_fn = _cast_fiber if got_fiber else _cast_bamboo
        pool    = _build_pool(BEACH_FISH, int(tick), lv)
        tick    = track_cast(_draw_fish_sdv(pool), tick, lv, cast_fn, ctr=pc["beach_ext"])

    _log(f"[{_tick_to_time(tick)}] Depart beach → walk to river ({TRANS_SOUP_TO_RIVER * 10} min)")
    tick += TRANS_SOUP_TO_RIVER

    # ── Phase 2a: River bamboo (skipped if Fiberglass already obtained) ───
    river_targets    = {"Shad", "Catfish", "Tiger_Trout", "Walleye"}
    fiber_from_river = False

    if not got_fiber:
        _log(f"[{_tick_to_time(tick)}] Phase 2a — River (Bamboo, no bait,"
             f" effective Lv{natural_level + 1})")
        while tick < RIVER_DEPART:
            if got_fiber:
                fiber_from_river = True
                break
            if not (uncaught & river_targets):
                break
            lv   = natural_level + 1
            pool = _build_pool(TOWN_FISH, int(tick), lv)
            tick = track_cast(_draw_fish_sdv(pool), tick, lv,
                              _cast_bamboo, RIVER_CAST_DISTANCE, ctr=pc["river_bamboo"])
    else:
        _log(f"[{_tick_to_time(tick)}] Phase 2a — skipped (Fiberglass already in hand)")

    if fiber_from_river:
        _log(f"[{_tick_to_time(tick)}] Willy's round-trip: buy Fiberglass"
             f" ({TRANS_LEVELUP_WILLY * 10} min)")
        tick += TRANS_LEVELUP_WILLY

    # ── Phase 2b: River fiberglass ────────────────────────────────────────
    if got_fiber:
        _log(f"[{_tick_to_time(tick)}] Phase 2b — River (Fiberglass+bait,"
             f" effective Lv{natural_level + 1})")
        while tick < RIVER_DEPART and (uncaught & river_targets):
            lv   = natural_level + 1
            pool = _build_pool(TOWN_FISH, int(tick), lv)
            tick = track_cast(_draw_fish_sdv(pool), tick, lv,
                              _cast_fiber, RIVER_CAST_DISTANCE, ctr=pc["river_fiber"])

    _log(f"[{_tick_to_time(tick)}] Depart river → coffee stop → beach"
         f" ({TRANS_RIVER_TO_OCEAN * 10} min)")
    tick += TRANS_RIVER_TO_OCEAN

    # ── Phase 3: Ocean PM ─────────────────────────────────────────────────
    cast_fn = _cast_fiber if got_fiber else _cast_bamboo
    rod_str = "Fiberglass+bait" if got_fiber else "Bamboo, no bait"
    ocean3  = uncaught & {"Sardine", "Red_Snapper", "Eel"}
    _log(f"[{_tick_to_time(tick)}] Phase 3 — Beach PM ({rod_str},"
         f" effective Lv{natural_level + 1})")
    if not ocean3:
        _log(f"  (no beach targets remaining — phase skipped)")

    while tick < TICK_2AM and ocean3:
        ocean_lv      = natural_level + 1
        pool          = _build_pool(BEACH_FISH, int(tick), ocean_lv)
        fish          = _draw_fish_sdv(pool)
        dt, bite_s    = cast_fn(ocean_lv)
        lv_before     = natural_level
        finish_before = finish_tick
        pc["ocean_pm"]["casts"] += 1

        if fish in JUNK_ITEMS:
            q, gained = do_catch(fish, tick, ocean_lv)
            _log_cast(fish, tick, bite_s, "JUNK", q, gained)
        elif want(fish):
            q, gained = do_catch(fish, tick, ocean_lv)
            ocean3.discard(fish)
            diff    = FISH_DIFFICULTY.get(fish, 0)
            is_perf = diff <= perfect_threshold
            minigame_secs += (MINIGAME_PERFECT_SECS if is_perf else MINIGAME_IMPERFECT_SECS)
            pc["ocean_pm"]["minigames"] += 1
            if is_perf:
                pc["ocean_pm"]["perfect"] += 1
            _log_cast(fish, tick, bite_s, "CATCH", q, gained)
        else:
            minigame_secs += SKIP_IDENTIFY_SECS
            _log_cast(fish, tick, bite_s, "SKIP", 0, 0.0)

        _log_events(lv_before, finish_before)
        tick += dt
        if tick >= TICK_7PM:
            ocean3 -= {"Sardine", "Red_Snapper"}

    if finish_tick is not None:
        _log(f"[{_tick_to_time(finish_tick)}] Run complete — all 8 fish caught.")
    else:
        missing = sorted(TARGET_FISH - caught)
        _log(f"[2AM] Run failed. Missing: {', '.join(m.replace('_', ' ') for m in missing)}")

    return {
        "caught":        caught,
        "got_fiber":     got_fiber,
        "levelup_tick":  levelup_tick,
        "xp":            xp,
        "minigame_secs": minigame_secs,
        "finish_tick":   finish_tick,
        "phase_stats":   pc,
    }


# ══════════════════════════════════════════════════════════════════════════════
# RUNNER
# ══════════════════════════════════════════════════════════════════════════════

def run_simulation(n: int = 100_000, perfect_threshold: int = 50) -> dict:
    _PHASES = ("beach_am", "beach_ext", "river_bamboo", "river_fiber", "ocean_pm")
    results = {}
    for strategy in ("catch_all", "rush_beach", "skip"):
        count_all           = 0
        sole_miss           = {f: 0 for f in TARGET_FISH}
        fiber_count         = 0
        levelup_ticks       = []
        finish_ticks        = []
        total_minigame_secs = 0.0
        phase_totals = {ph: {"casts": 0, "minigames": 0, "perfect": 0} for ph in _PHASES}

        for _ in range(n):
            r      = _sim_fish_day(strategy, perfect_threshold)
            caught = r["caught"]
            missed = TARGET_FISH - caught

            if not missed:
                count_all += 1
                if r["finish_tick"] is not None:
                    finish_ticks.append(r["finish_tick"])
            elif len(missed) == 1:
                sole_miss[next(iter(missed))] += 1

            if r["got_fiber"]:
                fiber_count += 1
                if r["levelup_tick"] is not None:
                    levelup_ticks.append(r["levelup_tick"])

            total_minigame_secs += r["minigame_secs"]
            for ph in _PHASES:
                for k in ("casts", "minigames", "perfect"):
                    phase_totals[ph][k] += r["phase_stats"][ph][k]

        avg_levelup = (sum(levelup_ticks) / len(levelup_ticks)) if levelup_ticks else None
        avg_finish  = (sum(finish_ticks)  / len(finish_ticks))  if finish_ticks  else None
        phase_avgs  = {ph: {k: v / n for k, v in ctr.items()}
                       for ph, ctr in phase_totals.items()}

        results[strategy] = {
            "count_all":         count_all,
            "sole_miss":         sole_miss,
            "fiber_pct":         fiber_count / n,
            "avg_levelup":       avg_levelup,
            "avg_finish":        avg_finish,
            "avg_minigame_secs": total_minigame_secs / n,
            # kept for backward compat with writeup text
            "avg_river_bamboo":  phase_avgs["river_bamboo"]["casts"],
            "avg_river_fiber":   phase_avgs["river_fiber"]["casts"],
            "phase_avgs":        phase_avgs,
        }

    results["n"] = n
    return results


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _tick_to_time(t: float) -> str:
    tick = int(t)
    hour   = 6 + tick // 6
    minute = (tick % 6) * 10
    if hour >= 24:
        hour -= 24
    suffix = "AM" if hour < 12 else "PM"
    h12    = hour if hour <= 12 else hour - 12
    if h12 == 0:
        h12 = 12
    return f"{h12}:{minute:02d}{suffix}" if minute else f"{h12}{suffix}"


def _avg_cast_secs(level: int, fiber: bool) -> float:
    max_raw = 30.0 - 0.25 * level
    if fiber:
        avg_bite = (0.6 + max_raw) / 2 * 0.75 * 0.5
        overhead = FIBER_OVERHEAD_TICKS
    else:
        avg_bite = (0.6 + max_raw) / 2 * 0.75
        overhead = BAMBOO_OVERHEAD_TICKS
    return (max(0.5, avg_bite) / SECS_PER_TICK + overhead) * SECS_PER_TICK


def _windows_str(windows: list) -> str:
    return ", ".join(f"{_tick_to_time(s)}–{_tick_to_time(e)}" for s, e in windows)


# ══════════════════════════════════════════════════════════════════════════════
# WRITEUP
# ══════════════════════════════════════════════════════════════════════════════

_PHASE_LABELS = [
    ("beach_am",     "Beach 7–9AM"),
    ("beach_ext",    "Beach 9AM–2PM"),
    ("river_bamboo", "River (bamboo)"),
    ("river_fiber",  "River (fiberglass)"),
    ("ocean_pm",     "Ocean 4PM–2AM"),
]


def _phase_tables(stats: dict) -> str:
    """Return two markdown tables: avg casts per phase, and perfection fraction."""
    strats = [("rush_beach", "Rush at beach"), ("catch_all", "Rush lvl 2"), ("skip", "Skip")]

    def _fmt_casts(ph, s_key):
        v = stats[s_key]["phase_avgs"][ph]["casts"]
        return f"{v:.1f}" if v >= 0.05 else "—"

    def _fmt_perf(ph, s_key):
        mg = stats[s_key]["phase_avgs"][ph]["minigames"]
        pf = stats[s_key]["phase_avgs"][ph]["perfect"]
        if mg < 0.05:
            return "—"
        return f"{pf/mg:.0%}"

    header = "| Phase | " + " | ".join(lbl for _, lbl in strats) + " |"
    sep    = "|---|" + "---|" * len(strats)

    # Table 1: average casts per phase
    rows1 = [header, sep]
    for ph, ph_lbl in _PHASE_LABELS:
        cells = " | ".join(_fmt_casts(ph, sk) for sk, _ in strats)
        rows1.append(f"| {ph_lbl} | {cells} |")
    totals = []
    for sk, _ in strats:
        t = sum(stats[sk]["phase_avgs"][ph]["casts"] for ph, _ in _PHASE_LABELS)
        totals.append(f"**{t:.1f}**")
    rows1.append("| **Total** | " + " | ".join(totals) + " |")

    # Table 2: perfection fraction
    rows2 = [header, sep]
    for ph, ph_lbl in _PHASE_LABELS:
        cells = " | ".join(_fmt_perf(ph, sk) for sk, _ in strats)
        rows2.append(f"| {ph_lbl} | {cells} |")
    # Overall perfect fraction
    overall = []
    for sk, _ in strats:
        total_mg = sum(stats[sk]["phase_avgs"][ph]["minigames"] for ph, _ in _PHASE_LABELS)
        total_pf = sum(stats[sk]["phase_avgs"][ph]["perfect"]   for ph, _ in _PHASE_LABELS)
        overall.append("—" if total_mg < 0.05 else f"{total_pf/total_mg:.0%}")
    rows2.append("| **Overall** | " + " | ".join(overall) + " |")

    return (
        "## Catches per Phase\n\n"
        "Average casts per phase per day (including junk; all strategies):\n\n"
        + "\n".join(rows1) + "\n\n"
        "Fraction of minigames that were perfect catches (difficulty ≤ 50):\n\n"
        + "\n".join(rows2)
    )


def generate_writeup(stats: dict) -> str:
    n    = stats["n"]
    ca   = stats["catch_all"]
    rb   = stats["rush_beach"]
    sk   = stats["skip"]

    def pct(x): return f"{x/n:.1%}"
    def pp(x):  return f"{x:.1%}"

    p_ca = ca["count_all"] / n
    p_rb = rb["count_all"] / n
    p_sk = sk["count_all"] / n

    lines = [
        "# Fall Fish Day — CC% Route Analysis",
        "(TheHaboo, SDV 1.6, Forest Farm, Remixed Mines, Year 1)",
        "",
        "---",
        "",
        "## Rush Fishing Level 2 at the Beach",
        "",
        "Fall fish day requires catching 8 specific fish across 3 locations on a single rainy day.",
        "The run-killer is the river phase: Tiger Trout and Walleye have low catch weights and",
        "narrow time windows, so the number of fast Fiberglass Rod casts you get at the river",
        "is the primary lever on success probability.",
        "",
        "The Fiberglass Rod requires fishing level 2 and is purchased from Willy, who is on the",
        "beach. Levelling up at the beach costs nothing — Willy's shop is right there. Levelling",
        "up at the river costs a 60-game-minute round trip (~7 minutes real time).",
        "",
        "Three strategies, all catching non-selectively pre-Lv2 for max XP:",
        "",
        f"**Rush lvl 2 at beach** — Fish non-selectively at the beach until Tilapia AND Lv2 are",
        f"both achieved, buying the Fiberglass Rod for free on the way out. River fishing starts",
        f"with fiber rod already in hand: avg {rb['avg_river_fiber']:.0f} fiber casts at river,",
        f"0 bamboo casts. P(all 8 fish) = **{pp(p_rb)}**.",
        "",
        f"**Rush lvl 2** — Same aggressive beach fishing, but departs for the river as soon as",
        f"Tilapia is caught, using the bamboo rod until levelling up mid-river. The Willy round",
        f"trip eats into fiber-rod time: avg {ca['avg_river_bamboo']:.0f} bamboo + {ca['avg_river_fiber']:.0f} fiber casts at river.",
        f"P(all 8 fish) = **{pp(p_ca)}** (–{pp(p_rb - p_ca)} vs rush at beach).",
        "",
        f"**Skip non-targets** — Cast only for target fish throughout; almost never reaches Lv2",
        f"({pp(sk['fiber_pct'])} of runs) and fishes the Eel phase with the slow bamboo rod.",
        f"Saves ~{sk['avg_minigame_secs']:.0f}s of minigame time per day but Tiger Trout and",
        f"Walleye kill runs at similar rates to the rush strategies.",
        f"P(all 8 fish) = **{pp(p_sk)}** (–{pp(p_rb - p_sk)} vs rush at beach).",
        "",
        "**Perfect catches matter for the XP model.** The ×2.4 XP multiplier on fish with",
        "difficulty ≤ 50 (Tilapia, Shad, Walleye, etc.) is what makes Lv2 achievable at the",
        "beach. If the runner isn't consistently clearing the minigame perfectly, level-up timing",
        "shifts later and the Lv2-at-beach guarantee weakens — see the ≤30/no-perfect rows",
        "in the comparison table above.",
        "",
        "**Strategic considerations:**",
        "- Run pacing well → prefer **rush lvl 2 at beach**: the risk-averse play that locks in",
        f"  a {pp(p_rb)} success rate at a cost of only ~{rb['avg_minigame_secs'] - sk['avg_minigame_secs']:.0f}s extra",
        "  minigame time per day compared to skipping.",
        "- Run pacing poorly → consider **skip non-targets**: save ~40s per reset to make more",
        "  attempts, accepting the lower per-day probability.",
        "- **Rush lvl 2** (no beach guarantee) is dominated by rush at beach: same time cost,",
        f"  lower success rate. Only prefer it if you're already Lv2 before Tilapia.",
        "",
        "---",
        "",
        f"| Strategy | P(all 8 fish) | Got Fiberglass | Minigame s/day | Avg level-up |",
        f"|---|---|---|---|---|",
    ]

    _pool = {"catch_all": ca, "rush_beach": rb, "skip": sk}
    for strategy, disp in STRATEGY_DISPLAY:
        s  = _pool[strategy]
        lu = _tick_to_time(s["avg_levelup"]) if s["avg_levelup"] else "never"
        p  = s["count_all"] / n
        lines.append(
            f"| {disp} | **{pp(p)}** | {pp(s['fiber_pct'])} | {s['avg_minigame_secs']:.0f}s | {lu} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Where Runs Die",
        "",
        "Days where that fish was the sole reason the run failed:",
        "",
        "**Rush lvl 2 at beach**",
        "```",
    ]

    ranked_rb = sorted(rb["sole_miss"].items(), key=lambda kv: kv[1], reverse=True)
    for fish, cnt in ranked_rb:
        bar = "█" * int(cnt / n * 40)
        lines.append(f"  {fish.replace('_',' '):<16}  {pct(cnt):<8}  {bar}")

    lines += [
        "```",
        "",
        "**Rush lvl 2**",
        "```",
    ]

    ranked_ca = sorted(ca["sole_miss"].items(), key=lambda kv: kv[1], reverse=True)
    for fish, cnt in ranked_ca:
        bar = "█" * int(cnt / n * 40)
        lines.append(f"  {fish.replace('_',' '):<16}  {pct(cnt):<8}  {bar}")

    lines += [
        "```",
        "",
        "**Skip non-targets**",
        "```",
    ]

    ranked_sk = sorted(sk["sole_miss"].items(), key=lambda kv: kv[1], reverse=True)
    for fish, cnt in ranked_sk:
        bar = "█" * int(cnt / n * 40)
        lines.append(f"  {fish.replace('_',' '):<16}  {pct(cnt):<8}  {bar}")

    lines += [
        "```",
        "",
        "---",
        "",
        _phase_tables(stats),
        "",
        "---",
        "",
        "## How the Day Is Routed",
        "",
        "One real second ≈ 1.4 in-game minutes. One tick = 10 in-game minutes = 7 real seconds.",
        "",
        f"**Phase 1a — Beach, 7AM–9AM** (Bamboo Rod, no bait, Lv{LEVEL_OCEAN_AM})",
        f"  Targets: Sardine, Red Snapper, Tilapia",
        f"  Avg cast: {_avg_cast_secs(LEVEL_OCEAN_AM, False):.1f}s (~20 game-min)",
        f"  Sunfish caught at farm pond first (Training Rod, guaranteed); arrive beach 7AM.",
        "",
        f"  **9AM — Willy's for Trout Soup** (+1 effective fishing level)",
        "",
        f"**Phase 1b — Beach, 9AM–2PM** (Bamboo or Fiberglass*, Lv{LEVEL_BAMBOO_RIVER}*)",
        f"  Rush at beach: stay until Tilapia caught AND Lv2 reached; buy rod free at Willy's.",
        f"  Rush lvl 2:    depart as soon as Tilapia is caught (or 2PM if Tilapia not found).",
        f"  Skip:          depart as soon as Tilapia is caught.",
        f"  Avg cast (Bamboo Lv{LEVEL_BAMBOO_RIVER}): {_avg_cast_secs(LEVEL_BAMBOO_RIVER, False):.1f}s",
        "",
        f"  **Walk to river: 30 game-min ({TRANS_SOUP_TO_RIVER} ticks)**",
        "",
        f"**Phase 2a — River bamboo** (Bamboo Rod, no bait, Lv{LEVEL_BAMBOO_RIVER}*)",
        f"  Skipped entirely if Fiberglass already obtained (rush at beach).",
        f"  Rush lvl 2 avg: {ca['avg_river_bamboo']:.0f} bamboo casts here before levelling up.",
        f"  Skip avg: {sk['avg_river_bamboo']:.0f} bamboo casts (targets only; rarely hits Lv2).",
        "",
        f"  **Level 2 at river → Willy's round-trip: 60 game-min ({TRANS_LEVELUP_WILLY} ticks)**",
        "",
        f"**Phase 2b — River fiberglass** (Fiberglass Rod, bait, Lv{LEVEL_FIBER_RIVER}*)",
        f"  Avg cast: {_avg_cast_secs(LEVEL_FIBER_RIVER, True):.1f}s (~10 game-min, WR observed exactly 10)",
        f"  Rush at beach avg: {rb['avg_river_fiber']:.0f} fiber casts | Rush lvl 2 avg: {ca['avg_river_fiber']:.0f} | Skip: {sk['avg_river_fiber']:.0f}",
        f"  Fish remaining river targets until caught or 3PM departure.",
        "",
        f"  **Leave river → coffee stop → beach: 60 game-min ({TRANS_RIVER_TO_OCEAN} ticks)**",
        "",
        f"**Phase 3 — Beach, 4PM–2AM** (Fiberglass or Bamboo*, Lv{LEVEL_OCEAN_PM})",
        f"  Targets: Eel (4PM–2AM, rain only); Sardine + Red Snapper until 7PM if missed earlier.",
        f"  Rush strategies: Fiberglass in {pp(rb['fiber_pct'])}/{pp(ca['fiber_pct'])} of runs → avg {_avg_cast_secs(LEVEL_OCEAN_PM, True):.1f}s/cast",
        f"  Skip: Fiberglass in {pp(sk['fiber_pct'])} of runs; Bamboo in remaining → avg {_avg_cast_secs(LEVEL_BAMBOO_RIVER, False):.1f}s/cast",
        "",
        "  * effective level = natural level + Trout Soup (+1)",
        "",
        "---",
        "",
        "## Assumptions in Plain English",
        "",
        "### Timing",
        "",
        "All timings from TheHaboo's world record run.",
        "",
        "- **7AM beach start.** Sunfish caught at farm pond (guaranteed via Training Rod), then walk to beach.",
        "- **9AM Willy's visit.** Buys Trout Soup (+1 fishing). Willy's is on the beach; no travel cost.",
        "- **Extended Tilapia window.** If Tilapia not caught by 9AM, continue at beach until it appears",
        "  or 2PM (when Tilapia's window closes). Sardine and Red Snapper caught opportunistically.",
        "- **River arrival.** 30-min walk from beach after leaving. Worst case: depart 2PM → arrive 2:30PM.",
        "- **Level-up at river → 60-min round trip to Willy's.** Only if rod not already obtained.",
        "- **River departure: 3PM.** 60-min walk to beach (includes coffee purchase). Beach 4PM.",
        "",
        "### Bite Time and Rod Mechanics",
        "",
        "Two cast functions fitted to WR observed real-time timestamps (n=14 casts):",
        "```",
        f"  Bamboo Pole (no bait):   bite = U(0.6, 30−0.25×level) × 0.75",
        f"    0.75 first-cast bonus universal (FishingRod.cs line 427; WR n=14 consistent)",
        f"    + {BAMBOO_OVERHEAD_TICKS:.1f} tick overhead (cast animation + pickup)",
        f"    Level {LEVEL_BAMBOO_RIVER}: avg {_avg_cast_secs(LEVEL_BAMBOO_RIVER, False):.1f}s per cast (~20 game-min)",
        "",
        f"  Fiberglass Rod + bait:   bite = U(0.6, 30−0.25×level) × 0.75 × 0.5",
        f"    + {FIBER_OVERHEAD_TICKS:.1f} tick overhead",
        f"    Level {LEVEL_FIBER_RIVER}: avg {_avg_cast_secs(LEVEL_FIBER_RIVER, True):.1f}s per cast (~10 game-min, WR observed exactly 10)",
        "```",
        "Cast distance does not affect bite time (confirmed: GameLocation.calculateTimeUntilFishingBite",
        "uses only fishing level, tackle, and bait — bobberTile checked only for fish ponds).",
        "Game clock is frozen during the fishing minigame; only bite wait advances the clock.",
        "",
        "### XP and Level-Up",
        "",
        "XP formula (FishingRod.cs doPullFishFromWater lines 1091-1104):",
        "  base_xp = floor((quality+1)×3 + difficulty/3)   [pre-boost quality]",
        "  if perfect: xp = base_xp + floor(base_xp × 1.4)   [≈ ×2.4 total]",
        "  Quality from fishSize = (depth/5) × (Skill+2)/10 × Random/100",
        "    depth: ocean=5, river=3 | Skill ~ U(even from floor_even(level) to 10)",
        "    fishSize < 0.33 → normal (0); 0.33–<0.66 → silver (1); ≥0.66 → gold (2)",
        "  Perfect catch assumed for difficulty ≤ 50. XP uses pre-boost quality.",
        "  Normal-quality fish (quality=0) do not receive an inventory quality boost on perfect",
        "  catch (FishingRod.cs lines 1077-1084: boost only if quality >= 1), but still earn ×2.4 XP.",
        f"  Starting XP: {int(_fish_xp('Sunfish', 0, True))} from Sunfish (Training Rod → quality always normal).",
        "",
        "Expected XP per fish by phase (quality distribution from fishSize formula):",
        "```",
    ]

    relevant = sorted(FISH_DIFFICULTY.items(), key=lambda kv: kv[1], reverse=True)
    lines.append(f"  {'Fish':<18}  {'diff':>4}  {'Lv1 beach':>9}  {'Lv2 river':>9}  {'Lv3 ocean':>9}")
    for name, diff in relevant:
        perfect_mark = "*" if diff <= 50 else ""
        if name == "Sunfish":
            xp0 = int(_fish_xp(name, 0, True))
            lines.append(f"  {(name.replace('_',' ') + perfect_mark):<18}  {diff:4d}  {'':>9}  {'':>9}  {'':>9}  → {xp0} XP (Training Rod, always normal quality)")
        else:
            x1 = _expected_xp(name, LEVEL_OCEAN_AM)
            x2 = _expected_xp(name, LEVEL_BAMBOO_RIVER, RIVER_CAST_DISTANCE)
            x3 = _expected_xp(name, LEVEL_OCEAN_PM)
            lines.append(f"  {(name.replace('_',' ') + perfect_mark):<18}  {diff:4d}  {x1:9.1f}  {x2:9.1f}  {x3:9.1f}")

    lines += [
        "  * = perfect catch assumed (difficulty ≤ 50)",
        "```",
        f"SDV fishing XP thresholds (cumulative): Lv1={XP_THRESHOLDS[1]}, Lv2={XP_THRESHOLDS[2]}, Lv3={XP_THRESHOLDS[3]}",
        "",
        "**catch_all / rush_beach** catch Smallmouth Bass, Salmon, Bream, etc. for XP pre-Lv2,",
        "accelerating the level-up. **skip** only catches target fish — non-target casts cost",
        "the same game-clock time (bite wait) but yield 0 XP.",
        "",
        "### Fish Pools and Catch Weights",
        "",
        "Rainy Fall day, SDV 1.6 game data (GameLocation.cs lines 13950-13961).",
        "Catch weight formula: chance = baseRate − max(0, maxDepth−depth)×depthMult×baseRate + level/50",
        "  capped at 0.90. Ocean depth=5 (no penalties); river depth=3 (Catfish penalty: −0.04).",
        "```",
        f"Phase 1 — Beach AM (depth 5, Lv{LEVEL_OCEAN_AM}):",
    ]

    def overlaps(windows, ps, pe):
        return any(ws < pe and we > ps for ws, we in windows)

    for name, base, windows in BEACH_FISH:
        if not overlaps(windows, TICK_BEACH_START, TICK_9_10AM): continue
        w   = min(0.90, base + 0.02 * LEVEL_OCEAN_AM)
        tag = "  ← target" if name in TARGET_FISH else ""
        lines.append(f"  {name.replace('_',' '):<18} {w:.2f}  {_windows_str(windows)}{tag}")

    lines += ["", f"Phase 2 — River (depth 3, Lv{LEVEL_BAMBOO_RIVER} bamboo / Lv{LEVEL_FIBER_RIVER} fiber):"]
    for name, base, windows in TOWN_FISH:
        if not overlaps(windows, TICK_9AM + TRANS_SOUP_TO_RIVER, RIVER_DEPART): continue
        w2 = min(0.90, base + 0.02 * LEVEL_BAMBOO_RIVER)
        w3 = min(0.90, base + 0.02 * LEVEL_FIBER_RIVER)
        tag = "  ← target" if name in TARGET_FISH else ""
        lines.append(f"  {name.replace('_',' '):<18} {w2:.2f}/{w3:.2f}  {_windows_str(windows)}{tag}")

    lines += ["", f"Phase 3 — Beach PM (depth 5, Lv{LEVEL_OCEAN_PM}):"]
    for name, base, windows in BEACH_FISH:
        if not overlaps(windows, RIVER_DEPART + TRANS_RIVER_TO_OCEAN, TICK_2AM): continue
        w   = min(0.90, base + 0.02 * LEVEL_OCEAN_PM)
        tag = "  ← target" if name in TARGET_FISH else ""
        lines.append(f"  {name.replace('_',' '):<18} {w:.2f}  {_windows_str(windows)}{tag}")

    lines += [
        "```",
        "",
        "### The Catch Algorithm",
        "",
        "Each cast: shuffle the eligible fish list, roll each fish independently against its",
        "weight, catch the first one that passes. Not a proportional draw — any fish can win",
        "if it draws position #1 in the shuffle, regardless of weight.",
        "",
        "### What This Model Doesn't Include",
        "",
        "- **Fishing bubbles.** Halve bite time. Not modelled; makes simulation slightly pessimistic.",
        "- **No escapes.** Assumes the runner clears the minigame on every cast.",
    ]

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

PERFECT_CONFIGS = [
    ("Perfect ≤50", 50),
    ("Perfect ≤30", 30),
    ("No perfect",  -1),
]


STRATEGY_DISPLAY = [
    ("rush_beach", "Rush lvl 2 at beach"),
    ("catch_all",  "Rush lvl 2"),
    ("skip",       "Skip non-targets"),
]


def _comparison_table(all_stats: dict, n: int) -> str:
    col_labels = [label for label, _ in PERFECT_CONFIGS]
    w = 21  # strategy column width

    def row(label, cells):
        return "| " + f"{label:<{w}}" + " | " + " | ".join(f"{c:<13}" for c in cells) + " |"

    divider = "|" + "-" * (w + 2) + "|" + "|".join("-" * 15 for _ in col_labels) + "|"
    header  = row("Strategy", col_labels)

    lines = [
        "## Comparison — Perfect Catch Threshold",
        "",
        "P(all 8 fish caught) on a single rainy Fall day attempt.",
        "",
        header,
        divider,
    ]
    for strategy, label in STRATEGY_DISPLAY:
        cells = []
        for col_label, _ in PERFECT_CONFIGS:
            s = all_stats[col_label][strategy]
            p = s["count_all"] / n
            cells.append(f"**{p:.1%}**")
        lines.append(row(label, cells))

    lines += [
        "",
        "Average finish time (successful runs only) and real-world minigame time per day:",
        f"  Perfect catch: {MINIGAME_PERFECT_SECS:.1f}s/fish | Non-perfect: {MINIGAME_IMPERFECT_SECS:.1f}s/fish | Skip identify: {SKIP_IDENTIFY_SECS:.1f}s",
        "",
        row("Strategy (≤50 threshold)", ["Avg finish", "Minigame s/day", "vs Skip"]),
        "|" + "-" * (w + 2) + "|" + "-" * 15 + "|" + "-" * 15 + "|" + "-" * 15 + "|",
    ]
    skip_mg = all_stats["Perfect ≤50"]["skip"]["avg_minigame_secs"]
    for strategy, label in STRATEGY_DISPLAY:
        s     = all_stats["Perfect ≤50"][strategy]
        mg    = s["avg_minigame_secs"]
        ft    = _tick_to_time(s["avg_finish"]) if s["avg_finish"] else "n/a"
        delta = mg - skip_mg
        sign  = "+" if delta >= 0 else ""
        lines.append(row(label, [ft, f"{mg:.0f}s", f"{sign}{delta:.0f}s"]))

    return "\n".join(lines)


def _run_sample_days(perfect_threshold: int = 50, seeds: tuple = (0, 1, 2)) -> str:
    """
    Run one day per strategy with verbose logging and return a markdown section.
    Each strategy uses a fixed seed for reproducibility; seeds=(rush_beach, catch_all, skip).
    """
    _STRAT_SEEDS = list(zip(
        [s for s, _ in STRATEGY_DISPLAY],
        [l for _, l in STRATEGY_DISPLAY],
        seeds,
    ))

    sections = [
        "## Sample Day Logs (perfect catch threshold ≤50)",
        "",
        "One randomly sampled day per strategy. Seed per strategy: "
        + ", ".join(f"{lbl}={seed}" for _, lbl, seed in _STRAT_SEEDS) + ".",
        "",
        "Column layout:",
        "```",
        "  [time]   bite_s  Fish name             event  quality  XP  flags  [cumulative XP / level]",
        "```",
        "Events: CATCH = minigame played and won | SKIP = minigame declined | JUNK = auto-received",
        "",
    ]

    for strategy, disp, seed in _STRAT_SEEDS:
        random.seed(seed)
        log: list[str] = []
        r = _sim_fish_day(strategy, perfect_threshold, log=log)
        caught  = r["caught"]
        outcome = "SUCCESS" if not (TARGET_FISH - caught) else "FAILED"
        sections += [
            f"### {disp} (seed={seed}) — {outcome}",
            "```",
        ] + log + [
            "```",
            "",
        ]

    return "\n".join(sections)


def main():
    n = 100_000
    all_stats = {}
    for label, threshold in PERFECT_CONFIGS:
        print(f"Running: {label} ({n:,} iterations × 3 strategies)...", file=sys.stderr)
        stats = run_simulation(n=n, perfect_threshold=threshold)
        all_stats[label] = stats
        for strategy, disp in STRATEGY_DISPLAY:
            s  = stats[strategy]
            p  = s["count_all"] / n
            lu = _tick_to_time(s["avg_levelup"]) if s["avg_levelup"] else "never"
            ft = _tick_to_time(s["avg_finish"])  if s["avg_finish"]  else "n/a"
            print(f"  {disp:<22}  P={p:.1%}  fiber={s['fiber_pct']:.1%}  "
                  f"minigame={s['avg_minigame_secs']:.0f}s/day  finish={ft}  levelup={lu}",
                  file=sys.stderr)

    table    = _comparison_table(all_stats, n)
    writeup  = generate_writeup(all_stats["Perfect ≤50"])
    print("Generating sample day logs...", file=sys.stderr)
    sample   = _run_sample_days()
    output   = table + "\n\n---\n\n" + writeup + "\n\n---\n\n" + sample
    print(output)
    with open("fish_day_analysis.md", "w") as f:
        f.write(output)
    print("\nSaved to fish_day_analysis.md", file=sys.stderr)


if __name__ == "__main__":
    main()
