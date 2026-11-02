def gr_cactus():
	while get_pos_x() != 0:
		move(West)
	while get_pos_y() != 0:
		move(South)
	while True:
		size = get_world_size()
		for row in range(size):
			for col in range(size):
				if get_world_size() != size:
					return
				if get_ground_type() != Grounds.Soil:
					till()
				ent = get_entity_type()
				if ent != Entities.Cactus:
					if ent != None:
						harvest()
					if not plant(Entities.Cactus):
						return
				move(East)
			move(North)
		for row in range(size):
			changed = True
			while changed:
				changed = False
				for col in range(size):
					if get_world_size() != size:
						return
					if col < size - 1 and measure() > measure(East):
						if not swap(East):
							return
						changed = True
					move(East)
			move(North)
		for col in range(size):
			changed = True
			while changed:
				changed = False
				for row in range(size):
					if get_world_size() != size:
						return
					if row < size - 1 and measure() > measure(North):
						if not swap(North):
							return
						changed = True
					move(North)
			move(East)
		for col in range(size):
			for row in range(size):
				while not can_harvest():
					if get_world_size() != size:
						return
				move(North)
			move(East)
		harvest()

gr_cactus()
