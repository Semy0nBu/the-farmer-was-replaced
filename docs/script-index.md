# Script index

Choose by unlocked features, not just by crop. Requirements are cumulative within each entry: a script listing Lists and Functions needs both. Mega Farm is optional for the scalable advanced scripts; the initial rectangular expansion uses the separate column scripts.

Each file runs on its own. See the linked guide for the algorithm and limits.

## First steps

[Guide](early-game.md)

### First harvest

[harvest_once.py](../scripts/01_first_steps/harvest_once.py)

Harvest the starting plot once before loops are unlocked.

- **Requires:** No research.
- **Start:** An ordinary grass plot ready for harvest.

### Hay before the first speed upgrade

[hay_loop.py](../scripts/01_first_steps/hay_loop.py)

Repeat harvesting before maturity checks are available.

- **Requires:** Loops.
- **Start:** Starting grass plot, before the first Speed upgrade.

### Hay with maturity checks

[hay_ready.py](../scripts/01_first_steps/hay_ready.py)

Harvest mature grass on the original plot.

- **Requires:** Loops, Speed.
- **Start:** A single Grassland plot growing grass.

### Hay on the first column

[hay_column.py](../scripts/01_first_steps/hay_column.py)

Visit every plot on a narrow starting field.

- **Requires:** Loops, Speed, Expand (first column).
- **Start:** A one-column grass field, including the first 1x3 expansion.

### Wood on one plot

[bush_plot.py](../scripts/01_first_steps/bush_plot.py)

Harvest and replant bushes without sensors.

- **Requires:** Loops, Speed, Plant.
- **Start:** The original Grassland or Soil plot, with grass or a bush.

### Wood on the first column

[bush_column.py](../scripts/01_first_steps/bush_column.py)

Grow bushes along the narrow starting field.

- **Requires:** Loops, Speed, Plant, Expand (first column).
- **Start:** A one-column field with grass or bushes.

## Single-drone farms

[Guide](early-game.md)

### Square hay before Operators

[hay_grid.py](../scripts/02_single_drone/hay_grid.py)

Traverse a square with nested loops before arithmetic and comparisons are unlocked.

- **Requires:** Loops, Speed, Expand (square field).
- **Start:** A square Grassland field growing grass.

### Square bushes before Operators

[bush_grid.py](../scripts/02_single_drone/bush_grid.py)

Grow bushes across a square without Operators, explicit variable assignments or sensors.

- **Requires:** Loops, Speed, Expand (square field), Plant.
- **Start:** A square field with grass or bushes.

### Hay before Senses

[hay_square.py](../scripts/02_single_drone/hay_square.py)

Collect hay on a square without sensors or custom functions.

- **Requires:** Loops, Speed, Expand (square field), Operators.
- **Start:** A square Grassland field growing grass.

### Bushes before Senses

[bush_square.py](../scripts/02_single_drone/bush_square.py)

Farm wood across a square with no sensors.

- **Requires:** Loops, Speed, Expand (square field), Operators, Plant.
- **Start:** A square field with grass or bushes.

### One-time soil preparation

[prepare_soil.py](../scripts/02_single_drone/prepare_soil.py)

Till every tile once before sensor-free carrot seeding.

- **Requires:** Speed, Expand (square field), Operators, Carrots.
- **Start:** Every tile must be Grassland; run once only.

### Carrots before Senses

[carrots_no_senses.py](../scripts/02_single_drone/carrots_no_senses.py)

Seed empty soil, then harvest and replant mature carrots; stop on failed planting.

- **Requires:** Loops, Speed, Expand (square field), Operators, Variables, Plant, Carrots.
- **Start:** Empty Soil on the entire square; sufficient hay and wood. Restarting on young carrots is unsupported.

### Hay with ground repair

[hay_senses.py](../scripts/02_single_drone/hay_senses.py)

Restore Grassland, remove conflicting crops and collect mature grass.

- **Requires:** Loops, Speed, Expand (square field), Operators, Variables, Senses, Carrots.
- **Start:** An ordinary square field; other crops may be removed.

