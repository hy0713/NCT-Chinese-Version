"""Sourced notes bound to complete, hand-read immutable 2012 fields."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/2012-{p}-source-snapshot.json') for p in 'abcdefghi'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'2012.'+id,'title':title,'category':'历史制度／政治典故',
        'contains':list(dict.fromkeys(parts[p][i]['source'] for p,ids in bindings for i in ids)),
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('arizona','亚利桑那移民法：保留一条不等于全法获认可',[('a',[38]),('b',[4,5,6,7])],
    ['2012年6月25日的判决认定，SB1070的第3、5(C)、6条被联邦法排除；对执法过程中核查移民身份的第2(B)条，则认为在州法院解释及实际实施之前，不宜先行禁止。',
     '这不是确认所有实施方式都合宪。判词仍保留对拖延释放、种族及其他宪法问题提出挑战的可能。游戏题干作了简化，选项中反对种族筛查、强调联邦权限或支持严格执法的立场仍各自保留。'],
    [('康奈尔转载：亚利桑那诉美国案多数判词，2012年6月25日','https://www.law.cornell.edu/supremecourt/text/11-182')])
add('citizens-united','联合公民案：独立支出与直接捐款',[('a',[42]),('b',[40,41,42,43]),('d',[29,55])],
    ['联邦选举委员会2010年说明，判决撤销了禁止公司及工会以自身资金支付独立支出和竞选传播的限制，但广告的付款声明、披露要求，以及公司和工会直接向候选人捐款的禁令仍然存在。',
     '因此，不能把它概括成所有竞选资金均无限制。独立广告、候选人筹款和不同类型政治行动委员会须分别理解；题目关于修宪或自愿放弃广告的选择，仍按原作政治立场呈现。'],
    [('联邦选举委员会：2010年联合公民案实施声明','https://www.fec.gov/updates/commission-statement-on-citizens-united-v-fec/')])
add('aca','奥巴马医改：保费、自付额与强制投保',[('a',[41]),('c',[28,29,30,31,32,33,34,35]),('i',[0,1,2])],
    ['2010年公法111-148区分保费与费用分担，规定年度费用分担上限，并禁止既往病史排除；个人投保义务也有豁免，条款分阶段生效。原作“每个美国人”和“年度保费上限”的概括不等于完整法律条文。',
     '保费是持有保险的缴费，自付上限是接受保障范围内服务时分担费用的上限，并不包括保费。正文保留原词，不把两者悄悄互换，也不把支持公共医保选项译成全面废除私人保险。此说明不套用2026年的金额到2012年。'],
    [('GovInfo：平价医疗法案原始公法，第1201、1302及1501节','https://www.govinfo.gov/content/pkg/PLAW-111publ148/html/PLAW-111publ148.htm'),
     ('HealthCare.gov：自付上限术语定义，仅用于区别概念','https://www.healthcare.gov/glossary/out-of-pocket-maximum-limit/')])
add('social-security','2033年预测：储备耗尽不是开始支付',[('f',[36,37,38,39]),('i',[30,31])],
    ['社会保障署2012年公告预测，合并信托基金资产将在2033年耗尽，并明确记载：不含利息的收入在2010年已低于支出；2011年计入利息后的总收入仍高于支出。',
     '所以原作把2033年说成开始净支出的日期，混淆了年度收支与储备耗尽。即使储备耗尽，当时预测持续收入仍可支付约75%的预定待遇，不等于一分钱也不发。原作数字及支持、改革、反对各选项保留；100万亿美元断言的估值口径尚未独立确认。'],
    [('社会保障署：2012年4月23日信托基金年度公告','https://www.ssa.gov/news/en/press/releases/2012-04-23.html')])
add('fast-furious','速度与激情：放枪追踪的执法丑闻',[('d',[58]),('e',[30,31,32,33])],
    ['司法部监察长2012年报告说明，ATF为追查贩枪网络高层，推迟逮捕代购者和扣押枪支；这些枪后来出现在墨西哥及美国犯罪现场，其中包括边境执法人员布赖恩·特里遇害案的相关现场。',
     'gunwalking不是持枪散步，是放任可疑枪支转手的追踪手法；这里的Fast and Furious是执法行动名称。相关枪支在现场被发现，不自动证明某一支就是发射致命子弹的枪。正文“直接导致死亡”仍作为原作政治指控，不能扩大成已核定弹道结论。'],
    [('司法部监察长：2012年4月至9月半年度报告，行动调查摘要','https://oig.justice.gov/archives/semiannual/1211/report.htm')])
add('faith-speech','信仰演说的年份',[('h',[32,33,34]),('g',[53])],
    ['罗姆尼竞选团队保存的新闻稿记载，他在乔治·布什总统图书馆发表“美国的信仰”演说的日期是2007年12月6日，谈的是宗教自由。',
     '原作回答写2008年，正文保留这一年份，不改英文或游戏条件。2008是竞选周期，不能因此把2007年已经发表的演说挪到次年。也不把候选人的摩门教信仰当作不忠于美国的证据。'],
    [('美国总统研究项目：罗姆尼竞选团队2007年12月6日新闻稿','https://www.presidency.ucsb.edu/documents/romney-campaign-press-release-photo-release-the-faith-america-address')])
add('unemployment','近百年最高失业率：竞选攻击与数据',[('g',[11]),('c',[44])],
    ['劳工统计局年度表列出：1982年失业率9.7%，2010年9.6%，2012年8.1%。单就这些年度数据，便不能把奥巴马任内失业率称为近百年来最高。',
     '正文保留原作候选人的攻击台词，不把它当成译者确认的经济史结论。年度平均、单月峰值与就业人数不是同一指标；也不因旁注修改支持率或选项效果。'],
    [('劳工统计局：历年就业与失业年度表','https://www.bls.gov/cps/cpsaat01.htm')])
add('warren','沃伦与消费者金融保护局',[('e',[5,52,53,54])],
    ['2011年9月6日，理查德·科德雷在参议院作证时以消费者金融保护局局长提名人身份发言，并感谢伊丽莎白·沃伦将这个机构从构想变为现实。',
     '原作Consumer Financial Protection Board的机构名称不准，规范名称为Bureau，中文使用消费者金融保护局。“原本该由她任职”是一种政治评价，不意味着沃伦已经正式获提名、随后遭到否决；不能把筹建工作与正式局长任命混为一谈。'],
    [('消费者金融保护局：科德雷2011年9月6日提名听证证词','https://www.consumerfinance.gov/archive/newsroom/testimony-of-richard-cordray-before-the-committee-on-banking-housing-and-urban-affairs/')])
add('federal-unions','联邦雇员并非一律没有集体谈判权',[('h',[50,51])],
    ['美国法典第5编第7102条列明，符合该章规定的联邦雇员可以通过其选出的代表就雇用条件进行集体谈判；此条源自1978年立法。',
     '具体适用人员、可谈事项与限制另有规定，不能把联邦制度概括成完全没有集体谈判。游戏的候选人回答保留原作说法；谈判权不等于不受限制的罢工权，也不等于所有工资项目都可自由谈判。'],
    [('康奈尔转载：美国法典第5编第7102条及1978年来源注','https://www.law.cornell.edu/uscode/text/5/7102')])
add('ten-thousand','一万美元打赌：不要与赛马混为一事',[('g',[56]),('h',[27,28])],
    ['2011年12月10日共和党初选辩论中，罗姆尼就佩里对其医保立场的说法提出一万美元赌约；保存的逐字稿可见双方争论及赌约。',
     '这为大额打赌的竞选话题提供真实背景，但不是他在赛马上实际下过一万美元赌注的证据。题目混合了马匹开支与赌注，正文保留；不替候选人补写未经证实的赌博经历。'],
    [('美国总统研究项目：2011年12月10日得梅因共和党辩论逐字稿','https://www.presidency.ucsb.edu/documents/republican-candidates-debate-des-moines-iowa')])
add('pell','佩尔助学金：受助者、年份与分母',[('h',[40,52,53,54,55])],
    ['国会预算办公室2013年报告说明，佩尔助学金帮助低收入学生接受中学后的教育，包括大学、社区学院与职业培训；2011至2012学年约940万人获336亿美元。',
     '这不能直接认证题目关于2010年所有大学生60%及360亿美元的组合数字：学年、财政年度及统计分母不同。正文原数值保留，60%的具体依据尚待核。回答中的secondary education按原文译为中等教育，不擅自改成大学；这句话与助学金针对中学后教育的实际范围须区分。'],
    [('国会预算办公室：2013年佩尔助学金增长与政策选项报告','https://www.cbo.gov/publication/44448')])
path=ROOT/'localization/annotations/notes.zh-CN.json'
data=read(path);byid={n['id']:n for n in data['notes']};byid.update({n['id']:n for n in notes})
data['notes']=list(byid.values());data['checkedAt']='2026-10-09'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched 2012 notes')
