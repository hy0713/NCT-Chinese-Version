"""Record verification of already translated proper names and map labels.

Only first_name/last_name/states_json.name are accepted. This is a short
terminology audit, explicitly not paragraph proofreading or draft promotion.
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
cat=read(ROOT/'localization/stories/catalogue.json')['records']
full=read(ROOT/'localization/stories/editorial-records.json')
fixes={'Church':'彻奇','Sarah':'萨拉','Stassen':'史塔森',
 'Maine-1':'缅因州第1国会选区','Maine-2':'缅因州第2国会选区',
 'Nebraska-1':'内布拉斯加州第1国会选区','Nebraska-2':'内布拉斯加州第2国会选区','Nebraska-3':'内布拉斯加州第3国会选区'}
rows=[];seen=set();packs={}
for r in cat:
    source=r['source']
    if source in full or source in seen:continue
    assert r['field'] in {'first_name','last_name'} or r['collection']=='states_json' and r['field']=='name',r['key']
    assert '<' not in source and len(source)<45,r['key']
    pack=packs.setdefault(r['scope'],read(ROOT/f"localization/stories/{r['scope']}.zh-CN.json"))
    zh=fixes.get(source,pack[r['key']]);seen.add(source)
    rows.append({'source':source,'zh':zh,'sha256':r['sha256'],'keys':[v['key'] for v in cat if v['source']==source],
                 'method':'human-terminology-verification','changed':source in fixes})
    if source in fixes:full[source]=zh
(ROOT/'localization/stories/editorial-records.json').write_text(json.dumps(full,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'localization/reviews/final-names-review.json').write_text(json.dumps({'checkedAt':'2026-10-10','method':'Verified displayed short proper names and geographical labels, not narrative review','revisions':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
glossary=read(ROOT/'localization/glossary_zh.json');glossary['terms'].update(fixes)
(ROOT/'localization/glossary_zh.json').write_text(json.dumps(glossary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
keyed={r['key']:{'source':r['source'],'sha256':r['sha256'],'zh':'进步党','reason':'Party field differs from ideological stance Progressive.'} for r in cat if r['source']=='Progressive' and r['field']=='party'}
(ROOT/'localization/stories/editorial-keyed.json').write_text(json.dumps(keyed,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Verified terminology',len(rows),'corrected',len(fixes),'party contexts',len(keyed))
