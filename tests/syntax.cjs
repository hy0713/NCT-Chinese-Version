const fs=require('fs'),path=require('path'),assert=require('assert'),{spawnSync}=require('child_process');
const {babel}=require('./runtime.cjs');
const report={date:new Date().toISOString(),javascript:[],json:[],inlineScenarioScripts:0,errors:[]};
const html=fs.readFileSync('campaign-trail/index.html','utf8').replace(/<!--[\s\S]*?-->/g,'');
const files=new Set([...html.matchAll(/<script\s[^>]*src=["']([^"']+)/g)].map(m=>path.normalize(path.join('campaign-trail',m[1].startsWith('/')?'..'+m[1]:m[1]))));
for(const file of fs.readdirSync('static/js/us-map-1.0.1',{recursive:true}))if(file.endsWith('.js'))files.add(path.join('static/js/us-map-1.0.1',file));
for(const file of files){const check=spawnSync(process.execPath,['--check',file],{encoding:'utf8'});if(check.status!==0)report.errors.push({file,error:check.stderr});else report.javascript.push(file);}
for(const file of fs.readdirSync('localization',{recursive:true}).filter(f=>f.endsWith('.json'))){const full=path.join('localization',file);try{JSON.parse(fs.readFileSync(full,'utf8'));report.json.push(full);}catch(e){report.errors.push({file:full,error:e.message});}}
for(const s of require('../localization/stories/catalogue.json').scenarios)for(const m of fs.readFileSync(s.file,'utf8').matchAll(/<script\b[^>]*>([\s\S]*?)<\/script\s*>/gi)){try{babel.babelParse(m[1],s.scope+'.js',false);report.inlineScenarioScripts++;}catch(e){report.errors.push({file:s.file,error:e.message});}}
fs.writeFileSync('tests/syntax-results.json',JSON.stringify(report,null,2)+'\n');assert.deepEqual(report.errors,[]);console.log('PASS syntax:',report.javascript.length,'JS files,',report.inlineScenarioScripts,'scenario scripts,',report.json.length,'JSON files');
