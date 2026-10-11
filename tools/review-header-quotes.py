"""Reviewed Chinese wording of all 48 active header slots (47 distinct keys).
This is a wording review. Only source-linked annotations certify researched
context; unannotated quotations are not claimed to have verified attribution.
"""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'tools/quotes-zh.json';zh=json.loads(path.read_text(encoding='utf-8'))
array=re.search(r'nct_stuff\.quotes = \[(.*?)\]\s*\n',(ROOT/'static/js/indexCode.js').read_text(encoding='utf-8'),re.S).group(1)
en=[a or b for a,b in re.findall(r'`([^`]*)`|\'([^\']*)\'',array)]
assert len(en)==len(zh)==48
changes={
1:'“约翰逊，一路支持到底！”',
4:'“骗我一次，丢脸的是……是你。再骗我……不能再上当了。”——乔治·W.·布什',
8:'“我不会出于政治目的，拿对手的年轻和经验不足做文章。”——罗纳德·里根',
11:'“我的失误在于判断，并非蓄意为之。”——尤利西斯·S.·格兰特',
12:'“总统做了，就说明这事不违法。”——理查德·尼克松',
14:'“为捍卫自由而采取极端立场，并非恶行。”——巴里·戈德华特',
18:'“我有满满几文件夹的女性！”——米特·罗姆尼',
20:'“听清楚了：不增新税。”——乔治·H.·W.·布什',
25:'“自由离消亡，永远只有一代人的距离。”——罗纳德·里根',
28:'“去他妈的，我们不去！”',
30:'“投给那个贪腐的家伙，这很重要！”',
35:'“让宝可梦‘GO’，去投票！”——希拉里·克林顿',
41:'“这次先投塔夫脱，布赖恩哪次都能投！”',
42:'“投给那个贪腐的家伙，这很重要！”',
43:'“布莱恩，布莱恩，詹姆斯·G.·布莱恩，缅因州来的举国大骗子！”',
45:'“分裂之家，不能长存。”——亚伯拉罕·林肯'
}
for i,value in changes.items():zh[i]=value
path.write_text(json.dumps(zh,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report={'checkedAt':'2026-10-08','slotsReviewed':48,'distinctKeys':47,'revisedSlots':sorted(changes),'scope':'Chinese wording reviewed; historical attribution only where a source-linked note is provided.','records':[{'index':i,'key':'quote.'+re.sub(r'[^a-z0-9]+','_',source.lower()).strip('_'),'source':source,'sha256':hashlib.sha256(source.encode()).hexdigest(),'zh':zh[i]} for i,source in enumerate(en)]}
(ROOT/'localization/annotations/header-editorial-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Reviewed 48 header slots; revised 16 slot wordings; no changes to English quote array or RNG.')
