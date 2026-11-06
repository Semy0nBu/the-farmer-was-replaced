import dlc_common

def find_points(arg,size):
	points, depth = arg
	reached = False
	for pos in points:
		if get_world_size() != size or not dlc_common.go_to(pos[0],pos[1],size):
			return None
		while get_pos_z() > depth:
			ground = get_ground_type()
			if ground == Grounds.Sand or ground == Grounds.Limestone or ground == Grounds.Bedrock:
				break
			if not dlc_common.dig_one():
				break
		ground = get_ground_type()
		if ground == Grounds.Sand or ground == Grounds.Limestone:
			return [get_pos_x(),get_pos_y()], True
		if get_pos_z() <= depth:
			reached = True
	return [], reached

def locate(size,depth=None):
	if size < 5:
		return False
	if get_ground_type() == Grounds.Limestone:
		return True
	axis = []
	x = 0
	while x < size:
		axis.append(x)
		x += 5
	points = []
	for row in range(len(axis)):
		for step in range(len(axis)):
			col = step
			if row % 2 == 1:
				col = len(axis) - 1 - step
			x = axis[col]
			y = axis[row]
			points.append((x,y))
	total = len(points)
	cnt = dlc_common.count_jobs(total)
	parts = []
	for i in range(cnt):
		lo = total * i // cnt
		hi = total * (i + 1) // cnt
		part = []
		for j in range(lo,hi):
			part.append(points[j])
		parts.append(part)
	low = get_pos_z() - 512
	floor = get_pos_z()
	while floor >= low:
		args = []
		for part in parts:
			args.append((part,floor))
		res = dlc_common.parallel(find_points,args,size)
		if res == None or get_world_size() != size:
			return False
		reached = False
		for part in res:
			if part == None:
				continue
			pos, ok = part
			if ok:
				reached = True
			if len(pos) == 0:
				continue
			if not dlc_common.go_to(pos[0],pos[1],size):
				return False
			for step in range(size + 4):
				if get_ground_type() == Grounds.Limestone:
					return True
				if get_world_size() != size or not dlc_common.dig_one():
					break
		if not reached:
			return False
		floor -= 1
	return False

def expose(z,size):
	while get_pos_z() > z:
		ground = get_ground_type()
		if ground == Grounds.Sand:
			return True
		if ground == Grounds.Limestone:
			return False
		if get_world_size() != size or not dlc_common.dig_one():
			return None
	if get_pos_z() != z:
		return False
	return get_ground_type() == Grounds.Limestone

def axis_bounds(arg,size):
	axis, sx, sy, z = arg
	way = East
	back = West
	origin = sx
	if axis == 1:
		way = North
		back = South
		origin = sy
	if not dlc_common.go_to(sx,sy,size):
		return None
	east = 0
	for step in range(1,size):
		if get_world_size() != size or not move(way):
			return None
		ok = expose(z,size)
		if ok == None:
			return None
		if not ok:
			break
		east += 1
	if east == size - 1:
		return axis, 0, size
	if not dlc_common.go_to(sx,sy,size):
		return None
	west = 0
	for step in range(1,size - east):
		if get_world_size() != size or not move(back):
			return None
		ok = expose(z,size)
		if ok == None:
			return None
		if not ok:
			break
		west += 1
	return axis, (origin - west) % size, east + west + 1

def prepare(arg,size):
	lo, hi, ox, oy, w, z = arg
	if not dlc_common.go_to(ox,(oy + lo) % size,size):
		return False
	for row in range(lo,hi):
		way = East
		if (row - lo) % 2 == 1:
			way = West
		for step in range(w):
			if get_world_size() != size or expose(z,size) != True:
				return False
			if step < w - 1 and not move(way):
				return False
		if row < hi - 1 and not move(North):
			return False
	return True

