# Cacti, mazes, and dinosaurs

These are ordinary resource farms. Each file runs on its own, and none needs the DLC.

Before switching crops, stop the previous program and let its drones disappear. The cactus and maze programs choose their drone count from the unlocked limit. With no Mega Farm research, they run on the original drone. They do not need a separate version for 4, 8, 16, or 32 drones.

## Pick a script

| File | Use it for | Extra requirements |
| --- | --- | --- |
| [cactus_cached.py](../scripts/04_special_farms/cactus_cached.py) | The main cactus farm | Cactus, Carrots for tilling, Lists |
| [cactus_bubble.py](../scripts/04_special_farms/cactus_bubble.py) | A more straightforward cactus sorting alternative | Cactus, Carrots for tilling, Lists |
| [maze_stations.py](../scripts/04_special_farms/maze_stations.py) | Reusing mapped mazes for gold | Mazes, Lists, Dictionaries |
| [dinosaur_cycle.py](../scripts/04_special_farms/dinosaur_cycle.py) | Faster early growth using shortcuts | Dinosaurs, Hats with the Gold Hat, Lists |
| [dinosaur_safe.py](../scripts/04_special_farms/dinosaur_safe.py) | A conservative cycle with less bookkeeping | Dinosaurs, Hats with the Gold Hat |

All five also use Loops, Variables, Operators, Functions, Senses, the `if` features from Speed, and the `for` / `get_world_size()` features from the second expansion. Cactus and maze files also need Plant. There is no requirement for Import, Utilities, Timing, Simulation, Watering, or Mega Farm. Unlock the language features before pasting an advanced file: a run-time crop check cannot make locked syntax available.

## Cactus: cache first, sort second

Use `cactus_cached` as the default. Each worker plants and measures its rows once. It repairs nearby inversions from that cache, then searches for the nearest part of the row that still needs work. After a barrier, workers sort the columns using the collected row values. Every column is checked for maturity before the final field harvest.

`cactus_bubble` keeps the older approach: compare adjacent plants, move along the line, and shorten the next pass to the last swap. It is easier to trace, but it usually spends more time moving and measuring. It remains useful as a readable reference and a fallback for comparing changes.

Both scripts accept an existing cactus field, replace other crops, and prepare soil where needed. Keep enough pumpkins for the missing plants. If a planting fails, the current job stops after joining its helpers; it does not keep flying around an empty field. Neither script waters plants or tries to force a smaller world size.

Rows are sorted before columns. Sorting the columns of a row-sorted matrix preserves the row order, which is what makes a full-field chain harvest possible. The scripts never swap across the outer boundary, even though ordinary travel may wrap around it.

Do not replace sorting with repeated immature harvesting and planting. The cactus keeps its size through those attempts. That approach can consume pumpkins forever without producing a usable field.

## Maze: build a map once, then reuse it

`maze_stations` spends Weird Substance to turn a bush into a full-field maze. The amount is calculated from the field size and current maze level; it is not a fixed stock number copied from an earlier save.

On a fresh maze, available drones split the initial exploration. The finished map is used to choose spread-out waiting positions and assign each tile to one station. A worker goes to treasure in its assigned region, reuses the treasure while resources and reuse limits allow it, and otherwise returns to its station. Newly opened passages improve that worker's routes.

The assignment is shared and stays fixed for that maze. This prevents two workers from deciding that the same treasure belongs to them. It chooses a nearby waiting station, not necessarily the drone closest to the treasure at that exact instant.

The program reuses a fresh maze up to 300 times, then harvests the final treasure. With a smaller supply, it takes the final treasure earlier. An existing maze is mapped by one drone and harvested once before the program starts a new one; this avoids treating an already reused, cyclic maze as a fresh tree.

Run it with a full-field maze or ordinary farmland. It replaces the crop under the drone when creating a new maze. Do not run another program that spends Weird Substance at the same time: the reuse count is inferred from that shared inventory. It stops when it cannot afford another maze.

## Dinosaur: choose speed or a simpler safety argument

Both dinosaur files collect a previous tail by changing hats, then **clear the farm before each new run**. Do not start either file while you want to keep the current crops. They use one drone because the game provides one dinosaur hat.

On an even square, `dinosaur_safe` follows a fixed cycle through every cell without crossing the boundary. It does not chase apples directly. This costs more travel early on, but the head follows the same order as the tail, so it can grow until the field fills, provided there is enough cactus for the apples. No Lists research is needed.

`dinosaur_cycle` precomputes that cycle and a set of possible shortcuts. It takes shortcuts during early growth, keeps a tail buffer, and switches to the simple cycle once the body has become contiguous along it. This is the version used for the later farm. The shortcut margin is a heuristic: unusual apple sequences can still block it before the field fills. In that case it collects the partial tail and starts again. Use the conservative version if that tradeoff is unwelcome.

A full cycle without wrapping cannot cover an odd square. For odd sizes, both files use a serpentine path, collect the resulting partial tail, and restart. This supports those fields without changing their size, but it is a lower-yield fallback rather than a promise to fill the board. Fields smaller than 2×2 are left alone.

Keep a cactus reserve. If apples cannot be purchased, the programs collect the tail they already have and stop when no more progress is possible. Power remains useful for ordinary execution speed; neither file farms its own input resources.

## What has been checked

The source algorithms were checked with separate API models for sortedness, line coverage, maturity, worker ownership, spawn failures, and selected dinosaur apple sequences. Those checks are useful for regressions, but they are not the game interpreter and their timing estimates are not published as game speedups.

The public copies remove the old 32-drone cap, guard drone APIs when Mega Farm is absent, and add the odd-size dinosaur fallback. These adaptations still need normal in-game observation on a player's own research levels. There is no claim that any of these algorithms is globally optimal.
