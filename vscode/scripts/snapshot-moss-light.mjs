// Refresh the pinned light source from the sibling Moss checkout. Normal theme
// builds read the JSON snapshot and do not require Moss or Node dependencies.
import fs from 'node:fs';
import {parse,formatHex,formatHex8} from '../../../moss/node_modules/culori/src/index.js';
const moss = new URL('../../../moss/', import.meta.url);
const read = path => JSON.parse(fs.readFileSync(new URL(path,moss),'utf8'));
const state=read('data/state.json');
const mode=state.meta.colorModes.light;
const roles={},selected={};
for(const [role,pool] of Object.entries(mode.pools)){
 const c=pool.find(c=>c.id===mode.defaults[role])??pool[0];if(!c?.color)continue;
 const parsed=parse(c.color);roles[role]={color:(parsed.alpha??1)<1?formatHex8(parsed):formatHex(parsed)};
 if(c.background)roles[role].background=formatHex(parse(c.background));selected[role]=c.id;
}
const variants=Object.fromEntries(read('tokens/base/base.json').tokens.filter(t=>t.owner).map(t=>[t.key,t.light]));
const tokens=read('tokens/vscode/vscode.json').tokens;
const tokenMap=Object.fromEntries(tokens.map(t=>[t.key,t]));
const overrides=state.meta.linkOverrides;
function resolve(kind,key,seen=new Set()){
 const id=kind+':'+key;if(seen.has(id))throw new Error('Cyclic source link '+id);seen.add(id);
 const link=overrides[kind]?.[key];
 if(link)return resolve(link.kind,link.key,seen);
 if(kind==='role')return variants[key]??roles[key]?.color;
 const t=tokenMap[key];if(!t?.owner||t.structural)return;
 if(t.variant)return resolve('role',`${t.owner}.${t.variant}`,seen);
 return t.channel==='background'?roles[t.owner]?.background:resolve('role',t.owner,seen);
}
const colors={},semanticTokenColors={};
for(const t of tokens){
 if(t.structural||!t.owner)continue;
 const value=t.kind==='syntax'?resolve('role',t.owner):resolve('vscode',t.key);
 if(value)(t.kind==='syntax'?semanticTokenColors:colors)[t.key]=value.toUpperCase();
}
fs.writeFileSync(new URL('../palette/moss-light-source.json',import.meta.url),JSON.stringify({provenance:{state:'moss/data/state.json:meta.colorModes.light',tokens:'moss/tokens/vscode/vscode.json',variants:'moss/tokens/base/base.json',links:overrides,selected},colors,semanticTokenColors},null,2)+'\n');
