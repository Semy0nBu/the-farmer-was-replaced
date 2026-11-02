# Common problems

## The script uses a locked feature

Read its requirements, including the language features. Crop research and programming research are separate. Use an earlier version until the missing feature is unlocked.

If a script is meant for a square field, do not run it on the first 1×3 expansion. Use the first-column version instead.

## The drone moves over soil without planting carrots

Check hay and wood. Both are consumed when a carrot is planted. Farm the missing input and restart the carrot script.

Also check whether the tile already holds a growing carrot. A script that preserves young plants may correctly move on without planting again.

## Soil keeps turning back into grassland

`till()` toggles the ground. Run an unsensed preparation script once, then run its matching farming script. A sensed version checks `get_ground_type()` before tilling and can be restarted more safely.

## Trees are slow

Check the four orthogonal neighbors. Adjacent trees increase growth time. Use the spaced tree layout rather than replacing every bush or grass tile with a tree.

On odd fields, include the wrapped border in that check. A checkerboard that looks separated in the middle may place neighboring trees across the edge.

## Pumpkins never form a complete crop

Make sure dead pumpkins are being replaced and carrots remain in stock. A dead pumpkin never becomes harvestable on its own.

Stop other scripts that might harvest living pumpkins. Do not manually collect an individual cell while the full-field farm is finishing its repairs.

## Sunflowers produce less power than expected

The bonus depends on both the number of flowers and the petal count of the selected flower. Harvesting a lower-petal flower can also affect the next harvest. Keep the script's ordered harvest and replanting phases together.

If the field is too small for the minimum flower count, expand it before expecting the bonus.

## Polyculture is a mixture of plants, but the bonus is missing

The requested type must be at the requested position. Plant diversity by itself is not enough. Requests can conflict, and the planning scripts cannot satisfy every request simultaneously.

Keep the inputs for companion carrots stocked. The tree polyculture's optional water supply helps growth, but does not make an incompatible companion request count.

## Cactus numbers do not change after replanting

That is expected for immature cactus. Its size is retained when it is destroyed and replanted before maturity. Sort it with adjacent swaps instead of repeatedly buying a new planting on the same tile.

## More drones do not make everything proportionally faster

A field can have fewer useful tasks than available drones. Growth, collecting returned measurements, and the final harvest also limit throughput. The advanced scripts cap workers by the amount of work they can safely divide.

When a spawn fails, work is handled locally. This keeps the farm functional, but it may take longer than a run with every worker available.

## A maze map no longer matches the field

Start a fresh mapping pass for a new maze. A stored map describes one generation only. Reused mazes can gain passages, which is different from generating a completely new maze.

If gold farming stops, check Weird Substance and the current maze upgrade. The repeated-maze script collects the final treasure when another reuse is no longer affordable.

## The dinosaur stops moving

Check whether it reached the edge or its tail. Dinosaur movement does not wrap. A blocked move is part of ending some runs; changing hats collects the tail's payout.

If the shortcut version behaves poorly on a particular sequence, use the conservative route. Check the odd-size notes before using a route designed around an even field.

## An edited file does not appear in the game

Confirm the active save and the exact code-window name. Enable File Watcher for edits to existing files. Reload the save for externally added files, or create the window in-game and paste the code there.

Stop and restart after changing code. Existing drones continue the program they started with.
