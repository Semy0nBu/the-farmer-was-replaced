# Checks and performance notes

The scripts are meant to run in the game. A successful static check or a farm model does not replace that interpreter.

## Repository checks

With Node.js 20 or later installed, run:

```sh
node tools/check.mjs
```

There are no packages to install. The check verifies that every script is indexed, local documentation links resolve, code-window names stay short, and the collection contains no DLC commands, leaderboard calls, external imports, printing, or unexpected watering and fertilizer use. It also checks a set of direct command-to-research requirements.

This is a consistency check, not a full parser or proof that every language construct is unlocked. The requirement tables and the in-game error messages still matter. The same check runs in GitHub Actions.

## Model checks used during preparation

Separate local models were used to examine routes, ownership of cells, maturity barriers, resource failures, and worker launch failures. Some checks translated the actual source into an API model; others tested an algorithm's geometry directly.

| Area | Checks performed |
| --- | --- |
| Early field traversal | 384 square circuits across the basic and shorter routes, including different starting positions |
| Tree placement | 63 toroidal layouts with odd and even side lengths |
| Early sunflower batches | 280 checks of harvest order and retained flower counts |
| Basic cactus sorting | 175 generated grids |
| Fresh-maze wall following | 180 generated tree mazes |
| Advanced crop farms | 51 translated-source cases, including single-drone operation without Mega Farm, worker failures, low resources, pumpkins, and companion planting |
| Special farms | 45 translated-source cases for cactus, maze, and dinosaur variants, including single-drone operation, larger worker limits, odd fields, and shortages |

These models are development checks. They are not bundled as a replacement game engine, and their tick estimates are not advertised as measured game speedups. The complete published set has not been run as one uninterrupted fresh-save campaign.

## Comparing speed in the game

Compare the same amount of harvested output. Use the same field size, research, starting inventory, power supply, and simulation seeds. Include initialization when it is required for normal operation. If one variant ends early after a failed planting, its shorter time is a failure, not a win.

Take several runs. A few favorable random fields are not enough to establish a useful improvement. Record real elapsed game time separately from how long an accelerated simulation takes on your computer.

The cached cactus, pumpkin queues, and companion planner were chosen to reduce avoidable work. That does not establish a universal optimum. Growth, available drones, resource reserves, and the game's operation costs can change which tradeoff is useful.

## Version notes

The source rules were checked against the installed English documentation from Steam build **26379745**, collected on **2 November 2026**. This collection targets base-game mechanics and excludes the mining expansion.

One important compatibility rule is the retained size of an immature cactus after harvesting and replanting. That behavior was also checked in a native simulation: eight repeated immature plantings on one tile returned the same measured value. The collection uses sorting rather than size rerolls.

For the mechanics reference and update links, see [sources](sources.md).
