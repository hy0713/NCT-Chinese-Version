"""Recover only contextual punctuation in five fully reviewed Chinese fields."""
import json
from pathlib import Path
base=Path(__file__).resolve().parents[1]/'localization/reviews'
edits={
 '2012-a':[(5,'��完美��','“完美”'),(6,'��突发新闻：罗姆尼狂热席卷美国��','“突发新闻：罗姆尼狂热席卷美国”'),(6,'让底特律破产吧��','让底特律破产吧”'),(7,'你��输掉','你输掉')],
 '2012-d':[(50,'��裙带资本主义��','“裙带资本主义”')],
 '2012-f':[(7,'��特赦��','“特赦”')]
}
for name,rows in edits.items():
 p=base/(name+'-revised.txt');lines=p.read_text(encoding='utf-8').splitlines()
 for i,old,new in rows:
  assert old in lines[i] or new in lines[i]
  lines[i]=lines[i].replace(old,new)
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
 m=base/(name+'-metadata.json');data=json.loads(m.read_text(encoding='utf-8'))
 for entry in data['sourceExceptions']:
  if entry['index'] in [r[0] for r in rows]:
   entry['reason']='Corrupted original punctuation interpreted from sentence context and restored in Chinese only. English bytes, HTML, placeholders and numerical content untouched; no missing prose invented.'
 m.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
