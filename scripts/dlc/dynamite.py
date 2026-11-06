import dlc_common

def neighbors(size,wrap):
	grid = []
	for y in range(size):
		for x in range(size):
			cells = []
			if not wrap:
				for ty in range(max(0,y - 1),min(size,y + 2)):
					for tx in range(max(0,x - 1),min(size,x + 2)):
						if tx != x or ty != y:
							cells.append(ty * size + tx)
				grid.append(cells)
				continue
			for dy in range(-1,2):
				for dx in range(-1,2):
					if dx == 0 and dy == 0:
						continue
					tx = x + dx
					ty = y + dy
					cell = (ty % size) * size + tx % size
					if cell != y * size + x and cell not in cells:
						cells.append(cell)
			grid.append(cells)
	return grid

def mark(cells,value,state,near,front,work,queued,safe):
	for cell in cells:
		old = state[cell]
		if old == 0:
			state[cell] = value
			if value == 3:
				safe.append(cell)
			for clue in near[cell]:
				if clue in front and clue not in queued:
					queued.add(clue)
					work.append(clue)
		elif (value == 2 and old != 2) or (value == 3 and old == 2):
			return False
	return True

def equations(state,counts,near,front):
	cons = []
	owners = {}
	for cell in front:
		left = counts[cell]
		unknown = []
		for other in near[cell]:
			if state[other] == 2:
				left -= 1
			elif state[other] == 0:
				unknown.append(other)
		if left < 0 or left > len(unknown):
			return None
		if len(unknown) == 0:
			continue
		idx = len(cons)
		cons.append((unknown,left))
		for other in unknown:
			if other not in owners:
				owners[other] = []
			owners[other].append(idx)
	return cons, owners

def overlap(cons,owners):
	for i in range(len(cons)):
		a, na = cons[i]
		checked = set()
		for cell in a:
			for j in owners[cell]:
				if j <= i or j in checked:
					continue
				checked.add(j)
				b, nb = cons[j]
				both = []
				a_only = []
				b_only = []
				for other in a:
					if other in b:
						both.append(other)
					else:
						a_only.append(other)
				for other in b:
					if other not in a:
						b_only.append(other)
				lo = max(0,na - len(a_only),nb - len(b_only))
				hi = min(len(both),na,nb)
				if lo > hi:
					return None
				parts = [[both,lo,hi],[a_only,na - hi,na - lo],[b_only,nb - hi,nb - lo]]
				for part in parts:
					cells, low, high = part
					if len(cells) == 0:
						continue
					if high == 0:
						return cells, 3
					if low == len(cells):
						return cells, 2
	return [], 0

def infer(state,counts,near,front,work):
	safe = []
	queued = set()
	for cell in work:
		queued.add(cell)
	head = 0
	while True:
		while head < len(work):
			cell = work[head]
			head += 1
			queued.remove(cell)
			if cell not in front:
				continue
			left = counts[cell]
			unknown = []
			for other in near[cell]:
				if state[other] == 2:
					left -= 1
				elif state[other] == 0:
					unknown.append(other)
			if left < 0 or left > len(unknown):
				return None
			if len(unknown) == 0:
				front.remove(cell)
			elif left == 0 or left == len(unknown):
				value = 2
				if left == 0:
					value = 3
				if not mark(unknown,value,state,near,front,work,queued,safe):
					return None
		if len(safe) > 0:
			return safe, [], {}
		result = equations(state,counts,near,front)
		if result == None:
			return None
		cons, owners = result
		result = overlap(cons,owners)
		if result == None:
			return None
		cells, value = result
		if len(cells) == 0:
			return safe, cons, owners
		if not mark(cells,value,state,near,front,work,queued,safe):
			return None

