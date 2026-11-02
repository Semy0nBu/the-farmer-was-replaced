# Early game and one-drone farms

Start with the smallest script your research allows. A later file can refer to a command or a language feature you have not unlocked yet, even if you only want its simplest behaviour. These files stay separate so there is no need to strip an advanced program down before using it.

Copy one file into a code window and run that window. Stop it before changing crops or launching another farm. None of these scripts imports another file, uses water or fertilizer, changes the field size, or resets the farm with `clear()`.

## The first plots

| File | Research and language features needed | Use it when |
| --- | --- | --- |
| [harvest_once.py](../scripts/01_first_steps/harvest_once.py) | No research | You have just started. Run it again when the grass is ready. |
| [hay_loop.py](../scripts/01_first_steps/hay_loop.py) | Loops | You can repeat commands but have not bought the first Speed upgrade. |
| [hay_ready.py](../scripts/01_first_steps/hay_ready.py) | Loops, Speed (`if`, `can_harvest`) | The drone is fast enough to reach grass before it has regrown. |
| [hay_column.py](../scripts/01_first_steps/hay_column.py) | Loops, Speed, first Expand (`move`) | The field is still a single column, including the first 1×3 expansion. |
| [bush_plot.py](../scripts/01_first_steps/bush_plot.py) | Loops, Speed, Plant | You need wood on the original plot. |
| [bush_column.py](../scripts/01_first_steps/bush_column.py) | Loops, Speed, Plant, first Expand | You need wood on the narrow starting field. |

The first file is deliberately just one command. The unrestricted hay loop belongs before the first Speed upgrade: once the drone gets faster, switch to the version that checks maturity. The column scripts never move east, so replace them when the farm becomes a square.

These first programs expect an ordinary grass field, or the crop they already grow. They do not inspect the ground or remove unrelated young crops. Grass grows back by itself; bushes must be planted after harvesting.

## Single-drone farms

### The square field, before Operators

The second expansion opens `for`, `range()` and `get_world_size()`. You can cover the new square before unlocking arithmetic, comparisons, explicit variable assignments or Senses.

| File | Requirements | Starting field |
| --- | --- | --- |
| [hay_grid.py](../scripts/02_single_drone/hay_grid.py) | Loops, Speed, square-field Expand | Grassland growing grass. |
| [bush_grid.py](../scripts/02_single_drone/bush_grid.py) | The hay requirements, plus Plant | Grassland or soil; grass and bushes are fine. |

Both use a complete northward circuit for each column, then move east. The loop names are only iterators and are never read. A complete field circuit takes `size² + size` moves. Once Operators is available, the next pair removes the extra northward step from every column.

### The square field, before Senses

The files below use comparisons and arithmetic, so unlock Operators first. None needs Lists, Dictionaries, Functions or Senses.

| File | Additional requirements | Starting field |
| --- | --- | --- |
| [hay_square.py](../scripts/02_single_drone/hay_square.py) | Loops, Speed, square-field Expand, Operators | Grassland growing grass. |
| [bush_square.py](../scripts/02_single_drone/bush_square.py) | The hay requirements, plus Plant | Grassland or soil; grass and bushes are fine. |
| [prepare_soil.py](../scripts/02_single_drone/prepare_soil.py) | Speed, square-field Expand, Operators, Carrots | **Every tile must still be Grassland. Run once.** |
| [carrots_no_senses.py](../scripts/02_single_drone/carrots_no_senses.py) | Loops, Speed, square-field Expand, Operators, Variables, Plant, Carrots | Empty soil, prepared for this launch. |

The route moves north `size - 1` times, then east once. After repeating that block `size` times, it has visited each tile exactly once and returned to its starting tile. It works from any starting coordinate on a square field and takes `size²` moves for a complete circuit.

For the first carrots:

1. Build a reserve of hay and wood.
2. Start on an all-Grassland field and run `prepare_soil.py` once. It ends after one complete circuit.
3. Run `carrots_no_senses.py`. It seeds the entire field, then only harvests mature carrots and replants those tiles.

`till()` toggles the ground. Running the preparation twice turns the soil back into Grassland. The preparation cannot detect mixed ground before Senses, and the carrot program cannot recognise an existing young carrot. Do not rerun its seeding phase on a partly planted field. If it stops because planting failed, recover the field deliberately or switch to the Senses version after unlocking it. Neither file calls `clear()` to hide that limitation.

The no-Senses carrot script stops at the first failed planting. That can mean insufficient hay or wood, occupied ground, or an incorrectly prepared tile. It does not keep doing empty laps. Stop and restart this version after expanding the farm; its starting size is fixed for the run.

### Senses and trees

Senses makes it possible to preserve young crops, recognise empty tiles and prepare only ground that needs tilling. These versions can take over an ordinary field containing a different crop. They will remove plants that conflict with the selected farm, including young ones, so harvest anything you want to keep first.

All four files need Loops, Speed, square-field Expand, Operators, Variables and Senses. The table lists the remaining requirements.

