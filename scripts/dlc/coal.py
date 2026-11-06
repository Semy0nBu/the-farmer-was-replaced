import dlc_common

last = None
rate = 0

def cr_worker(parts,size,layers,timeout):
	for depth in range(1,layers + 1):
		odd = depth % 2 == 1
		start_x = 0
		way = East
		up = North
		if not odd:
			start_x = size - 1
			way = West
			up = South
		for offset in range(len(parts)):
			index = offset
			if not odd:
				index = len(parts) - 1 - offset
			lo, hi = parts[index]
			y = lo
			if not odd:
				y = hi - 1
			if not dlc_common.go_to(start_x,y,size):
				return False
			for row in range(hi - lo):
				end = get_time() + timeout
				while get_pos_z(North) > 1 - depth or get_pos_z(South) > 1 - depth:
					if get_world_size() != size or get_time() > end:
						return False
				for x in range(size):
					if get_world_size() != size or get_pos_z() != 1 - depth:
						return False
					if not dig() or get_pos_z() != -depth:
						return False
					if x < size - 1 and not move(way):
						return False
				if row < hi - lo - 1:
					if not move(way) or not move(up):
						return False
	return True

def cr_world(parts,size,layers,timeout):
	own = [parts[0]]
	jobs = []
	for index in range(1,len(parts)):
		job = spawn_drone(cr_worker,[parts[index]],size,layers,timeout)
		if job == None:
			own.append(parts[index])
		else:
			jobs.append(job)
	ok = cr_worker(own,size,layers,timeout)
	for job in jobs:
		if dlc_common.wait_job(job,size) != True:
			ok = False
	return ok

def collect(size,layers=16,timeout=180):
	if layers < 1 or layers > 16 or timeout <= 0 or get_world_size() != size:
		return -1
	if not dlc_common.ready(Unlocks.Coal) or num_unlocked(Unlocks.Timing) == 0:
		return -1
	before = num_items(Items.Coal)
	if not cr_world(dlc_common.bands(size),size,layers,timeout):
		return -1
	return num_items(Items.Coal) - before

def gr_coal(rounds=0,layers=16,timeout=180):
	global last
	global rate
	if rounds < 0 or layers < 1 or layers > 16 or timeout <= 0 or dlc_common.current_count() != 1:
		return False
	if not dlc_common.ready(Unlocks.Coal) or num_unlocked(Unlocks.Timing) == 0:
		return False
	size = get_world_size()
	before = num_items(Items.Coal)
	start = get_time()
	done = 0
	empty = 0
	while rounds == 0 or done < rounds:
		if get_world_size() != size:
			return False
		dlc_common.reset()
		last = ("world",done + 1,num_items(Items.Coal) - before)
		mined = collect(size,layers,timeout)
		if mined < 0:
			return False
		elapsed = get_time() - start
		if elapsed > 0:
			rate = (num_items(Items.Coal) - before) * 60 / elapsed
		last = ("progress",done + 1,num_items(Items.Coal) - before,rate)
		if mined > 0:
			done += 1
			empty = 0
		else:
			empty += 1
			if empty >= 8:
				return False
	return True

if __name__ == "__main__":
	gr_coal()
