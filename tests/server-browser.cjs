/* Verify the server actually serves the native game at its selected port. */
const fs=require('fs'),assert=require('assert'),{chromium}=require('./runtime.cjs'),{start}=require('./stories-browser.cjs');
const scenario=require('../localization/stories/catalogue.json').scenarios.find(s=>s.scope==='2012_Obama_Biden');
const saved=fs.readFileSync('.nct-port','ascii').trim();
process.env.NCT_BASE_URL=process.env.NCT_BASE_URL||`http://localhost:${saved}`;
const report={date:new Date().toISOString(),status:'running',port:Number(saved),errors:[],checks:[]};
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.NCT_BROWSER||'C:/Program Files/Google/Chrome/Application/chrome.exe'});try{
 const context=await browser.newContext();const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
 await start(page,scenario,'zh-CN','1');assert.equal(new URL(page.url()).port,saved);await page.locator('.game_answers').first().check();await page.locator('#answer_select_button').click();if(await page.locator('#ok_button').count())await page.locator('#ok_button').click();await page.waitForSelector('.game_answers');
 assert.equal(await page.evaluate(()=>campaignTrail_temp.player_answers.length),1);
 const hidden=await context.request.get(process.env.NCT_BASE_URL+'/.nct-port');assert.equal(hidden.status(),404);
 assert.deepEqual(report.errors,[]);report.checks=['Game loads from actual selected port','Native scenario starts and first answer advances','Saved port file cannot be fetched over HTTP','No JavaScript errors'];report.status='passed';console.log('PASS real local-server browser checks',report.port);
}catch(e){report.status='failed';report.failure=e.message;throw e;}finally{fs.writeFileSync('tests/server-browser-results.json',JSON.stringify(report,null,2)+'\n');await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
