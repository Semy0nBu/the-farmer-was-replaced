ds = [North, East, South, West]
xs = [0, 1, 0, -1]
ys = [1, 0, -1, 0]

def wait_map(job,size):
	while not has_finished(job):
		if get_world_size() != size or num_drones() < 2:
			if has_finished(job):
				break
			return None, None, None
	return wait_for(job)

def scan(cur,size,g,edges=None):
	x = cur % size
	y = cur // size
	changed = False
	for d in range(4):
		if can_move(ds[d]):
			nxt = (x + xs[d]) % size + ((y + ys[d]) % size) * size
			if g[cur][d] != nxt:
				g[cur][d] = nxt
				g[nxt][(d + 2) % 4] = cur
				changed = True
				if edges != None:
					edges.append((cur,d,nxt))
	return changed

def map_maze(size,first=-1,slots=1):
	g = []
	for cell in range(size * size):
		g.append([-1, -1, -1, -1])
	cur = get_pos_x() + get_pos_y() * size
	seen = {cur: True}
	checked = {}
	cells = []
	if first != -1:
		scan(cur,size,g)
		checked[cur] = True
		cells.append(cur)
		if not move(ds[first]):
			return None, None, None
		cur = g[cur][first]
		seen[cur] = True
	stack = []
	jobs = []
	valid = True
	while True:
		ent = get_entity_type()
		if get_world_size() != size or (ent != Entities.Hedge and ent != Entities.Treasure):
			valid = False
			break
		if cur not in checked:
			scan(cur,size,g)
			checked[cur] = True
			cells.append(cur)
		if len(jobs) == 0 and len(seen) == size * size:
			break
		dir = -1
		options = 0
		for d in range(4):
			nxt = g[cur][d]
			if nxt != -1 and nxt not in seen:
				if dir == -1:
					dir = d
				options += 1
		if options > 1 and slots > 1:
			part = slots // 2
			job = spawn_drone(map_maze,size,dir,part)
			if job != None:
				jobs.append(job)
				seen[g[cur][dir]] = True
				slots -= part
				continue
		if dir == -1:
			if len(stack) == 0:
				break
			dir = (stack.pop() + 2) % 4
			if not move(ds[dir]):
				valid = False
				break
			cur = g[cur][dir]
		else:
			if not move(ds[dir]):
				valid = False
				break
			stack.append(dir)
			cur = g[cur][dir]
			seen[cur] = True
	for job in jobs:
		part, pos, marked = wait_map(job,size)
		if part == None:
			valid = False
		else:
			for cell in marked:
				if cell not in checked:
					checked[cell] = True
					cells.append(cell)
					g[cell] = part[cell]
	if not valid:
		return None, None, None
	return g, cur, cells

def has_wrap(g,size):
	for i in range(size):
		if g[i][2] != -1 or g[i + size * (size - 1)][0] != -1:
			return True
		if g[i * size][3] != -1 or g[i * size + size - 1][1] != -1:
			return True
	return False

def lower_bound(cur,goal,size,wrap=True):
	dx = goal % size - cur % size
	dy = goal // size - cur // size
	if dx < 0:
		dx = -dx
	if dy < 0:
		dy = -dy
	if wrap and dx > size / 2:
		dx = size - dx
	if wrap and dy > size / 2:
		dy = size - dy
	return dx + dy

def route(g,cur,goal,size,wrap=None):
	if wrap == None:
		wrap = has_wrap(g,size)
	path = []
	pos = cur
	dis = lower_bound(pos,goal,size,wrap)
	while dis > 0:
		dir = -1
		for d in range(4):
			nxt = g[pos][d]
			if nxt != -1 and lower_bound(nxt,goal,size,wrap) == dis - 1:
				dir = d
				break
		if dir == -1:
			break
		path.append(dir)
		pos = g[pos][dir]
		dis -= 1
	if pos == goal:
		return path
	back = {goal: -1}
	queue = [goal]
	head = 0
	while head < len(queue) and cur not in back:
		pos = queue[head]
		head += 1
		for d in range(4):
			nxt = g[pos][d]
			if nxt != -1 and nxt not in back:
				back[nxt] = (d + 2) % 4
				queue.append(nxt)
				if nxt == cur:
					break
	if cur not in back:
		return None
	path = []
	while cur != goal:
		dir = back[cur]
		path.append(dir)
		cur = g[cur][dir]
	return path

