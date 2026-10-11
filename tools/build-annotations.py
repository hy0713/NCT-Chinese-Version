"""Compile exact catalogue-key/source bindings; never scan or rewrite live DOM text."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
data=read(ROOT/'localization/annotations/notes.zh-CN.json')
data['notes']+=read(ROOT/'localization/annotations/header-notes.zh-CN.json')['notes']
cat=read(ROOT/'localization/stories/catalogue.json')
ui=read(ROOT/'localization/en-US.json')
ids=set();bindings={};endings={};uiBindings={};counts={};hits={}
for note in data['notes']:
    assert re.fullmatch(r'[a-z0-9]+(?:[.-][a-z0-9]+)+',note['id']) and note['id'] not in ids
    ids.add(note['id']);counts[note['id']]=0;hits[note['id']]=[]
    assert note['body'] and all(isinstance(s,str) and s.strip() for s in note['body'])
    assert note['sources'] and all(s['url'].startswith('https://') and s['title'] for s in note['sources'])
    for row in cat['records']:
        if row['collection']=='election_json' and row['field']=='recommended_reading':continue
        if not any(p.casefold() in row['source'].casefold() for p in note['contains']):continue
        assert hashlib.sha256(row['source'].encode()).hexdigest()==row['sha256']
        entry=bindings.setdefault(row['key'],{'source':row['source'],'sha256':row['sha256'],'notes':[]})
        entry['notes'].append(note['id']);counts[note['id']]+=1;hits[note['id']].append(row['key'])
        if row['collection']=='ending' or row['field'] in ['electoral_victory_message','electoral_loss_message','no_electoral_majority_message']:
            endings.setdefault(row['scope'],[]).append(row['key'])
    for key,source in ui.items():
        if not key.startswith('quote.') or not any(p.casefold() in source.casefold() for p in note['contains']):continue
        entry=uiBindings.setdefault(key,{'source':source,'sha256':hashlib.sha256(source.encode()).hexdigest(),'notes':[]})
        entry['notes'].append(note['id']);counts[note['id']]+=1;hits[note['id']].append('ui/'+key)
    assert counts[note['id']],f'No native source match: {note["id"]}'
# Literal header rendering normalizes whitespace; the original array also has
# two differently punctuated variants of the same crook quote key. Record each
# exact, reviewed source variant instead of permitting fuzzy runtime matching.
headers=read(ROOT/'localization/annotations/header-editorial-review.json')['records']
for key,entry in uiBindings.items():
    variants={entry['source']}
    for row in headers:
        if row['key']==key:
            variants.add(row['source']);variants.add(re.sub(r'\s+',' ',row['source']).strip())
    entry['sourceVariants']=[{'source':s,'sha256':hashlib.sha256(s.encode()).hexdigest()} for s in sorted(variants)]
runtime={'schema':1,'checkedAt':data['checkedAt'],'notes':{n['id']:{k:v for k,v in n.items() if k!='contains'} for n in data['notes']},'bindings':bindings,'uiBindings':uiBindings,'endings':{s:sorted(set(keys)) for s,keys in endings.items()}}
(ROOT/'localization/annotations/index.json').write_text(json.dumps(runtime,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
report={'checkedAt':data['checkedAt'],'notes':len(ids),'boundFields':len(bindings),'boundHeaderKeys':len(uiBindings),'headerKeysWithoutNotes':[k for k in ui if k.startswith('quote.') and k not in uiBindings],'noteBindings':sum(counts.values()),'byNote':counts,'keysByNote':hits,'scenarioScopes':sorted({k.split('/')[0] for k in bindings})}
(ROOT/'localization/annotations/coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 历史典故与网络梗校注','','查证日期：'+data['checkedAt']+'。解释随项目离线提供；来源网页仅在主动点击链接时访问。','',f'共{len(ids)}条说明，绑定{len(bindings)}个剧本原文位置与{len(uiBindings)}个页眉语录键（复用剧本会重复计数）。通过稳定键及原文匹配；原文变化时不套用旧注释。','', '不提供答案评分、选项效果或隐藏结局触发条件。用典推断明确标记；架空对白不当作史料。','']
for n in data['notes']:
    lines+=['## '+n['title'],'',n['category'],'']
    lines+=n['body']+['']
    lines+=['来源：'+ '；'.join('['+s['title']+']('+s['url']+')' for s in n['sources']), '']
(ROOT/'localization/annotations/NOTES_ZH.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['notes','boundFields','noteBindings']},ensure_ascii=False))
