const fs=require('fs'),assert=require('assert');
const {chromium}=require('./runtime.cjs');
const report={date:new Date().toISOString(),browser:process.env.NCT_BROWSER||'Chrome',checks:[],errors:[],external:[],missing:[]};
const check=name=>{report.checks.push(name);console.log('PASS',name);};
async function configure(page,year='21',candidate='300',mate='304'){
 await page.goto('http://localhost:8000/campaign-trail/index.html');
 await page.waitForFunction(()=>Array.isArray(campaignTrail_temp.running_mate_json));
 await page.locator('#game_start').first().click();await page.locator('#election_id').selectOption(year);await page.locator('#election_id_button').click();
 await page.locator('#candidate_id').selectOption(candidate);await page.locator('#candidate_id_button').click();
 await page.locator('#running_mate_id').selectOption(mate);await page.locator('#running_mate_id_button').click();
}
async function unchanged(page){assert.equal(await page.evaluate(()=>{const before=JSON.stringify(campaignTrail_temp);NCTI18n.setLanguage('en-US');NCTI18n.setLanguage('zh-CN');return before===JSON.stringify(campaignTrail_temp);}),true);}
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.NCT_BROWSER||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 report.version=browser.version();
 try {
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 await context.route('**/*',r=>{const u=new URL(r.request().url());if(!['localhost','127.0.0.1'].includes(u.hostname)&&!['data:','blob:'].includes(u.protocol)){report.external.push(u.href);return r.abort();}return r.continue();});
 const page=await context.newPage();page.setDefaultTimeout(8000);page.on('pageerror',e=>report.errors.push(e.stack));page.on('response',r=>{if(r.status()>=400)report.missing.push({url:r.url(),status:r.status()});});
 await configure(page); await unchanged(page);
 for(const id of ['1','2','3']){await page.locator('#game_type_id').selectOption(id);assert.ok(/[\u4e00-\u9fff]/.test(await page.locator('#opponent_selection_description_window').innerText()));await unchanged(page);}
 const difficulties=await page.locator('#difficulty_level_id option').evaluateAll(nodes=>nodes.map(n=>({value:n.value,text:n.textContent})));
 for(const d of difficulties){assert.match(d.text,/[\u4e00-\u9fff]/);await page.locator('#difficulty_level_id').selectOption(d.value);await unchanged(page);}
 check('All game mode descriptions and difficulty options are Chinese; values survive switching');
 await page.locator('#difficulty_level_id').selectOption('2');await page.locator('#game_type_id').selectOption('3');await page.locator('#opponent_selection_id_button').click();
 await page.waitForSelector('#question_form');await page.locator('#shining_menu_button').click();
 for(const id of ['funds','campaign_time','ad_campaign','staff','lobbies']) {
  const tab=page.locator(`button[onclick*="'${id}'"]`);
  if(await tab.isEnabled()) await tab.click();await unchanged(page);
 }
 await page.locator('button[onclick*="\'staff\'"]').click();assert.match(await page.locator('#staff_table').innerText(),/辩论教练|标出最有利/);
 await page.screenshot({path:'.test-artifacts/advanced-zh.png',fullPage:true});
 await page.locator('button[onclick*="\'ad_campaign\'"]').click();
 await page.locator('#shining_ad_state_sel').selectOption({label:'加利福尼亚州'});await page.locator('#ad_spending_amount').fill('1000');await page.locator('#add_ad_spending').click();
 const state=await page.evaluate(()=>JSON.stringify(campaignTrail_temp.shining_data));await unchanged(page);assert.equal(await page.evaluate(()=>JSON.stringify(campaignTrail_temp.shining_data)),state);
 await page.locator('.remove_ad_spend').click();await page.locator('#shining_back').click();await page.waitForSelector('#question_form');check('Advanced campaign funds, time, ads, staff, lobbies and back navigation');
 const q=await page.evaluate(()=>JSON.stringify(campaignTrail_temp));
 await page.evaluate(()=>benefitChecker());assert.match(await page.locator('#dialogue').innerText(),/答案|全国效果/);
 assert.equal(await page.evaluate(()=>JSON.stringify(campaignTrail_temp)),q);await unchanged(page);
 await page.screenshot({path:'.test-artifacts/benefits-zh.png',fullPage:true});await page.locator('.ui-dialog-titlebar-close').click();check('Built-in benefit dialog, localized effects and unchanged game state');
 await page.goto('http://localhost:8000/campaign-trail/index.html');await page.waitForFunction(()=>Array.isArray(campaignTrail_temp.running_mate_json));
 for(const zoom of [0.8,1,1.25,1.5]) {
  await page.evaluate(z=>document.documentElement.style.zoom=z,zoom);
  const bad=await page.locator('#game_start,#achievMenuButton,#infoMenuButton,#language-toggle').evaluateAll(nodes=>nodes.filter(n=>n.scrollHeight>n.clientHeight+2).map(n=>n.id));assert.deepEqual(bad,[]);
 }
 await page.evaluate(()=>document.documentElement.style.zoom=1);await page.screenshot({path:'.test-artifacts/home-zh.png',fullPage:true});check('Chinese home layout at 80/100/125/150 percent CSS zoom');
 assert.equal(await page.evaluate(()=>NCTI18n.text('unknown.key',{},'English fallback')),'English fallback');
 assert.match(await page.evaluate(()=>NCTI18n.text('game.visit',{state:'California'})),/加利福尼亚州/);
 await page.evaluate(()=>NCTI18n.setLanguage('en-US'));assert.match(await page.evaluate(()=>NCTI18n.text('game.visit',{state:'California'})),/California/);await page.evaluate(()=>NCTI18n.setLanguage('zh-CN'));check('Variable translation and missing-key fallback');
 for(const theme of ['shining','Omori','australia','carter','lgbtqpride']){
  await page.evaluate(t=>localStorage.setItem('theme',t),theme);await page.reload();await page.waitForTimeout(160);
 }
 await page.evaluate(()=>localStorage.setItem('theme','nct'));await page.reload();check('Optional themes remain local with cached assets or documented substitutes');
 await page.route('**/localization/zh-CN.json',async route=>{
  const response=await route.fetch();const pack=await response.json();delete pack['game.progress'];
  await route.fulfill({response,json:pack});
 });await page.reload();assert.equal(await page.evaluate(()=>NCTI18n.text('game.progress',{current:5,total:25})),'Question 5 of 25');
 await page.unroute('**/localization/zh-CN.json');await page.reload();check('Missing Chinese entry falls back to original English');
 await page.route('**/static/json/candidate.json',async route=>{await new Promise(resolve=>setTimeout(resolve,1200));await route.continue();});
 await page.goto('http://localhost:8000/campaign-trail/index.html',{waitUntil:'domcontentloaded'});
 assert.equal(await page.locator('#game_start').first().isDisabled(),true);
 await page.waitForFunction(()=>Array.isArray(campaignTrail_temp.candidate_json));
 assert.equal(await page.locator('#game_start').first().isEnabled(),true);
 await page.unroute('**/static/json/candidate.json');check('Slow native data load is safe; Start waits for data readiness');
 for(const [year,candidate,mate] of [['13','131','135'],['8','67','71']]) {
  await configure(page,year,candidate,mate);await page.locator('#game_type_id').selectOption('1');await page.locator('#opponent_selection_id_button').click();
  await page.waitForSelector('#question_form');await page.locator('#view_electoral_map').click();await page.waitForSelector('#map_container svg');
  await page.evaluate(()=>jQuery('#map_container').usmap('trigger','NY','mouseover',{}));assert.match(await page.locator('#state_info').innerText(),/纽约州/);await unchanged(page);
 }
 check('1844 and 1860 historical map libraries, native state info and switching');
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.external,[]);assert.deepEqual(report.missing,[]);check('Zero JS errors, missing assets or external requests');report.status='passed';
 }catch(error){report.status='failed';report.failure=error.stack;console.error(error);process.exitCode=1;}
 finally{fs.writeFileSync(process.env.NCT_EXT_REPORT||'tests/extended-results.json',JSON.stringify(report,null,2));await browser.close();}
})();
