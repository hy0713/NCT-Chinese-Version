"""Prepare immutable, runtime-derived source batches, never claim review done.

python tools/prepare-year-review.py 1916
Reads original catalogue and current review provenance. No translations written.
An existing year snapshot is reused rather than renumbered after partial work.
"""
import argparse,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'localization/reviews'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parser=argparse.ArgumentParser();parser.add_argument('year');parser.add_argument('--size',type=int,default=75)
args=parser.parse_args();assert re.fullmatch(r'\d{4}a?',args.year) and args.size>0
cat=read(ROOT/'localization/stories/catalogue.json')
scenarios=[s for s in cat['scenarios'] if s['year']==args.year]
assert scenarios,'Not a runtime built-in year'
snapshot=BASE/f'{args.year}-all-source-snapshot.json'
if snapshot.exists():rows=read(snapshot)
else:
    full=read(ROOT/'localization/stories/editorial-records.json')
    pending={r['source'] for r in read(ROOT/'localization/stories/review-queue.json')}
    scopes={s['scope'] for s in scenarios};pks={s[k] for s in scenarios for k in ['candidate','runningMate']}
    elections={s['election'] for s in scenarios};packs={};bySource={}
    for r in cat['records']:
        selected=r['scope'] in scopes or r['scope']=='base' and (
            r['collection']=='candidate_json' and r['location']['pk'] in pks or
            r['collection']=='election_json' and r['location']['pk'] in elections)
        prose=len(re.sub(r'<[^>]*>','',r['source']))>40
        if not selected or r['source'] in full or not (prose or r['source'] in pending):continue
        if r['scope'] not in packs:packs[r['scope']]=read(ROOT/'localization/stories'/f'{r["scope"]}.pack.json')
        bySource.setdefault(r['source'],{'source':r['source'],'zh':packs[r['scope']]['zh'][r['key']],'keys':[]})
    # Include every exact-source reuse, even in a different year.
    for r in cat['records']:
        if r['source'] in bySource:bySource[r['source']]['keys'].append(r['key'])
    rows=list(bySource.values())
    snapshot.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
records={r['key']:r for r in cat['records']}
for row in rows:
    digest=hashlib.sha256(row['source'].encode()).hexdigest()
    assert row['keys'] and all(records[k]['source']==row['source'] and records[k]['sha256']==digest for k in row['keys'])
for offset in range(0,len(rows),args.size):
    number=offset//args.size
    suffix=chr(ord('a')+number) if number<26 else f'part{number+1}'
    path=BASE/f'{args.year}-{suffix}-source-snapshot.json';part=rows[offset:offset+args.size]
    if path.exists():assert read(path)==part,f'Existing batch differs; do not overwrite {path}'
    else:path.write_text(json.dumps(part,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'year':args.year,'runtimePairings':len(scenarios),'snapshotSources':len(rows),
    'batches':(len(rows)+args.size-1)//args.size,'translationsGenerated':0},ensure_ascii=False))
