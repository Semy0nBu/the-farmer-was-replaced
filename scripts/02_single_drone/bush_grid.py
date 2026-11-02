while True:
	for col in range(get_world_size()):
		for row in range(get_world_size()):
			if can_harvest():
				harvest()
			plant(Entities.Bush)
			move(North)
		move(East)
