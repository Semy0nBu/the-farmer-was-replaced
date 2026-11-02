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

def wait_job(job,size):
	while not has_finished(job):
		if get_world_size() != size or num_drones() < 2:
			if has_finished(job):
				break
			return None
	return wait_for(job)

def prep_band(lo,hi,size):
	pend = []
	dir = East
	go_to(lo,0,size)
	for row in range(size):
		for col in range(hi - lo):
			if get_world_size() != size:
				return None
			if get_ground_type() != Grounds.Soil:
				till()
			ent = get_entity_type()
			if ent != Entities.Pumpkin:
				if ent != None and ent != Entities.Dead_Pumpkin:
					harvest()
				if not plant(Entities.Pumpkin):
					return None
				pend.append((get_pos_x(),row))
			elif not can_harvest():
				pend.append((get_pos_x(),row))
			if col < hi - lo - 1:
				move(dir)
		if row < size - 1:
			move(North)
		if dir == East:
			dir = West
		else:
			dir = East
	return pend

def check_pump(pend,size):
	while len(pend) > 0:
		rem = []
		for pos in pend:
			if get_world_size() != size:
				return False
			x, y = pos
			go_to(x,y,size)
			if get_world_size() != size:
				return False
			ent = get_entity_type()
			if ent == Entities.Pumpkin:
				if can_harvest():
					continue
			else:
				if get_ground_type() != Grounds.Soil:
					till()
				if ent != None and ent != Entities.Dead_Pumpkin:
					harvest()
				if not plant(Entities.Pumpkin):
					return False
			rem.append(pos)
		pend = rem
	return True

def pump_band(lo,hi,size):
	pend = prep_band(lo,hi,size)
	if pend == None:
		return False
	return check_pump(pend,size)

def pump_jobs(lo,hi,size,slots):
	if slots == 1:
		return pump_band(lo,hi,size)
	left = slots // 2
	mid = lo + (hi - lo) * left // slots
	job = spawn_drone(pump_jobs,mid,hi,size,slots - left)
	ok = pump_jobs(lo,mid,size,left)
	if job == None:
		other = pump_jobs(mid,hi,size,slots - left)
	else:
		other = wait_job(job,size)
	return ok and other == True

def gr_pump():
	if num_unlocked(Unlocks.Pumpkins) == 0:
		return
	ent = get_entity_type()
	if ent == Entities.Hedge or ent == Entities.Treasure:
		harvest()
	while True:
		size = get_world_size()
		ok = pump_jobs(0,size,size,drone_count(size))
		if get_world_size() != size:
			while num_unlocked(Unlocks.Megafarm) > 0 and num_drones() > 1:
				pass
			continue
		if not ok:
			return
		harvest()

gr_pump()
