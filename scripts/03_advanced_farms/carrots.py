def go_to(x,y,size):
	dis = (x - get_pos_x()) % size
	dir = East
	if dis > size / 2:
		dis = size - dis
		dir = West
	for st in range(dis):
		move(dir)
	dis = (y - get_pos_y()) % size
	dir = North
	if dis > size / 2:
		dis = size - dis
		dir = South
	for st in range(dis):
		move(dir)

def drone_count(size):
	cnt = 1
	if num_unlocked(Unlocks.Megafarm) > 0:
		cnt = max_drones()
	if size < cnt:
		cnt = size
	return cnt

def bands(size):
	cnt = drone_count(size)
	args = []
	for i in range(cnt):
		args.append((size * i // cnt,size * (i + 1) // cnt))
	return args

def wait_job(job,size):
	while not has_finished(job):
		if get_world_size() != size or num_drones() < 2:
			if has_finished(job):
				break
			return None
	return wait_for(job)

def parallel(task,args,size):
	res = []
	jobs = []
	own = []
	for i in range(len(args)):
		res.append(None)
		if i == 0:
			own.append(i)
		else:
			job = spawn_drone(task,args[i],size)
			if job == None:
				own.append(i)
			else:
				jobs.append((i,job))
	for i in own:
		res[i] = task(args[i],size)
	for pair in jobs:
		i, job = pair
		res[i] = wait_job(job,size)
	return res

def open_field():
	ent = get_entity_type()
	if ent == Entities.Hedge or ent == Entities.Treasure:
		harvest()

def work_band(band,size):
	lo, hi = band
	dir = East
	go_to(lo,0,size)
	for cycle in range(8):
		for row in range(size):
			for col in range(hi - lo):
				if get_world_size() != size:
					return False
				if get_ground_type() != Grounds.Soil:
					till()
				ent = get_entity_type()
				if can_harvest():
					harvest()
					ent = None
				if ent != Entities.Carrot:
					if ent != None and ent != Entities.Dead_Pumpkin:
						harvest()
					if not plant(Entities.Carrot):
						return False
				if col < hi - lo - 1:
					move(dir)
			move(North)
			if dir == East:
				dir = West
			else:
				dir = East
	return True

def gr_carrot():
	open_field()
	while True:
		size = get_world_size()
		res = parallel(work_band,bands(size),size)
		if get_world_size() != size:
			while num_unlocked(Unlocks.Megafarm) > 0 and num_drones() > 1:
				pass
			continue
		for ok in res:
			if ok != True:
				return

gr_carrot()
