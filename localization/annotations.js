/* Notes are attached only by explicit story renderers and verified source keys.
 * Their UI lives outside answer labels; opening it never touches game state. */
(function(){
 'use strict';
 let data={notes:{},bindings:{},endings:{}},panel=null,anchor=null;
 try{const x=new XMLHttpRequest();x.open('GET','/localization/annotations/index.json',false);x.send();if(x.status===200)data=JSON.parse(x.responseText);}catch(e){console.warn('NCT annotations unavailable',e);}
 const zh=()=>window.NCTI18n?.language==='zh-CN';
 function button(ids){return zh()&&ids.length?` <button type="button" class="nct-note-trigger" data-nct-notes="${[...new Set(ids)].join(' ')}" aria-haspopup="dialog" aria-label="查看历史典故与网络梗说明">典故${new Set(ids).size>1?' · '+new Set(ids).size:''}</button>`:'';}
 function inline(key,source){const entry=data.bindings[key];return entry?.source===source?button(entry.notes):'';}
 const attribute=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const matches=(entry,source)=>entry&&(entry.source===source||entry.sourceVariants?.some(v=>v.source===source));
 function ui(key,source){const entry=data.uiBindings?.[key];return matches(entry,source)?`<span data-nct-ui-note="${attribute(key)}" data-nct-ui-source="${attribute(source)}">${button(entry.notes)}</span>`:'';}
 function apply(root){for(const node of root.querySelectorAll('[data-nct-ui-note]')){const entry=data.uiBindings?.[node.dataset.nctUiNote];node.innerHTML=matches(entry,node.dataset.nctUiSource)?button(entry.notes):'';}}
 function ending(scope,source){const ids=[];for(const s of new Set([scope,'base']))for(const key of data.endings[s]||[]){const entry=data.bindings[key];if(entry&&source.includes(entry.source))ids.push(...entry.notes);}return button(ids);}
 function close(restoreFocus=false){if(panel)panel.remove();panel=null;if(anchor){anchor.setAttribute('aria-expanded','false');if(restoreFocus&&anchor.isConnected)anchor.focus();}anchor=null;}
 function place(){
  if(!panel||!anchor)return;
  if(!anchor.isConnected){close();return;}
  const r=anchor.getBoundingClientRect(),scale=panel.offsetWidth?panel.getBoundingClientRect().width/panel.offsetWidth:1;
  const width=Math.min(460,window.innerWidth-24);
  // Bounding rectangles use visual pixels; fixed CSS coordinates inherit the
  // page's CSS zoom. Convert once so the panel remains inside the viewport.
  panel.style.width=width/scale+'px';panel.style.maxHeight=(window.innerHeight-24)/scale+'px';
  panel.style.left=Math.max(12,Math.min(r.left,window.innerWidth-width-12))/scale+'px';
  panel.style.top=Math.max(12,Math.min(r.bottom+6,window.innerHeight-panel.getBoundingClientRect().height-12))/scale+'px';
 }
 function show(target){
  const notes=target.dataset.nctNotes.split(' ').map(id=>data.notes[id]).filter(Boolean);if(!zh()||!notes.length)return;
  if(target===anchor){close(true);return;}close();anchor=target;target.setAttribute('aria-expanded','true');
  panel=document.createElement('aside');panel.className='nct-note-panel';panel.setAttribute('role','dialog');panel.setAttribute('aria-label','历史典故与网络梗说明');
  const dismiss=document.createElement('button');dismiss.type='button';dismiss.className='nct-note-close';dismiss.textContent='关闭';dismiss.addEventListener('click',()=>close(true));panel.append(dismiss);
  for(const note of notes){
   const section=document.createElement('section'),heading=document.createElement('h4'),category=document.createElement('small');heading.textContent=note.title;category.textContent=note.category;section.append(heading,category);
   for(const text of note.body){const p=document.createElement('p');p.textContent=text;section.append(p);}
   const list=document.createElement('ul');list.setAttribute('aria-label','查证来源');
   for(const source of note.sources){const li=document.createElement('li'),link=document.createElement('a');link.textContent=source.title;link.href=source.url;link.target='_blank';link.rel='noopener noreferrer';li.append(link);list.append(li);}section.append(list);panel.append(section);
  }
  const footer=document.createElement('small');footer.textContent='说明已保存在本地。仅点击来源链接时联网。查证：'+data.checkedAt;panel.append(footer);document.body.append(panel);place();dismiss.focus();
 }
 document.addEventListener('click',event=>{
  const target=event.target.closest?.('.nct-note-trigger');
  if(target){event.preventDefault();event.stopPropagation();show(target);return;}
  if(panel&&!panel.contains(event.target))close();
 },true);
 document.addEventListener('keydown',event=>{
  const target=event.target.closest?.('.nct-note-trigger');
  // The original game's document/body shortcuts submit answers on Enter and
  // scroll/navigate on Space/arrow keys. Note controls must consume these first.
  if(target){event.stopPropagation();if(event.key==='Enter'||event.key===' '){event.preventDefault();show(target);}return;}
  if(panel){event.stopPropagation();if(event.key==='Escape'){event.preventDefault();close(true);}}
 },true);
 window.addEventListener('resize',place);
 document.addEventListener('nct:languagechange',()=>close());
 window.NCTNotes={inline,ending,ui,apply,close};
})();
