"""Generate an inert local movie when the upstream ending movie is unavailable.
Development-only ffmpeg helper; no dependency is required by the finished game.
The original onended callback remains unchanged.
"""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
exe=ROOT/'.tools/story-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
output=ROOT/'static/vendor/story-assets/unavailable.mp4'
subprocess.run([str(exe),'-y','-f','lavfi','-i','color=c=black:s=500x300:r=10:d=3','-an','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],check=True,capture_output=True)
manifestPath=ROOT/'static/vendor/story-assets/manifest.json';manifest=json.loads(manifestPath.read_text(encoding='utf-8'))
assetsPath=ROOT/'localization/assets.json';assets=json.loads(assetsPath.read_text(encoding='utf-8'))
for item in manifest:
 if 'onedrive.live.com' in item['source']:
  item.update(path='/static/vendor/story-assets/unavailable.mp4',fallback='Generated 3-second black video; original onended callback retained',fallbackSha256=hashlib.sha256(output.read_bytes()).hexdigest())
 elif item['status']=='unavailable-local-fallback' and '.mp3' not in item['source']:
  item['path']='/static/images/richard-nixon-1968.jpg' if 'nixonhell.gif' in item['source'] else '/static/images/black.jpg'
 assets[item['source']]=item['path']
for p,v in [(manifestPath,manifest),(assetsPath,assets)]:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Generated local fallback video:',output.stat().st_size,'bytes')
