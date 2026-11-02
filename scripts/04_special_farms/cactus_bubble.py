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

def fill_row(size):
	for col in range(size):
		if get_world_size() != size:
			return False
		if get_ground_type() != Grounds.Soil:
			till()
		ent = get_entity_type()
		if ent != Entities.Cactus:
			if ent != None and ent != Entities.Dead_Pumpkin:
				harvest()
			if not plant(Entities.Cactus):
				return False
		if col < size - 1:
			move(East)
	return True

def ripe(size):
	while not can_harvest():
		if get_world_size() != size or get_entity_type() != Entities.Cactus:
			return False
	return True

def sort_line(dir,size,ready):
	limit = size - 1
	if limit == 0 and ready:
		return ripe(size)
	while limit > 0:
		last_swap = -1
		a = measure()
		for pos in range(limit):
			if get_world_size() != size:
				return False
			b = measure(dir)
			if a == None or b == None:
				return False
			if a > b:
				if not swap(dir):
					return False
				last_swap = pos
			else:
				a = b
			if ready and not ripe(size):
				return False
			move(dir)
		if ready and not ripe(size):
			return False
		if dir == East:
			go_to(0,get_pos_y(),size)
		else:
			go_to(get_pos_x(),0,size)
		if last_swap < 0:
			break
		limit = last_swap
	return True

def rows(band,size):
	lo, hi = band
	for row in range(lo,hi):
		go_to(0,row,size)
		if not fill_row(size):
			return False
		go_to(0,row,size)
		if not sort_line(East,size,False):
			return False
	return True

def cols(band,size):
	lo, hi = band
	for col in range(lo,hi):
		go_to(col,0,size)
		if not sort_line(North,size,True):
			return False
	return True

def phase(task,size):
	res = parallel(task,bands(size),size)
	for ok in res:
		if ok != True:
			return False
	return True

def gr_cactus():
	if num_unlocked(Unlocks.Cactus) == 0:
		return
	open_field()
	while True:
		size = get_world_size()
		if not phase(rows,size):
			if get_world_size() != size:
				while num_unlocked(Unlocks.Megafarm) > 0 and num_drones() > 1:
					pass
				continue
			return
		if not phase(cols,size):
			if get_world_size() != size:
				while num_unlocked(Unlocks.Megafarm) > 0 and num_drones() > 1:
					pass
				continue
			return
		if get_world_size() != size:
			continue
		go_to(0,0,size)
		if not ripe(size):
			return
		harvest()

gr_cactus()
