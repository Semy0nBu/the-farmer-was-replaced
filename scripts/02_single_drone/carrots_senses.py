def gr_carrots():
	while True:
		size = get_world_size()
		for step in range(size):
			if get_ground_type() != Grounds.Soil:
				till()
			ent = get_entity_type()
			seed = False
			if ent == Entities.Carrot:
				if can_harvest():
					harvest()
					seed = True
			else:
				if ent != None:
					harvest()
				seed = True
			if seed and not plant(Entities.Carrot):
				return
			if step < size - 1:
				move(North)
			else:
				move(East)

gr_carrots()
