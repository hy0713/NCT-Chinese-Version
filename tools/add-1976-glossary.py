"""Record contextual editorial terms without replacing runtime game strings."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'localization/reviews/glossary-context.zh-CN.json'
d=json.loads(p.read_text(encoding='utf-8'))
terms=[
 ('rose garden strategy','玫瑰园战略；突出现任总统身份','园艺竞选政策','1976.rose-garden'),
 ('adultery in my heart','我在心里犯过奸淫；宗教自省','承认实际婚外情','1976.playboy'),
 ('draft evaders','逃避征兵者','与军中逃兵一律混称','1976.draft'),
 ('deserters','军中逃兵；擅离职守者','一切反战人士','1976.draft'),
 ('Humphrey-Hawkins (1976 proposal)','汉弗莱—霍金斯充分就业法案','1976年已生效的1978年法律','1976.humphrey-hawkins'),
 ('Scoop Jackson','斯库普·杰克逊；亨利·杰克逊的绰号','独家新闻杰克逊；安德鲁·杰克逊','1976.scoop'),
 ('Church Committee','彻奇委员会；情报活动调查委员会','教会委员会','1976.church-committee'),
 ('Scrooge','斯克鲁奇；吝啬冷酷的文学比喻','美国政治人物','1976.scrooge'),
 ('Clennon King','克伦农·金','马丁·路德·金','1976.church-race'),
 ('Bayh-Celler amendment','贝赫—塞勒修正案提议','已经生效的总统直选制度','1976.bayh-celler'),
 ('hardhat vote','建筑等行业工人选票','安全帽的投票',''),
 ('New South (Carter rhetoric)','新南方；摆脱旧有隔离政治的形象','当时已完全消除种族歧视',''),
]
existing={x['en']:x for x in d['terms']}
existing.update({en:{'en':en,'zh':zh,'avoid':avoid,'noteId':note} for en,zh,avoid,note in terms})
d['terms']=list(existing.values());d['checkedAt']='2026-10-09'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Editorial context terms',len(d['terms']))
