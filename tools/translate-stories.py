"""Development-only, resumable draft translation. Never loaded by the game.

Only public source text is sent to the explicitly selected draft service.
HTML, entities, URLs and game placeholders are split off and never submitted.
Successful segments are cached; failures remain reported rather than counted.
Use --offline to rebuild packages using the checked-in translation memory.
"""
import argparse,concurrent.futures,hashlib,json,re,time,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STORY=ROOT/'localization/stories'
split=re.compile(r'(<(?:/?[A-Za-z][^>]*|!--[\s\S]*?--)>|\{\{.*?\}\}|\$\{.*?\}|\{[A-Za-z_]\w*\}|&(?:#\d+|#x[\da-fA-F]+|\w+);|https?://[^\s<>]+)')
digest=lambda s:hashlib.sha256(s.encode()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def parts(s):return split.split(s)
def chunks(values,limit=2300):
 out=[];length=0
 for v in values:
  if out and length+len(v)+25>limit:yield out;out=[];length=0
  out.append(v);length+=len(v)+25
 if out:yield out
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');parser.add_argument('--single',action='store_true');parser.add_argument('--workers',type=int,default=2);args=parser.parse_args()
 cat=read(STORY/'catalogue.json');glossary=read(ROOT/'localization/glossary_zh.json')
 memoryPath=STORY/'translation-memory.json';memory=read(memoryPath) if memoryPath.exists() else {}
 strategy='draft-google-protected-proper-terms-v2'
 obsolete={k:v for k,v in memory.items() if v['method'].startswith('draft-') and v['method']!=strategy}
 if obsolete:
  backup=ROOT/'.test-artifacts/stories/obsolete-drafts.json'
  if not backup.exists():write(backup,obsolete)
  memory={k:v for k,v in memory.items() if k not in obsolete}
 overridesPath=STORY/'editorial-overrides.json';overrides=read(overridesPath) if overridesPath.exists() else {}
 recordOverrides=STORY/'editorial-records.json'
 if recordOverrides.exists():overrides.update(read(recordOverrides))
 rules=read(STORY/'editorial-rules.json')
 terms=glossary['terms']; names=glossary['names']
 frameworkSources=read(ROOT/'localization/source-keys.json');frameworkZh=read(ROOT/'localization/zh-CN.json')
 # Longest phrase wins. Boundaries protect words such as congressional/Johnson.
 ordinary={'Bill','Democratic','Democracy',"Democrat's",'Democrats','Republicans','Democrat','Republican','Senate','House of Representatives','Congress','Senator','Governor','Vice President','vice-president','Vice Presidential','electoral votes','electoral vote','popular votes','popular vote','running mate','swing states','swing state','the Midwest','The ticket','your ticket','our ticket','this ticket','on the ticket','ticket','stump speech','stumping','campaign trail','anti-slavery','pro-slavery','slavery','abolitionists','abolitionist','segregation','desegregation','integration','national bank','protective tariff','filibuster','lame duck','states rights',"states' rights"}
 protected={k:v for k,v in terms.items() if k not in ordinary}
 ordered=sorted(protected,key=len,reverse=True)
 pattern=re.compile(r'(?<![\w])('+ '|'.join(re.escape(k) for k in ordered)+r')(?![\w])',re.I)
 folded={k.casefold():i for i,k in enumerate(ordered)}
 def prepare(s):
  s=s.replace('\ufffd','').replace('��',"'")
  # Resolve specific election idioms using English context, never injecting
  # Chinese into an English-only draft engine.
  s=re.sub(r'\breturns\b','election results',s)
  s=re.sub(r'\binternal improvem(?:ents|nets)\b','domestic public infrastructure improvements',s,flags=re.I)
  return pattern.sub(lambda m:f'[NT{folded[m[0].casefold()]:04d}]',s)
 def restore(s,original):
  s=re.sub(r'[\[［]\s*NT\s*(\d{4})\s*[\]］]',lambda m:protected[ordered[int(m[1])]],s,flags=re.I)
  if 'libertarian' in original.lower() and 'liberal' not in original.lower():s=s.replace('自由主义者','自由意志主义者').replace('自由主义的','自由意志主义的')
  return s
 segments={p.strip() for r in cat['records'] for p in parts(r['source'])[::2] if re.search('[A-Za-z]',p)}
 for s in sorted(segments):
  key=digest(s)
  if s in overrides:memory[key]={'source':s,'zh':overrides[s],'method':'editorial'}
  elif re.sub(r'\s+',' ',s).strip() in frameworkSources:memory[key]={'source':s,'zh':frameworkZh[frameworkSources[re.sub(r'\s+',' ',s).strip()]],'method':'framework-reviewed'}
  elif s in names or s in terms:memory[key]={'source':s,'zh':names.get(s,terms.get(s)),'method':'glossary'}
 pending=[s for s in sorted(segments) if digest(s) not in memory]
 print('Segments',len(segments),'cached',len(segments)-len(pending),'pending',len(pending),flush=True)
 failures=[]
 if pending and not args.offline:
  batches=[[s] for s in pending] if args.single else list(chunks(pending));proxy=urllib.request.ProxyHandler()
  def translate(batch):
   opener=urllib.request.build_opener(proxy)
   text='\n'.join(f'[NCT{i:04d}] '+prepare(s).replace('\n',' ') for i,s in enumerate(batch))
   url='https://translate.googleapis.com/translate_a/single?'+urllib.parse.urlencode({'client':'gtx','sl':'en','tl':'zh-CN','dt':'t','q':text})
   data=json.load(opener.open(url,timeout=45));result=''.join(piece[0] or '' for piece in data[0])
   matches=list(re.finditer(r'\[\s*NCT\s*(\d{4})\s*\]',result,re.I))
   if len(matches)!=len(batch):raise ValueError('Lost batch markers')
   output=[]
   for i,m in enumerate(matches):
    if int(m[1])!=i:raise ValueError('Changed batch ordering')
    zh=restore(result[m.end():matches[i+1].start() if i+1<len(matches) else len(result)].strip(),batch[i])
    expected=re.findall(r'\[NT(\d{4})\]',prepare(batch[i]));actual=re.findall(r'[\[［]\s*NT\s*(\d{4})\s*[\]］]',result[m.end():matches[i+1].start() if i+1<len(matches) else len(result)],re.I)
    if sorted(expected)!=sorted(actual):raise ValueError('Changed protected terms')
    if not zh or not re.search('[\u3400-\u9fff]',zh):raise ValueError('Empty/non-Chinese draft')
    output.append((batch[i],zh))
   return output
  with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
   futures={pool.submit(translate,b):b for b in batches};done=0
   for future in concurrent.futures.as_completed(futures):
    done+=1
    try:
     for s,zh in future.result():memory[digest(s)]={'source':s,'zh':zh,'method':strategy}
    except Exception as e:failures.append({'sources':futures[future],'error':str(e)})
    if done%10==0 or done==len(batches):write(memoryPath,memory);print('Batches',done,'/',len(batches),'failures',len(failures),flush=True)
 write(memoryPath,memory);write(STORY/'translation-failures.json',failures)
 # Reconstitute exact original markup, whitespace and dynamic placeholders.
 def translated(r):
  s=r['source']
  if s in overrides:return overrides[s]
  output=[]
  for i,p in enumerate(parts(s)):
   if i%2:output.append(p);continue
   core=p.strip()
   if not core or not re.search('[A-Za-z]',core):output.append(p);continue
   entry=memory.get(digest(core))
   if not entry:return None
   zh=entry['zh']
   if entry['method'].startswith('draft-'):
    for rule in rules:
     if re.search(rule['source'],core,re.I) and not (rule.get('except') and re.search(rule['except'],core,re.I)):
      for before,after in rule['replacements'].items():zh=zh.replace(before,after)
    zh=re.sub(r'(?<=[\u3400-\u9fff，。、：；！？]) +(?=[\u3400-\u9fff])','',zh)
   output.append(p[:len(p)-len(p.lstrip())]+zh+p[len(p.rstrip()):])
  return ''.join(output)
 en={};zh={};index={};missing=[]
 keyed=read(STORY/'editorial-keyed.json') if (STORY/'editorial-keyed.json').exists() else {}
 for r in cat['records']:
  scope=r['scope'];en.setdefault(scope,{})[r['key']]=r['source']
  value=translated(r)
  if r['key'] in keyed:
   entry=keyed[r['key']]
   assert entry['source']==r['source'] and entry['sha256']==r['sha256'],r['key']
   assert split.findall(entry['zh'])==split.findall(r['source']),r['key']
   value=entry['zh']
  if value:zh.setdefault(scope,{})[r['key']]=value
  else:missing.append({'key':r['key'],'source':r['source']})
  index.setdefault(scope,{}).setdefault(r['collection'],{}).setdefault(str(r['location'].get('pk',r['id'])),{}).setdefault(r['field'],[]).append({'key':r['key'],'source':r['source']})
 for scope in en:
  write(STORY/(scope+'.en-US.json'),en[scope]);write(STORY/(scope+'.zh-CN.json'),zh.get(scope,{}))
 write(STORY/'index.json',index)
 write(STORY/'untranslated.json',missing)
 report={'date':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'entries':len(cat['records']),'translated':sum(map(len,zh.values())),'missing':len(missing),'reviewStatus':'Translation availability only; full-field and terminology review evidence is in reviews/final-field-audit.json.','scenarios':[]}
 for scenario in cat['scenarios']:
  scope=scenario['scope'];entries=len(en[scope]);count=len(zh.get(scope,{}))
  report['scenarios'].append({**scenario,'entries':entries,'translated':count,'coverage':round(count/entries*100,2) if entries else 100})
 write(STORY/'coverage.json',report)
 print('Package entries',report['translated'],'/',report['entries'],'untranslated',len(missing),flush=True)
 if missing:raise SystemExit('Incomplete package: inspect localization/stories/untranslated.json')
if __name__=='__main__':main()
