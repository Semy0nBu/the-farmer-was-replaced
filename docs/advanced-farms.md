# Advanced farms

These are the farms I use once functions and lists are available. Each file runs on its own. Copy one file into a game window and run it; there is no shared module to install.

Every farm reads the current square field size. Before Megafarm, it runs on one drone. After Megafarm, it uses the available limit, up to the number of useful work bands. A failed drone launch falls back to local work. The main drone counts toward the limit.

The scripts in this folder need **Loops, Speed, Expand 2 or later, Variables, Operators, Functions, Lists, and Senses**. `num_unlocked()` comes with Senses; Auto Unlocks is not needed. Crop requirements are listed below. If those programming features are still locked, use the [earlier versions](early-game.md).

| File | Additional research | What it produces |
| --- | --- | --- |
| [hay.py](../scripts/03_advanced_farms/hay.py) | Carrots, for `till()` | Hay on a full grass field |
| [carrots.py](../scripts/03_advanced_farms/carrots.py) | Plant, Carrots | Carrots without fertilizer |
| [weird_substance.py](../scripts/03_advanced_farms/weird_substance.py) | Plant, Carrots, Fertilizer | Infected carrots and Weird_Substance |
| [tree_bush.py](../scripts/03_advanced_farms/tree_bush.py) | Plant, Trees | Wood from separated trees and bushes |
| [tree_hay.py](../scripts/03_advanced_farms/tree_hay.py) | Plant, Trees, Carrots | Wood and hay on the same field |
| [pumpkins.py](../scripts/03_advanced_farms/pumpkins.py) | Plant, Carrots, Pumpkins | One merged pumpkin covering the field |
| [sunflowers.py](../scripts/03_advanced_farms/sunflowers.py) | Plant, Carrots, Sunflowers | Power with the maximum-petal bonus |
| [poly_hay.py](../scripts/03_advanced_farms/poly_hay.py) | Plant, Carrots, Trees, Costs, Dictionaries, Polyculture | Hay with companion planting |
| [poly_wood.py](../scripts/03_advanced_farms/poly_wood.py) | Plant, Carrots, Trees, Costs, Dictionaries, Polyculture | Wood with companion planting |
| [poly_carrots.py](../scripts/03_advanced_farms/poly_carrots.py) | Plant, Carrots, Trees, Costs, Dictionaries, Polyculture | Carrots with companion planting |

Run one farm at a time. These programs use the whole field and replace crops that do not belong to their layout. They keep young plants of their own crop. They do not call `clear()` or change the field size. When switching from a maze, they collect or remove the maze first.

## Choosing a farm

`hay.py` restores grassland and leaves young grass alone. `carrots.py` prepares soil and stops if a new carrot cannot be planted. Carrots need both hay and wood, so keep those two farms ahead of carrot production. More drones cannot fix an empty resource stock.

`weird_substance.py` is the dedicated Weird_Substance farm. It attempts one fertilizer use after each successful new carrot planting. Existing young carrots are not fertilized repeatedly. Without fertilizer it continues as a normal carrot farm; future plantings use fertilizer again when some becomes available. It never spends Weird_Substance.

`tree_bush.py` fills the field with wood crops. On an even field, trees and bushes form the usual checkerboard. On an odd field, one diagonal is kept free of trees so trees do not touch across the wrapping edge. A one-cell field uses a bush. `tree_hay.py` reserves roughly half the area for grass instead; on odd fields, a few bushes fill the remaining wood positions. This balances planted area, not the number of hay and wood items produced per second.

## Pumpkins

`pumpkins.py` starts its workers once per harvest. Each worker fills its band, then keeps a local list of pumpkins that still need attention. Dead pumpkins are replaced and checked again later. A pumpkin that is confirmed mature leaves the list for the rest of that crop.

The main drone waits for every worker before harvesting. This keeps a repaired corner from being harvested while the rest of the field is still growing. If planting fails, the program joins its workers and stops. Refill carrots and run it again. No water or fertilizer is used.

## Sunflowers

`sunflowers.py` needs at least ten field cells; on the normal square progression that means **4 by 4 or larger**. It stops on smaller fields rather than pretending the bonus is available.

Flowers are grouped by their measured petal count, from 15 down to 7. Only one petal level is harvested at a time, and the workers finish that level before the next one begins. The script leaves nine flowers standing, replants the empty positions, then starts another harvest batch. New planting never changes the maximum while a batch is being collected.

The script waits for an assigned flower to mature before collecting it. That keeps the bonus rules correct, although a different route can sometimes avoid more waiting. The nearest-next-flower choice is a practical route heuristic, not a proof of the shortest total tour. Keep carrots in stock for replanting. No watering is used.

## Polyculture

The three `poly_` files share the same planner. Primary crops occupy alternating cells. The other cells support requests returned by `get_companion()`. On odd fields larger than one, the final row and column are reserved for support so the primary trees do not touch across the wrapping edge.

Several plants can ask for different companions on the same cell. The planner counts those requests, keeps the existing crop on a tie, and chooses the crop with the most requests. A request that points to another primary cell is skipped. As a result, some plants get a bonus and others do not. This is deliberate: primary crops are not removed to satisfy conflicting requests.

Companion planting finishes before primary harvesting starts. The planner passes only changed support cells to workers, and workers launch in a binary tree to reduce the delay of starting a large group. Trees and carrots must be unlocked even for hay polyculture because either can be requested as a companion.

Companion carrots are optional when hay or wood is short: an unaffordable request is skipped. Failure to plant a primary carrot stops that farm. The bonus does not require a companion to be mature.

Only `poly_wood.py` uses water. With Watering unlocked, it tops up primary trees toward a moisture level of 0.75, using the available stock. It skips watering when there is no water. Companion crops are not watered. The other files in this folder use no water, and only `weird_substance.py` uses fertilizer.

## Changing field size

The programs read the field size rather than storing a fixed 8, 16, or 32. If research changes the size during execution, workers stop when they observe the change and the main loop builds fresh bands. Stop and restart after a major change if the field looks wrong. A size change can happen between a sensor read and the next action, so this is recovery behavior rather than an atomic pause.

The crop layouts handle one-cell and odd-sized fields where the crop permits it. On 1 by 1, `tree_hay.py` grows a bush for wood; it cannot grow wood and hay simultaneously on one tile. Sunflowers need the larger field described above. The early rectangular 1 by 3 field has its own scripts in the earlier stages.

## Checks

The published adaptations were checked with translated-source models for one drone without Megafarm, odd and even fields, failed drone launches, low resources, pumpkin repairs, companion ownership and watering placement. These checks catch route and scheduling mistakes; they do not run the game's interpreter or establish a universal speed record. The sunflower harvest planner is carried over from the earlier version, with its drone limit made adaptive.
