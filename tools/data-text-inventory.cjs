const fs=require('fs');
const b=require('../tests/runtime.cjs').babel;
const issues=new Set(), achievements=[];
function walk(n){if(!n||typeof n!=='object')return;
 if(n.type==='AssignmentExpression'&&n.left.type==='MemberExpression'&&n.left.property.name==='issues_json'&&n.right.type==='CallExpression'&&n.right.arguments[0]?.type==='StringLiteral') {
  for(const item of JSON.parse(n.right.arguments[0].value)) for(const [key,value] of Object.entries(item.fields)) if(key==='name'||/^stance_[1-7]$/.test(key)) if(typeof value==='string'&&value) issues.add(value);
 }
 if(n.type==='AssignmentExpression'&&n.left.name==='achList') for(const p of n.right.properties) achievements.push([p.key.value,...p.value.elements.filter(e=>e?.type==='StringLiteral').map(e=>e.value)]);
 for(const [k,v] of Object.entries(n)) if(!['loc','extra','comments'].includes(k)){if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v==='object')walk(v);}
}
walk(b.babelParse(fs.readFileSync('static/js/campaign_trail.js','utf8'),'game.js',false));
for(const file of fs.readdirSync('static/questionset')){
 let html=fs.readFileSync('static/questionset/'+file,'utf8');
 for(const m of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g))if(m[1].trim())try{walk(b.babelParse(m[1],file+'.js',false));}catch(e){console.error(file,e.message);}
}
console.log(JSON.stringify({issues:[...issues].sort(),achievements},null,2));
fs.writeFileSync('tests/data-text-inventory.json',JSON.stringify({issues:[...issues].sort(),achievements},null,2));
