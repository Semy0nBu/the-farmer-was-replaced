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

def split_groups(groups,size):
	flat = []
	for group in groups:
		for pos in group:
			flat.append(pos)
	tot = len(flat)
	if tot == 0:
		return []
	cnt = drone_count(size)
	if cnt > tot:
		cnt = tot
	res = []
	for i in range(cnt):
		part = []
		for j in range(tot * i // cnt,tot * (i + 1) // cnt):
			part.append(flat[j])
		res.append(part)
	return res

def nearest_index(pos,size):
	x = get_pos_x()
	y = get_pos_y()
	best = 0
	best_dis = size * 2
	for i in range(len(pos)):
		tx, ty = pos[i]
		dx = (tx - x) % size
		dy = (ty - y) % size
		if dx > size / 2:
			dx = size - dx
		if dy > size / 2:
			dy = size - dy
		dis = dx + dy
		if dis < best_dis:
			best = i
			best_dis = dis
	return best

def seed_cell():
	if get_ground_type() != Grounds.Soil:
		till()
	ent = get_entity_type()
	if ent != Entities.Sunflower:
		if ent != None and ent != Entities.Dead_Pumpkin:
			harvest()
		if not plant(Entities.Sunflower):
			return None
	return measure()

def seed_band(band,size):
	lo, hi = band
	dir = East
	res = []
	go_to(lo,0,size)
	for row in range(size):
		for col in range(hi - lo):
			if get_world_size() != size:
				return None
			petals = seed_cell()
			if petals == None:
				return None
			res.append((get_pos_x(),get_pos_y(),petals))
			if col < hi - lo - 1:
				move(dir)
		move(North)
		if dir == East:
			dir = West
		else:
			dir = East
	return res

def pick(arg,size):
	pos, petals, region = arg
	done = []
	while len(pos) > 0:
		if get_world_size() != size:
			return None
		x, y = pos.pop(nearest_index(pos,size))
		go_to(x,y,size)
		if get_entity_type() != Entities.Sunflower or measure() != petals:
			return None
		while not can_harvest():
			if get_world_size() != size or get_entity_type() != Entities.Sunflower:
				return None
		harvest()
		done.append((x,y))
	return region, done

def refill(pos,size):
	res = []
	while len(pos) > 0:
		if get_world_size() != size:
			return None
		x, y = pos.pop()
		go_to(x,y,size)
		petals = seed_cell()
		if petals == None:
			return None
		res.append((x,y,petals))
	return res

def gr_sun():
	open_field()
	while True:
		size = get_world_size()
		if size * size < 10:
			return
		cnt = drone_count(size)
		res = parallel(seed_band,bands(size),size)
		if get_world_size() != size:
			while num_unlocked(Unlocks.Megafarm) > 0 and num_drones() > 1:
				pass
			continue
		flowers = [[], [], [], [], [], [], [], [], []]
		for part in res:
			if part == None:
				return
			for cell in part:
				x, y, petals = cell
				flowers[petals - 7].append((x,y))
		while get_world_size() == size:
			empty = []
			for i in range(cnt):
				empty.append([])
			rem = size * size
			for petals in range(15,6,-1):
				if rem <= 9:
					break
				groups = []
				for i in range(cnt):
					groups.append([])
				while len(flowers[petals - 7]) > 0 and rem > 9:
					x, y = flowers[petals - 7].pop()
					groups[x * cnt // size].append((x,y))
					rem -= 1
				groups = split_groups(groups,size)
				args = []
				for i in range(len(groups)):
					if len(groups[i]) > 0:
						args.append((groups[i],petals,i))
				res = parallel(pick,args,size)
				if get_world_size() != size:
					break
				for part in res:
					if part == None:
						return
					region, done = part
					for pos in done:
						empty[region].append(pos)
			if get_world_size() != size:
				break
			args = split_groups(empty,size)
			res = parallel(refill,args,size)
			if get_world_size() != size:
				break
			for part in res:
				if part == None:
					return
				for cell in part:
					x, y, petals = cell
					flowers[petals - 7].append((x,y))
		while num_unlocked(Unlocks.Megafarm) > 0 and num_drones() > 1:
			pass

gr_sun()
