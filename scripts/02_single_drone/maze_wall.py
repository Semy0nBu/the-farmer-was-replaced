def gr_maze():
	if get_entity_type() == Entities.Hedge:
		return
	while True:
		size = get_world_size()
		amount = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		if num_items(Items.Weird_Substance) < amount:
			return
		if get_entity_type() != None:
			harvest()
		if not plant(Entities.Bush):
			return
		if not use_item(Items.Weird_Substance,amount):
			return
		face = 0
		steps = 0
		while get_entity_type() != Entities.Treasure:
			if get_world_size() != size or steps >= 4 * size * size:
				return
			face = (face + 3) % 4
			moved = False
			for turn in range(4):
				dir = North
				if face == 1:
					dir = East
				elif face == 2:
					dir = South
				elif face == 3:
					dir = West
				if move(dir):
					moved = True
					break
				face = (face + 1) % 4
			if not moved:
				return
			steps += 1
		harvest()

gr_maze()
