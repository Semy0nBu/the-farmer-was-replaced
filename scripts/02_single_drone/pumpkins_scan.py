def gr_pumpkins():
	while True:
		size = get_world_size()
		ready = True
		for col in range(size):
			for row in range(size):
				if get_world_size() != size:
					return
				if get_ground_type() != Grounds.Soil:
					till()
				ent = get_entity_type()
				if ent != Entities.Pumpkin:
					if ent != None and ent != Entities.Dead_Pumpkin:
						harvest()
					if not plant(Entities.Pumpkin):
						return
					ready = False
				elif not can_harvest():
					ready = False
				if row < size - 1:
					move(North)
				else:
					move(East)
		if ready:
			harvest()

gr_pumpkins()
