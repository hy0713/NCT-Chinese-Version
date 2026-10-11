// Check canonical AST hashes against the untouched upstream algorithm snapshot.
const fs=require('fs'),assert=require('assert'),crypto=require('crypto');
const b=require('./runtime.cjs').babel;
const names=new Set(['A','F','divideElectoralVotesProp','dHondtAllocation','M','E','S']);
function clean(node){
 if(Array.isArray(node))return node.map(clean);
 if(node&&typeof node==='object')return Object.fromEntries(Object.entries(node).filter(([key])=>!['start','end','loc','extra','comments','leadingComments','trailingComments','innerComments'].includes(key)).map(([k,v])=>[k,clean(v)]));
 return node;
}
function hashes(file){const result={};
 function walk(n){if(!n||typeof n!=='object')return;
 const name=n.type==='FunctionDeclaration'?n.id?.name:n.type==='VariableDeclarator'&&['ArrowFunctionExpression','FunctionExpression'].includes(n.init?.type)?n.id.name:null;
 if(names.has(name))result[name]=crypto.createHash('sha256').update(JSON.stringify(clean(n))).digest('hex');
 for(const[k,v]of Object.entries(n))if(!['loc','extra','comments'].includes(k)){if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v==='object')walk(v);}
 }walk(b.babelParse(fs.readFileSync(file,'utf8'),file,false));return result;
}
function embeddedData(file){const result=[];
 function walk(n){if(!n||typeof n!=='object')return;
 if(n.type==='CallExpression'&&n.callee.type==='MemberExpression'&&n.callee.object.name==='JSON'&&n.callee.property.name==='parse'&&n.arguments[0]?.type==='StringLiteral')result.push(crypto.createHash('sha256').update(n.arguments[0].value).digest('hex'));
 for(const[k,v]of Object.entries(n))if(!['loc','extra','comments'].includes(k)){if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v==='object')walk(v);}
 }walk(b.babelParse(fs.readFileSync(file,'utf8'),file,false));return result;
}
if(process.argv.includes('--capture')) {
 fs.writeFileSync('tests/original-algorithm-sha256.json',JSON.stringify({commit:'d6655ef6ad80ab9a8fe5510d0fd43874e57dacbf',functions:hashes('.test-artifacts/original/campaign_trail.js'),embedded:{'campaign_trail.js':embeddedData('.test-artifacts/original/campaign_trail.js'),'indexCode.js':embeddedData('.test-artifacts/original/indexCode.js')},staff:crypto.createHash('sha256').update(fs.readFileSync('static/js/sea_to_sea.js')).digest('hex')},null,2));
}
const baseline=JSON.parse(fs.readFileSync('tests/original-algorithm-sha256.json','utf8'));
assert.deepEqual(hashes('static/js/campaign_trail.js'),baseline.functions);
for(const[file,hashes]of Object.entries(baseline.embedded))assert.deepEqual(embeddedData('static/js/'+file),hashes,file);
assert.equal(crypto.createHash('sha256').update(fs.readFileSync('static/js/sea_to_sea.js')).digest('hex'),baseline.staff);
const data=JSON.parse(fs.readFileSync('tests/original-data-sha256.json','utf8'));
for(const [file,digest] of Object.entries(data))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),digest,file);
const en=JSON.parse(fs.readFileSync('localization/en-US.json','utf8')),zh=JSON.parse(fs.readFileSync('localization/zh-CN.json','utf8'));
assert.deepEqual(Object.keys(en).sort(),Object.keys(zh).sort());
for(const key of Object.keys(en))assert.deepEqual((en[key].match(/\{\w+\}/g)||[]).sort(),(zh[key].match(/\{\w+\}/g)||[]).sort(),key);
for(const key of Object.keys(en))assert.ok(zh[key].length,key);
console.log(`PASS ${Object.keys(baseline.functions).length} original algorithms, ${Object.keys(data).length} original data files, ${Object.keys(en).length} bilingual keys and variable signatures`);