### Carrots with sensors

[carrots_senses.py](../scripts/02_single_drone/carrots_senses.py)

Maintain carrots while preserving young plants and stopping on failed planting.

- **Requires:** Loops, Speed, Expand (square field), Operators, Variables, Functions, Plant, Carrots, Senses.
- **Start:** An ordinary square field; enough hay and wood for carrots.

### Separated trees and hay

[trees_and_hay.py](../scripts/02_single_drone/trees_and_hay.py)

Grow nonadjacent trees with grass on the other tiles, including wrap-safe odd squares.

- **Requires:** Loops, Speed, Expand (square field), Operators, Variables, Functions, Plant, Trees, Carrots, Senses.
- **Start:** An ordinary square of at least 2x2; conflicting crops may be removed.

### Separated trees and bushes

[trees_and_bushes.py](../scripts/02_single_drone/trees_and_bushes.py)

Use separated trees for wood and bushes on the remaining tiles.

- **Requires:** Loops, Speed, Expand (square field), Operators, Variables, Plant, Trees, Senses.
- **Start:** An ordinary square field; conflicting crops may be removed. A 1x1 field grows a bush.

### Pumpkins without Lists

[pumpkins_scan.py](../scripts/02_single_drone/pumpkins_scan.py)

Repair dead pumpkins with full-field passes and harvest only when the whole square is ready.

- **Requires:** Loops, Speed, Expand (square field), Operators, Variables, Functions, Plant, Carrots, Senses, Pumpkins.
- **Start:** An ordinary square field and a reserve of carrots.

### Sunflowers without Lists

[sunflowers_scan.py](../scripts/02_single_drone/sunflowers_scan.py)

Harvest petal counts from 15 down to 7, keeping nine flowers when the field can hold ten.

- **Requires:** Loops, Speed, Expand (square field), Operators, Variables, Functions, Plant, Carrots, Senses, Sunflowers.
- **Start:** An ordinary square field and enough carrots to plant sunflowers.

### Fresh-maze wall follower

[maze_wall.py](../scripts/02_single_drone/maze_wall.py)

Create and solve fresh mazes without Lists, mapping or treasure relocation.

- **Requires:** Loops, Speed, Expand (square field), Operators, Variables, Functions, Plant, Senses, Mazes.
- **Start:** An ordinary field or a treasure tile, outside any existing hedge maze; sufficient Weird Substance.

### Cactus without Lists

[cactus_bubble.py](../scripts/02_single_drone/cactus_bubble.py)

Bubble-sort rows and columns, then harvest the mature field.

- **Requires:** Loops, Speed, Expand (square field), Operators, Variables, Functions, Plant, Carrots, Senses, Cactus.
- **Start:** An ordinary square field and enough pumpkins to plant cacti.

## Advanced crop farms

[Guide](advanced-farms.md)

### Hay

[hay.py](../scripts/03_advanced_farms/hay.py)

Restore grassland and harvest mature grass.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Carrots.
- **Start:** Any ordinary field.

### Carrots

[carrots.py](../scripts/03_advanced_farms/carrots.py)

Keep the field planted with carrots.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Plant, Carrots.
- **Start:** Keep hay and wood in stock.

### Weird substance

[weird_substance.py](../scripts/03_advanced_farms/weird_substance.py)

Fertilize each new carrot once to produce Weird_Substance.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Plant, Carrots, Fertilizer.
- **Start:** Keep hay, wood and fertilizer in stock.

### Trees and bushes

[tree_bush.py](../scripts/03_advanced_farms/tree_bush.py)

Grow separated trees and fill the other cells with bushes.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Plant, Trees.
- **Start:** Any ordinary field.

### Trees and hay

[tree_hay.py](../scripts/03_advanced_farms/tree_hay.py)

Share the field between wood and grass.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Plant, Trees, Carrots.
- **Start:** Any ordinary field.

### Whole-field pumpkins

[pumpkins.py](../scripts/03_advanced_farms/pumpkins.py)

