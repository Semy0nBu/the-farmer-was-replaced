for col in range(get_world_size()):
	for row in range(get_world_size()):
		till()
		if row < get_world_size() - 1:
			move(North)
		else:
			move(East)
