"""Additional 1988 notes from actually read primary speeches and court history."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
c=read(ROOT/'localization/reviews/1988-c-source-snapshot.json')
a=read(ROOT/'localization/reviews/1988-a-source-snapshot.json')
dpart=read(ROOT/'localization/reviews/1988-d-source-snapshot.json')
notes=[]
def add(id,title,indices,body,sources):
    notes.append({'id':'1988.'+id,'title':title,'category':'历史制度／政治典故','contains':[c[i]['source'] for i in indices],
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('inf','中导条约：消除一类导弹，不是全面核裁军',[32,46,47],
    ['里根与戈尔巴乔夫于1987年12月8日签署《中程核力量条约》。里根在签署讲话中说明将销毁有关陆基中程导弹，强调现场检查及“信任，但要核查”。1988年6月1日在莫斯科交换批准书后生效。',
     '这里的支持选项赞许美苏削减军备的进展；并不意味着所有核武器已经销毁，也不意味着游戏里支持的其他武器项目因此自动取消。'],
    [('里根图书馆：1987年12月8日中导条约签署讲话','https://www.reaganlibrary.gov/archives/speech/remarks-signing-intermediate-range-nuclear-forces-treaty'),
     ('里根图书馆：1988年6月10日致参议院生效说明','https://www.reaganlibrary.gov/archives/speech/message-senate-soviet-united-states-intermediate-range-nuclear-forces-treaty')])
add('noriega-defense','诺列加与七届政府：竞选辩护的出处',[55,56,57,58,64],
    ['1988年9月25日首场总统辩论中，杜卡基斯批评美国与诺列加的关系，布什则说七届政府都与他打过交道，并以里根—布什政府提出起诉作为辩护。剧本选项沿用了这套论辩。',
     '辩论记录能证明布什这样说过，不能据此证明美国此前毫不知情，或确认原作所写每个年代细节。认错、否认有何可说和以多届政府为自己辩护，是不同的政治选择；中文保留这些区别。'],
    [('米勒中心：1988年9月25日总统辩论原文','https://millercenter.org/the-presidency/presidential-speeches/september-25-1988-debate-michael-dukakis')])
add('classroom-prayer','课堂祈祷：学校主持与个人宗教活动的区别',[54,60,62],
    ['1962年恩格尔诉维塔莱案针对公立学校主持的祈祷。法院多数意见认为，即使不限定教派、允许学生退出，也不能消除政府介入宗教的问题。',
     '因此，选项之间的争论在于地方学校是否组织日常祈祷，不能把反对学校带领祈祷译成禁止个人信教。旁注讲的是当时的判例语境；正文仍保留支持地方决定和反对校方主持两种立场。'],
    [('美国联邦法院：恩格尔诉维塔莱案事实与判决摘要','https://www.uscourts.gov/about-federal-courts/educational-resources/educational-activities/first-amendment-activities/engel-v-vitale/facts-and-case-summary-engel-v-vitale')])
add('north-american-trade','三国自由贸易区：1988年仍是政策设想',[31,34,35,40,41,42,43,44,45,52],
    ['本题问的是是否支持涵盖墨西哥、美国和加拿大的自由贸易区。不能在1988年的问题里把它直接写成已经生效的《北美自由贸易协定》。',
     '白宫1993年9月的背景简报明确列出协定的生效日为1994年1月1日。剧本中对就业、产业转移和劳动保障的判断是竞选政策及顾问评价，不能用后来的实际经济结果改写选项立场。'],
    [('美国国家档案馆：1993年9月14日北美自由贸易协定白宫简报','https://clintonwhitehouse6.archives.gov/1993/09/1993-09-14-background-briefing-nafta.html')])
add('drug-czar','禁毒主管：沙皇比喻及机构时点',[38],
    ['Drug Czar用“沙皇”比喻集中协调禁毒政策的负责人，并非君主头衔；正文译为国家禁毒主管。',
     '里根于1988年11月18日签署《反毒品滥用法》，在大选之后。里根基金会的当日日记页面概述该法建立了内阁级禁毒主管职位。剧本把加强主管权力放在竞选选项里，仍按原作保留；不要由此误以为后来设立的职位在竞选时已经按相同制度运作。'],
    [('美国总统项目：1988年11月18日法案签署讲话','https://www.presidency.ucsb.edu/documents/remarks-signing-the-anti-drug-abuse-act-1988'),
     ('里根基金会：1988年11月18日日记及事件摘要','https://www.reaganfoundation.org/ronald-reagan/white-house-diaries/on-this-day/diary-day-1118/diary-entry-11181988')])
add('silver-foot','含着银脚出生：富家子与失言的双关',[],
    ['英语“含着银勺出生”指家境优裕；“把脚塞进嘴里”形容说错话、失言。把银勺换成银脚，同时讥讽布什的出身和讲话表现。正文保留奇怪的银脚形象，借旁注解释笑点。',
     '安·理查兹在1988年民主党全国代表大会的演说中使用了这句话；2007年国会纪念她的记录也明确重述此事。游戏让杜卡基斯选用这句攻击话，不意味着这句话最初由他提出。'],
    [('美国国会记录：纪念安·理查兹，2007年','https://www.govinfo.gov/content/pkg/CRECB-2007-pt4/html/CRECB-2007-pt4-Pg4710.htm')])
notes[-1]['contains']=[dpart[11]['source']]
add('dukakis-birth','希腊移民之子：原作一处人物经历错误',[],
    ['东北大学保存的杜卡基斯总统竞选档案说明，他于1933年11月3日出生在马萨诸塞州布鲁克莱恩，父母为希腊移民。本人不是出生在希腊后移居美国的移民。',
     '原作一处选项却称本人为希腊移民。英文和正文沿用原作说法，以此旁注指出错误；其他正确写为移民之子的段落也保持其原有意义。不能从错误选项推断他不具备总统参选资格。'],
    [('东北大学档案：杜卡基斯总统竞选档案人物历史说明','https://archivesspace.library.northeastern.edu/repositories/2/resources/798')])
notes[-1]['contains']=[dpart[41]['source'],c[70]['source']]
add('sdi','星球大战：战略防御倡议的绰号',[],
    ['战略防御倡议试图研究拦截战略弹道导弹的防御技术。“星球大战”是该计划的流行绰号，不能理解成电影项目或当时已经部署成功的太空武器系统。',
     '里根在1983年3月23日讲话中提出长期研发方向，也承认技术艰巨、可能需要数十年，并要求继续维持核威慑。题目中的支持或反对仍是1988年的政策选择，不把未来技术成败写进候选人的回答。'],
    [('里根图书馆：1983年3月23日国防与国家安全讲话','https://www.reaganlibrary.gov/archives/speech/address-nation-defense-and-national-security')])
notes[-1]['contains']=[a[50]['source']]
path=ROOT/'localization/annotations/notes.zh-CN.json';d=read(path)
byid={n['id']:n for n in d['notes']};byid.update({n['id']:n for n in notes})
d['notes']=list(byid.values());d['checkedAt']='2026-10-09'
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'1988 treaty and policy notes')
