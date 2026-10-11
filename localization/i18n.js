/* Presentation only. No game data, RNG, scoring or event handlers are modified here. */
(function () {
  'use strict';
  const base = '/localization/';
  function load(file) {
    try { const xhr = new XMLHttpRequest(); xhr.open('GET', base + file, false); xhr.send();
      if (xhr.status === 200) return JSON.parse(xhr.responseText);
    } catch (error) { console.warn('NCT language resource unavailable:', file); }
    return {};
  }
  const packs = { 'en-US': load('en-US.json'), 'zh-CN': load('zh-CN.json') };
  const sources = load('source-keys.json');
  const terms = load('term-keys.json');
  const assets = load('assets.json');
  let language = 'zh-CN';
  try { const saved = localStorage.getItem('nct.language'); if (saved in packs) language = saved; } catch (_) {}
  const normalize = value => String(value ?? '').replace(/\s+/g, ' ').trim();
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function text(key, params = {}, fallback = key) {
    const template = packs[language][key] ?? packs['en-US'][key] ?? fallback;
    return template.replace(/\{([a-zA-Z_][a-zA-Z0-9_]*)\}/g, (m,k) => params[k] === undefined ? m : ['state','issue','candidate','affected'].includes(k) ? term(params[k]) : String(params[k]));
  }
  function html(key, params = {}, fallback = packs['en-US'][key] ?? key) {
    return `<span data-i18n="${escape(key)}" data-i18n-params="${escape(JSON.stringify(params))}" data-i18n-fallback="${escape(fallback)}">${escape(text(key,params,fallback))}</span>` + (window.NCTNotes?.ui(key,fallback)||'');
  }
  function literal(value) {
    const original = normalize(value), key = sources[original] || terms[original];
    return key ? html(key,{},original) : escape(value);
  }
  function term(value) {
    const original = String(value ?? '');
    const key = terms[original] || sources[normalize(original)];
    return key ? text(key,{},original) : window.NCTStory ? NCTStory.term(original) : original;
  }
  function termHtml(value) {
    return `<span data-i18n-term="${escape(value)}">${escape(term(value))}</span>`;
  }
  function option(key,params,value) {
    return `<option value="${escape(value)}" data-i18n="${escape(key)}" data-i18n-params="${escape(JSON.stringify(params))}">${escape(text(key,params))}</option>`;
  }
  function bindTerm(node,value) { node.dataset.i18nTerm=String(value); node.textContent=term(value); }
  function describe(value) {
    // Only the ability paragraph of the built-in staffing panel is localized.
    // The historical biography and the source game data stay in English.
    const template=document.createElement('template'); template.innerHTML=value;
    const first=template.content.querySelector('p');
    if (!first) return value;
    const walker=document.createTreeWalker(first,NodeFilter.SHOW_TEXT),nodes=[];
    while(walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) {
      const original=normalize(node.textContent),key=sources[original];
      if (key) { const span=document.createElement('span');span.dataset.i18n=key;span.textContent=text(key);node.replaceWith(span); }
    }
    return template.innerHTML;
  }
  function apply(root) {
    for (const node of root.querySelectorAll('[data-i18n]')) {
      const params = JSON.parse(node.getAttribute('data-i18n-params') || '{}');
      node.textContent = text(node.dataset.i18n,params,node.dataset.i18nFallback || node.textContent);
    }
    for (const node of root.querySelectorAll('[data-i18n-term]')) {
      if (node.querySelector('[data-i18n]')) continue;
      const original = node.dataset.i18nTerm || node.textContent;
      node.dataset.i18nTerm = original;
      node.textContent = term(original);
    }
    for (const node of root.querySelectorAll('[data-i18n-placeholder]')) node.placeholder = text(node.dataset.i18nPlaceholder);
    for (const node of root.querySelectorAll('[data-i18n-title]')) node.title = text(node.dataset.i18nTitle);
    for (const node of root.querySelectorAll('[data-i18n-aria-label]')) node.setAttribute('aria-label',text(node.dataset.i18nAriaLabel));
    if (window.NCTStory) NCTStory.apply(root);
    if (window.NCTNotes) NCTNotes.apply(root);
    for (const node of root.querySelectorAll('[src]')) {
      const src = node.getAttribute('src'); if (assets[src]) node.setAttribute('src', assets[src]);
    }
  }
  function render(value) {
    if (typeof value !== 'string' || !value.includes('<')) return value;
    const template = document.createElement('template'); template.innerHTML = value;
    apply(template.content); return template.innerHTML;
  }
  function canonicalHTML(value) {
    const template = document.createElement('template'); template.innerHTML = value;
    for (const node of template.content.querySelectorAll('[data-i18n]')) node.textContent = packs['en-US'][node.dataset.i18n] ?? node.dataset.i18nFallback ?? '';
    for (const node of template.content.querySelectorAll('[data-i18n-term]')) node.textContent = node.dataset.i18nTerm;
    // Expanded note state is transient accessibility UI, not a banner edit.
    // The original header timer must not replace the focused note button.
    for (const node of template.content.querySelectorAll('.nct-note-trigger')) node.removeAttribute('aria-expanded');
    return template.innerHTML;
  }
  function setLanguage(value) {
    if (!(value in packs)) return;
    language = value; try { localStorage.setItem('nct.language',value); } catch (_) {}
    document.documentElement.lang = value;
    apply(document);
    document.title = text('ui.the_new_campaign_trail');
    const toggle = document.getElementById('language-toggle');
    if (toggle) { toggle.textContent = text(value === 'zh-CN' ? 'menu.switch_to_english' : 'menu.switch_to_chinese'); toggle.setAttribute('aria-label',text('menu.language')); }
    // Keep the original header cache in the selected language across later renders.
    if (typeof window.corrr === 'string') window.corrr = render(window.corrr);
    if (window.jQuery && jQuery('#dialogue').hasClass('ui-dialog-content')) jQuery('#dialogue').dialog('option','title',text('ui.benefit_check'));
    document.dispatchEvent(new CustomEvent('nct:languagechange',{detail:{language}}));
  }
  function loadQuestion(target,url,callback) {
    // Match jQuery.load's script execution, but resolve native remote images
    // before the HTML enters the live document.
    jQuery.ajax({url,dataType:'html',success(response,status,xhr) {
      if (window.NCTStory) { NCTStory.use(url); response=NCTStory.prepare(response); }
      target.html(render(response)); callback.call(target[0],response,status,xhr);
    },error() { target.html(html('error.load')); }});
  }
  window.NCTI18n = {text,html,literal,term,termHtml,option,bindTerm,describe,apply,render,canonicalHTML,setLanguage,loadQuestion,get language(){return language;},asset: src => assets[src] || src};
  document.addEventListener('DOMContentLoaded', () => {
    const controls=document.getElementById('language-controls');
    for(const type of ['keydown','keyup'])controls.addEventListener(type,event=>event.stopPropagation());
    setLanguage(language);
    document.getElementById('language-toggle').addEventListener('click', () => setLanguage(language === 'zh-CN' ? 'en-US' : 'zh-CN'));
  });
})();
