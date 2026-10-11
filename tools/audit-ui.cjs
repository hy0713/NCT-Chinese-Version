const fs=require('fs');
const babel=require('../tests/runtime.cjs').babel;
const files=['campaign_trail.js','indexCode.js','bigshot.js','campaign_trail_other.js','christmas.js'];
const out=[];
for(const file of files) {
 const ast=babel.babelParse(fs.readFileSync('static/js/'+file,'utf8'),file,false);
 function walk(n) {
  if(!n||typeof n!=='object')return;
  let s=n.type==='StringLiteral'?n.value:n.type==='TemplateElement'?(n.value.cooked||n.value.raw):null;
  if(s&&s.includes('<')) {
   s=s.replace(/<span\b[^>]*data-i18n[^>]*>[\s\S]*?<\/span>/g,'').replace(/<!--[\s\S]*?-->/g,'');
   const words=[...s.matchAll(/(?:^|>)([^<>]+)(?=<|$)/g)].map(m=>m[1].replace(/\s+/g,' ').trim()).filter(s=>/[a-zA-Z]{2}/.test(s)&&!/[={}]/.test(s));
   if(words.length)out.push({file,line:n.loc.start.line,words});
  }
  for(const [k,v]of Object.entries(n))if(!['loc','extra','comments'].includes(k)){if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v==='object')walk(v);}
 }walk(ast);
}
console.log(JSON.stringify(out,null,2));
