/* Exercise real ending functions with synthetic boundary result fixtures.
 * Fixtures live only in this fresh test browser, never in upstream files. */
const fs=require('fs'),assert=require('assert'),{chromium}=require('./runtime.cjs');
const cat=JSON.parse(fs.readFileSync('localization/stories/catalogue.json','utf8'));
const report={date:new Date().toISOString(),fixtures:[],checks:[],errors:[],external:[],missing:[],warnings:[],upstreamEmptyEndings:[],upstreamMediaEndings:[]};
async function load(page,s){
 await page.goto((process.env.NCT_BASE_URL || 'http://localhost:8000').replace(/\/$/, '') + '/campaign-trail/index.html');
 await page.waitForFunction(()=>typeof campaignTrail_temp!=='undefined'&&campaignTrail_temp.running_mate_json&&campaignTrail_temp.temp_election_list&&!document.querySelector('#game_start').disabled);
 await page.locator('#game_start').first().click();await page.locator('#election_id').selectOption(String(s.election));await page.locator('#election_id_button').click();
 await page.locator('#candidate_id').selectOption(String(s.candidate));await page.locator('#candidate_id_button').click();
 await page.locator('#running_mate_id').selectOption(String(s.runningMate));await page.locator('#running_mate_id_button').click();await page.locator('#opponent_selection_id_button').click();await page.waitForSelector('.game_answers');
}
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.NCT_BROWSER||'C:/Program Files/Google/Chrome/Application/chrome.exe'});report.browser=browser.version();
 try{
 const context=await browser.newContext();await context.route('**/*',r=>{const u=new URL(r.request().url());if(!['localhost','127.0.0.1'].includes(u.hostname)&&!['data:','blob:'].includes(u.protocol)){report.external.push(u.href);return r.abort();}return r.continue();});
 const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.stack));page.on('response',r=>{if(r.status()>=400)report.missing.push(r.url());});
 for(const s of cat.scenarios){
  await load(page,s);
  const result=await page.evaluate(()=>{
   const e=campaignTrail_temp,outputs=[],warnings=[],empty=[];
   const ids=e.candidate_json.filter(c=>c.fields.election===e.election_id&&!e.running_mate_json.some(r=>r.fields.running_mate===c.pk)).map(c=>c.pk);
   if(!ids.includes(e.candidate_id))ids.unshift(e.candidate_id);
   const others=ids.filter(id=>id!==e.candidate_id);while(others.length<3)others.push(others[0]||e.candidate_id);
   const evs=[0,1,2,3,4,50,77,78,90,91,100,152,153,200,201,218,219,235,236,269,270,300,301,302,341,342,400,401,532,533,537,538];
   for(const outcome of ['win','loss','tie'])for(const ev of evs)for(const popwin of [true,false]){
    e.final_outcome=outcome;const rows=[e.candidate_id,...others].map((candidate,i)=>({candidate,electoral_votes:i===0?ev:i===1?538-ev:0,popular_votes:i===0?popwin?600:400:i===1?popwin?400:600:1,percent:i===0?popwin?60:40:i===1?popwin?40:60:0}));
    const aa=(outcome==='win'?rows:[rows[1],rows[0],...rows.slice(2)]);e.final_overall_results=aa;
    e.final_state_results=e.states_json.map(state=>({state:state.pk,result:aa}));window.currstate=e.states_json[0].pk;
    const me=e.candidate_json.find(c=>c.pk===e.candidate_id);
    let source=typeof endingPicker==='function'&&e.multiple_endings?endingPicker(outcome,1001,aa,[ev,popwin?60:40,ev===0?99:600]):false;
    if(!source)source=me.fields[{win:'electoral_victory_message',loss:'electoral_loss_message',tie:'no_electoral_majority_message'}[outcome]];
    NCTI18n.setLanguage('zh-CN');const fragment=NCTStory.ending(source);const template=document.createElement('template');template.innerHTML=fragment;
    const text=template.content.textContent;
    if(source&&text&&/[A-Za-z\u3400-\u9fff]/.test(source.replace(/<[^>]*>/g,''))&&!/[\u3400-\u9fff]/.test(text))warnings.push({outcome,ev,popwin,source,text});
    if(source&&!/[A-Za-z\u3400-\u9fff]/.test(source.replace(/<[^>]*>/g,'')))empty.push({outcome,ev,popwin,source});
    outputs.push(source);
   }
   return {fixtures:outputs.length,uniqueOutputs:new Set(outputs).size,warnings,empty};
  });
  report.fixtures.push({scope:s.scope,...result});report.warnings.push(...result.warnings.map(w=>({scope:s.scope,...w})));for(const w of result.empty)(/<(?:img|video|audio)\b/.test(w.source)?report.upstreamMediaEndings:report.upstreamEmptyEndings).push({scope:s.scope,...w});console.log('PASS ENDINGS',s.scope,result.uniqueOutputs,'outputs');
 }
 // The unavailable upstream Wallace movie has a local playable placeholder.
 const wallace=cat.scenarios.find(s=>s.scope==='1968_Wallace_Thurmond');await load(page,wallace);
 await page.evaluate(()=>{NCTI18n.setLanguage('zh-CN');campaignTrail_temp.final_outcome='win';const aa=[{candidate:25,electoral_votes:538,popular_votes:1000},{candidate:23,electoral_votes:0,popular_votes:0},{candidate:24,electoral_votes:0,popular_votes:0}];const raw=endingPicker('win',1000,aa,[538,100,1000]);const originalVideo=videoDone,originalNext=nextTask;window.__movieEnded=false;window.__eventFinished=false;videoDone=()=>{__movieEnded=true;originalVideo();};nextTask=()=>{__eventFinished=true;originalNext();};document.getElementById('game_window').innerHTML=NCTI18n.render(NCTStory.ending(raw));});
 await page.waitForFunction(()=>window.__movieEnded,{},{timeout:10000});await page.waitForFunction(()=>/[\u3400-\u9fff]/.test(document.getElementById('dialogueText')?.textContent||''));
 await page.waitForFunction(()=>window.__eventFinished,{},{timeout:25000});
 report.checks.push('Synthetic win/loss/tie, popular-vote inversion and EV boundary fixtures for all 105 pairings','Original endingPicker output resolves to Chinese without modifying source files','Wallace special ending: local video ended, Chinese typewriter ran, original nextTask completed offline');
 assert.deepEqual(report.warnings,[]);assert.deepEqual(report.errors,[]);assert.deepEqual(report.missing,[]);assert.deepEqual(report.external,[]);
 }catch(e){report.failure=e.stack;throw e;}finally{fs.writeFileSync('tests/story-endings-results.json',JSON.stringify(report,null,2)+'\n');await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
