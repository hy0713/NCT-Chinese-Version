"""Explicit hand-reviewed short terminology, never a paragraph replacement rule."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
terms=read(ROOT/'localization/reviews/final-terms.zh-CN.json')
catalogue=read(ROOT/'localization/stories/catalogue.json')['records']
full=read(ROOT/'localization/stories/editorial-records.json')
glossary=read(ROOT/'localization/glossary_zh.json')
rows=[]
for source,zh in terms.items():
    assert '<' not in source and len(source)<60 and source!=zh
    keys=[r['key'] for r in catalogue if r['source']==source]
    if keys:
        full[source]=zh
        rows.append({'source':source,'zh':zh,'sha256':hashlib.sha256(source.encode()).hexdigest(),'keys':keys,'method':'human-short-terminology'})
    glossary['terms'][source]=zh
(ROOT/'localization/stories/editorial-records.json').write_text(json.dumps(full,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'localization/glossary_zh.json').write_text(json.dumps(glossary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'localization/reviews/final-terms-review.json').write_text(json.dumps({'checkedAt':'2026-10-10','method':'Explicit whole short-field review; not automatic prose review','revisions':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Reviewed short fields',len(rows))
