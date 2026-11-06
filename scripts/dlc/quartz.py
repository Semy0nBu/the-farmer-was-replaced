import dlc_common
import coal
import iron

def quartz_fit(points,size):
	if len(points) != 4:
		return None
	a, b, c, d = points
	dx = b[0] - a[0]
	dy = c[1] - b[1]
	dz = d[2] - c[2]
	if dx == 0 or dy == 0 or dz == 0:
		return None
	z = (d[2] * d[2] - c[2] * c[2] + c[3] - d[3]) / (2 * dz)
	y = (c[1] * c[1] - b[1] * b[1] + c[2] * c[2] - b[2] * b[2] + b[3] - c[3] - 2 * (c[2] - b[2]) * z) / (2 * dy)
	x = (b[0] * b[0] - a[0] * a[0] + b[2] * b[2] - a[2] * a[2] + a[3] - b[3] - 2 * (b[2] - a[2]) * z) / (2 * dx)
	tx = (x + 0.5) // 1
	ty = (y + 0.5) // 1
	tz = (z + 0.5) // 1
	if abs(x - tx) > 0.0001 or abs(y - ty) > 0.0001 or abs(z - tz) > 0.0001:
		return None
	for pos in points:
		x = pos[0] - tx
		y = pos[1] - ty
		z = pos[2] - tz
		if abs(x * x + y * y + z * z - pos[3]) > 0.0001:
			return None
	return tx % size,ty % size,tz

def quartz_read(size):
	if get_world_size() != size or num_items(Items.Iron) == 0:
		return None
	dis = prospect_quartz()
	if dis == None:
		return None
	return get_pos_x(),get_pos_y(),get_pos_z(),dis * dis

def quartz_locate(size):
	points = []
	used = 0
	if size < 2:
		return None,points,used
	for step in range(4):
		if get_world_size() != size:
			return None,points,used
		if get_ground_type() == Grounds.Quartz:
			return [get_pos_x(),get_pos_y(),get_pos_z()],points,used
		if num_items(Items.Iron) == 0:
			return None,points,used
		pos = quartz_read(size)
		used += 1
		if pos == None:
			return None,points,used
		points.append(pos)
		if step == 0:
			dir = East
			if get_pos_x() == size - 1:
				dir = West
			if not move(dir):
				return None,points,used
		elif step == 1:
			dir = North
			if get_pos_y() == size - 1:
				dir = South
			if not move(dir):
				return None,points,used
		elif step == 2:
			if not dlc_common.dig_one():
				return None,points,used
	return quartz_fit(points,size),points,used

def quartz_scout(arg,size):
	x, y, budget = arg
	if not dlc_common.go_to(x,y,size):
		return False
	for step in range(64):
		if get_world_size() != size:
			return False
		ground = get_ground_type()
		if ground == Grounds.Quartz:
			return get_pos_x(),get_pos_y(),get_pos_z()
		hardness = get_hardness()
		if ground == Grounds.Rock or hardness == None or hardness >= 3:
			break
		if not dlc_common.dig_one():
			return None
	for attempt in range(3):
		if get_world_size() != size:
			return False
		if get_ground_type() == Grounds.Quartz:
			return get_pos_x(),get_pos_y(),get_pos_z()
		if budget >= 4 and size > 1:
			target, points, used = quartz_locate(size)
			budget -= used
			if target != None:
				return target
		for step in range(8):
			if get_world_size() != size:
				return False
			if get_ground_type() == Grounds.Quartz:
				return get_pos_x(),get_pos_y(),get_pos_z()
			if not dlc_common.dig_one():
				return None
	if get_ground_type() == Grounds.Quartz:
		return get_pos_x(),get_pos_y(),get_pos_z()
	return None

def quartz_mine(target,size):
	if not dlc_common.go_to(target[0],target[1],size):
		return -1
	mined = 0
	floor = target[2] - 2
	for step in range(256):
		if get_world_size() != size:
			return -1
		ground = get_ground_type()
		if ground == Grounds.Quartz:
			if not dlc_common.dig_one():
				break
			mined += 1
		elif mined > 0 or get_pos_z() < floor:
			break
		elif not dlc_common.dig_one():
			break
	return mined

def quartz_args(size):
	cnt = dlc_common.count_jobs(size * size)
	if num_items(Items.Iron) >= 4 and num_items(Items.Iron) // 4 < cnt:
		cnt = num_items(Items.Iron) // 4
	budget = num_items(Items.Iron) // cnt
	if budget > 12:
		budget = 12
	nx = 1
	while nx * nx < cnt:
		nx += 1
	ny = (cnt + nx - 1) // nx
	args = []
	for i in range(cnt):
		x = (i % nx) * size // nx
		y = (i // nx) * size // ny
		args.append((x,y,budget))
	return args

def collect(size):
	res = dlc_common.parallel(quartz_scout,quartz_args(size),size)
	if res == None:
		return -1
	seen = set()
	args = []
	for pos in res:
		if pos == False:
			return -1
		if pos != None:
			key = pos[0] + pos[1] * size
			if key not in seen:
				seen.add(key)
				args.append(pos)
	if len(args) == 0:
		return 0
	res = dlc_common.parallel(quartz_mine,args,size)
	if res == None:
		return -1
	total = 0
	for part in res:
		if part == None or part < 0:
			return -1
		total += part
	return total

def quartz_supply(size):
	if size == 1:
		return True
	cnt = dlc_common.count_jobs(size * size)
	need = cnt * 12
	if num_items(Items.Iron) >= need:
		return True
	if not dlc_common.ready(Unlocks.Iron):
		return num_items(Items.Iron) >= 4
	prospect = num_unlocked(Unlocks.Prospecting) > 0
	have_coal = dlc_common.ready(Unlocks.Coal)
	empty = 0
	for attempt in range(8):
		if get_world_size() != size:
			return False
		dlc_common.reset()
		if prospect and have_coal and num_items(Items.Coal) < cnt * 4:
			if coal.collect(size) < 0:
				return False
		before = num_items(Items.Iron)
		if iron.collect(size) < 0 or get_world_size() != size:
			return False
		if num_items(Items.Iron) >= need:
			return True
		if num_items(Items.Iron) <= before:
			empty += 1
			if empty >= 3:
				return num_items(Items.Iron) >= 4
		else:
			empty = 0
	return num_items(Items.Iron) >= 4

def gr_quartz(rounds=0):
	if dlc_common.current_count() != 1 or not dlc_common.ready(Unlocks.Quartz):
		return False
	if not quartz_supply(get_world_size()):
		return False
	if not dlc_common.begin(Unlocks.Quartz):
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
		if num_items(Items.Iron) < 4 and get_world_size() > 1:
			if not quartz_supply(get_world_size()):
				return False
		else:
			dlc_common.reset()

if __name__ == "__main__":
	gr_quartz()
