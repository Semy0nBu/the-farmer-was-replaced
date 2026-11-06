import dlc_common

def adjacent(cell,size):
	x = cell % size
	y = cell // size
	return [x + ((y + 1) % size) * size,((x + 1) % size) + y * size,x + ((y - 1) % size) * size,((x - 1) % size) + y * size]

def make_jobs(size,rounds):
	holes = set()
	for y in range(size):
		for x in range(size):
			if (x + 2 * y) % 5 == 0:
				holes.add(x + y * size)
	if size % 5 == 2:
		for x in range(1,size,5):
			holes.add(x)
		for y in range(3,size,5):
			holes.add(size - 1 + y * size)
	for cell in range(size * size):
		if cell in holes:
			continue
		ok = False
		for other in adjacent(cell,size):
			if other in holes:
				ok = True
				break
		if not ok:
			holes.add(cell)
	backs = [North,East,South,West]
	ways = [South,West,North,East]
	jobs = []
	for band in dlc_common.bands(size):
		pos = []
		for y in range(band[0],band[1]):
			for col in range(size):
				x = col
				if y % 2 == 1:
					x = size - 1 - col
				cell = x + y * size
				if cell in holes:
					continue
				near = adjacent(cell,size)
				for i in range(4):
					if near[i] in holes:
						p = near[i]
						pos.append((x,y,p % size,p // size,ways[i],backs[i]))
						break
		jobs.append((pos,rounds))
	return jobs

def bamboo_job(arg,size):
	pos, rounds = arg
	pend = []
	for cell in pos:
		x, y, px, py, way, back = cell
		if not hover(18) or get_world_size() != size or not dlc_common.go_to(x,y,size):
			return False
		ground = get_ground_type()
		if ground != Grounds.Soil and ground != Grounds.Dirt and ground != Grounds.Perlite:
			till()
		if get_entity_type() != Entities.Bamboo:
			if get_entity_type() != None:
				harvest()
			if not plant(Entities.Bamboo):
				return False
		h = measure()
		if h == None or not move(back):
			return False
		pend.append((cell,h,get_time() + h + 1,0,0))
	while len(pend) > 0:
		next = []
		soon = -1
		for rec in pend:
			cell, h, due, stage, done = rec
			x, y, px, py, way, back = cell
			if get_world_size() != size:
				return False
			if get_time() >= due:
				if not hover(18) or not dlc_common.go_to(px,py,size):
					return False
				if stage == 2:
					if not hover(1) or not move(way) or get_entity_type() != Entities.Bamboo:
						return False
					nh = measure()
					if nh == None or not hover(18) or not move(back):
						return False
					done += 1
					if done >= rounds:
						continue
					due = get_time() + nh
					rec = (cell,nh,due,0,done)
				else:
					if not hover(h) or not move(way):
						return False
					nh = measure()
					ready = False
					if nh == h:
						ready = can_harvest()
					if nh == None or not move(back):
						return False
					if nh > h:
						due = get_time() + nh - h + 1
						rec = (cell,nh,due,stage + 1,done)
					elif ready:
						due = get_time()
						rec = (cell,h,due,2,done)
					else:
						due = get_time() + 1
						rec = (cell,h,due,stage,done)
			next.append(rec)
			if soon < 0 or due < soon:
				soon = due
		pend = next
		if len(pend) > 0:
			while get_time() < soon:
				if get_world_size() != size:
					return False
	return hover(18)

def single(size):
	if get_ground_type() != Grounds.Soil and get_ground_type() != Grounds.Perlite:
		till()
	if get_entity_type() != None:
		harvest()
	if not plant(Entities.Bamboo):
		return False
	h = measure()
	if h == None or not hover(18):
		return False
	due = get_time() + h + 1
	while get_time() < due:
		if get_world_size() != size:
			return False
	harvest()
	return True


def gr_bamboo(rounds=0,batch=8):
	if rounds < 0 or batch < 1 or dlc_common.current_count() != 1:
		return False
	if not dlc_common.ready(Unlocks.Bamboo) or num_unlocked(Unlocks.Timing) == 0:
		return False
	dlc_common.reset()
	change_hat(Hats.Gold_Hat)
	size = get_world_size()
	done = 0
	while rounds == 0 or done < rounds:
		if get_world_size() != size:
			return False
		count = batch
		if rounds > 0:
			count = min(count,rounds - done)
		if size == 1:
			if not single(size):
				return False
			done += 1
			continue
		res = dlc_common.parallel(bamboo_job,make_jobs(size,count),size)
		if res == None:
			return False
		for ok in res:
			if ok != True:
				return False
		done += count
	return True

if __name__ == "__main__":
	gr_bamboo()
