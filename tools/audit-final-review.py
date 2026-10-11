"""Fail closed on uncovered native text; distinguish prose from short names.

Full fields in editorial-records were explicitly authored in the dated batches
or the earlier biography/running-mate authoring tools. Segment/rule output is
not sufficient evidence for this audit. No mutation of translation or source.
"""
import collections,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
cat=read(ROOT/'localization/stories/catalogue.json')
full=read(ROOT/'localization/stories/editorial-records.json')
keyed=read(ROOT/'localization/stories/editorial-keyed.json')
names={r['source']:r for r in read(ROOT/'localization/reviews/final-names-review.json')['revisions']}
terms={r['source']:r for r in read(ROOT/'localization/reviews/final-terms-review.json')['revisions']}
packs={s:read(ROOT/f'localization/stories/{s}.pack.json') for s in {r['scope'] for r in cat['records']}}
counts=collections.Counter();by_scope={};missing=[]
for r in cat['records']:
    assert hashlib.sha256(r['source'].encode()).hexdigest()==r['sha256'],r['key']
    pack=packs[r['scope']];assert pack['en'][r['key']]==r['source'],r['key']
    zh=pack['zh'].get(r['key']);status=None
    if r['key'] in keyed:
        item=keyed[r['key']];assert item['sha256']==r['sha256'] and item['source']==r['source']
        assert zh==item['zh'];status='human-contextual-short-term'
    elif r['source'] in terms:
        assert zh==terms[r['source']]['zh'];status='human-short-terminology'
    elif r['source'] in names:
        assert r['field'] in {'first_name','last_name'} or r['collection']=='states_json' and r['field']=='name'
        assert zh==names[r['source']]['zh'];status='human-proper-name-verification'
    elif r['source'] in full:
        assert zh==full[r['source']],r['key'];status='human-full-field'
    else:missing.append(r['key']);status='unreviewed'
    assert zh,r['key'];counts[status]+=1
    by_scope.setdefault(r['scope'],collections.Counter())[status]+=1
assert not missing,missing
assert len(cat['scenarios'])==105
note_ids=read(ROOT/'localization/annotations/index.json')['notes']
context_terms=read(ROOT/'localization/reviews/glossary-context.zh-CN.json')['terms']
assert all(not t.get('noteId') or t['noteId'] in note_ids for t in context_terms)
for metadata in (ROOT/'localization/reviews').glob('*-metadata.json'):
    research=read(metadata).get('research')
    assert not research or (metadata.parent/research).is_file(),metadata.name
report={'checkedAt':'2026-10-10','entries':len(cat['records']),'unreviewed':missing,
        'counts':dict(counts),'scopes':{s:dict(c) for s,c in by_scope.items()},
        'nativePairings':105,'years':list(dict.fromkeys(s['year'] for s in cat['scenarios'])),
        'limits':['Full-field editorial review is not independent scholarly certification of every historical claim.',
                  'Proper-name verification is explicitly separate from paragraph review.',
                  'Runtime, RNG and ending regression results are recorded separately in tests/.']}
path=ROOT/'localization/reviews/final-field-audit.json'
path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'entries':report['entries'],'counts':report['counts'],'unreviewed':len(missing)},ensure_ascii=False))
