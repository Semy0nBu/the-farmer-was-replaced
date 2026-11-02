def cycle_dir(x,y,size):
	if x == 0:
		if y < size - 1:
			return North
		return East
	if y == 0:
		return West
	row = size - 1 - y
	if row % 2 == 0:
		if x < size - 1:
			return East
		return South
	if x > 1:
		return West
	return South

def grow_path(size):
	dir = East
	for row in range(size):
		for col in range(size - 1):
			if get_world_size() != size:
				return True
			if not move(dir):
				return True
		if row < size - 1:
			if get_world_size() != size or not move(North):
				return True
		if dir == East:
			dir = West
		else:
			dir = East
	return True

def grow_cycle(size):
	tot = size * size
	while get_world_size() == size:
		before = num_items(Items.Cactus)
		for step in range(tot):
			if get_world_size() != size:
				return True
			dir = cycle_dir(get_pos_x(),get_pos_y(),size)
			if not move(dir):
				return True
		if num_items(Items.Cactus) >= before:
			return False
	return True

def gr_dino():
	if num_unlocked(Unlocks.Dinosaurs) == 0:
		return
	change_hat(Hats.Gold_Hat)
	while True:
		size = get_world_size()
		if size < 2 or num_items(Items.Cactus) == 0:
			return
		clear()
		change_hat(Hats.Dinosaur_Hat)
		if get_entity_type() != Entities.Apple:
			change_hat(Hats.Gold_Hat)
			return
		if size % 2 == 0:
			again = grow_cycle(size)
		else:
			again = grow_path(size)
		change_hat(Hats.Gold_Hat)
		if not again:
			return

gr_dino()
