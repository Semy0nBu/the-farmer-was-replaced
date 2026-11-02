def gr_wood_hay():
	while True:
		size = get_world_size()
		if size < 2:
			return
		for step in range(size):
			diag = (get_pos_x() + get_pos_y()) % size
			wood = diag % 2 == 0 and diag < size - 1
			if wood:
				ent = get_entity_type()
				if ent != Entities.Tree:
					if ent != None:
						harvest()
					plant(Entities.Tree)
				elif can_harvest():
					harvest()
					plant(Entities.Tree)
			else:
				if get_ground_type() != Grounds.Grassland:
					till()
				ent = get_entity_type()
				if ent != None and ent != Entities.Grass:
					harvest()
				elif can_harvest():
					harvest()
			if step < size - 1:
				move(North)
			else:
				move(East)

gr_wood_hay()
