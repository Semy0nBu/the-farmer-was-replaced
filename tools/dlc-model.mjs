// A small source translator for the algorithm models in check-dlc.mjs.
// This is not the game's interpreter, geology or timing model.
import vm from 'node:vm';

export const range = (start, end, step = 1) => {
	if (end === undefined) { end = start; start = 0; }
	const result = [];
	for (let n = start; step > 0 ? n < end : n > end; n += step) result.push(n);
	return result;
};
export const mod = (a, b) => ((a % b) + b) % b;
export const contains = (value, key) => value instanceof Set ? value.has(key)
	: Array.isArray(value) || typeof value === 'string' ? value.includes(key) : Object.hasOwn(value, key);
export const iter = value => value[Symbol.iterator] ? value
	: Object.keys(value).map(key => /^\d+$/.test(key) ? Number(key) : key);
export const len = value => value.size ?? value.length ?? Object.keys(value).length;
export const set = values => new Set(values);
export const list = values => Array.from(iter(values));
export const floor_div = (a, b) => Math.floor(a / b);
export function rng(seed) {
	let state = seed >>> 0;
	return limit => { state = (Math.imul(state, 1664525) + 1013904223) >>> 0; return Math.floor(state / 4294967296 * limit); };
}

function split(source) {
	const parts = []; let depth = 0, start = 0;
	for (let n = 0; n < source.length; n++) {
		if ('([{'.includes(source[n])) depth++;
		if (')]}'.includes(source[n])) depth--;
		if (source[n] === ',' && depth === 0) { parts.push(source.slice(start, n)); start = n + 1; }
	}
	parts.push(source.slice(start)); return parts;
}

function floorDivision(source) {
	for (let index; (index = source.indexOf('//')) >= 0;) {
		let begin = index - 1, end = index + 2, depth = 0;
		for (; begin >= 0; begin--) {
			const char = source[begin];
			if (')]}'.includes(char)) depth++;
			else if ('([{'.includes(char)) { if (depth === 0) break; depth--; }
			else if (depth === 0 && '+-,<>=!&|?:'.includes(char)) break;
		}
		depth = 0;
		for (; end < source.length; end++) {
			const char = source[end];
			if ('([{'.includes(char)) depth++;
			else if (')]}'.includes(char)) { if (depth === 0) break; depth--; }
			else if (depth === 0 && '*/%+-,<>=!&|?:'.includes(char)) break;
		}
		const left = source.slice(begin + 1, index).trim(), right = source.slice(index + 2, end).trim();
		if (!left || !right) throw Error(`Unsupported integer division: ${source}`);
		source = source.slice(0, begin + 1) + `floor_div(${left},${right})` + source.slice(end);
	}
	return source;
}

export function section(source, first, next) {
	const from = source.indexOf(`def ${first}(`);
	if (from < 0) throw Error(`Missing function ${first}`);
	const end = next ? source.indexOf(`def ${next}(`, from + 1) : source.indexOf('\nif __name__', from);
	if (next && end < 0) throw Error(`Missing function ${next}`);
	return source.slice(from, end < 0 ? undefined : end);
}

export function compile(source, apis = []) {
	const functions = new Set([...source.matchAll(/^def (\w+)\(/gm)].map(match => match[1]));
	const generators = new Set([...functions, ...apis]);
	function calls(text) {
		const pattern = /\b([A-Za-z_]\w*)\(/g;
		let result = '', start = 0;
		for (let match; (match = pattern.exec(text));) {
			const begin = pattern.lastIndex; let depth = 1, end = begin;
			while (end < text.length && depth) {
				if (text[end] === '(') depth++;
				if (text[end] === ')') depth--;
				end++;
			}
			if (depth) throw Error(`Unbalanced expression: ${text}`);
			const invocation = `${match[1]}(${calls(text.slice(begin, end - 1))})`;
			result += text.slice(start, match.index) + (generators.has(match[1]) ? `(yield* ${invocation})` : invocation);
			start = end; pattern.lastIndex = end;
		}
		return result + text.slice(start);
	}
	function expression(text) {
		return calls(floorDivision(text.replace(/\b(\w+(?:\[[^\]]+\])?)\s+not\s+in\s+(\w+)\b/g, '!contains($2,$1)')
			.replace(/\b(\w+(?:\[[^\]]+\])?)\s+in\s+(\w+)\b/g, 'contains($2,$1)')
			.replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false').replace(/\bNone\b/g, 'null')
			.replace(/\band\b/g, '&&').replace(/\bor\b/g, '||').replace(/\bnot\b/g, '!')
			.replace(/\.append\(/g, '.push(').replace(/\.remove\(/g, '.delete(')
			.replace(/\{(\w+):/g, '{[$1]:').replace(/\.push\(\(([^()]*)\)\)/g, '.push([$1])')));
	}
	const output = [], blocks = [];
	const tick = 'yield {op:"cpu",args:[]};';
	for (const raw of source.split('\n')) {
		const text = raw.trim();
		if (!text || text.startsWith('#') || text.startsWith('global ')) continue;
		const indent = raw.match(/^\t*/)[0].length;
		while (blocks.length && blocks.at(-1) >= indent) { output.push('}'); blocks.pop(); }
		let match;
		if ((match = text.match(/^def (\w+)\((.*)\):$/))) {
			output.push(`function* ${match[1]}(${expression(match[2])}){`); blocks.push(indent);
		} else if ((match = text.match(/^(if|elif|while) (.*):$/))) {
			output.push(`${match[1] === 'elif' ? 'else if' : match[1]} (${expression(match[2])}){`); blocks.push(indent);
		} else if (text === 'else:') { output.push('else {'); blocks.push(indent); }
		else if ((match = text.match(/^for (\w+) in (.*):$/))) {
			output.push(`for(var ${match[1]} of iter(${expression(match[2])})){`); blocks.push(indent);
		} else if (text.startsWith('return ')) {
			const parts = split(text.slice(7));
			output.push(tick, `return ${parts.length > 1 ? `[${expression(parts.join(','))}]` : expression(parts[0])};`);
		} else if (text === 'return') output.push(tick, 'return;');
		else if ((match = text.match(/^([\w, ]+) = (.*)$/))) {
			if (indent) output.push(tick);
			const names = match[1].trim();
			output.push(`var ${names.includes(',') ? `[${names}]` : names} = ${expression(match[2])};`);
		} else if (text === 'pass') output.push(tick);
		else { if (indent) output.push(tick); output.push(`${expression(text)};`); }
	}
	while (blocks.length) { output.push('}'); blocks.pop(); }
	return output.join('\n');
}

export function context(source, apis = [], values = {}) {
	const ctx = { range, mod, contains, iter, len, set, list, floor_div, min: Math.min, max: Math.max, abs: Math.abs, ...values };
	for (const name of apis) ctx[name] = function* (...args) { return yield {op: name, args}; };
	vm.createContext(ctx);
	new vm.Script(compile(source, apis)).runInContext(ctx);
	return ctx;
}

export function run(generator, action = op => { throw Error(`Unexpected API ${op}`); }, limit = 3000000) {
	let value;
	for (let count = 0; count < limit; count++) {
		const next = generator.next(value);
		if (next.done) return next.value;
		value = next.value.op === 'cpu' ? undefined : action(next.value.op, next.value.args);
	}
	throw Error('Model operation limit reached');
}
