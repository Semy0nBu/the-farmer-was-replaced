import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

// Translate the mapping functions only. This checks worker cleanup against a
// small API model; it does not run the game's parser or estimate game speed.
const file = new URL('../scripts/04_special_farms/maze_stations.py', import.meta.url);
const source = fs.readFileSync(file,'utf8').split('\ndef has_wrap')[0];

const apiNames = ['get_world_size', 'get_pos_x', 'get_pos_y', 'get_entity_type',
  'can_move', 'move', 'measure', 'num_items', 'num_unlocked', 'max_drones',
  'num_drones', 'spawn_drone', 'has_finished', 'wait_for', 'plant', 'harvest', 'use_item'];

function parts(s) {
  const out = []; let depth = 0, from = 0;
  for (let i = 0; i < s.length; i++) {
    if ('([{'.includes(s[i])) depth++;
    if (')]}'.includes(s[i])) depth--;
    if (s[i] === ',' && depth === 0) { out.push(s.slice(from, i)); from = i + 1; }
  }
  out.push(s.slice(from)); return out;
}

function compile(src, extraApis = []) {
  const names = [...src.matchAll(/^def (\w+)\(/gm)].map(m => m[1]);
  const generators = new Set([...names, ...apiNames, ...extraApis]);
  function calls(s) {
    let out = '', from = 0;
    const re = /\b([A-Za-z_]\w*)\(/g;
    for (let m; (m = re.exec(s));) {
      const begin = re.lastIndex; let depth = 1, end = begin;
      while (end < s.length && depth) {
        if (s[end] === '(') depth++;
        if (s[end] === ')') depth--;
        end++;
      }
      if (depth) throw Error('Unbalanced expression: ' + s);
      const invocation = m[1] + '(' + calls(s.slice(begin, end - 1)) + ')';
      out += s.slice(from, m.index) + (generators.has(m[1]) ? '(yield* ' + invocation + ')' : invocation);
      from = end; re.lastIndex = end;
    }
    return out + s.slice(from);
  }
  function expr(s) {
    s = s.replace(/\b(\w+(?:\[[^\]]+\])?)\s+not\s+in\s+(\w+)\b/g, '!contains($2,$1)')
      .replace(/\b(\w+(?:\[[^\]]+\])?)\s+in\s+(\w+)\b/g, 'contains($2,$1)')
      .replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false').replace(/\bNone\b/g, 'null')
      .replace(/\band\b/g, '&&').replace(/\bor\b/g, '||').replace(/\bnot\b/g, '!')
      .replace(/\b(\w+)\s*\/\/\s*(\w+)\b/g, 'Math.floor($1 / $2)')
      .replace(/\.append\(/g, '.push(').replace(/\{(\w+):/g, '{[$1]:')
      .replace(/\.push\(\(([^()]*)\)\)/g, '.push([$1])')
      .replace('(x + xs[d]) % size + ((y + ys[d]) % size) * size',
        'mod(x + xs[d],size) + mod(y + ys[d],size) * size');
    return calls(s);
  }
  const out = [], blocks = [];
  const cpu = 'yield {op:"cpu",args:[]};';
  for (const raw of src.split('\n')) {
    const s = raw.trim(); if (!s || s.startsWith('#')) continue;
    const indent = raw.match(/^\t*/)[0].length;
    while (blocks.length && blocks.at(-1) >= indent) { out.push('}'); blocks.pop(); }
    let m;
    if ((m = s.match(/^def (\w+)\((.*)\):$/))) {
      out.push('function* ' + m[1] + '(' + expr(m[2]) + '){'); blocks.push(indent);

    } else if ((m = s.match(/^if (.*):$/))) {
      out.push('if (' + expr(m[1]) + '){'); blocks.push(indent);
    } else if ((m = s.match(/^elif (.*):$/))) {
      out.push('else if (' + expr(m[1]) + '){'); blocks.push(indent);
    } else if (s === 'else:') {
      out.push('else {'); blocks.push(indent);
    } else if ((m = s.match(/^while (.*):$/))) {
      out.push('while (' + expr(m[1]) + '){'); blocks.push(indent);
    } else if ((m = s.match(/^for (\w+) in (.*):$/))) {
      out.push('for(var ' + m[1] + ' of ' + expr(m[2]) + '){'); blocks.push(indent);
    } else if (s.startsWith('return ')) {
      const p = parts(s.slice(7));
      out.push(cpu, 'return ' + (p.length > 1 ? '[' + expr(p.join(',')) + ']' : expr(p[0])) + ';');
    } else if (s === 'return') out.push(cpu, 'return;');
    else if ((m = s.match(/^([\w, ]+) = (.*)$/))) {
      const lhs = m[1].trim();
      if (indent) out.push(cpu);
      out.push('var ' + (lhs.includes(',') ? '[' + lhs + ']' : lhs) + ' = ' + expr(m[2]) + ';');
    } else if (s === 'pass') out.push(cpu);
    else {
      if (indent) out.push(cpu);
      out.push(expr(s) + ';');
    }
  }
  while (blocks.length) { out.push('}'); blocks.pop(); }
  return out.join('\n');
}


function scenario(name,{slots=2,failMove=false,failBacktrack=false,entityLost=false,resize=false,spawnFail=false}={}) {
	const graph = [[2,1,-1,-1],[-1,-1,-1,0],[-1,3,0,-1],[-1,-1,-1,2]];
	const state = {cell:0,spawned:0,joined:0,checks:0,moves:0,done:false};
	const ctx = {
		North:0,East:1,South:2,West:3,
		Entities:{Hedge:'hedge',Treasure:'treasure'},
		range:n=>Array.from({length:n},(_,i)=>i),len:a=>a.length,
		contains:(a,k)=>Object.prototype.hasOwnProperty.call(a,k),
		mod:(a,b)=>(a%b+b)%b
	};
	for(const op of ['get_pos_x','get_pos_y','get_world_size','get_entity_type','can_move','move','spawn_drone','has_finished','num_drones','wait_for']) {
		ctx[op]=function*(...args){return yield {op,args};};
	}
	vm.createContext(ctx);
	new vm.Script(compile(source)).runInContext(ctx);
	const gen = ctx.map_maze(2,-1,slots);
	let value;
	for(let steps=0;steps<10000;steps++) {
		const item = gen.next(value);value=undefined;
		if(item.done){state.done=true;state.result=item.value;break;}
		const {op,args}=item.value;
		switch(op) {
			case 'cpu':break;
			case 'get_pos_x':value=state.cell%2;break;
			case 'get_pos_y':value=Math.floor(state.cell/2);break;
			case 'get_world_size':value=resize&&state.spawned?3:2;break;
			case 'get_entity_type':value=entityLost&&state.spawned?null:'hedge';break;
			case 'can_move':value=graph[state.cell][args[0]]!==-1;break;
			case 'move': {
				state.moves++;
				if((failMove&&state.spawned)||(failBacktrack&&state.spawned&&args[0]===3)) {value=false;break;}
				const next=graph[state.cell][args[0]];
				assert.notEqual(next,-1,'Move through wall');state.cell=next;value=true;break;
			}
			case 'spawn_drone':
				if(spawnFail){value=null;break;}
				assert.equal(state.spawned,0);state.spawned++;value=1;break;
			case 'has_finished':state.checks++;value=!resize&&state.checks>=2;break;
			case 'num_drones':value=resize?1:2;break;
			case 'wait_for':
				assert.ok(!resize,'Destroyed worker must not be waited on');
				state.joined++;value=[graph,0,[0,2,3]];break;
			default:throw Error('Unexpected API '+op);
		}
	}
	assert.ok(state.done,name+' did not return');
	if(failMove||failBacktrack||entityLost||resize) {
		assert.deepEqual(Array.from(state.result),[null,null,null],name+' must abort');
		assert.equal(state.joined,resize?0:1,name+' must join a surviving worker before returning');
	} else assert.ok(state.result[0],name+' must return a completed map');
	if(slots===1||spawnFail)assert.equal(state.joined,0);
	return {name,passed:true,spawned:state.spawned,joined:state.joined,moves:state.moves};
}

function finishRace(lost=false) {
	const state={checks:0,joined:0};
	const ctx={North:0,East:1,South:2,West:3};
	for(const op of ['get_world_size','has_finished','num_drones','wait_for'])ctx[op]=function*(...args){return yield {op,args};};
	vm.createContext(ctx);new vm.Script(compile(source)).runInContext(ctx);
	const gen=ctx.wait_map(1,2);let value,result;
	for(let i=0;i<100;i++){
		const item=gen.next(value);value=undefined;
		if(item.done){result=item.value;break;}
		switch(item.value.op){
			case 'cpu':break;
			case 'get_world_size':value=2;break;
			case 'has_finished':state.checks++;value=!lost&&state.checks>=2;break;
			case 'num_drones':value=1;break;
			case 'wait_for':state.joined++;value=['map','position','cells'];break;
			default:throw Error('Unexpected wait API');
		}
	}
	assert.equal(state.joined,lost?0:1);
	assert.deepEqual(Array.from(result),lost?[null,null,null]:['map','position','cells']);
	return {name:lost?'lost handle':'last worker finishes between sensors',passed:true};
}

const results=[
	scenario('move failure after spawn',{failMove:true}),
	scenario('backtrack failure after spawn',{failBacktrack:true}),
	scenario('maze removed after spawn',{entityLost:true}),
	scenario('resize destroys workers',{resize:true}),
	scenario('spawn failure falls back locally',{spawnFail:true}),
	scenario('single drone without worker APIs',{slots:1}),
	finishRace(),finishRace(true)
];

console.log('Checked '+results.length+' maze worker lifecycle regressions (model only).');