def bases_for(g,size,cnt):
	near = []
	home = []
	for cell in range(len(g)):
		near.append(-1)
		home.append(-1)
	bases = []
	cur = size // 2 + (size // 2) * size
	for i in range(cnt):
		if i > 0:
			cur = -1
			best = 0
			for cell in range(len(g)):
				if near[cell] > best:
					cur = cell
					best = near[cell]
			if cur == -1:
				break
		bases.append(cur)
		near[cur] = 0
		home[cur] = i
		queue = [cur]
		head = 0
		while head < len(queue):
			pos = queue[head]
			head += 1
			dis = near[pos] + 1
			for nxt in g[pos]:
				if nxt != -1 and (near[nxt] == -1 or dis < near[nxt]):
					near[nxt] = dis
					home[nxt] = i
					queue.append(nxt)
	return bases, home

def station(g,home,bases,me,mine,size,lvl,amount,start):
	cur = get_pos_x() + get_pos_y() * size
	base = bases[me]
	dest = -1
	path = []
	head = 0
	wrap = has_wrap(g,size)
	while True:
		if get_world_size() != size:
			return False
		ent = get_entity_type()
		if ent != Entities.Hedge and ent != Entities.Treasure:
			return True
		pos = measure()
		if pos == None:
			return False
		goal = pos[0] + pos[1] * size
		target = base
		if home[goal] in mine:
			target = goal
		if cur == target:
			if cur == goal and home[goal] in mine:
				stock = num_items(Items.Weird_Substance)
				spent = start - stock
				if spent < 0 or spent % amount != 0 or spent // amount >= 300 or stock < amount or num_unlocked(Unlocks.Mazes) != lvl:
					harvest()
					return True
				gold = num_items(Items.Gold)
				if not use_item(Items.Weird_Substance,amount):
					if get_world_size() == size and get_entity_type() == Entities.Treasure:
						harvest()
						return True
					return False
				if num_items(Items.Gold) <= gold:
					if get_world_size() == size and get_entity_type() == Entities.Treasure:
						harvest()
						return True
				dest = -1
			else:
				for idle in range(32):
					pass
			continue
		changed = scan(cur,size,g)
		if changed:
			wrap = has_wrap(g,size)
		if target != dest or (changed and len(path) - head > lower_bound(cur,target,size,wrap)):
			path = route(g,cur,target,size,wrap)
			head = 0
			dest = target
			if path == None:
				return False
		dir = path[head]
		if not move(ds[dir]):
			return False
		cur = g[cur][dir]
		head += 1

def join_stations(jobs,size):
	for job in jobs:
		while not has_finished(job):
			if get_world_size() != size or num_drones() < 2:
				if has_finished(job):
					break
				return False
		wait_for(job)
	return True

def gr_maze():
	if num_unlocked(Unlocks.Mazes) == 0:
		return
	while True:
		size = get_world_size()
		cnt = 1
		if num_unlocked(Unlocks.Megafarm) > 0:
			cnt = max_drones()
		if size * size < cnt:
			cnt = size * size
		lvl = num_unlocked(Unlocks.Mazes)
		amount = size * 2 ** (lvl - 1)
		ent = get_entity_type()
		fresh = False
		if ent != Entities.Hedge and ent != Entities.Treasure:
			if num_items(Items.Weird_Substance) < amount:
				return
			if ent != Entities.Bush:
				if ent != None and ent != Entities.Dead_Pumpkin:
					harvest()
				if not plant(Entities.Bush):
					return
			if not use_item(Items.Weird_Substance,amount):
				return
			fresh = True
		slots = 1
		if fresh:
			slots = cnt
		g, cur, cells = map_maze(size,-1,slots)
		if g == None:
			return
		if not fresh:
			pos = measure()
			if pos == None:
				return
			goal = pos[0] + pos[1] * size
			path = route(g,cur,goal,size)
			if path == None:
				return
			for dir in path:
				if get_world_size() != size or not move(ds[dir]):
					return
			if get_entity_type() != Entities.Treasure:
				return
			harvest()
			continue
		bases, home = bases_for(g,size,cnt)
		start = num_items(Items.Weird_Substance)
		jobs = []
		mine = [0]
		for i in range(1,len(bases)):
			job = spawn_drone(station,g,home,bases,i,[i],size,lvl,amount,start)
			if job == None:
				mine.append(i)
			else:
				jobs.append(job)
		ok = station(g,home,bases,0,mine,size,lvl,amount,start)
		if not join_stations(jobs,size) or not ok:
			return

gr_maze()
