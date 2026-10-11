const fs=require('fs'),b=require('../tests/runtime.cjs').babel;
const source=JSON.parse(fs.readFileSync('localization/source-keys.json','utf8')),values=new Set();
function walk(n){if(!n||typeof n!=='object')return;
 if(n.type==='ObjectProperty'&&n.key.name==='description'&&n.value.type==='StringLiteral'){
  const first=n.value.value.match(/^<p>(.*?)<\/p>/s)?.[1] || n.value.value;
  for(const m of first.matchAll(/(?:^|>)([^<>]+)(?=<|$)/g)) {const s=m[1].replace(/\s+/g,' ').trim();if(/[A-Za-z]{2}/.test(s)&&!source[s])values.add(s);}
 }
 for(const[k,v]of Object.entries(n))if(!['loc','extra','comments'].includes(k)){if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v==='object')walk(v);}
}walk(b.babelParse(fs.readFileSync('static/js/sea_to_sea.js','utf8'),'sea.js',false));
console.log(JSON.stringify([...values],null,2));
