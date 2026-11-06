import dlc_common

def dig_band(arg,size):
	lo, hi, depth, phase, colors = arg
	active = 0
	for y in range(lo,hi):
		cy = y % 2
		if colors == 3 and y == size - 1:
			cy = 2
		x = (phase - cy) % colors
		cnt = size // 2
		if colors == 3:
			cnt = (size - 1) // 2
			if x == 2:
				x = size - 1
				cnt = 1
		if colors == 1:
			x = 0
			cnt = 1
		dir = East
		if y % 2 == 1:
			dir = West
			x += 2 * (cnt - 1)
		if get_world_size() != size or not dlc_common.go_to(x,y,size):
			return None
		for step in range(cnt):
			if get_world_size() != size:
				return None
			if get_ground_type() != Grounds.Bedrock:
				while get_pos_z() > depth:
					if not dlc_common.dig_one():
						if get_ground_type() != Grounds.Bedrock:
							return None
						break
				if get_ground_type() != Grounds.Bedrock:
					active += 1
			if step < cnt - 1:
				if not move(dir) or not move(dir):
					return None
	return active

def gr_layers(layers=0):
	if dlc_common.current_count() != 1 or not dlc_common.ready(Unlocks.Mining):
		return False
	dlc_common.reset()
	size = get_world_size()
	parts = dlc_common.bands(size)
	colors = 2
	if size % 2 == 1:
		colors = 3
	if size == 1:
		colors = 1
	depth = 0
	done = 0
	while True:
		depth -= 1
		active = 0
		for phase in range(colors):
			args = []
			for band in parts:
				args.append((band[0],band[1],depth,phase,colors))
			res = dlc_common.parallel(dig_band,args,size)
			if res == None:
				return False
			for part in res:
				if part == None:
					return False
				active += part
		done += 1
		if layers > 0 and done >= layers:
			return True
		if active == 0:
			if layers > 0:
				return True
			dlc_common.reset()
			depth = 0

if __name__ == "__main__":
	gr_layers()