def verify(arg,size):
	lo, hi, ox, oy, w, z = arg
	if not dlc_common.go_to(ox,(oy + lo) % size,size):
		return False
	for row in range(lo,hi):
		way = East
		if (row - lo) % 2 == 1:
			way = West
		for step in range(w):
			if get_world_size() != size:
				return False
			ground = get_ground_type()
			height = get_pos_z()
			if ground == Grounds.Limestone:
				if height != z:
					return False
			elif ground != Grounds.Sand or height <= z:
				return False
			if step < w - 1 and not move(way):
				return False
		if row < hi - 1 and not move(North):
			return False
	return True

def sand(arg,size):
	lo, hi, ox, oy, w, layer, z = arg
	width = w - layer * 2
	if not dlc_common.go_to((ox + layer) % size,(oy + lo) % size,size):
		return False
	for row in range(lo,hi):
		way = East
		if (row - lo) % 2 == 1:
			way = West
		for step in range(width):
			if get_world_size() != size:
				return False
			if get_pos_z() < z:
				return False
			ground = get_ground_type()
			if ground != Grounds.Sand and ground != Grounds.Limestone:
				return False
			while get_pos_z() < z + layer + 1:
				old_z = get_pos_z()
				if not place(Grounds.Sand) or get_pos_z() <= old_z:
					return False
			if step < width - 1 and not move(way):
				return False
		if row < hi - 1 and not move(North):
			return False
	return True

def restore(size,depth=None):
	if not locate(size):
		return False
	z = get_pos_z()
	sx = get_pos_x()
	sy = get_pos_y()
	args = []
	args.append((0,sx,sy,z))
	args.append((1,sx,sy,z))
	res = dlc_common.parallel(axis_bounds,args,size)
	if res == None:
		return False
	bounds = [None,None]
	for part in res:
		if part == None:
			return False
		axis, start, width = part
		bounds[axis] = [start,width]
	if bounds[0] == None or bounds[1] == None:
		return False
	ox, w = bounds[0]
	oy, h = bounds[1]
	if w != h or w % 2 == 0:
		return False
	args = []
	cnt = dlc_common.count_jobs(w)
	for i in range(cnt):
		lo = w * i // cnt
		hi = w * (i + 1) // cnt
		args.append((lo,hi,ox,oy,w,z))
	res = dlc_common.parallel(prepare,args,size)
	if res == None:
		return False
	for ok in res:
		if ok != True:
			return False
	cx = (ox + w // 2) % size
	cy = (oy + w // 2) % size
	top = z + w // 2 + 1
	if not dlc_common.go_to(cx,cy,size):
		return False
	while get_pos_z() >= top:
		if get_ground_type() != Grounds.Sand or not dlc_common.dig_one():
			return False
	res = dlc_common.parallel(verify,args,size)
	if res == None:
		return False
	for ok in res:
		if ok != True:
			return False
	for layer in range(w // 2):
		width = w - layer * 2
		cnt = dlc_common.count_jobs(width)
		args = []
		for i in range(cnt):
			lo = layer + width * i // cnt
			hi = layer + width * (i + 1) // cnt
			args.append((lo,hi,ox,oy,w,layer,z))
		res = dlc_common.parallel(sand,args,size)
		if res == None:
			return False
		for ok in res:
			if ok != True:
				return False
	if get_world_size() != size or not dlc_common.go_to(cx,cy,size):
		return False
	while get_pos_z() < top:
		old_z = get_pos_z()
		if not place(Grounds.Sand):
			return False
		if get_ground_type() == Grounds.Limestone:
			break
		if get_pos_z() <= old_z:
			return False
	if get_entity_type() != Entities.Sunflower:
		return False
	while not can_harvest():
		if get_world_size() != size or get_entity_type() != Entities.Sunflower:
			return False
	return harvest()

def gr_pyramid(rounds=0):
	if get_world_size() < 5 or not dlc_common.begin(Unlocks.Pyramid):
		return False
	done = 0
	while True:
		ok = restore(get_world_size())
		if rounds > 0:
			if not ok:
				return False
			done += 1
			if done >= rounds:
				return True
		dlc_common.reset()

if __name__ == "__main__":
	gr_pyramid()
