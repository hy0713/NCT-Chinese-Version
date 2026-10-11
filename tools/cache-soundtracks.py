"""Cache upstream optional music. Use HTTPS_PROXY only during maintenance."""
from pathlib import Path
import urllib.request,json,re,hashlib,concurrent.futures
root=Path(__file__).resolve().parents[1];dest=root/'static/vendor/soundtracks';dest.mkdir(exist_ok=True)
assets=json.loads((root/'localization/assets.json').read_text())
urls=set(re.findall(r'"(https://[^"\s]+\.mp3)"',(root/'static/js/campaign_trail_other.js').read_text(encoding='utf8')))
def fetch(url):
 try:
  # GitHub raw endpoint avoids the extra HTML redirect.
  request_url=url.replace('https://github.com/newcampaigntrail/resources/raw/main/','https://raw.githubusercontent.com/newcampaigntrail/resources/main/')
  data=urllib.request.urlopen(request_url,timeout=25).read()
  if not(data.startswith(b'ID3') or data.startswith(b'\xff')):raise ValueError('Not MP3 data')
  name=hashlib.sha256(url.encode()).hexdigest()[:14]+'.mp3';(dest/name).write_bytes(data)
  return {'source':url,'path':'/static/vendor/soundtracks/'+name,'status':'cached','sha256':hashlib.sha256(data).hexdigest()}
 except Exception as error:return {'source':url,'status':'unavailable','reason':str(error)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:result=list(pool.map(fetch,sorted(urls)))
for item in result:
 print(item['status'],item['source'],flush=True)
 # Optional missing tracks use a bundled silent clip so the game remains offline.
 assets[item['source']]=item.get('path','/static/vendor/soundtracks/unavailable.wav')
import wave
with wave.open(str(dest/'unavailable.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(8000);f.writeframes(b'\0\0'*8000)
(root/'localization/assets.json').write_text(json.dumps(assets,indent=2),encoding='utf8')
(dest/'manifest.json').write_text(json.dumps(result,indent=2),encoding='utf8')
