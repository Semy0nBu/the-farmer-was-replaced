import dlc_common

def block_job(pos,size):
	x, y = pos
	if not dlc_common.go_to(x,y,size):
		return False
	senses = num_unlocked(Unlocks.Underground_Senses) > 0
	for step in range(6):
		if get_world_size() != size:
			return False
		if senses:
			if get_ground_type() == Grounds.Bedrock:
				break
		dig()
	return True

def block_surface(size):
	pos = []
	for y in range(size):
		for col in range(size):
			x = col
			if y % 2 == 1:
				x = size - 1 - col
			if size % 2 == 0:
				if (x + y) % 2 == 0:
					pos.append((x,y))
			else:
				res = (x + y) % size
				if size == 1 or res % 2 == 0 and res < size - 1:
					pos.append((x,y))
	return pos

def surface_jobs(pos,cnt):
	args = []
	for i in range(cnt):
		part = []
		for j in range(len(pos) * i // cnt,len(pos) * (i + 1) // cnt):
			part.append(pos[j])
		args.append(part)
	return args

def surface_job(pos,size):
	for cell in pos:
		if get_world_size() != size or not dlc_common.go_to(cell[0],cell[1],size):
			return False
		for attempt in range(64):
			if get_world_size() != size:
				return False
			if get_pos_z() < 0 or get_ground_type() == Grounds.Bedrock:
				break
			if dig():
				break
			if attempt == 63:
				return False
	return True

def gr_blocks(rounds=0):
	if dlc_common.current_count() != 1 or num_unlocked(Unlocks.Mining) == 0:
		return False
	done = 0
	old_size = 0
	old_cnt = 0
	pos = []
	args = []
	while True:
		dlc_common.reset()
		size = get_world_size()
		if num_unlocked(Unlocks.Underground_Senses) > 0 and dlc_common.count_jobs(size) > 1:
			if size != old_size:
				pos = block_surface(size)
				old_size = size
				old_cnt = 0
			cnt = dlc_common.count_jobs(len(pos))
			if cnt != old_cnt:
				args = surface_jobs(pos,cnt)
				old_cnt = cnt
			res = dlc_common.parallel(surface_job,args,size)
		else:
			span = size // 3
			if span < 1:
				span = 1
			legacy = []
			for i in range(dlc_common.count_jobs(span * span)):
				legacy.append(((i % span) * 3,(i // span) * 3))
			res = dlc_common.parallel(block_job,legacy,size)
		if res == None:
			return False
		for ok in res:
			if ok != True:
				return False
		done += 1
		if rounds > 0 and done >= rounds:
			return True

if __name__ == "__main__":
	gr_blocks()
