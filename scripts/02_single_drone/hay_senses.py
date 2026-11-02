while True:
	size = get_world_size()
	for step in range(size):
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
