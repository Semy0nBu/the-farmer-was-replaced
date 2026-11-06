import dlc_common

ds = [North,East,South,West]
xs = [0,1,0,-1]
ys = [1,0,-1,0]
last = None
stage = None

def seek_mushroom(size):
	for step in range(1024):
		if get_world_size() != size or get_ground_type() == Grounds.Bedrock:
			return False
		if get_ground_type() == Grounds.Mushroom:
			return True
		if get_ground_type() == Grounds.Limestone:
			if not move(East):
				return False
		elif not dlc_common.dig_one():
			return False
	return get_ground_type() == Grounds.Mushroom

def remember(a,zs,cnt,index,kind,z):
	old = a[index]
	if old != kind:
		if old >= 0:
			cnt[old] -= 1
		if kind >= 0:
			cnt[kind] += 1
		a[index] = kind
	zs[index] = z

def snapshot(a,zs,cnt,ox,oy,width,height,floor):
	x = get_pos_x() - ox
	y = get_pos_y() - oy
	for side in range(5):
		tx = x
		ty = y
		dir = None
		if side < 4:
			tx += xs[side]
			ty += ys[side]
			dir = ds[side]
		if tx < 0 or tx >= width or ty < 0 or ty >= height:
			continue
		kind = -1
		z = get_pos_z(dir)
		if z >= floor and get_ground_type(dir) == Grounds.Mushroom:
			value = measure(dir)
			if value != None:
				kind = value
		remember(a,zs,cnt,ty * width + tx,kind,z)

