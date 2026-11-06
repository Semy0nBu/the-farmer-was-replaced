import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { context, section, run, rng, range, mod } from './dlc-model.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const directory = path.join(root, 'scripts', 'dlc');
const names = (await fs.readdir(directory)).filter(name => name.endsWith('.py')).sort();
const sources = new Map(await Promise.all(names.map(async name => [name.slice(0, -3), await fs.readFile(path.join(directory, name), 'utf8')])));
const counts = {};
const check = (kind, fn) => { fn(); counts[kind] = (counts[kind] ?? 0) + 1; };
const withoutModule = source => source.replaceAll('dlc_common.', '');
const common = sources.get('dlc_common');
assert.ok(common, 'Missing shared DLC module');

// Import closure is checked separately from the game API stubs.
const imports = new Map();
for (const [name, source] of sources) {
	const dependencies = [...source.matchAll(/^import (\w+)$/gm)].map(match => match[1]);
	for (const dependency of dependencies) assert.ok(sources.has(dependency), `${name}: missing ${dependency}.py`);
	imports.set(name, dependencies);
}
function visit(name, pending, complete) {
	assert.ok(!pending.has(name), `Import cycle at ${name}`);
	if (complete.has(name)) return;
	pending.add(name);
	for (const dependency of imports.get(name)) visit(dependency, pending, complete);
	pending.delete(name); complete.add(name);
}
for (const name of sources.keys()) check('imports', () => visit(name, new Set(), new Set()));