Repair dead pumpkins in parallel and collect one merged field.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Plant, Carrots, Pumpkins.
- **Start:** Keep carrots in stock.

### Sunflowers

[sunflowers.py](../scripts/03_advanced_farms/sunflowers.py)

Harvest petals from high to low while preserving the bonus.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Plant, Carrots, Sunflowers.
- **Start:** A square field of at least 4 by 4; keep carrots in stock.

### Hay polyculture

[poly_hay.py](../scripts/03_advanced_farms/poly_hay.py)

Grow grass on primary cells and satisfy compatible companion requests.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Plant, Carrots, Trees, Costs, Dictionaries, Polyculture.
- **Start:** Keep hay and wood available for companion carrots.

### Wood polyculture

[poly_wood.py](../scripts/03_advanced_farms/poly_wood.py)

Grow primary trees with companions; water those trees when available.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Plant, Carrots, Trees, Costs, Dictionaries, Polyculture.
- **Start:** Keep hay and wood available for companion carrots. Watering is optional.

### Carrot polyculture

[poly_carrots.py](../scripts/03_advanced_farms/poly_carrots.py)

Grow primary carrots with compatible companion crops.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Plant, Carrots, Trees, Costs, Dictionaries, Polyculture.
- **Start:** Keep hay and wood in stock.

## Special farms

[Guide](special-farms.md)

### Cached cactus sorting

[cactus_cached.py](../scripts/04_special_farms/cactus_cached.py)

Sort rows from cached sizes, then columns, and harvest the complete field.

- **Requires:** Loops, Speed (if / can_harvest), Variables, Operators, Expand 2 (for / get_world_size), Plant, Senses, Functions, Carrots (till), Cactus, Lists.
- **Start:** Any ordinary square field; keep enough pumpkins for the missing cacti. Mega Farm is optional.

### Cactus bubble sort

[cactus_bubble.py](../scripts/04_special_farms/cactus_bubble.py)

Readable adjacent-swap alternative with an early finish after the last inversion.

- **Requires:** Loops, Speed (if / can_harvest), Variables, Operators, Expand 2 (for / get_world_size), Plant, Senses, Functions, Carrots (till), Cactus, Lists.
- **Start:** Any ordinary square field; keep enough pumpkins for the missing cacti. Mega Farm is optional.

### Mapped maze with waiting stations

[maze_stations.py](../scripts/04_special_farms/maze_stations.py)

Map a fresh maze, assign treasure regions, and reuse it up to 300 times.

- **Requires:** Loops, Speed (if / can_harvest), Variables, Operators, Expand 2 (for / get_world_size), Plant, Senses, Functions, Mazes, Lists, Dictionaries.
- **Start:** Ordinary farm or a full-field maze. Supply Weird Substance; run no other substance consumer at the same time. Mega Farm is optional.

### Dinosaur with early shortcuts

[dinosaur_cycle.py](../scripts/04_special_farms/dinosaur_cycle.py)

Use early shortcuts on even fields, then switch to a simple full-field cycle.

- **Requires:** Loops, Speed (if / can_harvest), Variables, Operators, Expand 2 (for / get_world_size), Plant, Senses, Functions, Dinosaurs, Hats (Gold Hat), Lists.
- **Start:** At least 2×2 and enough cactus for apples. Clears the farm for every new tail; odd sizes use short serpentine runs.
- **Field reset:** Calls `clear()` before each new dinosaur run. Existing crops are removed.

### Conservative dinosaur cycle

[dinosaur_safe.py](../scripts/04_special_farms/dinosaur_safe.py)

Follow a fixed Hamiltonian cycle on even fields without shortcut bookkeeping or lists.

- **Requires:** Loops, Speed (if / can_harvest), Variables, Operators, Expand 2 (for / get_world_size), Plant, Senses, Functions, Dinosaurs, Hats (Gold Hat).
- **Start:** At least 2×2 and enough cactus for apples. Clears the farm for every new tail; odd sizes use short serpentine runs.
- **Field reset:** Calls `clear()` before each new dinosaur run. Existing crops are removed.