def go(index,ox,oy,width,size):
	return dlc_common.go_to(ox + index % width,oy + index // width,size)

def prepare(z,a,zs,cnt,ox,oy,width,height,floor,size):
	for step in range(128):
		if get_world_size() != size:
			return False
		here = get_pos_z()
		if here == z:
			snapshot(a,zs,cnt,ox,oy,width,height,floor)
			return True
		if here > z:
			if not dlc_common.dig_one():
				return False
		else:
			if not place(Grounds.Dirt):
				return False
	return False

def fixture(source,target,a,zs,cnt,ox,oy,width,height,floor,size):
	x = target % width
	y = target // width
	z = zs[target]
	best = -1
	cost = 100000
	for way in range(4):
		tx = x + xs[way]
		ty = y + ys[way]
		if tx < 0 or tx >= width or ty < 0 or ty >= height:
			continue
		index = ty * width + tx
		if index == source:
			continue
		value = abs(tx - source % width) + abs(ty - source // width)
		if a[index] >= 0:
			value += 3
		if zs[index] > z - 2:
			value += zs[index] - z + 2
		if value < cost:
			best = way
			cost = value
	if best < 0:
		return -1
	index = (y + ys[best]) * width + x + xs[best]
	if not go(index,ox,oy,width,size) or not prepare(z - 2,a,zs,cnt,ox,oy,width,height,floor,size):
		return -1
	if not go(target,ox,oy,width,size):
		return -1
	kind = a[target]
	if get_ground_type() != Grounds.Mushroom or measure() != kind or get_pos_z() != z:
		snapshot(a,zs,cnt,ox,oy,width,height,floor)
		return -1
	if not push(ds[best]):
		snapshot(a,zs,cnt,ox,oy,width,height,floor)
		return -1
	snapshot(a,zs,cnt,ox,oy,width,height,floor)
	if not move(ds[best]):
		return -1
	snapshot(a,zs,cnt,ox,oy,width,height,floor)
	if a[index] != kind or get_pos_z() != z - 1:
		return -2
	return index

def match(source,target,a,zs,cnt,ox,oy,width,height,floor,size):
	if not go(target,ox,oy,width,size):
		return False
	snapshot(a,zs,cnt,ox,oy,width,height,floor)
	kind = a[source]
	if kind < 0 or a[target] != kind:
		return False
	if zs[source] < zs[target]:
		old = source
		source = target
		target = old
		if not go(target,ox,oy,width,size):
			return False
		snapshot(a,zs,cnt,ox,oy,width,height,floor)
	if zs[source] == zs[target]:
		target = fixture(source,target,a,zs,cnt,ox,oy,width,height,floor,size)
		if target == -2:
			return True
		if target < 0:
			return False
	if not go(source,ox,oy,width,size):
		return False
	snapshot(a,zs,cnt,ox,oy,width,height,floor)
	if a[source] != kind:
		return False
	z = get_pos_z()
	for step in range(width + height + 2):
		x = get_pos_x() - ox
		y = get_pos_y() - oy
		tx = target % width
		ty = target // width
		way = 0
		if x < tx:
			way = 1
		elif x > tx:
			way = 3
		elif y > ty:
			way = 2
		elif y == ty:
			return False
		next = (y + ys[way]) * width + x + xs[way]
		if next != target:
			if not go(next,ox,oy,width,size) or not prepare(z - 1,a,zs,cnt,ox,oy,width,height,floor,size):
				return False
			if not go(y * width + x,ox,oy,width,size):
				return False
		else:
			if get_ground_type(ds[way]) != Grounds.Mushroom or measure(ds[way]) != kind or get_pos_z(ds[way]) >= z:
				return False
		if get_ground_type() != Grounds.Mushroom or measure() != kind or get_pos_z() != z:
			snapshot(a,zs,cnt,ox,oy,width,height,floor)
			return False
		if not push(ds[way]):
			snapshot(a,zs,cnt,ox,oy,width,height,floor)
			return False
		snapshot(a,zs,cnt,ox,oy,width,height,floor)
		if not move(ds[way]):
			return False
		snapshot(a,zs,cnt,ox,oy,width,height,floor)
		if get_ground_type() != Grounds.Mushroom or measure() != kind or get_pos_z() != z:
			return True
	return False

def tile(arg,size):
	ox, oy, width, height, depth, window = arg
	floor = depth - window
	a = []
	zs = []
	cnt = [0,0,0,0,0,0]
	for cell in range(width * height):
		a.append(-1)
		zs.append(0)
	for y in range(height):
		for step in range(width):
			x = step
			if y % 2 == 1:
				x = width - 1 - step
			if get_world_size() != size or not go(y * width + x,ox,oy,width,size):
				return False
			while get_pos_z() >= depth and get_ground_type() != Grounds.Mushroom:
				if not dlc_common.dig_one():
					return False
			snapshot(a,zs,cnt,ox,oy,width,height,floor)
	used = set()
	for attempt in range(width * height * 3):
		if get_world_size() != size:
			return False
		px = get_pos_x() - ox
		py = get_pos_y() - oy
		source = -1
		near = width + height + 1
		for cell in range(len(a)):
			kind = a[cell]
			if kind < 0 or cnt[kind] < 2:
				continue
			dis = abs(cell % width - px) + abs(cell // width - py)
			if dis < near:
				source = cell
				near = dis
		if source < 0:
			return True
		kind = a[source]
		target = -1
		near = width + height + 1
		for cell in range(len(a)):
			if cell == source or a[cell] != kind or (source,cell,kind,zs[source],zs[cell]) in used:
				continue
			dis = abs(cell % width - source % width) + abs(cell // width - source // width)
			if dis < near:
				target = cell
				near = dis
		if target < 0:
			remember(a,zs,cnt,source,-1,zs[source])
			continue
		used.add((source,target,kind,zs[source],zs[target]))
		match(source,target,a,zs,cnt,ox,oy,width,height,floor,size)
	return True

def gr_mushrooms(rounds=0,window=4):
	global last
	global stage
	if rounds < 0 or window < 0 or window > 5 or get_world_size() < 2 or dlc_common.current_count() != 1:
		return False
	if not dlc_common.begin(Unlocks.Mushrooms):
		return False
	size = get_world_size()
	done = 0
	empty = 0
	attempt = 0
	while rounds == 0 or done < rounds:
		if get_world_size() != size:
			return False
		attempt += 1
		stage = ("seek",attempt,done)
		old = num_items(Items.Mushroom)
		if seek_mushroom(size):
			depth = get_pos_z()
			args = []
			for y in range(0,size,8):
				for x in range(0,size,4):
					args.append((x,y,min(4,size - x),min(8,size - y),depth,window))
			stage = ("pairs",attempt,depth)
			res = dlc_common.parallel(tile,args,size)
			if res == None or get_world_size() != size:
				return False
			for ok in res:
				if ok != True:
					return False
		gained = num_items(Items.Mushroom) - old
		last = (attempt,gained,done)
		if gained > 0:
			done += 1
			empty = 0
		else:
			empty += 1
			if empty >= 3:
				return False
		if rounds == 0 or done < rounds:
			dlc_common.reset()
	return True

if __name__ == "__main__":
	gr_mushrooms()
