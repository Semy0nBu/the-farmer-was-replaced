# Checks and performance notes

The scripts are meant to run in the game. A successful static check or a farm model does not replace that interpreter.

## Repository checks

With Node.js 20 or later installed, run:

```sh
node tools/check.mjs
```

There are no packages to install. The check verifies that every script is indexed, local documentation links resolve, and code-window names stay short. Base-game files are checked separately from the mining collection so DLC commands and dependencies cannot leak into the early farms. It rejects leaderboard calls, external imports, printing, size changes, and unexpected watering or fertilizer use. It also checks direct command-to-research requirements and runs the regression models below.

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

## November 2026 review

All 35 base-game scripts were reviewed again when the DLC collection was added. The existing 51 advanced-farm and 45 special-farm source-model cases passed on the reviewed files. A maze cleanup error was fixed: an interrupted mapping pass now joins its live scouts before returning. Eight bundled regressions cover that cleanup, interrupted handles, and the last worker completing between sensor reads.

The bundled DLC checks exercise the actual published functions in small API models. They cover local imports, private worker arguments, failed spawns, operation with Mega Farm locked, the last-worker race, wraparound movement, coal row markers, bamboo access geometry, rice phase ordering, dynamite deductions, and treasure-map instructions beginning with `D`. These are focused models, not a complete underground simulator. They do not certify competitive speed or every possible cave-in.

During the import adaptation, the quartz supply routine was also corrected so its boolean research flag could not shadow the imported `coal` module.

## Mining measurements and published adaptations

The mining programs come from routines exercised in the game's interpreter, then renamed and given general entry points for this repository. The renamed public set has not been run as a complete fresh-save campaign. Small and odd fields, missing worker upgrades, and failure paths rely on the source models as well as the stated size limits.

| Source routine | In-game evidence before publication |
| --- | --- |
| Shared dispatcher and ordinary block mining | Finite runs with one and 32 drones; dispatcher and block-route comparisons |
| Coal | Matched seed tests on 32×32 with 32 drones, followed by a real farming run |
| Iron and quartz | Finite ore runs with one and 32 drones, including supply preparation |
| Rice | Separated excavation and planting completed finite multi-cycle tests |
| Bamboo | The dense surface layout ran on a real 32×32 field through repeated regrowth cycles |
| Mushrooms | The two-axis matching core produced mushrooms on a real field; boundary-spanning pairs can remain |
| Dynamite | Safe deduction and cash-out farming produced dynamite in the game; it is not a guaranteed complete Minesweeper solver |
| Pyramids, fossilized pumpkins, and treasure maps | Finite in-game resource runs; the treasure path includes its initial map dig exactly once |
| Layer mining | Multi-drone excavation was observed; this is a general alternative rather than a maximum-yield ore farm |

One coal comparison used current research and inventory on four matching 32×32 seeds. Persistent workers collected 5,520 coal in 172.58 game seconds; independent rows collected 5,446 in 170.09 seconds. The throughput difference was about 0.1%, so the version preserving ore was retained. A sparse cave-in strategy made fewer direct digs but took longer in the game. These measurements describe that setup, not a promised rate for another research level or device.

No personal achievement targets, save files, resource edits, game assets, or extracted implementation files are included. The tests run locally with Node and in GitHub Actions.

## Comparing speed in the game

Compare the same amount of harvested output. Use the same field size, research, starting inventory, power supply, and simulation seeds. Include initialization when it is required for normal operation. If one variant ends early after a failed planting, its shorter time is a failure, not a win.

Take several runs. A few favorable random fields are not enough to establish a useful improvement. Record real elapsed game time separately from how long an accelerated simulation takes on your computer.

The cached cactus, pumpkin queues, and companion planner were chosen to reduce avoidable work. That does not establish a universal optimum. Growth, available drones, resource reserves, and the game's operation costs can change which tradeoff is useful.

## Version notes

The original base-game rules were checked against the installed English documentation from Steam build **26379745** on **2 November 2026**. The DLC sources were reviewed against the installed documentation and API, with build **26462009** installed at the **6 November 2026** review. The earlier mining runs above preceded that review; they are not claimed as new measurements on every subsequent patch.

One important compatibility rule is the retained size of an immature cactus after harvesting and replanting. That behavior was also checked in a native simulation: eight repeated immature plantings on one tile returned the same measured value. The collection uses sorting rather than size rerolls.

For the mechanics reference and update links, see [sources](sources.md).
