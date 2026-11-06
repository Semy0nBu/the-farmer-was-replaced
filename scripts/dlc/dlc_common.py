def current_count():
	if num_unlocked(Unlocks.Megafarm) == 0:
		return 1
	return num_drones()

def go_to(x,y,size):
	dis = (x - get_pos_x()) % size
	dir = East
	if dis > size / 2:
		dis = size - dis
		dir = West
	for step in range(dis):
		if not move(dir):
			return False
	dis = (y - get_pos_y()) % size
	dir = North
	if dis > size / 2:
		dis = size - dis
		dir = South
	for step in range(dis):
		if not move(dir):
			return False
	return True

def ready(tech):
	return num_unlocked(Unlocks.Mining) > 0 and num_unlocked(tech) > 0 and num_unlocked(Unlocks.Underground_Senses) > 0

def reset():
	change_hat(Hats.Gold_Hat)
	clear()
	change_hat(Hats.Mining_Hat)

def begin(tech):
	if current_count() != 1 or not ready(tech):
		return False
	reset()
	if num_unlocked(Unlocks.Jump) > 0:
		jump(tech)
	return True

def dig_one():
	if get_ground_type() == Grounds.Bedrock:
		return False
	for attempt in range(64):
		if dig():
			return True
	return False

def seek(ground,limit=512):
	for step in range(limit):
		if get_ground_type() == ground:
			return True
		if not dig_one():
			return False
	return get_ground_type() == ground

def count_jobs(work):
	cnt = 1
	if num_unlocked(Unlocks.Megafarm) > 0:
		cnt = max_drones()
	if cnt > work:
		cnt = work
	return cnt

def bands(size):
	args = []
	cnt = count_jobs(size)
	for i in range(cnt):
		args.append((size * i // cnt,size * (i + 1) // cnt))
	return args

def wait_job(job,size):
	while not has_finished(job):
		if current_count() < 2:
			if has_finished(job):
				break
			return None
	return wait_for(job)

def fork_jobs(task,args,size,cnt):
	if get_world_size() != size:
		return None
	res = []
	if cnt < 2:
		for arg in args:
			if get_world_size() != size:
				return None
			res.append(task(arg,size))
		return res
	left_cnt = cnt // 2
	cut = len(args) * left_cnt // cnt
	left = []
	right = []
	for i in range(len(args)):
		if i < cut:
			left.append(args[i])
		else:
			right.append(args[i])
	job = spawn_drone(fork_jobs,task,right,size,cnt - left_cnt)
	left = fork_jobs(task,left,size,left_cnt)
	if job == None:
		right = fork_jobs(task,right,size,cnt - left_cnt)
	else:
		right = wait_job(job,size)
	if left == None or right == None:
		return None
	for part in right:
		left.append(part)
	return left

def parallel(task,args,size):
	if len(args) == 0:
		return []
	res = fork_jobs(task,args,size,count_jobs(len(args)))
	if res == None or get_world_size() != size:
		return None
	return res
