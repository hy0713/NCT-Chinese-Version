/* Explicit, presentation-only adapters for the built-in scenario renderers.
 * Original game objects remain English. Matching requires scope, entity, field
 * and exact source text; duplicate upstream IDs are retained in the catalogue. */
(function(){
 'use strict';
 const cache=Object.create(null),base='/localization/stories/';
 let active='base';
 const escape=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function read(url){try{const x=new XMLHttpRequest();x.open('GET',url,false);x.send();if(x.status===200)return JSON.parse(x.responseText);}catch(e){console.warn('NCT story resource unavailable',url);}return {};}
 const glossary=read('/localization/glossary_zh.json');
 function pack(scope){return cache[scope]||(cache[scope]=read(base+scope+'.pack.json'));}
 function native(){return typeof window.modded==='undefined'||!window.modded;}
 function use(url){const m=String(url).match(/(?:^|\/)(\d{4}a?_[A-Za-z]+_[A-Za-z]+)\.html(?:[?#].*)?$/);active=m?m[1]:'base';if(m)pack(active);return active;}
 function resolve(collection,pk,field,source,scope){
  if(!native())return null;
  for(const s of [...new Set([scope||active,'base'])]){
   const p=pack(s),list=p.index?.[collection]?.[String(pk)]?.[field]||[];
   const key=list.find(k=>p.en?.[k]===source);
   if(key)return {scope:s,key};
  }
  return null;
 }
 function expanded(value){return typeof window.substitutePlaceholders==='function'?window.substitutePlaceholders(value):value;}
 function value(ref,source){const p=pack(ref.scope);return expanded(NCTI18n.language==='zh-CN'?(p.zh?.[ref.key]??source):source);}
 function html(collection,pk,field,source,scope){
  if(typeof source!=='string'||!source)return source??'';
  const ref=resolve(collection,pk,field,source,scope);
  if(!ref){
   // The original debate-coach ability adds this presentation wrapper to the
   // English answer. Retain the wrapper and resolve its original inner text.
   const highlight=source.match(/^(<span style=['"]color:green['"]>)([\s\S]*)(<\/span>)$/);
   if(highlight)return highlight[1]+html(collection,pk,field,highlight[2],scope)+highlight[3];
   return expanded(source);
  }
  const tag=/<(?:p|ul|ol|h[1-6]|div)\b/i.test(source)?'div':'span';
  return `<${tag} class="nct-story" data-story-scope="${escape(ref.scope)}" data-story-key="${escape(ref.key)}" data-story-original="${escape(source)}">${value(ref,source)}${window.NCTNotes?.inline(ref.key,source)||''}</${tag}>`;
 }
 function bind(node,collection,pk,field,source,scope){node.innerHTML=html(collection,pk,field,source,scope);}
 function term(source){if(NCTI18n.language!=='zh-CN'||!native())return source;return glossary.names?.[source]??glossary.terms?.[source]??source;}
 function staff(kind,row,field){return html(kind,row.pk,field,row[field],`staff.${campaignTrail_temp.election_id}.${campaignTrail_temp.candidate_id}`);}
 function assetMarkup(source){return String(source).replace(/https?:\/\/[^\s"'<>]+/g,url=>NCTI18n.asset(url));}
 function fragments(scope){const p=pack(scope);return Object.keys(p.en||{}).filter(k=>k.includes('/ending/')).map(key=>({key,source:p.en[key],zh:p.zh?.[key]})).filter(r=>r.zh).sort((a,b)=>b.source.length-a.source.length);}
 function endingValue(source,scope){
  if(NCTI18n.language!=='zh-CN'||!native())return source;
  const field={win:'electoral_victory_message',loss:'electoral_loss_message',tie:'no_electoral_majority_message'}[campaignTrail_temp.final_outcome];
  const ref=resolve('candidate_json',campaignTrail_temp.candidate_id,field,source,'base');
  if(ref)return value(ref,source);
  // This adapter is restricted to the output of the upstream endingPicker.
  // Its input is never written back or used for a condition or calculation.
  let result=source;
  for(const r of fragments(scope))result=result.split(r.source).join(r.zh);
  // Values concatenated by the original ending function (state or VP names)
  // have no string literal of their own; translate only text nodes here.
  const t=document.createElement('template');t.innerHTML=result;
  const walker=document.createTreeWalker(t.content,NodeFilter.SHOW_TEXT),nodes=[];
  while(walker.nextNode())nodes.push(walker.currentNode);
  const terms=Object.entries(glossary.terms||{}).filter(([s])=>s.length>3).sort((a,b)=>b[0].length-a[0].length);
  for(const node of nodes){let text=node.textContent;for(const [s,z]of terms){const escaped=s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');text=text.replace(new RegExp('(?<![A-Za-z])'+escaped+'(?![A-Za-z])','g'),z);}node.textContent=text;}
  return assetMarkup(t.innerHTML);
 }
 function ending(source){if(!native()||typeof source!=='string')return source;return `<div class="nct-story" data-story-ending="${escape(active)}" data-story-original="${escape(source)}">${endingValue(source,active)}${window.NCTNotes?.ending(active,source)||''}</div>`;}
 function eventValue(key,source){const p=pack(active);return NCTI18n.language==='zh-CN'?(p.zh?.[key]??source):source;}
 function prepare(response){
  const p=pack(active);let index=0;
  return response.replace(/(<script\b[^>]*>)([\s\S]*?)(<\/script\s*>)/gi,(whole,open,code,close)=>{
   const current=index++;const patches=[...(p.events||[]),...(p.presentations||[])].filter(r=>r.script===current).sort((a,b)=>b.start-a.start);
   for(const patch of patches){const literal=code.slice(patch.start,patch.end);if(literal!==patch.literal){console.warn('NCT presentation source changed; retaining English',active,patch.start);continue;}const replacement=patch.mode==='asset'?`NCTStory.assetMarkup(${literal})`:`NCTStory.eventValue(${JSON.stringify(patch.key)},${literal})`;code=code.slice(0,patch.start)+replacement+code.slice(patch.end);}
   return open+code+close;
  });
 }
 function apply(root){
  for(const n of root.querySelectorAll('[data-story-key]'))n.innerHTML=value({scope:n.dataset.storyScope,key:n.dataset.storyKey},n.dataset.storyOriginal)+(window.NCTNotes?.inline(n.dataset.storyKey,n.dataset.storyOriginal)||'');
  for(const n of root.querySelectorAll('[data-story-ending]'))n.innerHTML=endingValue(n.dataset.storyOriginal,n.dataset.storyEnding)+(window.NCTNotes?.ending(n.dataset.storyEnding,n.dataset.storyOriginal)||'');
 }
 pack('base');
 window.NCTStory={html,bind,staff,term,ending,eventValue,prepare,use,apply,resolve,assetMarkup,get active(){return active;}};
})();
