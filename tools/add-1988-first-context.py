"""Initial researched 1988 annotations, bound to immutable complete sources."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/1988-{p}-source-snapshot.json') for p in 'ab'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'1988.'+id,'title':title,'category':'历史制度／政治典故',
        'contains':list(dict.fromkeys(parts[p][i]['source'] for p,ids in bindings for i in ids)),
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('pledge','效忠誓词：反对强制，不等于反对国旗',
    [('a',[41,73,74])],
    ['巴内特案1943年保护学生不被强迫敬旗和宣读誓词。杜卡基斯任州长时另向州最高法院咨询1977年法案，要求每位教师每天带领班级宣读。法院多数意见认为侵犯教师的第一修正案权利，明确把巴内特理由延伸到教师；不同意见对法案是否构成强制有不同解释。',
     '所以这不是宣布国旗违法，也不是禁止自愿宣读。原作的攻击选项把法律争论用作爱国形象争论，译文保留政治立场，但不把候选人攻击认证为法院结论。'],
    [('马萨诸塞州最高法院1977年咨询意见：372 Mass.874原文转载','https://law.justia.com/cases/massachusetts/supreme-court/volumes/372/372mass874.html'),
     ('美国联邦法院：第一修正案与不敬旗的自由','https://www.uscourts.gov/about-federal-courts/educational-resources/about-educational-outreach/activity-resources/what-does-free-speech-mean')])
add('kinder-taxes','更加仁厚温和与读我的唇：真实口号及反常选项',
    [('a',[44,54,55]),('b',[19,20])],
    ['布什在1988年8月18日接受提名演说中希望国家更加仁厚温和，并许诺不加新税；“读我的唇”是强调自己绝不加税的说法。',
     '游戏另给出“对手会加税，我也会”的反常选项，不能因为与著名承诺相反就擅自改成不加税。保留自承加税、进一步减税和不排除加税三种不同立场；未来票数与税收分支是模拟，不是演说逐字史料。'],
    [('布什1988年接受共和党总统提名演说全文','https://www.presidency.ucsb.edu/documents/address-accepting-the-presidential-nomination-the-republican-national-convention-new')])
add('invalid','病人嘲讽：里根的话不是医学诊断',
    [('a',[49]),('b',[9,10,64])],
    ['1988年8月3日记者问杜卡基斯是否应公开医疗记录，并提到精神科诊治传闻，里根用invalid作嘲讽性回答。这里译为病人，不是无效的人；也不能据总统这句话确认候选人有精神疾病。',
     '实际场合是国防授权法否决后的记者问答，原问题概括成演说，正文保留原作叙述。游戏可以选择与这番话切割；顾问所说华盛顿今日风波，Beltway指首都政界，不是高速公路交通事故。'],
    [('里根1988年8月3日记者问答原文','https://www.presidency.ucsb.edu/documents/remarks-the-veto-the-national-defense-authorization-act-fiscal-year-1989-and-question-and')])
path=ROOT/'localization/annotations/notes.zh-CN.json';d=read(path)
byid={n['id']:n for n in d['notes']};byid.update({n['id']:n for n in notes})
d['notes']=list(byid.values());d['checkedAt']='2026-10-09'
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'initial 1988 notes')
