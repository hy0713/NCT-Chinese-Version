/* Actual UI playthroughs under a blocked external network, with seeded RNG. */
const fs=require('fs'),assert=require('assert'),{chromium}=require('./runtime.cjs');
const catalogue=JSON.parse(fs.readFileSync('localization/stories/catalogue.json','utf8'));
const report={date:new Date().toISOString(),network:'Only loopback/data/blob permitted',browser:'',pairings:[],errors:[],external:[],missing:[],checks:[]};
async function start(page,s,language,gameType){
 await page.goto((process.env.NCT_BASE_URL || 'http://localhost:8000').replace(/\/$/, '') + '/campaign-trail/index.html');
 await page.waitForFunction(()=>typeof campaignTrail_temp!=='undefined'&&campaignTrail_temp.running_mate_json&&campaignTrail_temp.temp_election_list&&document.querySelector('#game_start')&&!document.querySelector('#game_start').disabled);
 await page.evaluate(lang=>{NCTI18n.setLanguage(lang);let seed=1776;window.__rngCalls=0;Math.random=()=>{__rngCalls++;seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};},language);
 await page.locator('#game_start').first().click();await page.locator('#election_id').selectOption(String(s.election));await page.locator('#election_id_button').click();
 await page.locator('#candidate_id').selectOption(String(s.candidate));await page.locator('#candidate_id_button').click();
 await page.locator('#running_mate_id').selectOption(String(s.runningMate));await page.locator('#running_mate_id_button').click();if(gameType)await page.locator('#game_type_id').selectOption(String(gameType));await page.locator('#opponent_selection_id_button').click();
 await page.waitForFunction(()=>campaignTrail_temp.questions_json?.length&&document.querySelector('.game_answers'));
 assert.equal(await page.evaluate(()=>NCTStory.active),s.scope);
}
async function audit(page){return page.evaluate(()=>{
 const misses=[];let count=0;
 for(const collection of ['questions_json','answers_json','answer_feedback_json','issues_json'])for(const row of campaignTrail_temp[collection]||[])for(const[field,source]of Object.entries(row.fields)){
  if(typeof source!=='string'||!/[A-Za-z\u3400-\u9fff]/.test(source)||!['description','answer_feedback',...Array.from({length:7},(_,i)=>'stance_desc_'+(i+1))].includes(field))continue;
  count++;const ref=NCTStory.resolve(collection,row.pk,field,source);
  const t=document.createElement('template');t.innerHTML=NCTStory.html(collection,row.pk,field,source);
  if(!ref||!t.content.querySelector('[data-story-key]')||!/[\u3400-\u9fff]/.test(t.content.textContent))misses.push({collection,pk:row.pk,field,source});
 }
 const before=JSON.stringify(campaignTrail_temp),rng=__rngCalls;
 NCTI18n.setLanguage('en-US');NCTI18n.setLanguage('zh-CN');
 return {count,misses,stateUnchanged:before===JSON.stringify(campaignTrail_temp),rngUnchanged:rng===__rngCalls};
});}
async function play(page,language){
 let answers=0,visits=0;const seen=[];
 for(let step=0;step<160;step++){
  const action=await page.evaluate(lang=>{
   const click=id=>{const n=document.getElementById(id);if(n){n.click();return true;}return false;};
   if(document.getElementById('overall_results_button'))return {type:'done'};
   if(document.getElementById('ok_button')){click('ok_button');return {type:'ok'};}
   if(click('final_result_button'))return {type:'final'};
   if(click('confirm_visit_button'))return {type:'visit'};
   if(document.querySelector('.visit_text')){
    const abbreviation=campaignTrail_temp.states_json.find(s=>s.fields.abbr==='CA')?.fields.abbr||campaignTrail_temp.states_json[0].fields.abbr;
    jQuery('#map_container').usmap('trigger',abbreviation,'click',{});return {type:'map'};
   }
   const answer=document.querySelector('.game_answers');
   if(answer){
    const q=campaignTrail_temp.questions_json[campaignTrail_temp.question_number];
    const heading=document.querySelector('.inner_inner_window h3')?.textContent||'';
    const labels=[...document.querySelectorAll('#question_form label')].map(n=>n.textContent);
    answer.click();click('answer_select_button');
    return {type:'answer',pk:q.pk,answer:Number(answer.value),heading,labels};
   }
   return {type:'wait'};
  },language);
  if(action.type==='done')break;
  if(action.type==='answer'){
   answers++;seen.push({pk:action.pk,answer:action.answer});
   if(language==='zh-CN'){assert.match(action.heading,/[\u3400-\u9fff]/);for(const l of action.labels)assert.match(l,/[\u3400-\u9fff]/);}
  }
  if(action.type==='visit')visits++;
  if(action.type==='wait')await page.waitForTimeout(20);
 }
 await page.waitForSelector('#overall_results_button');
 const result=await page.evaluate(()=>({overall:campaignTrail_temp.final_overall_results,states:campaignTrail_temp.final_state_results,answers:campaignTrail_temp.player_answers,visits:campaignTrail_temp.player_visits,questionNumber:campaignTrail_temp.question_number,outcome:campaignTrail_temp.final_outcome,rngCalls:__rngCalls,ending:document.getElementById('final_results_description').textContent}));
 if(language==='zh-CN')assert.match(result.ending,/[\u3400-\u9fff]/);
 delete result.ending;return {answers,visits,seen,result};
}
module.exports={start,audit,play};
if(require.main===module)(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.NCT_BROWSER||'C:/Program Files/Google/Chrome/Application/chrome.exe'});report.browser=browser.version();
 try{
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 await context.route('**/*',r=>{const u=new URL(r.request().url());if(!['localhost','127.0.0.1'].includes(u.hostname)&&!['data:','blob:'].includes(u.protocol)){report.external.push(u.href);return r.abort();}return r.continue();});
 const page=await context.newPage();page.setDefaultTimeout(10000);page.on('pageerror',e=>report.errors.push(e.stack));page.on('response',r=>{if(r.status()>=400)report.missing.push({url:r.url(),status:r.status()});});
 const reviewSources=process.argv.includes('--review')?new Set(fs.readdirSync('localization/reviews').filter(n=>n.endsWith('-editorial-review.json')).flatMap(n=>JSON.parse(fs.readFileSync('localization/reviews/'+n,'utf8')).revisions.map(r=>r.source))):null;
 const reviewedScopes=reviewSources?new Set(catalogue.records.filter(r=>reviewSources.has(r.source)).map(r=>r.scope)):null;
 const reviewedCandidates=reviewSources?new Set(catalogue.records.filter(r=>r.scope==='base'&&r.collection==='candidate_json'&&reviewSources.has(r.source)).map(r=>r.location.pk)):null;
 const selected=process.env.NCT_SCOPE?catalogue.scenarios.filter(s=>s.scope===process.env.NCT_SCOPE):reviewSources?catalogue.scenarios.filter(s=>reviewedScopes.has(s.scope)||reviewedCandidates.has(s.candidate)||reviewedCandidates.has(s.runningMate)):process.argv.includes('--smoke')?catalogue.scenarios.filter(s=>['2012_Obama_Biden','1964_Johnson_Humphrey','2000_Nader_LaDuke','1844_Polk_Dallas','2020_Biden_Harris'].includes(s.scope)):catalogue.scenarios;
 assert.ok(selected.length,'No scenarios selected');
 for(const s of selected){
  await start(page,s,'zh-CN');const coverage=await audit(page);assert.deepEqual(coverage.misses,[],s.scope+' '+JSON.stringify(coverage.misses));assert.ok(coverage.stateUnchanged&&coverage.rngUnchanged);
  if(process.argv.includes('--smoke'))await page.screenshot({path:'.test-artifacts/stories/'+s.scope+'-question-zh.png',fullPage:true});
  // Reset after the language-toggle audit so both independent sessions start
  // with the same language and the same initial random stream.
  await start(page,s,'zh-CN');const zh=await play(page,'zh-CN');
  if(process.argv.includes('--smoke'))await page.screenshot({path:'.test-artifacts/stories/'+s.scope+'-ending-zh.png',fullPage:true});
  await start(page,s,'en-US');const en=await play(page,'en-US');
  assert.deepEqual(zh,en,s.scope+' bilingual numerical/choice equivalence');
  report.pairings.push({scope:s.scope,year:s.year,candidate:s.candidate,runningMate:s.runningMate,entriesChecked:coverage.count,answers:zh.answers,visits:zh.visits,rngCalls:zh.result.rngCalls,outcome:zh.result.outcome,status:'passed'});
  console.log('PASS',s.scope,zh.answers,'questions; bilingual states/results identical');
 }
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.missing,[]);assert.deepEqual(report.external,[]);
 report.checks.push('All selected pairings played to election results in both languages','Every loaded question/answer/feedback/issue description resolves to Chinese','Language toggle leaves the entire game object and RNG count unchanged','Same initial seed and choices yield identical votes, state results, answers, visits and random-call counts','No JS errors or external/missing core resources');
 }catch(e){report.failure=e.stack;throw e;}finally{fs.writeFileSync(process.argv.includes('--review')?'tests/stories-review-results.json':process.argv.includes('--smoke')?'tests/stories-smoke-results.json':'tests/stories-browser-results.json',JSON.stringify(report,null,2)+'\n');await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
