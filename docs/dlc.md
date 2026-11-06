# The Miner Was Replaced

These programs cover the mining expansion: blocks and ores, underground crops, and the puzzle layers. Start with the resource you have unlocked. The programs check research; they do not buy it for you.

The expansion is [The Miner Was Replaced](https://store.steampowered.com/app/4521700/The_Miner_Was_Replaced/). Its mining commands belong to the game's own language, just like the base-game farming commands.

## Installing the mining programs

1. Stop the current farm and back up anything you want to keep.
2. Create a window named **`dlc_common`** and paste [dlc_common.py](../scripts/dlc/dlc_common.py) into it.
3. Create a window with the chosen program's filename, without `.py`, and paste its entire contents.
4. For iron, also install **`coal`**. For quartz, install **`coal`** and **`iron`**. Keep these names unchanged because the imports use them.
5. Run the resource program. The shared module has no farming entry point, and importing another resource program does not start it.

All programs use the same flat set of in-game code windows. The repository folders organize the downloads; they are not Python package paths inside the game. You can also copy all 13 DLC files into the active save through an external editor, following the [File Watcher instructions](game-language.md#use-an-external-editor).

**Mining programs reset the world with `clear()`.** A reset removes existing crops and creates a fresh underground world. Run one program at a time. The programs do not resize your field, water crops, apply fertilizer, print messages, or submit leaderboard runs.

## Progression and program choice

The full language requirements for each file are in the [script index](script-index.md#mining-expansion). This table shows the main mining unlock and intended use.

| Stage or goal | Program | How it works |
| --- | --- | --- |
| First Mining unlock | [blocks.py](../scripts/dlc/blocks.py) | Collects ordinary blocks. Uses surface work when the sensors and extra drones are available; otherwise uses short shafts. |
| Underground Senses and Coal | [coal.py](../scripts/dlc/coal.py) | Keeps a group of workers alive through a shallow world, with neighboring row markers preventing ore-destroying depth gaps. |
| Iron | [iron.py](../scripts/dlc/iron.py) | Distributes scouts, checks visible neighboring ore, and uses prospecting when unlocked. |
| Quartz | [quartz.py](../scripts/dlc/quartz.py) | Uses distance measurements to propose a vein position, then checks the actual ground before mining. |
| Rice | [rice.py](../scripts/dlc/rice.py) | Exposes clay first, joins all miners, then plants and harvests rice. |
| Bamboo | [bamboo.py](../scripts/dlc/bamboo.py) | Uses access lanes, plucks fruit at its measured height, and regrows retained stems. |
| Mushrooms | [mushrooms.py](../scripts/dlc/mushrooms.py) | Matches colors horizontally and vertically inside independent rectangular work areas. |
| Dynamite | [dynamite.py](../scripts/dlc/dynamite.py) | Applies safe deductions and cashes out a layer when the remaining clues are uncertain. |
| Pyramids / Power | [pyramids.py](../scripts/dlc/pyramids.py) | Finds the foundation, exposes the ruin, and restores supported sand layers from the bottom up. |
| Fossilized pumpkins | [fossil_pumpkins.py](../scripts/dlc/fossil_pumpkins.py) | Searches for a fossil and opens a local area around the find. |
| Underground gold | [treasure_maps.py](../scripts/dlc/treasure_maps.py) | Measures basalt, finds its map, and follows the returned directions. |
| Broad excavation | [layer_mining.py](../scripts/dlc/layer_mining.py) | Advances the field through depth levels with barriers between worker phases. |

Mega Farm is optional. Work is limited by both the unlocked drone count and the number of useful tasks. Searching for a puzzle layer or interpreting its clues can still be sequential. More drones do not give every solver a proportional speedup.

Most programs need Underground Senses before they can inspect a layer safely. `blocks.py` includes a branch for the first Mining unlock. Iron works without Prospecting through bounded exploration; unlocking Prospecting makes its search more directed. Jump is optional and is used only where the program supports it.

## Resources to keep available

| Program | Supply to keep in reserve |
| --- | --- |
| Iron with prospecting | Coal |
| Quartz with distance measurements | Iron; coal is useful for refilling iron |
| Bamboo | Rice for planting |
| Mushrooms | Blocks for filling holes along a matching route |
| Pyramid restoration | Blocks for placing sand |
| Any long run | Power to keep execution fast |

Iron and quartz can prepare their own upstream ore supplies through the imported modules. This preparation can reset the world, so it belongs inside the selected farm's run. The other programs leave missing supplies for you to grow or mine separately.

## Mining rules that affect the code

`dig()` collects only the block dug directly. Nearby blocks removed by a cave-in yield nothing. A deep shaft can therefore expose a lot of ground while collecting little ore. The coal program keeps neighboring rows close in depth instead of treating every column as an independent shaft.

`get_pos_z()` reports the ground position, not the drone's hover height. Bamboo uses `hover()` to enter fruit at the right height. Digging and harvesting affect hover state, so the bamboo worker restores the height it needs before moving through the plants.

Workers have separate memory. Their results are returned with `wait_for()`, and each phase joins before a reset or an operation that depends on all earlier work being complete. Rice uses a full excavation barrier before planting so another worker cannot dig beside a young plant.

Jump is not a resettable teleport. A program may use it once; calling `clear()` later does not make it available again. Its return value is not used as a success flag.

## Size and solver limits

- The scripts read the current square size and available drone count. They do not force a 32×32 field or require 32 drones.
- A 1×1 field cannot hold a mushroom pair. Pyramid restoration needs a field of at least 5×5. Those programs stop when the required geometry is unavailable.
- Coal generation on a tiny field can produce no ore. Empty results are bounded rather than retried forever.
- The bamboo layout keeps access lanes. Its 32×32 arrangement holds 806 plants; smaller and odd fields use the same layout rules with remainder handling.
- Mushroom matching is local to each worker's rectangle. It uses both axes, but can leave matches that cross worker boundaries or are hidden by the geology.
- Quartz measurements can refer to different nearby veins. The geometry gives a candidate, not proof of a deposit; the program keeps ground checks and bounded attempts.
- The dynamite solver uses forced deductions. It does not guarantee that every layer can be solved completely without a guess. Cashing out an uncertain layer is part of the farming strategy.
- Layer mining does not preserve every block or solve every puzzle it uncovers. Use a dedicated program when a particular resource or puzzle is the goal.

Stop the program before changing field size or switching to another farm. After a change, restart so workers and cached geometry begin together on the new field.

## Finite runs and progress

The entry call is at the bottom of each resource file. Most `gr_*` functions accept a `rounds` argument: `0` repeats, and a positive value requests a finite batch. A round means the operation described by that program, such as a productive ore world, bamboo regrowth cycle, or completed puzzle attempt. Layer mining uses its own `layers` limit.

For example, change the coal entry call to:

```python
gr_coal(3)
```

That requests three productive coal worlds. It does not set a Steam achievement target or change inventory directly. The coal program also exposes `rate` in collected coal per elapsed game minute; inspect it in the game without adding print calls.

The public programs are general farms. They do not contain a particular save's inventory targets, achievement counters, research purchases, or leaderboard launchers. Read [validation](validation.md) for the distinction between in-game source runs and checks of these published adaptations.
