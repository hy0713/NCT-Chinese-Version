const fs=require('fs'),assert=require('assert'),path=require('path'),crypto=require('crypto');
const {chromium}=require('./runtime.cjs');
const report={date:new Date().toISOString(),browser:'Chrome (Windows)',offline:'All requests except localhost/127.0.0.1 blocked',checks:[],errors:[],external:[],missing:[],pairings:[]};
const check=(name,details={})=>{report.checks.push({name,status:'passed',...details});console.log('PASS',name);};
const root=path.resolve(__dirname,'..');fs.mkdirSync(path.join(root,'.test-artifacts'),{recursive:true});
async function start(page,year,candidate,mate,mode='1') {
 await page.goto('http://localhost:8000/campaign-trail/index.html');
 await page.waitForFunction(()=>Array.isArray(campaignTrail_temp.temp_election_list)&&Array.isArray(campaignTrail_temp.running_mate_json));
 await page.locator('#game_start').first().click();await page.locator('#election_id').selectOption(String(year));await page.locator('#election_id_button').click();
 await page.locator('#candidate_id').selectOption(String(candidate));await page.locator('#candidate_id_button').click();
 await page.locator('#running_mate_id').selectOption(String(mate));await page.locator('#running_mate_id_button').click();
 await page.locator('#game_type_id').selectOption(mode);await page.locator('#opponent_selection_id_button').click();
 await page.waitForSelector('#question_form'); await page.waitForFunction(()=>campaignTrail_temp.questions_json?.length>0);
}
async function invariantSwitch(page) {
 const result=await page.evaluate(()=>{
   const before=JSON.stringify(campaignTrail_temp),answer=document.querySelector('.game_answers:checked')?.value;
   const oldRandom=Math.random;let calls=0;Math.random=()=>{calls++;return oldRandom();};
   NCTI18n.setLanguage('en-US');NCTI18n.setLanguage('zh-CN');Math.random=oldRandom;
   return {same:before===JSON.stringify(campaignTrail_temp),calls,answerSame:answer===document.querySelector('.game_answers:checked')?.value};
 });assert.deepEqual(result,{same:true,calls:0,answerSame:true});
}
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.NCT_BROWSER || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 report.browser='Chrome '+browser.version()+' (Windows)';
 try {
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 await context.route('**/*',r=>{const u=new URL(r.request().url());if(!['localhost','127.0.0.1'].includes(u.hostname)&&!['data:','blob:'].includes(u.protocol)){report.external.push(u.href);return r.abort();}return r.continue();});
 const page=await context.newPage();page.setDefaultTimeout(10000);
 page.on('pageerror',e=>report.errors.push(e.stack));page.on('response',r=>{if(r.status()>=400)report.missing.push({url:r.url(),status:r.status()});});
 await page.goto('http://localhost:8000/campaign-trail/index.html');
 assert.equal(await page.locator('html').getAttribute('lang'),'zh-CN');
 assert.match(await page.locator('#game_start').first().innerText(),/开始/);check('Chinese default and home');
 await page.locator('#language-toggle').click();await page.waitForTimeout(180);assert.match(await page.locator('#game_start').first().innerText(),/begin/);
 await page.reload();assert.equal(await page.locator('html').getAttribute('lang'),'en-US');
 await page.locator('#language-toggle').click();check('Toggle and localStorage persistence');
 await page.locator('#achievMenuButton').click();assert.match(await page.locator('#achBox').innerText(),/殊途同归/);await page.locator('#backButton').click();
 await page.locator('#infoMenuButton').click();assert.match(await page.locator('#infoBox').innerText(),/制作人员/);await page.locator('#backButton').click();check('Achievements and help');
 const candidates=JSON.parse(fs.readFileSync('static/json/candidate.json','utf8'));
 const mates=JSON.parse(fs.readFileSync('static/json/running_mate.json','utf8'));
 const years=JSON.parse(fs.readFileSync('static/json/election_list.json','utf8'));
 if(process.argv.includes('--quick')) {
   const previous=JSON.parse(fs.readFileSync('tests/test-results.json','utf8'));
   report.pairings=previous.pairings;report.pairingsVerifiedAt=previous.pairingsVerifiedAt||previous.date;
 }
 else for(const year of years) for(const candidate of candidates.filter(c=>c.fields.election===year.id&&c.fields.is_active===1)) {
   const pairs=mates.filter(m=>m.fields.candidate===candidate.pk);
   for(const pair of pairs) {
     await start(page,year.id,candidate.pk,pair.fields.running_mate);
     assert.equal(await page.evaluate(()=>Number(campaignTrail_temp.candidate_id)),candidate.pk);
     assert.equal(await page.evaluate(()=>Number(campaignTrail_temp.running_mate_id)),pair.fields.running_mate);
     assert.match(await page.locator('#progress_bar').innerText(),/第 1 题/);
     await invariantSwitch(page);
     report.pairings.push({year:year.display_year,candidate:candidate.pk,mate:pair.fields.running_mate,status:'passed'});
   }
   console.log('PAIRINGS',year.display_year,candidate.fields.last_name,pairs.length);
 }
 check('All native year/candidate/running-mate combinations load',{count:report.pairings.length});
 if(!report.pairingsVerifiedAt) report.pairingsVerifiedAt=report.date;
 await start(page,3,16,30);
 await page.screenshot({path:'.test-artifacts/question-zh.png',fullPage:true});
 await page.locator('#answer_select_button').click();assert.match(await page.locator('#feedback_content').innerText(),/请先选择/);await page.locator('#ok_button').click();check('Answer validation popup');
 await page.locator('.game_answers').first().check();await invariantSwitch(page);check('Switch does not mutate any game field, selection, or RNG');
 await page.locator('#view_electoral_map').click();
 await page.waitForSelector('#map_container svg');
 await page.evaluate(()=>jQuery('#map_container').usmap('trigger','CA','mouseover',{}));
 assert.match(await page.locator('#state_info').innerText(),/加利福尼亚州/);assert.match(await page.locator('#state_info').innerText(),/经济政策|经济|社会议题/);
 await invariantSwitch(page);await page.screenshot({path:'.test-artifacts/polls-zh.png',fullPage:true});
 await page.locator('#pvswitcher').click();assert.match(await page.locator('#pvswitcher').innerText(),/州/);await page.locator('#ev_est').click();
 for(const button of ['#AdvisorButton','#AdvisorButton','#margin_switcher','#margin_switcher']) {
   await page.locator(button).click();await page.locator('#view_electoral_map').click();
 }
 await page.locator('#resume_questions_button').click();check('Poll map, state names, PV/EV, gradient and advisor control');
 let answers=0,visits=0;
 for(let step=0;step<130;step++) {
  if(await page.locator('#overall_results_button').count())break;
  if(await page.locator('#ok_button').count()){await page.locator('#ok_button').click();continue;}
  if(await page.locator('#final_result_button').count()){await page.locator('#final_result_button').click();continue;}
  if(await page.locator('#confirm_visit_button').count()){await invariantSwitch(page);await page.locator('#confirm_visit_button').click();visits++;continue;}
  if(await page.locator('.visit_text').count()){await page.evaluate(()=>jQuery('#map_container').usmap('trigger','CA','click',{}));continue;}
  if(await page.locator('.game_answers').count()){
    await page.locator('.game_answers').first().check();await page.locator('#answer_select_button').click();answers++;await page.waitForTimeout(15);continue;
  }
  await page.waitForTimeout(100);
 }
 await page.waitForSelector('#overall_results_button');assert.equal(answers,25);assert.ok(visits>0);
 check('Complete native game through 25 answers and state visits',{answers,visits,outcome:await page.evaluate(()=>campaignTrail_temp.final_outcome)});
 await invariantSwitch(page);await page.waitForTimeout(250);assert.ok(await page.locator('#overall_results_button').count());check('Language toggle on results does not trigger upstream integrity reload');
 await page.screenshot({path:'.test-artifacts/results-zh.png',fullPage:true});
 for(const button of ['#final_election_map_button','#state_results_button','#overall_details_button','#recommended_reading_button','#overall_results_button']) {
   await page.locator(button).click();await invariantSwitch(page);await page.waitForTimeout(120);
   if(button==='#state_results_button') {
     assert.match(await page.locator('#state_tab option').first().innerText(),/州|特区/);
     await page.evaluate(()=>NCTI18n.setLanguage('en-US'));
     const options=await page.locator('#sort_tab option').allTextContents();
     assert.ok(options.some(s=>s.includes('Closest ')&&s.includes(' Wins')),options.join(' | '));
     const englishValues=await page.locator('#sort_tab option').evaluateAll(ns=>ns.map(n=>n.value));
     await page.evaluate(()=>NCTI18n.setLanguage('zh-CN'));
     const localized=await page.locator('#sort_tab option').evaluateAll(ns=>ns.filter(n=>Number(n.value)>=10).map(n=>n.textContent));
     assert.ok(localized.every(s=>/[\u3400-\u9fff]/.test(s)&&!/(Closest|Wins|Highest)/.test(s)),localized.join(' | '));
     assert.deepEqual(await page.locator('#sort_tab option').evaluateAll(ns=>ns.map(n=>n.value)),englishValues);
     for(const sort of ['1','2','3']) await page.locator('#sort_tab').selectOption(sort);
     await page.locator('#state_tab').selectOption({label:'加利福尼亚州'});
   }
 }
 assert.match(await page.locator('#map_footer').innerText(),/再玩一局/);check('All result tabs and live language switching');
 await page.locator('#play_again_button').click();assert.match(await page.locator('#new_game_window').innerText(),/确定要开始/);await page.locator('#cancel_button').click();check('Replay confirmation');
 for(const zoom of [0.8,1,1.25,1.5]) {
  await page.evaluate(z=>document.documentElement.style.zoom=String(z),zoom);
  const clipped=await page.locator('#map_footer button').evaluateAll(nodes=>nodes.filter(n=>n.scrollHeight>n.clientHeight+2).map(n=>n.id));assert.deepEqual(clipped,[]);
  await page.screenshot({path:`.test-artifacts/results-zoom-${zoom}.png`,fullPage:true});
 }
 check('80%, 100%, 125%, 150% CSS zoom: result button text fits');
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.external,[]);assert.deepEqual(report.missing,[]);check('No JS errors, no missing resources, zero external requests');
 const hashes=JSON.parse(fs.readFileSync('tests/original-data-sha256.json','utf8'));
 for(const [file,digest] of Object.entries(hashes))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),digest,file);
 check('All original JSON and question-set files byte-for-byte unchanged',{count:Object.keys(hashes).length});
 report.status='passed';
 } catch(e) { report.status='failed';report.failure=e.stack;console.error(e);process.exitCode=1; }
 finally {fs.writeFileSync('tests/test-results.json',JSON.stringify(report,null,2));await browser.close();}
})();