## Mining expansion

[Guide and installation](dlc.md). Create the listed helper windows before running a program. Research requirements below include both programming features and the target mining unlock.

### DLC helpers

[dlc_common.py](../scripts/dlc/dlc_common.py)

Shared movement, guarded drone scheduling and mining helpers.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining.
- **Start:** Import this module without running a farm. Sensor-based helpers need Underground Senses; the first blocks program can use the unsensed branch.
- **Shared module:** Importing this file does not run a farm.

### Blocks

[blocks.py](../scripts/dlc/blocks.py)

Collect ordinary blocks with short shafts or a parallel surface pass.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining.
- **Start:** Run one farm at a time; the field is reset before every batch.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Coal

[coal.py](../scripts/dlc/coal.py)

Use a persistent group of row workers to mine the first sixteen layers.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Coal, Timing.
- **Start:** Start this file from any field; each world is cleared. Coal can be scarce on tiny fields.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Iron

[iron.py](../scripts/dlc/iron.py)

Scout for iron, follow nearby ore and optionally spend coal on prospecting.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Iron, Coal, Timing.
- **Start:** Coal is replenished through the Coal farm when prospecting is available.
- **Helper windows:** dlc_common, coal. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Quartz

[quartz.py](../scripts/dlc/quartz.py)

Locate quartz from four distance readings and mine the deduplicated targets.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Quartz, Iron, Coal, Timing, Dictionaries.
- **Start:** Keep iron in stock or allow the ore dependency chain to replenish it.
- **Helper windows:** dlc_common, coal, iron. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Rice

[rice.py](../scripts/dlc/rice.py)

Expose clay in one phase, then grow and harvest rice after all digging stops.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Rice, Plant.
- **Start:** The field is reset at startup and after the useful clay is exhausted.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Bamboo

[bamboo.py](../scripts/dlc/bamboo.py)

Grow dense bamboo beside access lanes and retain the bases after harvest.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Bamboo, Plant, Carrots, Dictionaries, Timing.
- **Start:** Keep rice available for the first planting; every worker finishes a bounded batch.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Mushrooms

[mushrooms.py](../scripts/dlc/mushrooms.py)

Match nearby mushroom pairs horizontally and vertically within small tiles.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Mushrooms, Dictionaries.
- **Start:** Keep blocks for filling gaps. Pairs across tile boundaries are not combined. Requires at least two cells per side.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Dynamite

[dynamite.py](../scripts/dlc/dynamite.py)

Use safe clue deductions and cash out a layer when no further safe move is known.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Dynamite, Dictionaries, Timing.
- **Start:** The solver can leave a puzzle incomplete; it does not guess an unknown cell.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Pyramids

[pyramids.py](../scripts/dlc/pyramids.py)

Find a limestone foundation, restore sand layers and harvest the reward.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Pyramid.
- **Start:** Requires a field at least 5 by 5 and enough blocks for placing sand.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Fossilized pumpkins

[fossil_pumpkins.py](../scripts/dlc/fossil_pumpkins.py)

Expose the local fossil cluster, then mine it in separate color phases.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Petrified Pumpkins.
- **Start:** Resets between clusters; search is local to a 9 by 9 window after discovery.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Treasure maps

[treasure_maps.py](../scripts/dlc/treasure_maps.py)

Read an underground map and follow every direction and dig instruction.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses, Treasure Map, Dictionaries.
- **Start:** The first D already digs the map. Resets after each treasure.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.

### Layer mining

[layer_mining.py](../scripts/dlc/layer_mining.py)

Remove successive depth levels with barriers between color phases.

- **Requires:** Loops, Speed, Expand 2, Variables, Operators, Functions, Lists, Senses, Import, Utilities, Hats, Mining, Underground Senses.
- **Start:** Use a positive layer count for a finite run; ordinary cave-in losses are possible.
- **Helper windows:** dlc_common. Install their dependencies too.
- **Field reset:** Uses `clear()` through the shared mining module; existing crops are removed.
