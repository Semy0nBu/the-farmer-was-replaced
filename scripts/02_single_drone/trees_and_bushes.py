while True:
	size = get_world_size()
	for step in range(size):
		diag = (get_pos_x() + get_pos_y()) % size
		want = Entities.Bush
		if diag % 2 == 0 and diag < size - 1:
			want = Entities.Tree
		ent = get_entity_type()
		if ent != want:
			if ent != None:
				harvest()
			plant(want)
		elif can_harvest():
			harvest()
			plant(want)
		if step < size - 1:
			move(North)
		else:
			move(East)
