# Running and editing the scripts

## Pick the right version first

Every script has a requirements entry in the [script index](script-index.md). Those requirements include programming features as well as crops. A script using a list is a later-stage script even if its only crop is grass.

The early versions are separate files so locked features do not have to be hidden inside a large universal program. Once functions and collections are available, the advanced farms can share a consistent structure without importing helper files.

## Paste a file into the game

Create a code window, give it the script's filename without `.py`, and paste the entire file. Stop any existing farm before starting another one on the same field.

Keep the indentation. These scripts use tabs. Do not paste Markdown fences such as ` ```python ` into the game window.

Base-game scripts are self-contained. DLC programs import local code windows: create the modules named in the [mining setup](dlc.md#installing-the-mining-programs) before starting a farm. You do not need Python packages or an editor stub. Unless a script's guide says otherwise, its entry call is already at the bottom.

## Use an external editor

The game stores code as `.py` files. On Windows, the usual save location is:

```text
%USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves
```

On macOS, look under:

```text
~/Library/Application Support/com.TheFarmerWasReplaced.TheFarmerWasReplaced/Saves
```

Steam/Proton installations keep the Windows-style save folder inside the game's compatibility prefix. Use the game's link to its save folder if your installation differs.

Open the active save folder in your editor. Enable **File Watcher** in the game to load edits to existing files. Newly created or deleted external files may require reloading the save. Creating the named window in-game first is another practical way to establish the file.

The save's generated `__builtins__.py` helps editor completion. Leave that generated file in the save; it is not one of the farm scripts and is not an implementation of the game.

## Similar to Python, with different rules

- Game functions and constants exist inside the game. CPython does not provide `move`, `plant`, or `Entities`.
- Use the supported game language rather than importing Python libraries.
- `None` is a possible result from measurements, companion queries, and failed drone spawns. Check it before unpacking or indexing.
- A new drone gets copied arguments and separate memory. Mutating its list does not update the parent's list.
- `wait_for()` retrieves a worker's result. A barrier between sorting phases prevents workers from exchanging cells while another worker still relies on the old measurements.
- `move()` normally wraps around the farm; cactus `swap()` does not wrap. Dinosaur movement does not wrap either.
- A successful `dig()` collects the block dug directly. Blocks removed by a cave-in give no resources. Check the return value as well as the resulting depth.
- `jump()` is a one-use shortcut for a program run. A later `clear()` does not grant another jump, and its return value is not a success flag.
- Mining workers must finish before a global reset. Crop growth and puzzle steps can also require barriers between phases.

## Restarting a farm

Stop the program, save the edit, and start it again. An external edit does not replace the code of a worker that is already running.

Changing field size resets the world in ways a running program must notice. The advanced crop farms rebuild their work distribution after detecting a change. Stopping and restarting after a research purchase is still a simple way to begin cleanly.

Avoid opening the same save for writing in several tools while switching saves. If a save write fails, stop the program, save the code windows, close tools holding those files, and retry from the game. Keep a backup of important saves.
