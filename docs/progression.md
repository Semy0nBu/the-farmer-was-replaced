# Progression guide

You do not need the most complicated script to make progress. Use the smallest version that can do the current job, build a reserve of its inputs, and move on when another resource becomes the bottleneck.

The research tree allows different routes. The stages below describe capabilities, rather than a fixed list of purchases or prices. Prices and yields change with upgrades; check the game instead of relying on a hard-coded cost from an old guide.

## 1. Work the first plot

At the very beginning, harvest by hand or run the straight-line first-plot example. Once Loops is available, a repeating hay script can keep that plot working.

After the first Speed upgrade, use the version that checks `can_harvest()`. Faster execution makes blind harvesting a poor habit: removing grass before it grows does not produce the hay you want.

See the [first-step scripts](early-game.md). These deliberately avoid variables, functions, and collections where those features are still locked.

## 2. Use the first expansion

The first expansion is a column, not a square. Its useful direction is `North`. Use the first-column script instead of assuming that `get_world_size()` describes a square at this stage.

When later expansions produce a square and `for` loops are available, switch to the square-field route. Before Operators, the grid versions use plain nested loops. With arithmetic and comparisons available, the shorter square versions save one extra move per column. That is the point where a complete traversal matters more than repeating one movement forever.

## 3. Establish hay and wood

Planting unlocks bushes. Bushes provide a wood supply before trees are available. Keep enough hay alongside it so the next crop can be planted.

When trees are unlocked, use a spaced layout. Orthogonally adjacent trees grow more slowly, so a full field of tightly packed trees is usually a poor starting layout. The wood-and-hay version leaves grass between trees; the tree-and-bush version uses the remaining cells for bushes.

On odd-sized toroidal fields, a plain checkerboard meets itself across the border. The sensed and advanced layouts account for this instead of assuming that every field has an even side length.

## 4. Grow carrots

Carrots require soil and consume both hay and wood.

Before Senses is available, use the clearly documented preparation and farming pair. Prepare the ground once, then run the carrot loop. Do not repeat an unconditional `till()` on every visit: the second call turns soil back into grassland.

Once ground and entity sensors are available, switch to a sensed version. It can prepare only the cells that need it and distinguish a growing carrot from a different plant. If planting stops, refill hay or wood before changing the route.

## 5. Grow pumpkins

Build a carrot reserve first. A pumpkin field needs more than one planting per cell because some plants die while growing.

The basic version uses repeated full-field checks without lists. The advanced version keeps local work queues, replaces dead pumpkins, and stops checking cells whose pumpkins have already been confirmed. Workers finish their own repairs before the final full-field harvest.

Do not harvest individual living pumpkins while waiting for the square to finish. Early harvests break the large-field crop you are trying to assemble.

## 6. Add sunflower power

Power speeds up later work, so a reserve is useful before long farming runs.

For the sunflower bonus, harvest a flower with the highest petal count and keep enough flowers planted. The basic script works without collections; the advanced version groups measured positions and harvests in order.

A small field may not hold enough flowers for the bonus. The script can still grow power, but a larger field makes the ordered harvest more useful. The detailed guide states how each version handles small fields.

## 7. Use companion planting

Once Polyculture and the required programming features are available, choose one main resource: hay, wood, or carrots. Its script reads companion requests, plans compatible plantings, and grows the requested resource on the main cells.

The companion does not have to be fully grown for the bonus. It does have to be the requested type at the requested position. Requests change with newly planted main crops, so a fixed decorative mixture is not a replacement for `get_companion()`.

Companion planting also consumes planting inputs. Keep hay and wood available when a plan needs carrots. Read the [advanced farm guide](advanced-farms.md) for the layout and resource behavior.

## 8. Add more drones when available

Mega Farm increases useful parallel work; it does not give workers shared memory. Each worker receives its own copied arguments and returns results when joined.

The advanced scripts choose a worker count from the available limit and the amount of useful work. One drone still works. Buying another drone upgrade does not require replacing a constant throughout the repository.

More workers cannot eliminate crop growth or a sequential final harvest. On small fields, some scripts intentionally use fewer workers than the maximum.

## 9. Produce Weird Substance

Use the dedicated infected-carrot farm when you need Weird Substance for mazes. It applies fertilizer deliberately; the ordinary carrot farm does not.

Keep its carrot inputs and fertilizer stocked. Fertilized crops change the mix of resources received, so use the ordinary carrot farm when carrots themselves are the goal.

## 10. Farm gold in mazes

Start with enough Weird Substance to create a maze. The first-maze solver is useful for learning and collecting an initial treasure. The station-based version maps a maze and assigns workers to regions for repeated treasure collection.

A newly generated maze has a different map. Do not reuse a stored map from an earlier maze. Reusing the treasure can open passages; the advanced solver can take advantage of those changes while keeping ownership of a target unambiguous.

The script checks its supply before spending more Weird Substance. It collects the final treasure when it cannot continue reusing the current maze.

## 11. Sort cactus

Use pumpkins to seed the field. Cactus harvesting rewards a fully grown, sorted field, so planting and measuring are only the first half of the job.

The cached version sorts rows and then columns, retaining the measurements it already paid to obtain. The simpler bubble-sort version is included as an alternative that is easier to follow.

Destroying and replanting an immature cactus does not reroll its size. Repeated planting until a cell produces a desired number is therefore not a valid sorting shortcut in current versions. See the [special farm notes](special-farms.md).

## 12. Farm dinosaur bones

Build a cactus reserve before equipping the dinosaur hat. Start with the conservative route if you want predictable movement. Try the shortcut version when you understand how the tail constrains the available moves.

The dinosaur hat changes the movement rules: the edges stop wrapping, and running into the tail blocks a move. A larger tail is only useful once it is cashed out by changing hats. Bone farming uses one dinosaur; extra drones do not provide independent dinosaur tails.

Odd field sizes need a different route from an even square. Read the [dinosaur limitations](special-farms.md) before expecting a full-field tail on every size.

## Keep the supply chain moving

| Goal | Input to keep available |
| --- | --- |
| Carrots | Hay and wood |
| Pumpkins | Carrots |
| Cactus | Pumpkins |
| Dinosaur apples | Cactus |
| Mazes | Weird Substance |
| Infected carrots | Carrot planting inputs and fertilizer |

Power is useful across the later farms. Water is optional in this collection and is used only by the tree polyculture version. Refill an upstream resource when a farm runs out, then resume the farm you were working on.

## Continue underground

For **The Miner Was Replaced**, follow the separate [mining progression guide](dlc.md). Start with blocks and Underground Senses, then choose the unlocked ore or crop program. The DLC files share a small local module rather than repeating the dispatcher in every program. They do not buy research automatically.