// Closed research must stop before clear(), planting, digging or worker creation.
for (const [name, source] of sources) {
	if (name === 'dlc_common') continue;
	const entry = source.match(/^def (gr_\w+)\(/m)?.[1]; assert.ok(entry, `${name}: missing entry point`);
	check('researchPreflight', () => {
		const unlocks = Object.fromEntries([...source.matchAll(/Unlocks\.(\w+)/g)].map(match => [match[1], match[1]]));
		const ctx = context(withoutModule(section(source, entry)), ['current_count', 'ready', 'begin', 'num_unlocked', 'get_world_size'], {Unlocks: unlocks});
		const value = run(ctx[entry](1), op => {
			if (op === 'current_count') return 1;
			if (op === 'ready' || op === 'begin' || op === 'num_unlocked') return 0;
			if (op === 'get_world_size') return 32;
			throw Error(`Mutation before research preflight: ${op}`);
		});
		assert.notEqual(value, true);
	});
}

const directions = {North: 0, East: 1, South: 2, West: 3};
const dx = [0, 1, 0, -1], dy = [1, 0, -1, 0];
const movement = section(common, 'go_to', 'ready')
	.replaceAll('(x - get_pos_x()) % size', 'mod(x - get_pos_x(),size)')
	.replaceAll('(y - get_pos_y()) % size', 'mod(y - get_pos_y(),size)');
for (const size of [1, 2, 3, 8, 22, 31, 32]) {
	for (const [fromX, fromY, toX, toY] of [[0, 0, size - 1, size - 1], [size - 1, 0, 0, size - 1], [0, size - 1, size >> 1, 0]]) {
		check('shortestRoutes', () => {
			let x = fromX, y = fromY, steps = 0;
			const ctx = context(movement, ['get_pos_x', 'get_pos_y', 'move'], directions);
			assert.equal(run(ctx.go_to(toX, toY, size), (op, args) => {
				if (op === 'get_pos_x') return x;
				if (op === 'get_pos_y') return y;
				if (op === 'move') { x = mod(x + dx[args[0]], size); y = mod(y + dy[args[0]], size); steps++; return true; }
				throw Error(op);
			}), true);
			assert.deepEqual([x, y], [toX, toY]);
			const distance = (a, b) => Math.min(mod(a - b, size), mod(b - a, size));
			assert.equal(steps, distance(fromX, toX) + distance(fromY, toY));
		});
	}
}

const currentCountSource = section(common, 'current_count', 'go_to');
const waitSource = currentCountSource + section(common, 'wait_job', 'fork_jobs');
for (const race of ['finished_between_sensors', 'destroyed', 'ordinary_completion']) {
	check('lastWorkerRace', () => {
		let reads = 0, joins = 0;
		const ctx = context(waitSource, ['has_finished', 'num_drones', 'num_unlocked', 'wait_for'], {Unlocks: {Megafarm: 'megafarm'}});
		const value = run(ctx.wait_job(17, 32), op => {
			if (op === 'num_unlocked') return 1;
			if (op === 'has_finished') return race !== 'destroyed' && ++reads >= 2;
			if (op === 'num_drones') return race === 'ordinary_completion' ? 2 : 1;
			if (op === 'wait_for') { joins++; return 123; }
			throw Error(op);
		});
		assert.equal(value, race === 'destroyed' ? null : 123);
		assert.equal(joins, race === 'destroyed' ? 0 : 1);
	});
}

// Only model API boundaries and randomized scheduling. Arguments are copied at spawn.
function copy(value) {
	if (Array.isArray(value)) return value.map(copy);
	if (value && typeof value === 'object' && !(value instanceof Set)) return Object.fromEntries(Object.entries(value).map(([key, entry]) => [key, copy(entry)]));
	return value;
}
function dispatchModel(size, cap, failEvery, failingTask) {
	const api = ['num_unlocked', 'max_drones', 'get_world_size', 'num_drones', 'spawn_drone', 'has_finished', 'wait_for'];
	const ctx = context(currentCountSource + section(common, 'count_jobs'), [...api, 'task'], {Unlocks: {Megafarm: 'megafarm'}});
	const random = rng(size * 113 + cap * 17 + failEvery), calls = [], actors = [];
	let now = 0, spawnCount = 0, highWater = 1;
	function* task(arg) {
		const id = arg[0]; arg.push(99);
		for (let tick = 0; tick < 2 + id % 3; tick++) yield {op: 'cpu', args: []};
		calls.push(id);
		return id === failingTask ? false : id * 3;
	}
	function add(generator) { const actor = {generator, done: false, blocked: null, at: now, value: undefined}; actors.push(actor); return actor; }
	const args = range(size).map(index => [index]);
	const rootActor = add(ctx.parallel(task, args, size));
	for (let operations = 0; operations < 200000; operations++) {
		for (const actor of actors) if (!actor.done && actor.blocked?.done) { actor.value = copy(actor.blocked.result); actor.blocked = null; }
		const runnable = actors.filter(actor => !actor.done && !actor.blocked).sort((a, b) => a.at - b.at || actors.indexOf(a) - actors.indexOf(b));
		if (!runnable.length) { assert.ok(actors.every(actor => actor.done), 'Dispatcher deadlocked'); break; }
		const actor = runnable[0]; now = actor.at;
		const next = actor.generator.next(actor.value); actor.value = undefined;
		if (next.done) { actor.done = true; actor.result = next.value; continue; }
		const {op, args: values} = next.value;
		let result;
		if (cap === 1 && ['max_drones', 'num_drones', 'spawn_drone', 'has_finished', 'wait_for'].includes(op)) throw Error(`Locked Megafarm API: ${op}`);
		if (op === 'num_unlocked') result = cap > 1 ? 1 : 0;
		else if (op === 'max_drones') result = cap;
		else if (op === 'get_world_size') result = size;
		else if (op === 'num_drones') result = actors.filter(other => !other.done).length;
		else if (op === 'spawn_drone') {
			spawnCount++;
			result = (failEvery && spawnCount % failEvery === 0) || actors.filter(other => !other.done).length >= cap
				? null : add(values[0](...copy(values.slice(1))));
		} else if (op === 'has_finished') result = values[0].done;
		else if (op === 'wait_for') { if (values[0].done) result = copy(values[0].result); else actor.blocked = values[0]; }
		else assert.equal(op, 'cpu');
		if (!actor.blocked) actor.value = result;
		actor.at = now + 1 + random(4);
		highWater = Math.max(highWater, actors.filter(other => !other.done).length);
		assert.ok(highWater <= cap);
	}
	assert.ok(rootActor.done && actors.every(actor => actor.done), 'Dispatcher did not join all descendants');
	assert.deepEqual(Array.from(rootActor.result), range(size).map(index => index === failingTask ? false : index * 3));
	assert.deepEqual(calls.sort((a, b) => a - b), range(size));
}
for (const size of [1, 3, 8, 22, 32]) for (const cap of [1, 2, 3, 32]) for (const refusal of [0, 1, 2, 7]) {
	check('dispatcher', () => dispatchModel(size, cap, refusal, refusal === 2 ? 0 : -1));
}

// Persistent row markers must protect adjacent and diagonal coal while workers
// complete at different speeds. The fixture uses stability one and bounded edges.
const coalWorkers = withoutModule(section(sources.get('coal'), 'cr_worker', 'collect'));
function coalModel(size, cap, failEvery) {
	const apis = ['get_world_size', 'get_pos_z', 'get_time', 'go_to', 'move', 'dig', 'spawn_drone', 'wait_job'];
	const ctx = context(coalWorkers, apis, directions), random = rng(size * 17 + cap * 13 + failEvery);
	const count = Math.min(size, cap), layers = 6;
	const bands = range(count).map(index => [Math.floor(size * index / count), Math.floor(size * (index + 1) / count)]);
	const depths = Array(size * size).fill(0);
	const ore = depths.map(() => new Set(range(2, layers).filter(() => random(5) === 0)));
	const available = ore.reduce((sum, levels) => sum + levels.size, 0), actors = [];
	const inside = (x, y) => x >= 0 && y >= 0 && x < size && y < size;
	const key = (x, y) => x + y * size;
	let now = 0, collected = 0, lost = 0, spawnCount = 0;
	function add(generator, pos) { const actor = {generator, pos: [...pos], at: now, value: undefined, done: false, blocked: null}; actors.push(actor); return actor; }
	const main = add(ctx.cr_world(bands, size, layers, 180), [0, 0]);
	for (let steps = 0; steps < 1500000; steps++) {
		for (const actor of actors) if (!actor.done && actor.blocked?.done) { actor.value = actor.blocked.result; actor.blocked = null; }
		const runnable = actors.filter(actor => !actor.done && !actor.blocked).sort((a, b) => a.at - b.at || actors.indexOf(a) - actors.indexOf(b));
		if (!runnable.length) break;
		const actor = runnable[0]; now = actor.at;
		const next = actor.generator.next(actor.value); actor.value = undefined;
		if (next.done) { actor.done = true; actor.result = next.value; continue; }
		const {op, args} = next.value; let value, duration = 1;
		if (cap === 1 && ['spawn_drone', 'wait_job'].includes(op)) throw Error(`Locked Megafarm API: ${op}`);
		if (op === 'get_world_size') value = size;
		else if (op === 'get_time') value = now / 1000;
		else if (op === 'get_pos_z') {
			const side = args[0];
			const x = side === undefined ? actor.pos[0] : mod(actor.pos[0] + dx[side], size);
			const y = side === undefined ? actor.pos[1] : mod(actor.pos[1] + dy[side], size);
			value = -depths[key(x, y)];
		} else if (op === 'go_to') { actor.pos = args.slice(0, 2); value = true; }
		else if (op === 'move') { actor.pos = [mod(actor.pos[0] + dx[args[0]], size), mod(actor.pos[1] + dy[args[0]], size)]; value = true; duration = 2; }
		else if (op === 'dig') {
			const [x, y] = actor.pos, cell = key(x, y), old = depths[cell];
			assert.ok(old < layers);
			if (ore[cell].has(old)) collected++;
			depths[cell]++;
			for (let sy = -1; sy <= 1; sy++) for (let sx = -1; sx <= 1; sx++) {
				if (!inside(x + sx, y + sy)) continue;
				const other = key(x + sx, y + sy);
				assert.ok(Math.abs(depths[cell] - depths[other]) <= 1, 'Premature row marker or unsafe diagonal');
				if (Math.abs(sx) + Math.abs(sy) === 1) for (let depth = depths[other]; depth < old; depth++) if (ore[other].has(depth)) lost++;
			}
			value = true; duration = 2 + random(40);
		} else if (op === 'spawn_drone') {
			spawnCount++;
			value = (failEvery && spawnCount % failEvery === 0) || actors.filter(other => !other.done).length >= cap
				? null : add(args[0](...copy(args.slice(1))), actor.pos);
		} else if (op === 'wait_job') { if (args[0].done) value = args[0].result; else actor.blocked = args[0]; }
		else assert.equal(op, 'cpu');
		if (!actor.blocked) actor.value = value;
		actor.at = now + duration;
	}
	assert.ok(main.done && actors.every(actor => actor.done), 'Coal workers did not join');
	assert.equal(main.result, true);
	assert.ok(depths.every(depth => depth === layers), 'Unmined column');
	assert.equal(collected, available); assert.equal(lost, 0);
}
for (const size of [1, 2, 3, 8, 22, 32]) for (const cap of [1, 2, 32]) {
	check('coalRowMarkers', () => coalModel(size, cap, 0));
}
for (const refusal of [1, 2, 7]) check('coalRowMarkers', () => coalModel(32, 32, refusal));

// Refill callers must clear first: the full coal sweep starts on a flat surface.
for (const size of [2, 8, 32]) for (const cap of [1, 32]) {
	check('oreRefillContracts', () => {
		let coal = 0, iron = 0, fresh = false, refills = 0;
		const ctx = context(withoutModule(section(sources.get('quartz'), 'quartz_supply', 'gr_quartz')),
			['count_jobs', 'num_items', 'ready', 'num_unlocked', 'get_world_size', 'reset'], {
				Items: {Coal: 'coal', Iron: 'iron'}, Unlocks: {Coal: 'coal', Iron: 'iron', Prospecting: 'prospecting'},
				coal: {collect: () => { assert.ok(fresh, 'Coal refill did not start after reset'); coal += 200; refills++; return 200; }},
				iron: {collect: () => { iron += cap * 12; return cap * 12; }}
			});
		assert.equal(run(ctx.quartz_supply(size), (op, args) => {
			if (op === 'count_jobs') return cap;
			if (op === 'num_items') return args[0] === 'coal' ? coal : iron;
			if (op === 'ready' || op === 'num_unlocked') return 1;
			if (op === 'get_world_size') return size;
			if (op === 'reset') { fresh = true; return; }
			throw Error(op);
		}), true);
		assert.equal(refills, 1);
	});
}

const rice = sources.get('rice');
for (const size of [1, 3, 8, 32]) {
	check('ricePhaseBarrier', () => {
		let prepared = false, farms = 0;
		const ctx = context(withoutModule(section(rice, 'gr_rice')), ['begin', 'get_world_size', 'seek', 'get_pos_z', 'bands', 'parallel', 'reset'], {
			Unlocks: {Rice: 'rice'}, Grounds: {Clay: 'clay'}, prepare_band: () => {}, rice_band: () => {}
		});
		assert.equal(run(ctx.gr_rice(1), (op, args) => {
			if (op === 'begin' || op === 'seek') return true;
			if (op === 'get_world_size') return size;
			if (op === 'get_pos_z') return -20;
			if (op === 'bands') return [[0, size]];
			if (op === 'parallel') {
				if (args[0] === ctx.prepare_band) { prepared = true; return [[[0, 0]]]; }
				assert.equal(args[0], ctx.rice_band); assert.ok(prepared, 'Rice planted before excavation joined'); farms++; return [1];
			}
			throw Error(op);
		}), true);
		assert.equal(farms, 1);
	});
	check('riceGrowthDoesNotDig', () => {
		let planted = false, ripeChecks = 0, harvested = 0;
		const ctx = context(withoutModule(section(rice, 'rice_band', 'gr_rice')),
			['get_world_size', 'go_to', 'get_ground_type', 'plant', 'get_entity_type', 'can_harvest', 'harvest'], {
				Grounds: {Clay: 'clay'}, Entities: {Rice: 'rice'}
			});
		assert.equal(run(ctx.rice_band([[0, 0]], size), op => {
			if (op === 'get_world_size') return size;
			if (op === 'go_to') return true;
			if (op === 'get_ground_type') return 'clay';
			if (op === 'plant') { planted = true; return true; }
			if (op === 'get_entity_type') return planted ? 'rice' : null;
			if (op === 'can_harvest') return ++ripeChecks >= 3;
			if (op === 'harvest') { assert.ok(ripeChecks >= 3); harvested++; return true; }
			throw Error(`Forbidden action during rice growth: ${op}`);
		}), 1);
		assert.equal(harvested, 1);
	});
}

// The bamboo geometry must leave a usable cardinal passage beside every plant.
const bamboo = sources.get('bamboo');
const geometry = withoutModule(section(bamboo, 'adjacent', 'bamboo_job'))
	.replaceAll('(y - 1) % size', 'mod(y - 1,size)').replaceAll('(x - 1) % size', 'mod(x - 1,size)')
	.replace(/\.append\(\((.*)\)\)/g, '.append([$1])');
for (const size of [2, 3, 8, 22, 31, 32, 64]) for (const cap of [1, 2, 32]) {
	check('bambooPassages', () => {
		const ctx = context(geometry, ['bands'], directions);
		const jobs = run(ctx.make_jobs(size, 8), op => {
			assert.equal(op, 'bands'); const count = Math.min(size, cap);
			return range(count).map(index => [Math.floor(size * index / count), Math.floor(size * (index + 1) / count)]);
		});
		const plants = new Set(), routes = [];
		for (const [positions, rounds] of jobs) {
			assert.equal(rounds, 8);
			for (const [x, y, px, py, way, back] of positions) {
				const key = x + y * size; assert.ok(!plants.has(key), 'Repeated bamboo owner'); plants.add(key);
				routes.push({x, y, px, py, way, back});
			}
		}
		for (const {x, y, px, py, way, back} of routes) {
			assert.ok(!plants.has(px + py * size), 'Bamboo passage was planted');
			assert.deepEqual([mod(x + dx[back], size), mod(y + dy[back], size)], [px, py]);
			assert.deepEqual([mod(px + dx[way], size), mod(py + dy[way], size)], [x, y]);
		}
		if (size === 32) assert.equal(plants.size, 806);
	});
}

for (const [size, rounds, failAt] of [[32, 1, 0], [31, 9, 0], [8, 17, 0], [32, 0, 2], [1, 3, 0]]) {
	check('bambooBatches', () => {
		let resets = 0, batches = 0, completed = 0;
		const controller = withoutModule(section(bamboo, 'gr_bamboo'));
		const ctx = context(controller, ['current_count', 'ready', 'num_unlocked', 'reset', 'change_hat', 'get_world_size', 'make_jobs', 'parallel', 'single'], {
			Unlocks: {Bamboo: 'bamboo', Timing: 'timing'}, Hats: {Gold_Hat: 'gold'}, bamboo_job: () => {}
		});
		assert.equal(run(ctx.gr_bamboo(rounds, 8), (op, args) => {
			if (op === 'current_count' || op === 'num_unlocked') return 1;
			if (op === 'ready') return true;
			if (op === 'get_world_size') return size;
			if (op === 'reset') { resets++; return; }
			if (op === 'change_hat') return;
			if (op === 'single') { completed++; return true; }
			if (op === 'make_jobs') return [[[], args[1]]];
			if (op === 'parallel') {
				batches++; const count = args[1][0][1];
				assert.ok(count > 0 && count <= 8); completed += count;
				return [batches !== failAt];
			}
			throw Error(op);
		}), failAt === 0);
		assert.equal(resets, 1);
		if (!failAt) assert.equal(completed, rounds);
		else assert.equal(batches, failAt);
	});
}

for (const size of [2, 3, 5, 7, 8, 9, 22, 31, 32, 33]) {
	check('mushroomPartitions', () => {
		let stock = 0, batches = 0;
		const controller = withoutModule(section(sources.get('mushrooms'), 'gr_mushrooms')).replace(/\.append\(\((.*)\)\)/g, '.append([$1])');
		const ctx = context(controller, ['current_count', 'begin', 'get_world_size', 'seek_mushroom', 'num_items', 'get_pos_z', 'parallel', 'reset'], {
			Unlocks: {Mushrooms: 'mushrooms'}, Items: {Mushroom: 'mushroom'}, tile: () => {}
		});
		assert.equal(run(ctx.gr_mushrooms(2, 4), (op, args) => {
			if (op === 'current_count') return 1;
			if (op === 'begin' || op === 'seek_mushroom') return true;
			if (op === 'get_world_size') return size;
			if (op === 'num_items') return stock;
			if (op === 'get_pos_z') return -64;
			if (op === 'reset') return;
			if (op === 'parallel') {
				batches++; const covered = new Set();
				for (const [ox, oy, width, height, depth, window] of args[1]) {
					assert.equal(depth, -64); assert.equal(window, 4);
					assert.ok(width > 0 && width <= 4 && height > 0 && height <= 8);
					for (let y = oy; y < oy + height; y++) for (let x = ox; x < ox + width; x++) {
						assert.ok(x >= 0 && x < size && y >= 0 && y < size);
						const cell = x + y * size; assert.ok(!covered.has(cell), 'Overlapping mushroom workers'); covered.add(cell);
					}
				}
				assert.equal(covered.size, size * size); stock += 100;
				return args[1].map(() => true);
			}
			throw Error(op);
		}), true);
		assert.equal(batches, 2);
	});
}

// Compare the solver's deductions to a hidden ground-truth mine layout.
const dynamite = sources.get('dynamite');
const inference = section(dynamite, 'mark', 'distance');
const logic = context(inference);
for (let seed = 1; seed <= 500; seed++) {
	check('dynamiteDeductions', () => {
		const random = rng(seed), size = 2 + random(7), wrap = seed % 2 === 0;
		const near = range(size * size).map(cell => {
			const neighbours = new Set();
			for (let sy = -1; sy <= 1; sy++) for (let sx = -1; sx <= 1; sx++) {
				let x = cell % size + sx, y = Math.floor(cell / size) + sy;
				if (!wrap && (x < 0 || y < 0 || x >= size || y >= size)) continue;
				x = mod(x, size); y = mod(y, size);
				if (x + y * size !== cell) neighbours.add(x + y * size);
			}
			return [...neighbours];
		});
		const mines = near.map(() => random(4) === 0);
		const state = mines.map(mine => mine ? (random(5) === 0 ? 2 : 0) : (random(3) === 0 ? 1 : 0));
		const clues = {}, front = new Set();
		for (let cell = 0; cell < state.length; cell++) if (state[cell] === 1) { clues[cell] = near[cell].filter(other => mines[other]).length; front.add(cell); }
		for (let pass = 0; pass < 4; pass++) {
			const result = run(logic.infer(state, clues, near, front, [...front]));
			assert.notEqual(result, null, 'Consistent clues rejected');
			for (let cell = 0; cell < state.length; cell++) {
				if (state[cell] === 2) assert.equal(mines[cell], true, 'False mine flag');
				if (state[cell] === 3) assert.equal(mines[cell], false, 'Unsafe forced move');
			}
			for (const cell of result[0]) { state[cell] = 1; clues[cell] = near[cell].filter(other => mines[other]).length; front.add(cell); }
		}
	});
}

// The initial D already digs the map. A non-D path needs one separate opening dig.
const treasure = withoutModule(section(sources.get('treasure_maps'), 'treasure', 'gr_treasure'));
for (const route of ['DNE', 'NED', 'DDN', 'EN']) {
	check('treasureMapStart', () => {
		const actions = []; let reads = 0;
		const ctx = context(treasure, ['seek', 'get_pos_z', 'measure', 'go_to', 'get_ground_type', 'get_world_size', 'dig_one', 'move', 'get_entity_type', 'harvest'], {
			...directions, Grounds: {Basalt: 'basalt', Treasure_Map: 'map'}, Entities: {Underground_Treasure: 'treasure'}
		});
		assert.equal(run(ctx.treasure(32), (op, args) => {
			if (op === 'seek' || op === 'go_to') return true;
			if (op === 'get_pos_z') return -20;
			if (op === 'measure') return ++reads === 1 ? [0, 0] : route;
			if (op === 'get_ground_type') return 'map';
			if (op === 'get_world_size') return 32;
			if (op === 'dig_one') { actions.push('D'); return true; }
			if (op === 'move') { actions.push(['N', 'E', 'S', 'W'][args[0]]); return true; }
			if (op === 'get_entity_type') return 'treasure';
			if (op === 'harvest') { actions.push('H'); return true; }
			throw Error(op);
		}), true);
		assert.equal(actions.join(''), (route[0] === 'D' ? '' : 'D') + route + 'H');
	});
}

console.log(`DLC source models passed: ${Object.entries(counts).map(([name, count]) => `${name}=${count}`).join(', ')}. These are models, not native game runs or speed benchmarks.`);
