def make_cycle(size):
	path = []
	for y in range(size):
		path.append(y * size)
	for row in range(size - 1):
		y = size - 1 - row
		if row % 2 == 0:
			for x in range(1,size):
				path.append(x + y * size)
		else:
			for col in range(1,size):
				x = size - col
				path.append(x + y * size)
	for col in range(1,size):
		path.append(size - col)
	tot = size * size
	rank = []
	for i in range(tot):
		rank.append(0)
	for i in range(tot):
		rank[path[i]] = i
	dirs = []
	cuts = []
	for i in range(tot):
		cell = path[i]
		next = path[(i + 1) % tot]
		if next == cell + size:
			dirs.append(North)
		elif next == cell - size:
			dirs.append(South)
		elif next == cell + 1:
			dirs.append(East)
		else:
			dirs.append(West)
		x = cell % size
		y = cell // size
		near = []
		if y < size - 1:
			near.append((cell + size,North))
		if x < size - 1:
			near.append((cell + 1,East))
		if y > 0:
			near.append((cell - size,South))
		if x > 0:
			near.append((cell - 1,West))
		part = []
		for pair in near:
			node, dir = pair
			idx = rank[node]
			dist = (idx - i) % tot
			if dist > 1 and dist < tot - 1:
				part.append((dist,idx,dir))
		cuts.append(part)
	return rank, dirs, cuts

def fast_cycle(dirs,head,size):
	tot = size * size
	for i in range(head,tot):
		if not move(dirs[i]):
			return True
	while get_world_size() == size:
		before = num_items(Items.Cactus)
		for dir in dirs:
			if not move(dir):
				return True
		if num_items(Items.Cactus) >= before:
			return False
	return True

def grow_dino(rank,dirs,cuts,size):
	tot = size * size
	body = []
	for i in range(tot):
		body.append(0)
	read = 0
	write = 1
	count = 1
	head = 0
	food = 0
	limit = tot // 4
	if limit > 100:
		limit = 100
	reserve = size * 2
	while get_world_size() == size:
		if count >= tot:
			return True
		tail = body[read]
		span = (head - tail) % tot + 1
		if count >= limit and span == count:
			return fast_cycle(dirs,head,size)
		ate = head == food
		last = False
		if ate:
			pos = measure()
			if pos == None:
				last = True
			else:
				food = rank[pos[0] + pos[1] * size]
		next = (head + 1) % tot
		dir = dirs[head]
		if count < limit and not last:
			free = (tail - head) % tot
			if count == 1:
				free = tot
			reach = (food - head) % tot
			best = 1
			for cut in cuts[head]:
				dist, idx, way = cut
				if dist > best and dist <= reach and dist < free - reserve:
					best = dist
					next = idx
					dir = way
		if not move(dir):
			return True
		head = next
		body[write] = head
		write = (write + 1) % tot
		if ate:
			count += 1
		else:
			read = (read + 1) % tot
		if last:
			return False
	return True

def grow_path(size):
	dir = East
	for row in range(size):
		for col in range(size - 1):
			if get_world_size() != size:
				return True
			if not move(dir):
				return True
		if row < size - 1:
			if get_world_size() != size or not move(North):
				return True
		if dir == East:
			dir = West
		else:
			dir = East
	return True

def gr_dino():
	if num_unlocked(Unlocks.Dinosaurs) == 0:
		return
	change_hat(Hats.Gold_Hat)
	while True:
		size = get_world_size()
		if size < 2:
			return
		if num_items(Items.Cactus) == 0:
			return
		if size % 2 == 0:
			rank, dirs, cuts = make_cycle(size)
		while get_world_size() == size:
			clear()
			change_hat(Hats.Dinosaur_Hat)
			if get_entity_type() != Entities.Apple:
				change_hat(Hats.Gold_Hat)
				return
			if size % 2 == 0:
				again = grow_dino(rank,dirs,cuts,size)
			else:
				again = grow_path(size)
			change_hat(Hats.Gold_Hat)
			if not again:
				return

gr_dino()
