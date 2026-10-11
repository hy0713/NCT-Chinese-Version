"""Apply a reproducible full-field review; original source and HTML stay intact.

python tools/apply-historical-review.py 1844
Numbered draft lines use the immutable source snapshot, never a regenerated queue.
The report records provenance and remains independently auditable.
"""
import hashlib,json,re,sys
from datetime import datetime,timedelta,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
name=sys.argv[1]
assert re.fullmatch(r'[a-zA-Z0-9_-]+',name)
base=ROOT/'localization/reviews'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
snapshot=read(base/f'{name}-source-snapshot.json')
translations=(base/f'{name}-revised.txt').read_text(encoding='utf-8').splitlines()
assert len(snapshot)==len(translations),(len(snapshot),len(translations))
catalogue=read(ROOT/'localization/stories/catalogue.json')['records']
bykey={r['key']:r for r in catalogue}
full=read(ROOT/'localization/stories/editorial-records.json')
tags=lambda s:re.findall(r'<(?:/?[A-Za-z][^>]*|!--[\s\S]*?--)>',s)
tokens=lambda s:re.findall(r'\{\{[^{}]+\}\}|\$\{[^{}]+\}|\{[A-Za-z_][A-Za-z_0-9]*\}',s)
revisions=[];seen=set()
for i,(row,zh) in enumerate(zip(snapshot,translations)):
    source=row['source'];digest=hashlib.sha256(source.encode()).hexdigest()
    assert source not in seen;seen.add(source)
    assert zh.strip() and re.search(r'[\u3400-\u9fff]',zh) and source!=zh,i
    assert tags(source)==tags(zh),(i,'HTML changed')
    assert tokens(source)==tokens(zh),(i,'placeholders changed')
    assert all(bykey[k]['source']==source and bykey[k]['sha256']==digest for k in row['keys']),i
    before=full.get(source);full[source]=zh
    revisions.append({'index':i,'source':source,'sha256':digest,'zh':zh,
        'keys':row['keys'],'method':'human-full-field','changed':before!=zh})
metadata=read(base/f'{name}-metadata.json') if (base/f'{name}-metadata.json').exists() else {}
report={'checkedAt':metadata.get('checkedAt',datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')),'batch':name,'uniqueSourcesReviewed':len(revisions),
    'recordPositions':sum(r['source'] in seen for r in catalogue),
    'method':'Full-field editorial translation with era-specific historical research; not an independent scholarly certification.',
    'sourceExceptions':[{'index':71,'reason':'Original does derive may be missing not; retain literal claim and attach explanation.'},
        {'index':193,'reason':'Original Thomas Birney retained; note identifies historical James G. Birney.'},
        {'index':206,'reason':'Original some of all is malformed; contextual some or all reading explicitly disclosed in note.'}] if name=='1844' else [],
    'revisions':revisions}
if 'sourceExceptions' in metadata:report['sourceExceptions']=metadata['sourceExceptions']
(ROOT/'localization/stories/editorial-records.json').write_text(json.dumps(full,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(base/f'{name}-editorial-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['batch','uniqueSourcesReviewed','recordPositions']},ensure_ascii=False))
