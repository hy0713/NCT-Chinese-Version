"""Compile exact catalogue-key/source bindings; never scan or rewrite live DOM text."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
data=read(ROOT/'localization/annotations/notes.zh-CN.json')
data['notes']+=read(ROOT/'localization/annotations/header-notes.zh-CN.json')['notes']
reading=read(ROOT/'localization/annotations/beginner-notes.zh-CN.json')
assert reading['schema']==2
assert set(reading['notes'])=={note['id'] for note in data['notes']},'Reading edition must cover every note exactly'
for note in data['notes']:
    entry=reading['notes'][note['id']]
    assert isinstance(entry['title'],str) and entry['title'].strip() and '<' not in entry['title']
    assert isinstance(entry['body'],list) and len(entry['body'])>=2
    assert all(isinstance(p,str) and p.strip() and '<' not in p for p in entry['body'])
    note.update(title=entry['title'],body=entry['body'])
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
runtime={'schema':1,'checkedAt':data['checkedAt'],'readingEdition':reading['editedAt'],'notes':{n['id']:{k:v for k,v in n.items() if k!='contains'} for n in data['notes']},'bindings':bindings,'uiBindings':uiBindings,'endings':{s:sorted(set(keys)) for s,keys in endings.items()}}
(ROOT/'localization/annotations/index.json').write_text(json.dumps(runtime,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
report={'checkedAt':data['checkedAt'],'readingEdition':reading['editedAt'],'beginnerNotes':len(reading['notes']),'notes':len(ids),'boundFields':len(bindings),'boundHeaderKeys':len(uiBindings),'headerKeysWithoutNotes':[k for k in ui if k.startswith('quote.') and k not in uiBindings],'noteBindings':sum(counts.values()),'byNote':counts,'keysByNote':hits,'scenarioScopes':sorted({k.split('/')[0] for k in bindings})}
(ROOT/'localization/annotations/coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lines=['# 历史典故与网络梗','','本版正文修订于 '+reading['editedAt']+'。', '', f'共 {len(ids)} 条离线说明，覆盖 {len(bindings)} 处剧本原文和 {len(uiBindings)} 个页眉语录键。正文先讲来历，再说这段话在剧情里为什么重要。','']
for n in data['notes']:
    lines+=['## '+n['title'],'']
    for paragraph in n['body']:
        lines += [paragraph,'']
    lines+=['资料来源','',*['- ['+s['title']+']('+s['url']+')' for s in n['sources']], '']
(ROOT/'localization/annotations/NOTES_ZH.md').write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({k:report[k] for k in ['notes','boundFields','noteBindings']},ensure_ascii=False))
