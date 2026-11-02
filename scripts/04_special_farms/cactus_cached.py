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

def seed_row(size):
	a = []
	for col in range(size):
		if get_world_size() != size:
			return None
		if get_ground_type() != Grounds.Soil:
			till()
		ent = get_entity_type()
		if ent != Entities.Cactus:
			if ent != None and ent != Entities.Dead_Pumpkin:
				harvest()
			if not plant(Entities.Cactus):
				return None
		v = measure()
		if v == None:
			return None
		a.append(v)
		if col < size - 1:
			move(East)
	return a

def trouble(a,pos,size):
	cnt = 0
	if pos > 0 and a[pos - 1] > a[pos]:
		cnt += 1
	if pos < size - 1 and a[pos] > a[pos + 1]:
		cnt += 1
	if pos > 0 and pos < size - 1 and a[pos - 1] > a[pos + 1]:
		cnt += 1
	return cnt

def sort_cache(a,dir,size):
	back = South
	pos = get_pos_y()
	if dir == East:
		back = West
		pos = get_pos_x()
	while True:
		if get_world_size() != size:
			return False
		if pos > 0 and a[pos - 1] > a[pos]:
			if get_world_size() != size or not swap(back):
				return False
			v = a[pos]
			a[pos] = a[pos - 1]
			a[pos - 1] = v
		if pos < size - 1 and a[pos] > a[pos + 1]:
			if get_world_size() != size or not swap(dir):
				return False
			v = a[pos]
			a[pos] = a[pos + 1]
			a[pos + 1] = v
		if pos > 0 and a[pos - 1] > a[pos]:
			if get_world_size() != size or not swap(back):
				return False
			v = a[pos]
			a[pos] = a[pos - 1]
			a[pos - 1] = v
		dist = -1
		for step in range(1,size // 2 + 1):
			left = (pos - step) % size
			right = (pos + step) % size
			ls = trouble(a,left,size)
			rs = trouble(a,right,size)
			if ls > 0 or rs > 0:
				dist = step
				if ls >= rs:
					next = left
					way = back
				else:
					next = right
					way = dir
				break
		if dist < 0:
			return True
		for step in range(dist):
			if get_world_size() != size or not move(way):
				return False
		pos = next

def ripe(size):
	while not can_harvest():
		if get_world_size() != size or get_entity_type() != Entities.Cactus:
			return False
	return True

def mature_line(size):
	for row in range(size):
		if get_world_size() != size or not ripe(size):
			return False
		if row < size - 1:
			if not move(North):
				return False
	return True

def rows(band,size):
	lo, hi = band
	res = []
	for row in range(lo,hi):
		go_to(0,row,size)
		a = seed_row(size)
		if a == None or not sort_cache(a,East,size):
			return None
		res.append((row,a))
	return res

def cols(arg,size):
	lo, hi, grid = arg
	for col in range(lo,hi):
		a = []
		for row in grid:
			a.append(row[col])
		go_to(col,0,size)
		if not sort_cache(a,North,size):
			return False
		if not mature_line(size):
			return False
	return True

def gr_cactus():
	if num_unlocked(Unlocks.Cactus) == 0:
		return
	open_field()
	while True:
		size = get_world_size()
		res = parallel(rows,bands(size),size)
		if get_world_size() != size:
			while num_unlocked(Unlocks.Megafarm) > 0 and num_drones() > 1:
				pass
			continue
		grid = []
		for row in range(size):
			grid.append(None)
		for part in res:
			if part == None:
				return
			for pair in part:
				row, a = pair
				grid[row] = a
		args = []
		for band in bands(size):
			lo, hi = band
			args.append((lo,hi,grid))
		res = parallel(cols,args,size)
		if get_world_size() != size:
			while num_unlocked(Unlocks.Megafarm) > 0 and num_drones() > 1:
				pass
			continue
		for ok in res:
			if ok != True:
				return
		go_to(0,0,size)
		if get_world_size() != size or not ripe(size):
			continue
		harvest()

gr_cactus()
