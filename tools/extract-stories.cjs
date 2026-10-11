/* Read source ASTs without executing game code. Only explicit presentation fields
 * enter the catalogue; original English files are never rewritten. */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {babel}=require('../tests/runtime.cjs');
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const json=p=>JSON.parse(read(p));
const years=json('static/json/election_list.json'),candidates=json('static/json/candidate.json'),mates=json('static/json/running_mate.json');
const fields=new Set(['summary','recommended_reading','first_name','last_name','party','description','description_as_running_mate','electoral_victory_message','electoral_loss_message','no_electoral_majority_message','answer_feedback','name','stance_1','stance_2','stance_3','stance_4','stance_5','stance_6','stance_7','stance_desc_1','stance_desc_2','stance_desc_3','stance_desc_4','stance_desc_5','stance_desc_6','stance_desc_7']);
const records=[],scenarios=[],arrays={},diagnostics=[];
function add(scope,collection,id,field,source,location){
 if(typeof source!=='string'||!source.trim()||!/[A-Za-z\u3400-\u9fff]/.test(source.replace(/<[^>]*>/g,'')))return;
 const key=`${scope}/${collection}/${id}/${field}`;
 records.push({key,scope,collection,id,field,source,sha256:hash(source),location});
}
function entities(scope,collection,data,location){
 arrays[scope+'/'+collection]=data;
 const seen=new Set();
 for(const [i,row] of data.entries()){
  const id=row.pk??i;if(seen.has(id))diagnostics.push({type:'duplicate-id',scope,collection,id});seen.add(id);
  for(const [f,v] of Object.entries(row.fields||{}))if(fields.has(f))add(scope,collection,`${id}@${i}`,f,v,{...location,index:i,pk:id});
 }
}
function walk(node,visitor,ancestors=[]){if(!node||typeof node!=='object')return;visitor(node,ancestors);
 for(const [k,v] of Object.entries(node))if(!['loc','extra','comments','tokens'].includes(k)){
  if(Array.isArray(v))for(const n of v)walk(n,visitor,[...ancestors,node]);else if(v&&typeof v==='object')walk(v,visitor,[...ancestors,node]);
 }
}
function member(n){if(n?.type!=='MemberExpression')return '';return n.property.name??n.property.value??'';}
function literal(n){
 if(['StringLiteral','NumericLiteral','BooleanLiteral'].includes(n?.type))return n.value;
 if(n?.type==='NullLiteral')return null;
 if(n?.type==='UnaryExpression'&&n.operator==='-'&&n.argument.type==='NumericLiteral')return -n.argument.value;
 if(n?.type==='ArrayExpression')return n.elements.map(literal);
 if(n?.type==='ObjectExpression')return Object.fromEntries(n.properties.map(p=>{if(p.type!=='ObjectProperty'||p.computed)throw Error('Nonliteral data');return [p.key.name??p.key.value,literal(p.value)];}));
 throw Error('Nonliteral data '+n?.type);
}
const allIds=new Set(candidates.filter(c=>years.some(y=>y.id===c.fields.election)).map(c=>c.pk));
entities('base','election_json',json('static/json/election.json').filter(r=>years.some(y=>y.id===r.pk)),{file:'static/json/election.json'});
entities('base','candidate_json',candidates.filter(c=>allIds.has(c.pk)),{file:'static/json/candidate.json'});
for(const year of years)for(const candidate of candidates.filter(c=>c.fields.election===year.id&&c.fields.is_active===1))for(const pair of mates.filter(m=>m.fields.candidate===candidate.pk)){
 const mate=candidates.find(c=>c.pk===pair.fields.running_mate);if(!mate)throw Error('Dangling running mate '+pair.pk);
 const filename=`${year.display_year}_${candidate.fields.last_name}_${mate.fields.last_name}.html`;
 const file='static/questionset/'+filename,scope=filename.replace(/\.html$/,'');
 const scenario={scope,file,year:year.display_year,election:year.id,candidate:candidate.pk,runningMate:mate.pk,candidateName:candidate.fields.first_name+' '+candidate.fields.last_name,runningMateName:mate.fields.first_name+' '+mate.fields.last_name,sourceSha256:hash(read(file)),presentations:[]};scenarios.push(scenario);
 let scriptIndex=0;
 for(const match of read(file).matchAll(/<script\b[^>]*>([\s\S]*?)<\/script\s*>/gi)){
  const code=match[1],index=scriptIndex++;if(!code.trim())continue;
  const ast=babel.babelParse(code,file+'.'+index+'.js',false);
  walk(ast,(n,ancestors)=>{
   if(n.type==='StringLiteral'&&/https?:\/\//.test(n.value)){
    const parent=ancestors.at(-1),assignment=ancestors.findLast(a=>a.type==='AssignmentExpression');
    const property=member(assignment?.left);
    const setAttribute=parent?.type==='CallExpression'&&member(parent.callee)==='setAttribute'&&parent.arguments[0]?.value==='src';
    if((assignment&&['src','innerHTML','background','backgroundImage'].includes(property)&&!(parent.type==='CallExpression'&&member(parent.callee)==='parse'))||setAttribute)
     scenario.presentations.push({script:index,start:n.start,end:n.end,literal:code.slice(n.start,n.end),source:n.value,mode:'asset',property:property||'setAttribute(src)'});
   }
   if(n.type==='AssignmentExpression'&&n.right.type==='ArrayExpression'&&/_json$/.test(member(n.left))){
    entities(scope,member(n.left),literal(n.right),{file,script:index,line:n.loc.start.line});
   }
   if(n.type==='AssignmentExpression'&&n.right.type==='CallExpression'&&n.right.callee.type==='MemberExpression'&&n.right.callee.object.name==='JSON'&&member(n.right.callee)==='parse'&&n.right.arguments[0]?.type==='StringLiteral'){
    const collection=member(n.left),data=JSON.parse(n.right.arguments[0].value);
    if(Array.isArray(data))entities(scope,collection,data,{file,script:index,line:n.loc.start.line});
   }
   const ending=ancestors.some(a=>a.type==='FunctionDeclaration'&&a.id?.name==='endingPicker');
   if(n.type==='CallExpression'&&n.callee.name==='runDialogue'&&n.arguments[0]?.type==='StringLiteral'){
    const s=n.arguments[0];add(scope,'event',`s${index}.l${s.loc.start.line}.c${s.loc.start.column}`,'text',s.value,{file,script:index,line:s.loc.start.line,column:s.loc.start.column,start:s.start,end:s.end,literal:code.slice(s.start,s.end)});
   }
   // String fragments at presentation sites only. Comparison operands, paths,
   // identifiers and strings used by event logic are excluded.
   if(ending&&n.type==='StringLiteral'&&/[A-Za-z]{3}/.test(n.value.replace(/<[^>]*>/g,''))&&/\s/.test(n.value)&&!/^https?:\/\//.test(n.value)){
    const parent=ancestors.at(-1);
    if(parent?.type==='BinaryExpression'&&parent.operator!=='+')return;
    if(parent?.type==='CallExpression'&&parent.callee?.property?.name==='indexOf')return;
    add(scope,'ending',`s${index}.l${n.loc.start.line}.c${n.loc.start.column}`,'text',n.value,{file,script:index,line:n.loc.start.line,column:n.loc.start.column});
   }
  });
 }
 scenario.textEntries=records.filter(r=>r.scope===scope).length;
 scenario.collections=Object.fromEntries(Object.entries(arrays).filter(([k])=>k.startsWith(scope+'/')).map(([k,v])=>[k.split('/')[1],v.length]));
}
// Staff/lobby objects have executable callbacks: inspect literal properties,
// never evaluate them or extract callback strings as natural language.
const staffAst=babel.babelParse(read('static/js/sea_to_sea.js'),'staff.js',false);
function scalar(n){return n?.type==='NumericLiteral'||n?.type==='StringLiteral'?n.value:undefined;}
function prop(n,k){return n?.properties?.find(p=>(p.key.name??p.key.value)===k)?.value;}
walk(staffAst,n=>{if(n.type!=='AssignmentExpression'||member(n.left)!=='shining_info'||n.right.type!=='ArrayExpression')return;
 for(const config of n.right.elements){const election=scalar(prop(config,'pk')),candidate=scalar(prop(config,'candidate')),scope=`staff.${election}.${candidate}`;
  for(const kind of ['staff','lobby'])for(const [index,row] of (prop(config,kind)?.elements||[]).entries())for(const field of ['name','description'])add(scope,kind,`${scalar(prop(row,'pk'))}@${index}`,field,scalar(prop(row,field)),{file:'static/js/sea_to_sea.js',line:row.loc.start.line,pk:scalar(prop(row,'pk'))});
 }
});
const keys=new Set();for(const r of records){if(keys.has(r.key))throw Error('Duplicate translation key '+r.key);keys.add(r.key);}
fs.mkdirSync(path.join(root,'localization/stories'),{recursive:true});
const catalogue={schema:1,scenarios,records,diagnostics,stats:{scenarios:scenarios.length,entries:records.length,uniqueSources:new Set(records.map(r=>r.source)).size,sourceCharacters:[...new Set(records.map(r=>r.source))].reduce((n,s)=>n+s.length,0)}};
fs.writeFileSync(path.join(root,'localization/stories/catalogue.json'),JSON.stringify(catalogue,null,2)+'\n');
fs.mkdirSync(path.join(root,'.test-artifacts/stories'),{recursive:true});
fs.writeFileSync(path.join(root,'.test-artifacts/stories/source-data.json'),JSON.stringify(arrays)+'\n');
console.log(JSON.stringify(catalogue.stats));console.log('Diagnostics',JSON.stringify(diagnostics));
