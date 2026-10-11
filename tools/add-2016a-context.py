"""Offline notes for hand-read complete fields in the March 2016 scenario."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/2016a-{p}-source-snapshot.json') for p in 'abcdefg'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'2016a.'+id,'title':title,'category':'历史制度／政治典故',
        'contains':list(dict.fromkeys(parts[p][i]['source'] for p,ids in bindings for i in ids)),
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('garland','加兰：提名并不等于就任',[('a',[30]),('b',[19,20])],
    ['奥巴马在2016年3月16日宣布提名梅里克·加兰接替斯卡利亚。白宫保存的当天讲话明确使用提名人的身份；总统提名与参议院确认，是不同的程序。',
     '三月版中的争论应按当时提名仍待处理的视角理解。正文不倒灌后来的人事变化，也不把候选人关于确认或阻挠的政治立场改写成加兰已经成为最高法院大法官。'],
    [('奥巴马白宫档案：2016年3月16日提名讲话','https://obamawhitehouse.archives.gov/the-press-office/2016/03/16/remarks-president-announcing-judge-merrick-garland-his-nominee-supreme')])
add('marriage','同性婚姻判决：许可与跨州承认',[('a',[27]),('b',[16,17,18])],
    ['2015年6月26日奥伯格费尔诉霍奇斯案判决要求各州准许同性伴侣结婚，并承认在其他州依法缔结的同性婚姻，依据是第十四修正案的正当程序与平等保护。',
     '判决不是要求所有宗教团体举行婚礼，也不是取消一切婚姻规则。游戏保留支持、反对及诉诸州权的不同政治立场；旁注解释实际判决范围，不改变选项效果。'],
    [('康奈尔转载：奥伯格费尔案判词与判决摘要','https://www.law.cornell.edu/supremecourt/text/14-556')])
add('iran-assets','伊朗解冻资产不是美国赠款',[('c',[53]),('d',[4,5,6])],
    ['美国财政部2015年证词估计，伊朗央行全球外汇资产总额为1000亿至1250亿美元，解除制裁后可用流动资产为略多于500亿美元，其余许多资产无法迅速变现。',
     '解冻该国原有资产，不等于美国财政向它赠送同等金额。正文保留原作1500亿美元及候选人的攻击、辩护说法；上述不同口径不能混成一笔已经核定的美国援助。'],
    [('美国财政部：亚当·舒宾2015年参议院书面证词','https://home.treasury.gov/news/press-releases/jl0144')])
add('bully-pulpit','bully pulpit：总统的公共发声平台',[('a',[4])],
    ['国家公园管理局的西奥多·罗斯福历史教材，说明他把总统职位视为可以向公众倡议政策的强大发声平台。这里的bully不是在说欺凌，pulpit也不要求理解为真的教堂讲坛。',
     '结局中的意思是总统拥有影响公众议程的优势。拥有这种优势，不等于国会必然赞同或总统能单方面通过法案。'],
    [('国家公园管理局：罗斯福总统任期与公共发声平台历史教材','https://www.nps.gov/articles/theodore-roosevelt-inaugural-site-birthplace-of-the-modern-presidency-teaching-with-historic-places.htm')])
add('email-hypothetical','三月版的起诉情节是架空分支',[('d',[38]),('e',[27]),('f',[23,24]),('g',[2,3])],
    ['本剧本按2016年3月视角设想调查可能走向起诉，不能把游戏中的这一事件当成实际发生的法律结论。',
     '现实中，司法部长洛雷塔·林奇于2016年7月6日表示，接受调查人员与检察官一致建议，结束调查，并不对该调查范围内任何人提起刑事指控。这份后来公告只用于区分历史与架空情节，不写进三月正文，也不改游戏条件。'],
    [('美国司法部：林奇2016年7月6日关于邮件调查的声明','https://www.justice.gov/archives/opa/pr/statement-attorney-general-loretta-e-lynch-regarding-state-department-email-investigation')])
add('college-unit','大学方案：原作350的单位疑点',[('b',[39])],
    ['《时代》2015年8月10日报道，克林顿拟提出的大学负担能力方案，竞选团队估计十年成本约3500亿美元。',
     '原作只写350而没有十亿这一数量单位；正文保留，不擅自改数字。报道不是已通过的拨款法，官方完整方案本次未成功取得。'],
    [('时代：2015年8月10日大学方案报道，非官方方案原文','https://time.com/3990196/clinton-college-debt-affordable-plan/')])
path=ROOT/'localization/annotations/notes.zh-CN.json'
data=read(path); byid={n['id']:n for n in data['notes']};byid.update({n['id']:n for n in notes})
data['notes']=list(byid.values());data['checkedAt']='2026-10-10'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched March 2016 notes')
