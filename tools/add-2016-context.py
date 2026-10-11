"""Primary-source notes for full-field 2016 reviews; original numbers intact."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/2016-{p}-source-snapshot.json') for p in 'abcdefghi'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'2016.'+id,'title':title,'category':'历史事件／政治叙事',
        'contains':list(dict.fromkeys(parts[p][i]['source'] for p,ids in bindings for i in ids)),
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('pulse','奥兰多枪击：受害者与枪手分开计数',[('a',[30,53,54,55,56]),('f',[0,1,2]),('g',[19,22])],
    ['联邦调查局记录，2016年6月12日奥兰多Pulse夜总会袭击造成49名受害者死亡；警察随后击毙枪手。原作的50人与49名遇害者并不是同一种计数口径。',
     '正文保留50，不改原始数字。调查后认定为恐怖袭击，不表示事件初期每种动机猜测都已获确认；各个回答对拥枪权、宗教与LGBT群体的立场差别均保留。'],
    [('联邦调查局：Pulse夜总会枪击案历史记录','https://www.fbi.gov/history/cases-and-criminals/pulse-nightclub-shooting')])
add('nice','尼斯袭击：当时消息与事后统计',[('a',[34]),('b',[7,8,9]),('f',[13,14,15])],
    ['法国国家警察的纪念资料记载，2016年7月14日尼斯恐怖袭击造成86人死亡，400余人受伤。',
     '游戏写近100人，是原作概括，不是此处重新核定的确切死亡人数。正文保留；将事后确认统计与事发当天不断变化的消息区分，也不擅自推定每段候选人台词都是真实逐字引文。'],
    [('法国国家警察：尼斯袭击十周年纪念，2026年7月17日','https://www.police-nationale.interieur.gouv.fr/actualite/10-ans-de-lattentat-de-nice')])
add('hack-allegations','泄密归因：竞选话术与正式指控',[('b',[54,55,58]),('c',[54]),('g',[1,4])],
    ['联邦调查局公开资料记载，2018年7月13日大陪审团起诉12名俄罗斯军事情报人员，涉及2016年非法进入相关电脑系统、盗取材料并安排公开等指控。起诉是正式法律指控，不等同于已经定罪。',
     '原作把内部举报者和一名遭杀害的人联系起来，是角色提出的猜测，不是旁注证实的调查结论。此处不把“有人这样说”当成证据，也不把2018年的材料倒写成角色在2016年已经知道的事实。'],
    [('联邦调查局：2016年选举干预案起诉与通缉说明','https://www.fbi.gov/wanted/cyber/russian-interference-in-2016-u-s-elections/')])
add('university-civil','特朗普大学：民事和解不是刑事定罪',[('a',[38]),('b',[4,6]),('c',[25])],
    ['第九巡回上诉法院2018年判词回顾，相关案件于2016年12月19日达成和解，向集体诉讼成员支付2100万美元，另向纽约州司法部长支付400万美元；被告没有承认不当行为。',
     '因此，不能把和解翻译成刑事定罪，也不能把没有承认不当行为说成法院认定一切行为合法。正文保留候选人对政治动机及案件轻重的辩解；未据这份事后判词核准题干所称纽约听证及最初开庭日期。'],
    [('GovInfo：Simpson诉特朗普大学案上诉判词，第9页','https://www.govinfo.gov/content/pkg/USCOURTS-ca9-17-55635/pdf/USCOURTS-ca9-17-55635-0.pdf')])
add('email-no-charges','严厉批评、刑事起诉与后来发现邮件',[('a',[29,43]),('e',[41,50]),('f',[55,56])],
    ['司法部长林奇2016年7月6日声明，接受调查人员与检察官一致建议，结束调查，不对调查范围内任何人提起刑事指控。对处理邮件方式的批评，并不等于正式刑事起诉。',
     '这一公告只说明七月的决定，不能单凭它核准十月新邮件的内容，也不能把不予起诉泛化成所有政治争议都已消失。候选人的道歉、辩解与攻击按原作保留。'],
    [('美国司法部：2016年7月6日林奇声明','https://www.justice.gov/archives/opa/pr/statement-attorney-general-loretta-e-lynch-regarding-state-department-email-investigation')])
path=ROOT/'localization/annotations/notes.zh-CN.json'
data=read(path);byid={n['id']:n for n in data['notes']};byid.update({n['id']:n for n in notes})
data['notes']=list(byid.values());data['checkedAt']='2026-10-10'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched 2016 notes')
