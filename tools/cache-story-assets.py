"""Cache optional native-ending media. Unreachable upstream files get recorded
local fallbacks. Neither source URLs nor game data are rewritten."""
from pathlib import Path
import json,re,urllib.request,hashlib,concurrent.futures
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'static/vendor/story-assets';OUT.mkdir(exist_ok=True)
cat=json.loads((ROOT/'localization/stories/catalogue.json').read_text(encoding='utf-8'))
assets=json.loads((ROOT/'localization/assets.json').read_text(encoding='utf-8'))
manifestPath=OUT/'manifest.json'
previous=json.loads(manifestPath.read_text(encoding='utf-8')) if manifestPath.exists() else []
urls={u for s in cat['scenarios'] for u in re.findall(r'https?[^\s\x22\x27<>\\]+',(ROOT/s['file']).read_text(encoding='utf-8')) if u not in assets}
def fetch(url):
 try:
  opener=urllib.request.build_opener(urllib.request.ProxyHandler())
  response=opener.open(urllib.request.Request(url,headers={'User-Agent':'NCT personal offline study'}),timeout=25)
  data=response.read(20_000_001)
  if len(data)>20_000_000:raise ValueError('Optional media exceeds 20 MB limit')
  if data.startswith(b'\x89PNG'):ext='.png'
  elif data.startswith(b'\xff\xd8'):ext='.jpg'
  elif data.startswith(b'GIF8'):ext='.gif'
  elif data.startswith(b'ID3') or data[:2] in (b'\xff\xfb',b'\xff\xf3',b'\xff\xf2'):ext='.mp3'
  elif data[4:8]==b'ftyp':ext='.mp4'
  else:raise ValueError('Response is not supported native media')
  name=hashlib.sha256(url.encode()).hexdigest()[:14]+ext;(OUT/name).write_bytes(data)
  return {'source':url,'path':'/static/vendor/story-assets/'+name,'status':'cached','sha256':hashlib.sha256(data).hexdigest()}
 except Exception as e:
  fallback='/static/vendor/soundtracks/unavailable.wav' if '.mp3' in url else '/static/images/black.jpg' if ('cloudfront' in url or 'onedrive' in url) else '/static/images/richard-nixon-1968.jpg'
  return {'source':url,'path':fallback,'status':'unavailable-local-fallback','reason':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(fetch,sorted(urls)))
for r in result:assets[r['source']]=r['path'];print(r['status'],r['source'],flush=True)
(ROOT/'localization/assets.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
merged={r['source']:r for r in previous}
merged.update({r['source']:r for r in result})
manifestPath.write_text(json.dumps(list(merged.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
