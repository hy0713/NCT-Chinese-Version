"""Maintenance: preserve optional upstream theme resources locally when reachable.
Use HTTPS_PROXY if a proxy is needed. Runtime never needs this script or a proxy.
"""
from pathlib import Path
import urllib.request, json, re, hashlib, concurrent.futures, os
root=Path(__file__).resolve().parents[1]
dest=root/'static/vendor/theme-assets';dest.mkdir(exist_ok=True)
assets=json.loads((root/'localization/assets.json').read_text())
urls=set(re.findall(r'"(https://[^"\s]+)"',(root/'static/js/indexCode.js').read_text(encoding='utf8')[:(root/'static/js/indexCode.js').read_text(encoding='utf8').index('nct_stuff.quotes =')]))
urls={u for u in urls if not u.endswith('.mp3')}
urls.add('https://commons.wikimedia.org/wiki/Special:FilePath/Representative%20William%20E.%20Miller.png')
def fetch(url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'NCT-local-study/1.0 (personal offline assets)'})
  response=urllib.request.urlopen(req,timeout=18);data=response.read()
  if data.startswith(b'\x89PNG'):ext='.png'
  elif data.startswith(b'\xff\xd8'):ext='.jpg'
  elif data.startswith(b'GIF8'):ext='.gif'
  else:raise ValueError('Response is not a supported image')
  name=hashlib.sha256(url.encode()).hexdigest()[:14]+ext
  (dest/name).write_bytes(data)
  return {'source':url,'path':'/static/vendor/theme-assets/'+name,'sha256':hashlib.sha256(data).hexdigest(),'status':'cached'}
 except Exception as error:
  return {'source':url,'status':'unavailable','reason':str(error)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 result=list(pool.map(fetch,sorted(urls)))
for item in result:
 print(item['status'],item['source'],flush=True)
 if item['status']=='cached':assets[item['source']]=item['path']
 else:
  # Keep the original theme palette with a shipped background/banner as fallback.
  assets[item['source']]='/static/images/banner_1.png' if ('banner' in item['source'] or '/omor' in item['source'] or '/aus_ban' in item['source'] or 'lXxBoP4' in item['source']) else '/static/images/black.jpg'
portrait=next((x for x in result if 'Representative%20William' in x['source']),None)
if portrait and portrait['status']=='cached':assets['https://i.imgur.com/r3llYzE.png']=portrait['path']
(root/'localization/assets.json').write_text(json.dumps(assets,indent=2),encoding='utf8')
(dest/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
