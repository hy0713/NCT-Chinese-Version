/* Validate the complete extraction and its offline packs against upstream. */
const fs=require('fs'),assert=require('assert'),crypto=require('crypto'),{spawnSync}=require('child_process');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8')),sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const cat=read('localization/stories/catalogue.json');
const extracted=spawnSync(process.execPath,['tools/extract-stories.cjs'],{encoding:'utf8'});assert.equal(extracted.status,0,extracted.stderr);
assert.deepEqual(read('localization/stories/catalogue.json'),cat,'Extraction must be reproducible');
assert.equal(cat.scenarios.length,105);assert.equal(new Set(cat.scenarios.map(s=>s.scope)).size,105);
const original=read('tests/original-data-sha256.json');for(const[file,digest]of Object.entries(original))assert.equal(sha(fs.readFileSync(file)),digest,file);
const shapes=read('.test-artifacts/stories/source-data.json');
const protectedFields=['pk','model','priority','likelihood','issue_score','question','answer','candidate','running_mate','affected_candidate','state','electoral_votes'];
const report={date:new Date().toISOString(),scenarios:105,sourceFiles:Object.keys(original).length,entries:cat.records.length,checks:[],missing:[],qualityWarnings:[],references:[],duplicateIds:cat.diagnostics};
// Verify the exact runtime adapter: after removing its two permitted text/asset
// wrappers, every loaded script has the same AST as the original script.
const vm=require('vm'),babel=require('./runtime.cjs').babel;
const sandbox={console,NCTI18n:{language:'en-US'},XMLHttpRequest:class{open(_method,url){this.url=url;}send(){try{this.responseText=fs.readFileSync('.'+this.url,'utf8');this.status=200;}catch(_){this.status=404;}}}};
sandbox.window=sandbox;vm.createContext(sandbox);vm.runInContext(fs.readFileSync('localization/stories.js','utf8'),sandbox);
function canonical(n){
 if(Array.isArray(n))return n.map(canonical);
 if(!n||typeof n!=='object')return n;
 if(n.type==='CallExpression'&&n.callee.object?.name==='NCTStory'&&['eventValue','assetMarkup'].includes(n.callee.property?.name))return canonical(n.arguments[n.callee.property.name==='eventValue'?1:0]);
 return Object.fromEntries(Object.entries(n).filter(([k])=>!['start','end','loc','extra','comments','leadingComments','trailingComments','innerComments'].includes(k)).map(([k,v])=>[k,canonical(v)]));
}
for(const s of cat.scenarios){
 const source=fs.readFileSync(s.file,'utf8');sandbox.NCTStory.use(s.file);const loaded=sandbox.NCTStory.prepare(source);
 const scripts=h=>[...h.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script\s*>/gi)].map(m=>m[1]);
 const before=scripts(source),after=scripts(loaded);assert.equal(after.length,before.length,s.scope);
 before.forEach((code,i)=>assert.deepEqual(canonical(babel.babelParse(after[i],s.scope+'.js',false)),canonical(babel.babelParse(code,s.scope+'.js',false)),'Runtime adapter changed execution logic: '+s.scope));
}
const tag=s=>(s.match(/<(?:\/?[A-Za-z][^>]*|!--[\s\S]*?--)>/g)||[]);
const tokens=s=>(s.match(/\{\{.*?\}\}|\$\{.*?\}|\{[A-Za-z_]\w*\}|&(?:#\d+|#x[\da-fA-F]+|\w+);|https?:\/\/[^\s<>]+/g)||[]);
const packs=new Map();
for(const r of cat.records){
 if(!packs.has(r.scope))packs.set(r.scope,read('localization/stories/'+r.scope+'.pack.json'));
 const p=packs.get(r.scope);assert.equal(p.en[r.key],r.source,r.key);assert.equal(sha(r.source),r.sha256,r.key);
 const index=p.index[r.collection]?.[String(r.location.pk??r.id)]?.[r.field]||[];assert.ok(index.includes(r.key),'Unindexed '+r.key);
 const zh=p.zh[r.key];if(!zh){report.missing.push(r.key);continue;}
 assert.ok(typeof zh==='string'&&zh.trim(),r.key);
 assert.deepEqual(tag(zh),tag(r.source),'HTML tags/attributes changed '+r.key);
 assert.deepEqual(tokens(zh),tokens(r.source),'Placeholder/entity/URL changed '+r.key);
 if(r.collection==='event')assert.deepEqual(zh.match(/\^+|</g),r.source.match(/\^+|</g),'Typewriter controls '+r.key);
 if(/[A-Za-z]{3}/.test(r.source.replace(/<[^>]*>/g,''))&&!/[\u3400-\u9fff]/.test(zh))report.qualityWarnings.push({key:r.key,kind:'no-Chinese',source:r.source,zh});
 if(/\ufffd/.test(zh))report.qualityWarnings.push({key:r.key,kind:'replacement-character',zh});
}
// The source-file hashes above cover every field and record order. Reference
// auditing is separate: pre-existing dangling rows are reported, never repaired.
for(const scenario of cat.scenarios){
 const a=Object.fromEntries(Object.entries(shapes).filter(([k])=>k.startsWith(scenario.scope+'/')).map(([k,v])=>[k.split('/')[1],v]));
 for(const [collection,field,target]of [['answers_json','question','questions_json'],['answer_feedback_json','answer','answers_json'],['answer_score_global_json','answer','answers_json'],['answer_score_issue_json','answer','answers_json'],['answer_score_state_json','answer','answers_json']]){
  const ids=new Set((a[target]||[]).map(r=>r.pk));
  for(const r of a[collection]||[])if(!ids.has(r.fields[field]))report.references.push({scope:scenario.scope,collection,pk:r.pk,field,value:r.fields[field],status:'upstream reference outside loaded collection'});
 }
}
report.checks.push('105 scenario source files and six JSON source files byte-identical','105 loaded scenario script ASTs identical after unwrapping explicit presentation adapters','All natural-language keys unique and indexed','Exact original English and SHA-256 retained','HTML tags, attributes, entities, URLs and variable tokens preserved','Record counts/order, references and all numeric fields untouched (source-file hashes)');
fs.writeFileSync('tests/stories-integrity-results.json',JSON.stringify(report,null,2)+'\n');
assert.equal(report.missing.length,0,'Incomplete translations: '+report.missing.slice(0,5));
console.log(`PASS ${cat.scenarios.length} pairings; ${cat.records.length} entries; original source bytes and markup intact; ${report.qualityWarnings.length} quality warnings; ${report.references.length} original out-of-collection references`);
