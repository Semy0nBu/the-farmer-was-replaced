# The Farmer Was Replaced — scripts for every stage

A collection of farm scripts for the base game and **The Miner Was Replaced** DLC. Start with the first plot, work through the research tree, then use the crop farms, mining routines, and puzzle solvers that fit your current unlocks.

The early scripts keep their requirements small. The later ones use cached measurements, parallel workers, companion planting, and planned routes. There are alternatives where a simpler approach is useful.

The base-game collection has 35 standalone scripts. The DLC collection has 12 programs and one shared module. There are no leaderboard submissions or automatic research purchases.

## Start here

1. Find your current stage in the [progression guide](docs/progression.md).
2. Check the requirements beside the script. A crop unlock does not automatically unlock lists, functions, or dictionaries.
3. Create a code window in the game and paste in the chosen `.py` file. For DLC programs, also create the helper windows listed in the [mining setup](docs/dlc.md#installing-the-mining-programs).
4. Run one farm at a time. Stop it before switching to another crop on the same field.

These files run in the game's own language. The `.py` extension is useful for editing; running them with Python on your computer will not control the farm.

## Choose a script

| Where you are | What to use |
| --- | --- |
| First plot, first column, or just learning loops | [First steps](docs/early-game.md) |
| A square field, but some programming features are still locked | [Single-drone versions](docs/early-game.md#single-drone-farms) |
| Functions and collections are available | [Advanced crop farms](docs/advanced-farms.md) |
| Companion planting is available | [Polyculture farms](docs/advanced-farms.md) |
| Farming cactus, gold, or bones | [Special farms and alternatives](docs/special-farms.md) |
| Starting the mining expansion or farming its resources | [The Miner Was Replaced guide](docs/dlc.md) |

The [script index](docs/script-index.md) lists every file and its requirements.

## What is included

- Hay, bushes, trees, and balanced wood-and-hay layouts.
- Carrots before and after ground sensors become available.
- Pumpkins with dead-plant repair and full-field harvesting.
- Sunflowers with safe harvest ordering.
- Separate hay, wood, and carrot polyculture farms.
- An infected carrot farm for Weird Substance.
- Cached and simpler cactus sorting variants.
- Maze solving and repeated treasure collection.
- Dinosaur farming with a conservative route and a shortcut variant.
- Blocks, coal, iron, quartz, rice, and bamboo in the mining expansion.
- Mushroom matching, dynamite deduction, pyramid restoration, fossilized pumpkins, and treasure maps.
- A separate layer-by-layer mining alternative.

The scalable farms read the field size and available drone limit. They also have a single-drone path when Mega Farm is unavailable. Early rectangular expansion needs its own first-column script; the square-field scripts are for later expansions. Some DLC puzzles need a minimum field size or have a sequential solving stage; the mining guide lists those limits.

Most farms do not use water. The tree polyculture farm waters its main trees when water and the required research are available. Fertilizer is reserved for the explicitly named Weird Substance farm.

## Read before running

Planting carrots spends hay and wood. Pumpkins spend carrots, cactus spends pumpkins, and dinosaur apples spend cactus. A well-routed script cannot plant with an empty inventory: grow the missing input first.

`till()` toggles the ground, and `harvest()` can destroy an immature plant. Scripts that need an empty or prepared field say so in their instructions. Back up a save before trying a reset or preparation script on a field you want to keep.

Some farms run indefinitely; others stop when they cannot afford a planting. Dinosaur runs intentionally end a tail to collect bones and then begin again. The individual guides explain these differences.

Mining programs use `clear()` to start a fresh underground world. This removes the existing field. Stop other programs and finish anything you want to preserve before starting one. They leave research purchases and field size under your control.

## Editing and troubleshooting

- [Research and progression](docs/progression.md)
- [Mining progression, dependencies, and puzzle notes](docs/dlc.md)
- [Game language and editing files](docs/game-language.md)
- [Common problems](docs/troubleshooting.md)
- [Checks and performance notes](docs/validation.md)
- [Contributing](CONTRIBUTING.md)

This is an unofficial collection for [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/). The in-game documentation is the reference for your installed version. The scripts and original notes in this repository are available under the [MIT license](LICENSE).
