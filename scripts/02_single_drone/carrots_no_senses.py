size = get_world_size()
ok = True
for col in range(size):
	for row in range(size):
		if not plant(Entities.Carrot):
			ok = False
			break
		if row < size - 1:
			move(North)
		else:
			move(East)
	if not ok:
		break

while ok:
	for step in range(size):
		if can_harvest():
			harvest()
			if not plant(Entities.Carrot):
				ok = False
				break
		if step < size - 1:
			move(North)
		else:
			move(East)
