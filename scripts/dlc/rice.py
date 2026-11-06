import dlc_common

def prepare_band(arg,size):
	lo, hi, floor = arg
	ready = []
	for y in range(lo,hi):
		for col in range(size):
			x = col
			if y % 2 == 1:
				x = size - 1 - col
			if get_world_size() != size or not dlc_common.go_to(x,y,size):
				return None
			while True:
				ground = get_ground_type()
				if ground == Grounds.Clay:
					break
				if ground == Grounds.Rock or ground == Grounds.Bedrock or get_pos_z() < floor:
					break
				if not dlc_common.dig_one():
					break
			if get_ground_type() == Grounds.Clay:
				ready.append((x,y))
	return ready

def rice_band(ready,size):
	pend = []
	for i in range(len(ready) - 1,-1,-1):
		x, y = ready[i]
		if get_world_size() != size or not dlc_common.go_to(x,y,size):
			return -1
		if get_ground_type() == Grounds.Clay:
			if not plant(Entities.Rice):
				return -1
			pend.append((x,y))
	count = len(pend)
	while len(pend) > 0:
		next = []
		for i in range(len(pend) - 1,-1,-1):
			x, y = pend[i]
			if get_world_size() != size or not dlc_common.go_to(x,y,size):
				return -1
			if get_entity_type() != Entities.Rice:
				return -1
			if can_harvest():
				harvest()
			else:
				next.append((x,y))
		pend = next
	return count

def gr_rice(rounds=0):
	if not dlc_common.begin(Unlocks.Rice):
		return
	done = 0
	while True:
		size = get_world_size()
		if not dlc_common.seek(Grounds.Clay):
			dlc_common.reset()
			continue
		floor = get_pos_z() - 8
		args = []
		for band in dlc_common.bands(size):
			args.append((band[0],band[1],floor))
		while True:
			res = dlc_common.parallel(prepare_band,args,size)
			if res == None:
				return
			ready = []
			for part in res:
				if part == None:
					return
				if len(part) > 0:
					ready.append(part)
			if len(ready) == 0:
				break
			res = dlc_common.parallel(rice_band,ready,size)
			if res == None:
				return
			total = 0
			for part in res:
				if part < 0:
					return
				total += part
			if total == 0:
				break
			done += 1
			if rounds > 0 and done >= rounds:
				return True
		dlc_common.reset()

if __name__ == "__main__":
	gr_rice()
