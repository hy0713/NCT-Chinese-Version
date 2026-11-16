/* Real browser lifetime checks plus actual cmd/batch argument forwarding. */
const fs=require('fs'),path=require('path'),assert=require('assert'),{spawn,spawnSync}=require('child_process');
const {chromium}=require('./runtime.cjs');
const root=path.resolve(__dirname,'..'),artifacts=path.join(root,'.test-artifacts');fs.mkdirSync(artifacts,{recursive:true});
const python=process.env.NCT_PYTHON||'python';
const report={date:new Date().toISOString(),status:'running',checks:[],errors:[],external:[],missing:[]};
const children=[];let browser;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function server(managed,port=0){
 const child=spawn(python,[path.join(root,'server.py'),'--port',String(port),...(managed?['--auto-close']:[])],{cwd:root,windowsHide:true});children.push(child);
 let stdout='',stderr='';child.stdout.on('data',b=>stdout+=b);child.stderr.on('data',b=>stderr+=b);child.on('error',e=>report.errors.push(e.message));
 const exited=new Promise(resolve=>child.once('exit',(code,signal)=>resolve({code,signal})));
 for(let n=0;n<100;n++){const m=stdout.match(/NCT: http:\/\/localhost:(\d+)/);if(m)return {child,port:+m[1],url:`http://127.0.0.1:${m[1]}/campaign-trail/index.html`,exited,log:()=>({stdout,stderr})};if(child.exitCode!==null)throw Error(stdout+stderr);await sleep(100);}
 throw Error('Server startup timed out: '+stdout+stderr);
}
async function open(context,s){
 const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));page.on('response',r=>{if(r.status()>=400)report.missing.push(new URL(r.url()).pathname);});
 const live=page.waitForResponse(r=>new URL(r.url()).pathname==='/_nct/lifetime'&&r.status()===200);
 await page.goto(s.url,{waitUntil:'domcontentloaded'});await live;
 await page.waitForFunction(()=>document.getElementById('game_start')&&!document.getElementById('game_start').disabled);
 return page;
}
(async()=>{try{
 // Exercise both actual batch files with a stub only for the OS browser launch.
 const folder=fs.mkdtempSync(path.join(artifacts,'launcher path 中文 '));
 for(const f of ['start.bat','一键启动.bat'])fs.copyFileSync(path.join(root,f),path.join(folder,f));
 fs.writeFileSync(path.join(folder,'server.py'),'import json,sys,pathlib\npathlib.Path("args.json").write_text(json.dumps(sys.argv[1:]))\n');
 for(const f of ['start.bat','一键启动.bat']){
  const r=spawnSync(process.env.ComSpec||'cmd.exe',['/d','/c','call',path.join(folder,f),'--port','18081'],{cwd:artifacts,windowsHide:true,encoding:'utf8',timeout:15000});assert.equal(r.status,0,r.stderr+r.stdout);
  assert.deepEqual(JSON.parse(fs.readFileSync(path.join(folder,'args.json'),'utf8')),['--open','--auto-close','--port','18081']);
 }
 report.checks.push('Both batch entrypoints run from another directory, including Chinese/spaced paths, and forward port/open/auto-close flags');
 browser=await chromium.launch({headless:true,timeout:30000,executablePath:process.env.NCT_BROWSER||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const context=await browser.newContext();await context.route('**/*',r=>{const u=new URL(r.request().url());if(['localhost','127.0.0.1'].includes(u.hostname)||['data:','blob:'].includes(u.protocol))return r.continue();report.external.push(u.href);return r.abort();});
 const manual=await server(false),managed=await server(true);
 const raw=await context.request.get(managed.url);assert((await raw.text()).includes('new EventSource'));
 const invalid=await context.request.get(new URL('/_nct/lifetime?token=wrong',managed.url).href);assert.equal(invalid.status(),403);
 const first=await open(context,managed);
 await first.evaluate(()=>{NCTI18n.setLanguage('en-US');localStorage.setItem('nct.launcher.persistence-test','kept');});
 const second=await open(context,managed);assert.equal(await second.evaluate(()=>localStorage.getItem('nct.launcher.persistence-test')),'kept');
 await second.reload({waitUntil:'domcontentloaded'});await sleep(4500);assert.equal(managed.child.exitCode,null,'Reload stopped the server');
 report.checks.push('Two real game tabs connect; reload retains the service and same-origin preferences');
 const cdp=await context.newCDPSession(first);await cdp.send('Page.setWebLifecycleState',{state:'frozen'});
 await second.close();await sleep(6500);assert.equal(managed.child.exitCode,null,'Closing one tab stopped the remaining frozen game tab');await cdp.send('Page.setWebLifecycleState',{state:'active'});
 report.checks.push('Background/frozen page remains attached; closing one tab preserves the remaining game tab');
 await first.locator('#game_start').first().click();await first.locator('#election_id').selectOption('21');await first.locator('#election_id_button').click();
 await first.locator('#candidate_id').selectOption('300');await first.locator('#candidate_id_button').click();await first.locator('#running_mate_id').selectOption('304');await first.locator('#running_mate_id_button').click();await first.locator('#opponent_selection_id_button').click();await first.waitForSelector('.game_answers');
 const before=await first.evaluate(()=>{const random=Math.random;window.__launcherRandomCalls=0;Math.random=()=>{__launcherRandomCalls++;return random();};return [JSON.stringify(campaignTrail_temp),__launcherRandomCalls];});await sleep(1500);assert.deepEqual(await first.evaluate(()=>[JSON.stringify(campaignTrail_temp),__launcherRandomCalls]),before);
 await first.locator('.game_answers').first().check();await first.locator('#answer_select_button').click();await first.locator('#ok_button').click();await first.waitForSelector('.game_answers,.visit_text');
 report.checks.push('Native election setup, answer, feedback and next question work; idle connection does not change game state or RNG call count');
 const started=Date.now();await first.close();const exit=await Promise.race([managed.exited,sleep(10000).then(()=>{throw Error('Server survived last game tab closure');})]);assert.equal(exit.code,0,JSON.stringify(managed.log()));assert.equal(manual.child.exitCode,null,'Other server was stopped');report.closeToExitMs=Date.now()-started;
 report.checks.push('Last tab closure exits only its owned Python server successfully and leaves an independent server running');
 const restarted=await server(true,managed.port),again=await open(context,restarted);
 assert.equal(await again.evaluate(()=>localStorage.getItem('nct.launcher.persistence-test')),'kept');assert.equal(await again.evaluate(()=>NCTI18n.language),'en-US');await again.close();assert.equal((await Promise.race([restarted.exited,sleep(10000).then(()=>{throw Error('Restarted server did not stop');})])).code,0);
 report.checks.push('Restart on the same port preserves browser storage and language; new session token works');
 assert(!(await(await context.request.get(manual.url)).text()).includes('new EventSource'));
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.external,[]);assert.deepEqual(report.missing,[]);report.status='passed';console.log('PASS one-click launcher, close cleanup, reload, multiple tabs and retained preferences');
}catch(e){report.status='failed';report.failure=e.stack;throw e;}finally{
 if(browser)await browser.close();for(const child of children)if(child.exitCode===null)child.kill();
 fs.writeFileSync(path.join(root,'tests/launcher-results.json'),JSON.stringify(report,null,2)+'\n');
}})().catch(e=>{console.error(e);process.exitCode=1;});
