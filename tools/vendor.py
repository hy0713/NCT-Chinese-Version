"""Fetch the exact upstream browser libraries and their license notices."""
from pathlib import Path
import urllib.request, json, re, hashlib
root = Path(__file__).resolve().parents[1]
dest = root / 'static/vendor'
dest.mkdir(exist_ok=True)
opener = urllib.request.build_opener()
items = {
 'jquery-3.7.1.min.js':'https://code.jquery.com/jquery-3.7.1.min.js',
 'jquery-ui-1.14.1.min.js':'https://code.jquery.com/ui/1.14.1/jquery-ui.min.js',
 'jquery-ui.css':'https://code.jquery.com/ui/1.14.1/themes/base/jquery-ui.css',
 'jquery.blockUI.js':'https://malsup.github.io/jquery.blockUI.js',
 'LICENSE.jquery.txt':'https://raw.githubusercontent.com/jquery/jquery/3.7.1/LICENSE.txt',
 'LICENSE.jquery-ui.txt':'https://raw.githubusercontent.com/jquery/jquery-ui/1.14.1/LICENSE.txt',
}
manifest=[]
def download(name,url):
 data=opener.open(url,timeout=40).read(); p=dest/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data)
 manifest.append({'file':name,'url':url,'sha256':hashlib.sha256(data).hexdigest()})
for name,url in items.items():
 download(name,url)
# BlockUI ships its licensing URL and author notice in the source header.
(dest/'LICENSE.blockUI.txt').write_text('jQuery BlockUI Plugin, copyright M. Alsup. Dual MIT/GPL license.\nOriginal source: https://malsup.github.io/jquery.blockUI.js\nLicense notice: https://jquery.malsup.com/license.html\nThe unmodified source header is preserved in jquery.blockUI.js.\n',encoding='utf8')
for image in set(re.findall(r'url\(["\']?(images/[^)"\']+)',(dest/'jquery-ui.css').read_text())):
 download(image,'https://code.jquery.com/ui/1.14.1/themes/base/'+image)
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('Vendored',len(manifest),'files')