| File | Additional requirements | What it grows |
| --- | --- | --- |
| [hay_senses.py](../scripts/02_single_drone/hay_senses.py) | Carrots, for `till()` | Grass on Grassland; repairs soil and removes other crops. |
| [carrots_senses.py](../scripts/02_single_drone/carrots_senses.py) | Plant, Carrots, Functions | Carrots on soil; preserves young carrots and stops if a new planting fails. |
| [trees_and_hay.py](../scripts/02_single_drone/trees_and_hay.py) | Plant, Trees, Carrots, Functions | Separated trees with grass in between. Needs a square of at least 2×2. |
| [trees_and_bushes.py](../scripts/02_single_drone/trees_and_bushes.py) | Plant, Trees | Separated trees with bushes in the remaining tiles. |

The tree layout uses `(x + y) % size`. On even squares it is the usual checkerboard. On odd squares it leaves one extra diagonal without trees, so trees do not become neighbours across the field boundary. That gives trees room to grow on both odd and even fields. The trees-and-bushes file uses a bush on a 1×1 field; the trees-and-hay file stops there because one tile cannot grow the two crops at the same time.

The mixed tree-and-hay farm balances space, not item counts per second. Different growth times and research upgrades change the actual output. Use the dedicated hay or wood program when one resource is holding up the next purchase.

### Pumpkins without Lists

[pumpkins_scan.py](../scripts/02_single_drone/pumpkins_scan.py) needs Loops, Speed, square-field Expand, Operators, Variables, Functions, Plant, Carrots, Senses and Pumpkins. It does not need Lists or Megafarm.

Each pass prepares soil, plants missing pumpkins and replaces dead ones. A pass with every tile mature triggers one harvest for the whole square. It never harvests an individual pumpkin just because that one tile is ready. Dead pumpkins are replaced directly with `plant(Entities.Pumpkin)`.

Keep enough carrots for the whole field and several repairs. A failed planting stops the program; a field expansion also stops it so you can restart with the new size. It can preserve existing young pumpkins. Larger squares gain the full size bonus from 6×6 onward; the script also works on smaller squares while you are progressing.

### Sunflowers without Lists

[sunflowers_scan.py](../scripts/02_single_drone/sunflowers_scan.py) needs Loops, Speed, square-field Expand, Operators, Variables, Functions, Plant, Carrots, Senses and Sunflowers. It uses `measure()` from the sunflower research, but no lists.

The program fills the field, then scans petal counts from 15 down to 7. It waits for each chosen sunflower to mature before harvesting it. On fields containing at least ten flowers, it leaves nine standing and replants the empty tiles only after harvesting has finished. New flowers cannot introduce a larger petal count halfway through that harvest phase.

On a field smaller than ten tiles there is no ten-flower bonus to preserve, so it harvests the whole batch. The repeated scans cost movement; use the bucket-based version once Lists is available. Planting costs carrots, and insufficient resources stop the program.

### A first maze, without a map or Lists

[maze_wall.py](../scripts/02_single_drone/maze_wall.py) needs Loops, Speed, square-field Expand, Operators, Variables, Functions, Plant, Senses and Mazes. You also need a stock of Weird Substance from fertilized crops.

It grows a fresh full-field maze, follows the left wall until it reaches treasure, harvests the treasure and starts a new maze. The dose follows the current maze upgrade: `size * 2**(num_unlocked(Unlocks.Mazes) - 1)`. It checks the stock before planting the next bush.

This version is for fresh mazes, which have no cycles. It deliberately does not relocate treasure or reuse a maze. If launched while standing on a hedge, it stops and leaves the existing maze alone. Start outside an old maze or finish that maze first. If no direction is passable, the step budget is exhausted, or the field size changes, it ends the run without harvesting a hedge. Failed attempts to move into a wall are a normal part of finding the next passage.

### Cactus before Lists

[cactus_bubble.py](../scripts/02_single_drone/cactus_bubble.py) needs Loops, Speed, square-field Expand, Operators, Variables, Functions, Plant, Carrots, Senses and Cactus. It uses cactus measurements and swaps, but no lists, dictionaries or extra drones.

It plants the field, sorts rows eastward, sorts columns northward and checks that every cactus is mature before harvesting. Sorting the columns preserves the already sorted rows. Swaps never cross a field boundary. Planting costs pumpkins; a failed planting or swap ends the run.

This is the small, easy-to-follow baseline. The cached sorter later in the collection avoids much of its repeated movement and measuring. Repeatedly harvesting and replanting an immature cactus does not reroll its size, so this script sorts the values it gets.

## When to move on

Unlocking Lists allows pending-cell queues for pumpkins and petal buckets for sunflowers. Megafarm then lets independent rows or bands work in parallel. Keep a one-drone version when learning a new crop or when you have not unlocked the planning features used by a later script.

The route and layout checks for these files are local model checks. They are not evidence that every research combination has been run in the game's interpreter. Use the prerequisite tables, start on the stated field type and read any in-game error before moving to the next stage.
