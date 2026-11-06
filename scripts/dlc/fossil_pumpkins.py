import dlc_common

def fossil_color(x,y,size):
	if size == 1:
		return 0
	if size % 2 == 0:
		return (x + y) % 2
	cx = x % 2
	cy = y % 2
	if x == size - 1:
		cx = 2
	if y == size - 1:
		cy = 2
	return (cx + cy) % 3

def fossil_job(arg,size):
	work, depth, expose = arg
	found = []
	mined = 0
	for pos in work:
		if get_world_size() != size or not dlc_common.go_to(pos[0],pos[1],size):
			return None
		ground = get_ground_type()
		while ground != Grounds.Petrified_Pumpkin and get_pos_z() > depth:
			if not expose or not dlc_common.dig_one():
				break
			if get_world_size() != size:
				return None
			ground = get_ground_type()
		if ground == Grounds.Petrified_Pumpkin:
			if not expose and get_pos_z() >= depth:
				if not dlc_common.dig_one():
					return None
				mined += 1
			if expose or get_ground_type() == Grounds.Petrified_Pumpkin:
				found.append(pos)
	return found,mined

def fossil_jobs(work,depth,expose,size):
	cnt = dlc_common.count_jobs(len(work))
	args = []
	for i in range(cnt):
		part = []
		lo = len(work) * i // cnt
		hi = len(work) * (i + 1) // cnt
		for j in range(lo,hi):
			part.append(work[j])
		args.append((part,depth,expose))
	return args

def collect(size):
	if not dlc_common.seek(Grounds.Petrified_Pumpkin):
		return 0
	x = get_pos_x()
	y = get_pos_y()
	depth = get_pos_z()
	width = size
	if width > 9:
		width = 9
	work = []
	for j in range(width):
		ty = (y - 4 + j) % size
		for i in range(width):
			st = i
			if j % 2 == 1:
				st = width - 1 - i
			work.append([(x - 4 + st) % size,ty])
	res = dlc_common.parallel(fossil_job,fossil_jobs(work,depth,True,size),size)
	if res == None:
		return -1
	active = []
	for part in res:
		if part == None:
			return -1
		for pos in part[0]:
			active.append(pos)
	colors = 2
	if size % 2 == 1:
		colors = 3
	if size == 1:
		colors = 1
	total = 0
	for level in range(5):
		next = []
		for phase in range(colors):
			work = []
			for pos in active:
				if fossil_color(pos[0],pos[1],size) == phase:
					work.append(pos)
			if len(work) == 0:
				continue
			res = dlc_common.parallel(fossil_job,fossil_jobs(work,depth - level,False,size),size)
			if res == None:
				return -1
			for part in res:
				if part == None:
					return -1
				total += part[1]
				for pos in part[0]:
					next.append(pos)
		active = next
		if len(active) == 0:
			break
	return total

def gr_fossils(rounds=0):
	if not dlc_common.begin(Unlocks.Petrified_Pumpkins):
		return False
	done = 0
	while True:
		mined = collect(get_world_size())
		if mined < 0:
			return False
		if mined > 0:
			done += 1
			if rounds > 0 and done >= rounds:
				return True
		dlc_common.reset()

if __name__ == "__main__":
	gr_fossils()
