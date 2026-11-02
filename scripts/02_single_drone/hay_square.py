while True:
	for step in range(get_world_size()):
		if can_harvest():
			harvest()
		if step < get_world_size() - 1:
			move(North)
		else:
			move(East)
