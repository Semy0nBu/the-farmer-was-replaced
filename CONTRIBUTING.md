# Contributing

Useful changes make a farm easier to run, remove unnecessary work, or fix a real failure. A shorter script is welcome when it remains correct for the stage it targets.

For a bug report, include the script name, field size, available drone count, relevant unlocked research, and the exact error or visible behavior. Inventory shortages matter too. A save file is usually unnecessary.

For a change:

1. Use tabs for indentation. Keep base-game scripts self-contained; DLC programs may import the documented local mining modules.
2. Add or update its `catalog.json` entry and guide.
3. Preserve the earliest requirements of an existing early-stage script, or add a separate later version.
4. Check one drone, small fields, odd fields where applicable, and failed plantings or worker spawns.
5. Run `node tools/check.mjs`.

Performance reports should state the game version, field size, drone count, research levels, starting resources, measured task, and number of runs. Use matching simulation seeds and starting conditions when comparing alternatives. Include setup time if setup is part of normal use.

Keep model results separate from measurements in the game. A faster run that harvested less, stopped early, or used different research is not a fair comparison. Avoid calling a method optimal without a proof and a stated cost model.

Keep base-game mechanics in the numbered stage folders and mining mechanics in `scripts/dlc`. Document imported code-window names and include a guarded entry point so an import cannot start a second farm. Keep leaderboard submissions, saves, game assets, and generated editor stubs out of the collection.
