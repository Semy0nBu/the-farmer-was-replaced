import dlc_common
import coal

def iron_job(arg,size):
	x, y, budget, prospect = arg
	if not dlc_common.go_to(x,y,size):
		return -1
	mined = 0
	for step in range(64):
		if get_world_size() != size:
			return -1
		ground = get_ground_type()
		if ground == Grounds.Rock or ground == Grounds.Iron:
			break
		if not dlc_common.dig_one():
			return 0
	dirs = [North,East,South,West]
	floor = get_pos_z() - 32
	dig_left = 0
	for step in range(128):
		if get_world_size() != size:
			return -1
		if get_ground_type() == Grounds.Iron:
			if not dlc_common.dig_one():
				break
			mined += 1
			continue
		near = False
		for dir in dirs:
			if get_ground_type(dir) == Grounds.Iron:
				if not move(dir):
					return -1
				near = True
				break
		if near:
			continue
		if get_pos_z() < floor:
			break
		if dig_left > 0:
			dig_left -= 1
		elif prospect:
			if budget == 0 or num_items(Items.Coal) == 0:
				break
			dir = prospect_iron()
			budget -= 1
			if dir != None:
				if not move(dir):
					return -1
				continue
			dig_left = 7
		if not dlc_common.dig_one():
			break
	return mined

def iron_args(size):
	cnt = dlc_common.count_jobs(size * size)
	prospect = num_unlocked(Unlocks.Prospecting) > 0
	budget = 0
	if prospect:
		budget = num_items(Items.Coal) // cnt
		if budget > 24:
			budget = 24
	nx = 1
	while nx * nx < cnt:
		nx += 1
	ny = (cnt + nx - 1) // nx
	args = []
	for i in range(cnt):
		x = (i % nx) * size // nx
		y = (i // nx) * size // ny
		args.append((x,y,budget,prospect))
	return args

def collect(size):
	res = dlc_common.parallel(iron_job,iron_args(size),size)
	if res == None:
		return -1
	total = 0
	for part in res:
		if part == None or part < 0:
			return -1
		total += part
	return total

def gr_iron(rounds=0):
	if dlc_common.current_count() != 1 or not dlc_common.ready(Unlocks.Iron):
		return False
	dlc_common.reset()
	jumped = False
	done = 0
	prospect = num_unlocked(Unlocks.Prospecting) > 0
	while True:
		size = get_world_size()
		if prospect:
			need = dlc_common.count_jobs(size * size) * 4
			empty = 0
			while num_items(Items.Coal) < need:
				if not dlc_common.ready(Unlocks.Coal):
					return False
				dlc_common.reset()
				before = num_items(Items.Coal)
				if coal.collect(size) < 0:
					return False
				if num_items(Items.Coal) <= before:
					empty += 1
					if empty >= 8:
						return False
		if not jumped and num_unlocked(Unlocks.Jump) > 0:
			jump(Unlocks.Iron)
			jumped = True
		mined = collect(size)
		if mined < 0:
			return False
		if mined > 0:
			done += 1
			if rounds > 0 and done >= rounds:
				return True
		if mined == 0 or not prospect:
			dlc_common.reset()

if __name__ == "__main__":
	gr_iron()
