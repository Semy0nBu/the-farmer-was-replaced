def gr_sunflowers():
	while True:
		size = get_world_size()
		for col in range(size):
			for row in range(size):
				if get_world_size() != size:
					return
				if get_ground_type() != Grounds.Soil:
					till()
				ent = get_entity_type()
				if ent != Entities.Sunflower:
					if ent != None:
						harvest()
					if not plant(Entities.Sunflower):
						return
				if row < size - 1:
					move(North)
				else:
					move(East)
		left = size * size
		keep = 0
		if left >= 10:
			keep = 9
		for petals in range(15,6,-1):
			for col in range(size):
				for row in range(size):
					if get_world_size() != size:
						return
					if left > keep and get_entity_type() == Entities.Sunflower:
						if measure() == petals:
							while not can_harvest():
								if get_world_size() != size:
									return
							harvest()
							left -= 1
					if row < size - 1:
						move(North)
					else:
						move(East)

gr_sunflowers()
