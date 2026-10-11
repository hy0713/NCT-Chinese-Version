from pathlib import Path
import json, urllib.request, concurrent.futures, hashlib
root=Path(__file__).resolve().parents[1]
urls=set()
for name in ['candidate.json','election.json']:
 for item in json.loads((root/'static/json'/name).read_text(encoding='utf8')):
  for key in ['image_url','advisor_url']:
   value=item['fields'].get(key) or ''
   if value.startswith('https://'): urls.add(value)
def download(url):
 try:
  data=urllib.request.urlopen(url,timeout=18).read()
  if not data.startswith(b'\x89PNG'): raise ValueError('Not a PNG: '+url)
  name=url.rsplit('/',1)[1]; dest=root/'static/vendor/native-images'/name; dest.parent.mkdir(exist_ok=True)
  dest.write_bytes(data)
  return {'source':url,'path':'/static/vendor/native-images/'+name,'sha256':hashlib.sha256(data).hexdigest(),'status':'cached'}
 except Exception as error:return {'source':url,'status':'unavailable','reason':str(error)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: result=list(pool.map(download,urls))
assets=json.loads((root/'localization/assets.json').read_text())
for item in result:
 print(item['status'],item['source'],flush=True)
 if item['status']=='cached': assets[item['source']]=item['path']
(root/'localization/assets.json').write_text(json.dumps(assets,indent=2),encoding='utf8')
(root/'static/vendor/native-images/manifest.json').write_text(json.dumps(result,indent=2),encoding='utf8')
