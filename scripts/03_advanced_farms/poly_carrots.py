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

def parallel_jobs(task,args,size):
	count = len(args)
	if count == 0:
		return []
	if count == 1:
		return [task(args[0],size)]
	mid = count // 2
	left = []
	right = []
	for i in range(mid):
		left.append(args[i])
	for i in range(mid,count):
		right.append(args[i])
	job = spawn_drone(parallel_jobs,task,right,size)
	res = parallel_jobs(task,left,size)
	if job == None:
		part = parallel_jobs(task,right,size)
	else:
		part = wait_job(job,size)
	if part == None:
		for i in range(len(right)):
			res.append(None)
	else:
		for value in part:
			res.append(value)
	return res

def parallel(task,args,size):
	return parallel_jobs(task,args,size)

def open_field():
	ent = get_entity_type()
	if ent == Entities.Hedge or ent == Entities.Treasure:
		harvest()

def split_tasks(flat,size):
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

def main_cell(x,y,size):
	if (x + y) % 2 != 0:
		return False
	if size > 1 and size % 2 == 1:
		if x == size - 1 or y == size - 1:
			return False
	return True

def put(crop,size):
	if get_world_size() != size:
		return False
	ent = get_entity_type()
	if ent == crop:
		return True
	if crop == Entities.Carrot:
		cost = get_cost(crop)
		for item in cost:
			if num_items(item) < cost[item]:
				return False
	if ent != None:
		harvest()
	if crop == Entities.Carrot:
		if get_ground_type() != Grounds.Soil:
			till()
	elif crop == Entities.Grass:
		if get_ground_type() != Grounds.Grassland:
			till()
	if get_entity_type() == crop:
		return True
	return plant(crop)

def farm_band(arg,size):
	lo, hi, crop, ready = arg
	reqs = []
	cur = []
	dir = East
	go_to(lo,0,size)
	for row in range(size):
		for col in range(hi - lo):
			if get_world_size() != size:
				return None
			x = get_pos_x()
			y = get_pos_y()
			if main_cell(x,y,size):
				if ready and get_entity_type() == crop and can_harvest():
					harvest()
				if not put(crop,size):
					return None
				req = get_companion()
				if req != None:
					reqs.append(req)
			else:
				if not ready and crop == Entities.Tree and get_entity_type() == Entities.Tree:
					if not put(Entities.Bush,size):
						return None
				cur.append((x + y * size,get_entity_type()))
			if col < hi - lo - 1:
				move(dir)
		move(North)
		if dir == East:
			dir = West
		else:
			dir = East
	return reqs, cur

def make_plan(res,size,crop):
	votes = {}
	for part in res:
		if part == None:
			return None
		reqs, old = part
		for req in reqs:
			kind = req[0]
			pos = req[1]
			x = pos[0]
			y = pos[1]
			if x < 0 or y < 0 or x >= size or y >= size:
				continue
			if main_cell(x,y,size) or kind == crop:
				continue
			if kind != Entities.Grass and kind != Entities.Bush and kind != Entities.Tree and kind != Entities.Carrot:
				continue
			key = x + y * size
			if key not in votes:
				votes[key] = {}
			score = votes[key]
			if kind not in score:
				score[kind] = 0
			score[kind] += 1
	tasks = []
	for part in res:
		reqs, old = part
		for pair in old:
			key, old_kind = pair
			kind = Entities.Bush
			if old_kind == Entities.Grass or old_kind == Entities.Bush or old_kind == Entities.Tree or old_kind == Entities.Carrot:
				kind = old_kind
			if crop == Entities.Tree and kind == Entities.Tree:
				kind = Entities.Bush
			if key in votes:
				score = votes[key]
				best = 0
				if kind in score:
					best = score[kind]
				for other in score:
					if score[other] > best:
						kind = other
						best = score[other]
			if old_kind != kind:
				tasks.append((key % size,key // size,kind))
	return split_tasks(tasks,size)

def supply(pos,size):
	for row in pos:
		if get_world_size() != size:
			return False
		x, y, crop = row
		go_to(x,y,size)
		if not put(crop,size):
			if get_world_size() != size or crop != Entities.Carrot:
				return False
	return True

def gr_poly(crop):
	if num_unlocked(Unlocks.Polyculture) == 0:
		return
	open_field()
	while True:
		size = get_world_size()
		args = []
		run = []
		for band in bands(size):
			lo, hi = band
			args.append((lo,hi,crop,False))
			run.append((lo,hi,crop,True))
		res = parallel(farm_band,args,size)
		while get_world_size() == size:
			tasks = make_plan(res,size,crop)
			if tasks == None:
				return
			done = parallel(supply,tasks,size)
			if get_world_size() != size:
				break
			for ok in done:
				if ok != True:
					return
			res = parallel(farm_band,run,size)
		while num_unlocked(Unlocks.Megafarm) > 0 and num_drones() > 1:
			pass

gr_poly(Entities.Carrot)