def distance(cell,x,y,size):
	dx = (cell % size - x) % size
	dy = (cell // size - y) % size
	return min(dx,size - dx) + min(dy,size - dy)

def open_cells(arg,size):
	cells, depth = arg
	pending = list(cells)
	res = []
	while len(pending) > 0:
		x = get_pos_x()
		y = get_pos_y()
		cell = pending[0]
		best = distance(cell,x,y,size)
		for other in pending:
			dis = distance(other,x,y,size)
			if dis < best:
				cell = other
				best = dis
		pending.remove(cell)
		if get_world_size() != size or not dlc_common.go_to(cell % size,cell // size,size):
			return res, -1
		for step in range(64):
			ground = get_ground_type()
			if ground == Grounds.Dynamite or ground == Grounds.Soot:
				break
			if get_pos_z() < depth - 2 or ground == Grounds.Bedrock or not dlc_common.dig_one():
				return res, -1
		if get_ground_type() == Grounds.Dynamite:
			if not dlc_common.dig_one():
				return res, -1
		if get_ground_type() != Grounds.Soot:
			return res, -1
		value = measure()
		if value == None:
			return res, 1
		res.append((cell,value))
	return res, 0

def open_batch(cells,depth,size):
	cnt = dlc_common.count_jobs(len(cells))
	args = []
	for i in range(cnt):
		part = []
		for j in range(len(cells) * i // cnt,len(cells) * (i + 1) // cnt):
			part.append(cells[j])
		args.append((part,depth))
	return dlc_common.parallel(open_cells,args,size)

def enclosed(state,near):
	total = 0
	for cell in range(len(state)):
		if state[cell] != 2:
			continue
		ok = True
		for other in near[cell]:
			if state[other] != 1 and state[other] != 2:
				ok = False
				break
		if ok:
			total += 1
	return total

def cashout(state,size):
	if get_ground_type() == Grounds.Soot:
		if measure() == None:
			return True
		return dlc_common.dig_one()
	for cell in range(len(state)):
		if state[cell] != 1:
			continue
		if get_world_size() != size or not dlc_common.go_to(cell % size,cell // size,size):
			return False
		if get_ground_type() == Grounds.Soot:
			if measure() == None:
				return True
			return dlc_common.dig_one()
	return False

def solve_safe(size,near,stop,phases=1024):
	depth = get_pos_z()
	state = []
	counts = []
	for cell in range(size * size):
		state.append(0)
		counts.append(-1)
	front = set()
	queue = [get_pos_y() * size + get_pos_x()]
	for phase in range(phases):
		parts = open_batch(queue,depth,size)
		if parts == None:
			return False,0
		work = []
		failed = False
		solved = False
		for part in parts:
			if part == None:
				failed = True
				continue
			opened, status = part
			if status == 1:
				solved = True
			if status < 0:
				failed = True
			for pair in opened:
				cell, value = pair
				state[cell] = 1
				counts[cell] = value
				front.add(cell)
				work.append(cell)
		if solved:
			return True,enclosed(state,near)
		if failed or get_time() >= stop or phase + 1 >= phases:
			break
		result = infer(state,counts,near,front,work)
		if result == None:
			break
		queue = result[0]
		if len(queue) == 0:
			break
	q = enclosed(state,near)
	return cashout(state,size),q

def seek(size,stop,limit):
	for step in range(limit):
		if get_world_size() != size or get_time() >= stop:
			return False
		if get_ground_type() == Grounds.Dynamite:
			return True
		if get_ground_type() == Grounds.Limestone:
			if not move(East):
				return False
		elif not dlc_common.dig_one():
			return False
	return get_ground_type() == Grounds.Dynamite

def gr_dynamite(rounds=0,seconds=600,depth_limit=2048,phases=1024):
	if rounds < 0 or seconds <= 0 or depth_limit < 1 or phases < 1 or dlc_common.current_count() != 1:
		return False
	if num_unlocked(Unlocks.Timing) == 0 or not dlc_common.begin(Unlocks.Dynamite):
		return False
	size = get_world_size()
	near = neighbors(size,False)
	done = 0
	empty = 0
	while rounds == 0 or done < rounds:
		if get_world_size() != size:
			return False
		if not seek(size,get_time() + seconds,1024):
			empty += 1
			if empty >= 3:
				return False
			dlc_common.reset()
			continue
		depth = -get_pos_z()
		before = num_items(Items.Dynamite)
		ok, count = solve_safe(size,near,get_time() + seconds,phases)
		gained = num_items(Items.Dynamite) - before
		if gained > 0:
			done += 1
			empty = 0
		else:
			empty += 1
			if empty >= 3:
				return False
		if get_world_size() != size:
			return False
		if not ok or gained <= 0 or depth >= depth_limit:
			dlc_common.reset()
	return True

if __name__ == "__main__":
	gr_dynamite()
