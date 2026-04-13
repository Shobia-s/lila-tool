# Insights

---

## Insight 1: Cave House is the Deadliest Zone on AmbroseValley

**What I noticed:**
When filtering for AmbroseValley matches and enabling the Kill heatmap, a dense red cluster consistently appears around the Cave House area in the upper-center of the map. This happens across multiple days and matches — it is not a one-match anomaly.

**Evidence:**
Across Feb 10–14, the majority of Kill and Killed events on AmbroseValley are concentrated within a small radius around Cave House. The heatmap shows this area glowing significantly brighter than Labour Quarters, Engineer's Quarters, or Gas Station. Bot kills in this area are also high, suggesting bots are routing through the same chokepoint.

**Actionable items:**
- The Cave House area may be over-tuned as a conflict zone — too much loot, too narrow pathways, or too central a routing point
- Metrics to watch: Kill density per square unit (Cave House vs other named zones), average player survival time for players who pass through Cave House vs those who avoid it
- Level design action: Consider widening approach paths into Cave House, reducing loot tier to make it less of a magnet, or adding alternate routing options so players are not funneled into a single kill zone

**Why a level designer should care:**
A single dominant kill zone means matches become predictable. Players learn to either camp Cave House or avoid it entirely, reducing the variety of match experiences. Spreading combat more evenly across the map leads to richer, more replayable sessions.

---

## Insight 2: Large Areas of All Three Maps Are Almost Never Visited

**What I noticed:**
When enabling Human Paths across multiple matches on any map, the paths cluster heavily around 30–40% of the map area. The outer edges — particularly the bottom-left of AmbroseValley, the far west of GrandRift, and the southern reaches of Lockdown — show almost no path lines or event markers at all.

**Evidence:**
Filtering for any full day of matches and viewing positions across all matches, the dead zones are visually obvious — large sections of the minimap have zero blue lines and zero event markers across hundreds of matches. The Burnt Zone on AmbroseValley appears in the UI label but generates almost no player traffic.

**Actionable items:**
- Dead zones are wasted art and level design budget — no players are experiencing that content
- Metrics to watch: % of map area with at least one player position event per match, average number of unique grid cells visited per match
- Level design action: Either add loot incentives or objectives to draw players into neglected zones, or redesign the storm path to push players through those areas naturally. Alternatively, consider shrinking the map boundary so these dead zones are eliminated entirely

**Why a level designer should care:**
If large map sections never see play, the studio is spending resources on content no one experiences. Addressing dead zones either improves content ROI or helps resize maps to create denser, more intense match experiences.

---

## Insight 3: Storm Deaths Are Rare — Players Are Extracting or Getting Killed First

**What I noticed:**
Across all matches and maps, KilledByStorm events are very infrequent compared to Kill and Killed events. The purple storm death markers on the map are sparse even in matches with high overall death counts.

**Evidence:**
In the match stats panel, Storm Deaths consistently show 0 or 1 across most matches, while Kill counts are in the range of 5–15 for the same matches. This pattern holds across all three maps and all five days of data.

**Actionable items:**
- The storm may not be creating enough pressure — if players are rarely dying to it, it is not effectively forcing movement or driving urgency
- Metrics to watch: Storm death rate as % of total deaths per match, average player distance from storm boundary at match end, time-to-first-storm-death per match
- Level design action: Consider accelerating the storm speed in the mid-game phase, reducing the storm warning time, or tightening the final storm circle to force more end-game confrontations. The storm should feel like a constant threat, not a background mechanic

**Why a level designer should care:**
In extraction shooters, the storm (or equivalent zone mechanic) is the primary tool for controlling pacing and forcing player engagement. If it has no teeth, matches can stagnate — players camp indefinitely rather than moving and fighting. A more aggressive storm creates more dynamic, exciting matches.
