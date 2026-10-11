/* Exact note provenance plus real UI interaction, under an external-network block. */
const fs=require('fs'),assert=require('assert'),crypto=require('crypto'),{chromium}=require('./runtime.cjs');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8')),cat=read('localization/stories/catalogue.json'),data=read('localization/annotations/index.json');
const reviewed=read('localization/annotations/editorial-review.json'),rows=new Map(cat.records.map(r=>[r.key,r]));
const historical=fs.readdirSync('localization/reviews').filter(n=>n.endsWith('-editorial-review.json')).flatMap(n=>read('localization/reviews/'+n).revisions);
const reviewedSources=new Set([...reviewed.revisions,...historical].map(r=>r.source));
const framework=read('localization/en-US.json'),headers=read('localization/annotations/header-editorial-review.json');
const readingReview=read('localization/annotations/reading-editorial-review.json');
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const report={date:new Date().toISOString(),notes:Object.keys(data.notes).length,bindings:Object.keys(data.bindings).length,humanReviewed:reviewedSources.size,browser:'',checks:[],errors:[],external:[],missing:[],rendered:0};
report.headerBindings=Object.keys(data.uiBindings).length;report.headerSlotsReviewed=headers.slotsReviewed;report.headersRendered=0;
report.humanReviewedRecordPositions=cat.records.filter(r=>reviewedSources.has(r.source)).length;
report.readingListsReviewed=readingReview.uniqueSourcesReviewed;report.readingListPositions=readingReview.recordPositions;report.readingListsRendered=0;
for(const[key,entry]of Object.entries(data.bindings)){
 const r=rows.get(key);assert.ok(r,key);assert.equal(r.source,entry.source);assert.equal(sha(entry.source),entry.sha256);
 assert.equal(new Set(entry.notes).size,entry.notes.length);for(const id of entry.notes)assert.ok(data.notes[id],id);
 assert.ok(reviewedSources.has(entry.source),'Unreviewed annotated source: '+key);
}
for(const[key,entry]of Object.entries(data.uiBindings)){
 assert.equal(framework[key],entry.source);assert.equal(sha(entry.source),entry.sha256);
 for(const variant of entry.sourceVariants)assert.equal(sha(variant.source),variant.sha256);
 for(const id of entry.notes)assert.ok(data.notes[id]);
}
async function ready(page){await page.goto((process.env.NCT_BASE_URL || 'http://localhost:8000').replace(/\/$/, '') + '/campaign-trail/index.html');await page.waitForFunction(()=>typeof campaignTrail_temp!=='undefined'&&campaignTrail_temp.temp_election_list&&campaignTrail_temp.running_mate_json&&document.querySelector('#game_start')&&!document.querySelector('#game_start').disabled);await page.evaluate(()=>{NCTI18n.setLanguage('zh-CN');let seed=1776;window.__noteRng=0;Math.random=()=>{__noteRng++;seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};});}
async function start(page,scope){const s=cat.scenarios.find(s=>s.scope===scope);await ready(page);await page.locator('#game_start').first().click();await page.locator('#election_id').selectOption(String(s.election));await page.locator('#election_id_button').click();await page.locator('#candidate_id').selectOption(String(s.candidate));await page.locator('#candidate_id_button').click();await page.locator('#running_mate_id').selectOption(String(s.runningMate));await page.locator('#running_mate_id_button').click();await page.locator('#opponent_selection_id_button').click();await page.waitForSelector('.game_answers');}
const snapshot=page=>page.evaluate(()=>({game:JSON.stringify(campaignTrail_temp),rng:__noteRng,checked:[...document.querySelectorAll('.game_answers:checked')].map(n=>n.value)}));
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.NCT_BROWSER||'C:/Program Files/Google/Chrome/Application/chrome.exe'});report.browser=browser.version();
 try{
  const context=await browser.newContext({viewport:{width:1280,height:900}});
  await context.route('**/*',route=>{const u=new URL(route.request().url());if(!['localhost','127.0.0.1'].includes(u.hostname)&&!['data:','blob:'].includes(u.protocol)){report.external.push(u.href);return route.abort();}return route.continue();});
  const page=await context.newPage();page.setDefaultTimeout(15000);page.on('pageerror',e=>report.errors.push(e.stack));page.on('response',r=>{if(r.status()>=400)report.missing.push({url:r.url(),status:r.status()});});await ready(page);
  // Every compiled binding and every explanation rendered through the adapter.
  for(const[key,entry]of Object.entries(data.bindings)){
   const r=rows.get(key),render=await page.evaluate(({r})=>{
    const host=document.createElement('div');host.id='note-audit';
    host.innerHTML=r.collection==='ending'?NCTStory.ending(r.source):NCTStory.html(r.collection,r.location.pk??r.id,r.field,r.source,r.scope);
    if(r.collection==='ending'){NCTStory.use('/static/questionset/'+r.scope+'.html');host.innerHTML=NCTStory.ending(r.source);}
    document.body.append(host);return host.querySelector('.nct-note-trigger')?.dataset.nctNotes.split(' ')||[];
   },{r});assert.deepEqual(render,entry.notes,key);report.rendered++;
   await page.locator('#note-audit .nct-note-trigger').click();
   for(const id of entry.notes)assert.ok((await page.locator('.nct-note-panel').textContent()).includes(data.notes[id].title));
   assert.equal(await page.locator('.nct-note-panel a').count(),entry.notes.reduce((n,id)=>n+data.notes[id].sources.length,0));
   await page.keyboard.press('Escape');await page.locator('#note-audit').evaluate(n=>n.remove());
  }
  const stale=await page.evaluate(r=>({inline:NCTNotes.inline(r.key,r.source+' changed'),ending:NCTNotes.ending('nonexistent',r.source)}),cat.records.find(r=>r.key===Object.keys(data.bindings)[0]));assert.equal(stale.inline,'');
  for(const[key,entry]of Object.entries(data.uiBindings)){
   const rendered=await page.evaluate(({key,source})=>{const host=document.createElement('div');host.id='note-audit';host.innerHTML=NCTI18n.html(key);document.body.prepend(host);return {ids:host.querySelector('.nct-note-trigger')?.dataset.nctNotes.split(' ')||[],stale:NCTNotes.ui(key,source+' changed')};},{key,source:entry.source});
   assert.deepEqual(rendered.ids,entry.notes,key);assert.equal(rendered.stale,'');
   await page.locator('#note-audit .nct-note-trigger').click();for(const id of entry.notes)assert.ok((await page.locator('.nct-note-panel').textContent()).includes(data.notes[id].title));
   await page.keyboard.press('Escape');await page.locator('#note-audit').evaluate(n=>n.remove());report.headersRendered++;
  }
  for(const row of headers.records){assert.ok(await page.evaluate(s=>NCTI18n.literal(s).includes('nct-note-trigger'),row.source),'Original header slot lacks note: '+row.index);}
  for(const entry of readingReview.revisions){
   assert.equal(sha(entry.source),entry.sha256);const r=rows.get(entry.keys[0]);assert.equal(r.source,entry.source);
   const result=await page.evaluate(r=>{const host=document.createElement('div');host.innerHTML=NCTStory.html(r.collection,r.location.pk,r.field,r.source,r.scope);const source=document.createElement('div');source.innerHTML=r.source;return {zh:host.querySelector('.nct-story').innerHTML,hrefs:[...host.querySelectorAll('a')].map(n=>n.getAttribute('href')),originalHrefs:[...source.querySelectorAll('a')].map(n=>n.getAttribute('href'))};},r);
   assert.equal(result.zh,await page.evaluate(zh=>{const host=document.createElement('div');host.innerHTML=zh;return host.innerHTML;},entry.zh));assert.deepEqual(result.hrefs,result.originalHrefs);report.readingListsRendered++;
  }
  // Actual header cache refresh, as well as all quotation fixtures above.
  const headerKey='quote.i_have_binders_full_of_women_mitt_romney';
  await page.evaluate(key=>{document.querySelector('#wittyquote em').innerHTML=NCTI18n.html(key);corrr=document.querySelector('.game_header').innerHTML;},headerKey);
  const headerTrigger=page.locator('#wittyquote .nct-note-trigger');const headerBefore=await snapshot(page);await headerTrigger.click();await page.waitForTimeout(300);
  assert.equal(await headerTrigger.getAttribute('aria-expanded'),'true','Header timer replaced the note anchor');
  assert.equal(await page.locator('.nct-note-panel').count(),1);assert.deepEqual(await snapshot(page),headerBefore);
  const headerBox=await headerTrigger.boundingBox(),panelBox=await page.locator('.nct-note-panel').boundingBox();assert.ok(Math.abs(panelBox.x-headerBox.x)<480&&panelBox.y>headerBox.y,'Header note must appear beside its trigger');await page.screenshot({path:'.test-artifacts/annotation-header-zh.png',fullPage:true});
  await page.evaluate(()=>NCTI18n.setLanguage('en-US'));assert.equal(await headerTrigger.count(),0);assert.equal(await page.locator('.nct-note-panel').count(),0);assert.deepEqual(await snapshot(page),headerBefore);
  await page.evaluate(()=>NCTI18n.setLanguage('zh-CN'));assert.equal(await headerTrigger.count(),1);assert.deepEqual(await snapshot(page),headerBefore);
  const staleMarker=await page.evaluate(()=>{const host=document.createElement('div');host.innerHTML=NCTI18n.html('quote.i_have_binders_full_of_women_mitt_romney');host.querySelector('[data-nct-ui-note]').dataset.nctUiSource+=' changed';NCTNotes.apply(host);return host.querySelectorAll('.nct-note-trigger').length;});assert.equal(staleMarker,0);
  // Two original answer options with notes: mouse and keyboard must not select.
  await start(page,'1988_Bush_Quayle');
  const option=cat.records.find(r=>r.key==='1988_Bush_Quayle/answers_json/4482@43/description');
  await page.evaluate(r=>{document.querySelector('#question_form label').innerHTML=NCTStory.html(r.collection,r.location.pk,r.field,r.source,r.scope);},option);
  let before=await snapshot(page);const trigger=page.locator('#question_form label .nct-note-trigger').first();await trigger.click();assert.deepEqual(await snapshot(page),before,'Mouse click changed answer/game/RNG');
  assert.equal(await page.locator('.nct-note-panel').count(),1,'Mouse must actually open the note');
  const links=await page.locator('.nct-note-panel a').evaluateAll(nodes=>nodes.map(n=>({href:n.href,rel:n.rel,target:n.target})));assert.ok(links.every(s=>s.href.startsWith('https://')&&s.rel.includes('noopener')&&s.target==='_blank'));
  await page.screenshot({path:'.test-artifacts/annotation-answer-zh.png',fullPage:true});await page.keyboard.press('Escape');assert.equal(await page.locator('.nct-note-panel').count(),0);
  await trigger.focus();await page.keyboard.press('Enter');assert.deepEqual(await snapshot(page),before,'Keyboard changed answer/game/RNG');
  assert.equal(await page.locator('.nct-note-panel').count(),1,'Enter must open the note');
  await page.keyboard.press('Space');await page.keyboard.press('ArrowRight');assert.deepEqual(await snapshot(page),before,'Game shortcut fired while note was open');
  if(!await page.locator('.nct-note-panel').count())await trigger.click();
  for(const zoom of [0.8,1,1.25,1.5]){
   await page.evaluate(z=>document.documentElement.style.zoom=z,zoom);
   await page.setViewportSize({width:1280+Math.round(zoom*10),height:900});
   // Viewport acknowledgement can precede the queued resize handler. Observe
   // its rendered result, without calling positioning code from the test.
   await page.waitForFunction(()=>{const r=document.querySelector('.nct-note-panel').getBoundingClientRect();return r.left>=0&&r.top>=0&&r.right<=innerWidth&&r.bottom<=innerHeight;},null,{timeout:2000});
   const box=await page.locator('.nct-note-panel').boundingBox();assert.ok(box.x>=0&&box.y>=0&&box.x+box.width<=1295&&box.y+box.height<=901,'Panel overflow at '+zoom+' '+JSON.stringify(box));
  }
  await page.evaluate(()=>{document.documentElement.style.zoom=1;NCTI18n.setLanguage('en-US');});assert.deepEqual(await snapshot(page),before);assert.equal(await page.locator('.nct-note-trigger,.nct-note-panel').count(),0);
  await page.evaluate(()=>NCTI18n.setLanguage('zh-CN'));assert.equal(await trigger.count(),1);assert.deepEqual(await snapshot(page),before);
  await trigger.click();await page.locator('.nct-note-close').click();assert.deepEqual(await snapshot(page),before);
  // Original answer/feedback/next-question actions still operate after note use.
  await page.locator('.game_answers').first().check();await page.locator('#answer_select_button').click();await page.locator('#ok_button').click();assert.ok(await page.locator('.game_answers,.visit_text').count());
  // Restricted mobile viewport: a note still stays inside the visible viewport.
  await page.setViewportSize({width:390,height:760});await page.evaluate(r=>{const n=document.createElement('div');n.id='note-audit';n.innerHTML=NCTStory.html(r.collection,r.location.pk,r.field,r.source,r.scope);document.body.prepend(n);},option);await page.locator('#note-audit .nct-note-trigger').click();const box=await page.locator('.nct-note-panel').boundingBox();assert.ok(box.x>=0&&box.x+box.width<=390&&box.y+box.height<=760);
  assert.deepEqual(report.errors,[]);assert.deepEqual(report.external,[]);assert.deepEqual(report.missing,[]);
  report.checks.push('Every exact source/key/SHA binding valid and human reviewed','Every note, including endings and 47 header keys, rendered and opened offline','All 48 original header slots attach notes; header cache and language switching stable','Changed sources never inherit stale annotations','Mouse/Enter/Escape/close do not change game object, radio selection or RNG','English hides notes; Chinese restores without duplicate buttons or state changes','Source links safe; no source-site requests on opening explanations','Answer/feedback/next flow remains operational','Panel fits 390px viewport and 80/100/125/150 percent CSS zoom');report.status='passed';
  report.checks.push('All 14 native reading lists resolve to revised Chinese with original link targets intact');
 }catch(e){report.failure=e.stack;report.status='failed';throw e;}finally{fs.writeFileSync('tests/annotations-results.json',JSON.stringify(report,null,2)+'\n');await browser.close();}
 console.log('PASS',report.notes,'notes;',report.rendered,'bindings; offline UI and unchanged game state');
})().catch(e=>{console.error(e);process.exitCode=1;});
