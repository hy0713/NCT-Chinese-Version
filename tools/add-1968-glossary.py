"""Editorial terminology only; no runtime source replacement."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'localization/reviews/glossary-context.zh-CN.json'
d=json.loads(p.read_text(encoding='utf-8'))
terms=[
 ('Jumbo (LBJ meme)','巨无霸；约翰逊的粗俗绰号','另一位政治人物／已认证的逐字史料','1968.jumbo'),
 ('Dump the Hump','甩掉汉弗莱','丢掉驼峰','1968.hump'),
 ('pointy-headed intellectuals','尖脑袋知识分子；脱离现实的精英的讥称','生理疾病','1968.pointy-heads'),
 ('Head Start','启蒙计划','大学提前录取','1968.head-start'),
 ('devolution (federal responsibilities)','权责下放给州政府','生物退化',''),
 ('judicial activism','司法能动主义／积极运用司法审查','法官参加街头抗议','1968.court-rights'),
 ('police riot (Chicago 1968)','警察制造的暴乱','警察平息暴乱','1968.chicago'),
 ('long, hot summer (1967)','1967年漫长炎热的夏季；城市骚乱的历史称呼','仅指天气／1968年金遇刺','1968.summer'),
 ('Kennedy Round','肯尼迪回合','肯尼迪1967年亲自主持会议','1968.kennedy-round'),
 ('mongrelize (racist rhetoric)','杂种化；保留种族主义侮辱语气','中性化成普通交流','1968.affirmative'),
 ('useful idiot (political insult)','有用的傻瓜；被政治势力利用者的讥称','无证认定列宁逐字发明',''),
 ('detente','缓和关系','完全撤销防务',''),
]
existing={x['en']:x for x in d['terms']}
existing.update({en:{'en':en,'zh':zh,'avoid':avoid,'noteId':note} for en,zh,avoid,note in terms})
d['terms']=list(existing.values());d['checkedAt']='2026-10-09'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Editorial context terms',len(d['terms']))
