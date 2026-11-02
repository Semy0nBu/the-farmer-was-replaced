import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const errors = [];
const fail = (file, message) => errors.push(`${file}: ${message}`);

async function walk(dir) {
	const files = [];
	for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
		if (entry.name === '.git' || entry.name === 'node_modules') continue;
		const file = path.join(dir, entry.name);
		if (entry.isDirectory()) files.push(...await walk(file));
		else files.push(file);
	}
	return files.sort();
}

const relative = file => path.relative(root, file).replaceAll(path.sep, '/');
const files = await walk(root);
const scripts = files.filter(file => file.endsWith('.py'));
const catalogs = files.filter(file => path.basename(file) === 'catalog.json');
const entries = new Map();

for (const catalog of catalogs) {
	const list = JSON.parse(await fs.readFile(catalog, 'utf8'));
	if (!Array.isArray(list)) {
		fail(relative(catalog), 'catalog must be an array');
		continue;
	}
	for (const item of list) {
		if (typeof item.file !== 'string' || !/^scripts\/[a-z0-9_/]+\.py$/.test(item.file)) {
			fail(relative(catalog), 'invalid script path');
			continue;
		}
		if (entries.has(item.file)) fail(item.file, 'duplicate catalog entry');
		entries.set(item.file, item);
		for (const key of ['title', 'purpose', 'start']) {
			if (typeof item[key] !== 'string' || !item[key].trim()) fail(item.file, `missing ${key}`);
		}
		if (!Array.isArray(item.requires) || item.requires.some(req => typeof req !== 'string')) fail(item.file, 'invalid requirements');
		if (typeof item.uses_clear !== 'boolean') fail(item.file, 'uses_clear must be boolean');
		try { await fs.access(path.join(root, item.file)); }
		catch { fail(item.file, 'catalog points to a missing file'); }
	}
}

const allowed = {
	Entities: new Set(['Grass', 'Bush', 'Tree', 'Carrot', 'Pumpkin', 'Dead_Pumpkin', 'Sunflower', 'Cactus', 'Apple', 'Hedge', 'Treasure']),
	Grounds: new Set(['Grassland', 'Soil']),
	Items: new Set(['Hay', 'Wood', 'Carrot', 'Pumpkin', 'Power', 'Cactus', 'Bone', 'Gold', 'Water', 'Fertilizer', 'Weird_Substance']),
	Hats: new Set(['Gold_Hat', 'Dinosaur_Hat']),
	Unlocks: new Set(['Plant', 'Carrots', 'Trees', 'Pumpkins', 'Sunflowers', 'Cactus', 'Dinosaurs', 'Mazes', 'Megafarm', 'Watering', 'Fertilizer', 'Polyculture'])
};

for (const file of scripts) {
	const name = relative(file);
	const source = await fs.readFile(file, 'utf8');
	const item = entries.get(name);
	if (!item) {
		fail(name, 'missing catalog entry');
		continue;
	}
	const has = term => item.requires.some(req => req.startsWith(term));
	const need = (term, why) => { if (!has(term)) fail(name, `requires ${term} for ${why}`); };
	if (path.basename(file, '.py').length > 20) fail(name, 'window name exceeds 20 characters');
	if (source.charCodeAt(0) === 0xfeff) fail(name, 'UTF-8 BOM');
	if (source.includes('\r')) fail(name, 'use LF line endings');
	if (!source.endsWith('\n')) fail(name, 'missing final newline');
	for (const [index, line] of source.split('\n').entries()) {
		if (/^\t* +\S/.test(line)) fail(name, `space indentation on line ${index + 1}`);
		if (/[ \t]+$/.test(line)) fail(name, `trailing whitespace on line ${index + 1}`);
	}
	if (/\b(?:print|quick_print|leaderboard_run)\s*\(|\bLeaderboards\./.test(source)) fail(name, 'output or leaderboard API');
	if (/\b(?:dig|can_dig|jump|place|collapse|get_pos_z|get_hardness|prospect)\s*\(/.test(source)) fail(name, 'DLC API');
	if (/^\s*(?:from\s|import\s)/m.test(source)) fail(name, 'scripts must be self-contained');
	if (/\b(?:set_world_size|set_execution_speed)\s*\(/.test(source)) fail(name, 'farm should not change world size or execution speed');
	for (const match of source.matchAll(/\b(Entities|Grounds|Items|Hats|Unlocks)\.([A-Za-z_][A-Za-z_0-9]*)/g)) {
		if (!allowed[match[1]].has(match[2])) fail(name, `unexpected base-game constant ${match[0]}`);
	}
	if (/^\s*while\b/m.test(source)) need('Loops', 'while');
	if (/^\s*def\b/m.test(source)) need('Functions', 'custom functions');
	if (/^\s*(?:if|elif)\b/m.test(source)) need('Speed', 'if');
	if (/\b(?:get_world_size|range)\s*\(/.test(source)) need('Expand', 'square-field loops');
	if (/\b(?:get_pos_x|get_pos_y|get_entity_type|get_ground_type|num_items|num_unlocked)\s*\(/.test(source)) need('Senses', 'sensors');
	if (/\bplant\s*\(/.test(source)) need('Plant', 'planting');
	if (/\btill\s*\(/.test(source)) need('Carrots', 'tilling');
	if (/\bget_companion\s*\(/.test(source)) need('Polyculture', 'companion requests');
	if (/\bget_cost\s*\(/.test(source)) need('Costs', 'cost queries');
	if (/\b(?:min|max|abs|random)\s*\(/.test(source)) need('Utilities', 'utility functions');
	if (/\.append\s*\(|=\s*\[/.test(source)) need('Lists', 'lists');
	if (/=\s*\{|\bset\s*\(/.test(source)) need('Dictionaries', 'dictionaries or sets');
	if (/\b(?:max_drones|num_drones|spawn_drone|has_finished|wait_for)\s*\(/.test(source) && !/num_unlocked\(Unlocks\.Megafarm\)/.test(source)) {
		need('Megafarm', 'unguarded drone APIs');
	}
	if (/\bclear\s*\(/.test(source) !== item.uses_clear) fail(name, 'clear() does not match catalog');
	if (/\bItems\.Water\b|\bget_water\s*\(/.test(source) && path.basename(file) !== 'poly_wood.py') fail(name, 'unexpected watering');
	if (/\bItems\.Fertilizer\b/.test(source) && path.basename(file) !== 'weird_substance.py') fail(name, 'unexpected fertilizer');
}

const privatePattern = /C:[\\/]Users[\\/]|\/Users\/|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9]{24,}/;
for (const file of files) {
	const name = relative(file);
	if (/\.(?:png|jpg|zip|exe|dll)$/i.test(file)) { fail(name, 'unexpected binary'); continue; }
	const source = await fs.readFile(file, 'utf8');
	if (privatePattern.test(source)) fail(name, 'private path or credential pattern');
	if (!file.endsWith('.md')) continue;
	for (const match of source.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
		let target = match[1].replace(/^<|>$/g, '').split('#')[0];
		if (!target || /^[a-z]+:/i.test(target)) continue;
		target = decodeURIComponent(target);
		const resolved = path.resolve(path.dirname(file), target);
		if (path.relative(root, resolved).startsWith('..')) { fail(name, `link leaves repository: ${target}`); continue; }
		try { await fs.access(resolved); }
		catch { fail(name, `broken link: ${target}`); }
	}
}

if (errors.length) {
	for (const error of errors) console.error(error);
	process.exitCode = 1;
} else {
	console.log(`Checked ${scripts.length} scripts, ${catalogs.length} catalogs, requirements, repository links and publication hygiene.`);
}
