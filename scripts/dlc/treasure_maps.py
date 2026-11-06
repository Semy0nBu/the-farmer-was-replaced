import dlc_common

def treasure(size):
	if not dlc_common.seek(Grounds.Basalt):
		return False
	depth = get_pos_z() - 1
	pos = measure()
	if pos == None or not dlc_common.go_to(pos[0],pos[1],size):
		return False
	while get_ground_type() != Grounds.Treasure_Map:
		if get_world_size() != size or get_pos_z() < depth or not dlc_common.dig_one():
			return False
	path = measure()
	if path == None or len(path) == 0:
		return False
	if path[0] != "D":
		if not dlc_common.dig_one():
			return False
	dirs = {"N":North,"E":East,"S":South,"W":West}
	for letter in path:
		if get_world_size() != size:
			return False
		if letter == "D":
			if not dlc_common.dig_one():
				return False
		elif letter in dirs:
			if not move(dirs[letter]):
				return False
		else:
			return False
	if get_entity_type() == Entities.Underground_Treasure:
		return harvest()
	return False

def gr_treasure(rounds=0):
	if not dlc_common.begin(Unlocks.Treasure_Map):
		return False
	done = 0
	while True:
		ok = treasure(get_world_size())
		if rounds > 0:
			if not ok:
				return False
			done += 1
			if done >= rounds:
				return True
		dlc_common.reset()

if __name__ == "__main__":
	gr_treasure()
