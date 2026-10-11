"""Optional authoring step: researched 1896 notes, exact source bindings."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
rows=read(ROOT/'localization/reviews/1896-all-source-snapshot.json')
data=read(ROOT/'localization/annotations/notes.zh-CN.json');notes=[]
def add(id,title,indices,body,sources):
    notes.append({'id':id,'title':title,'category':'历史制度／政治修辞',
        'contains':[rows[i]['source'] for i in indices],'body':body,
        'sources':[{'title':t,'url':u} for t,u in sources]})
add('1896.silver-system','自由铸银、有限购银与金银比价',[0,14,67,68,69,70,75,105,106,107,128,129,147,148,281],
    ['自由铸银要求开放白银铸币，并取消相应数量限制；不是政府免费赠送银币。金银复本位同时以两种金属为本位。按16∶1的法定比价，指按重量一份黄金相当于十六份白银；不能把这个数字改成当时市场价格。',
     '《布兰德—艾利森法》采取有限购银与铸币，是不同于自由、无限制铸银的折中方案。游戏还提供按市场比价调整的选项，译文保留固定比价、浮动比价和有限购银之间的政策差别。'],
    [('美国参议院：艾利森与有限铸银的立法折中','https://www.senate.gov/art-artifacts/fine-art/paintings/32_00004_000.htm'),
     ('国会图书馆：1896年选举的数字史料','https://guides.loc.gov/presidential-election-1896/digital-collections')])
add('1896.front-porch','前廊竞选：候选人为何在家接待选民？',[16,45,46,127,220,355],
    ['麦金莱在俄亥俄州坎顿的家中接待各地代表团，发表准备好的演说；布赖恩则乘火车巡回演说。这是两种竞选组织方式的对照，不是麦金莱退出竞选。',
     '游戏人物认为候选人亲自拉票“有失身份”，反映一种竞选礼仪观念；不能据此说此前从来没有候选人巡回竞选。免费三明治是原作的具体叙述，此处不把每个来访者都得到三明治当作已经逐项证实的史实。'],
    [('国会图书馆：1896年总统选举及前廊演说','https://guides.loc.gov/chronicling-america-1896-presidential-election'),
     ('海斯总统图书馆与博物馆：麦金莱1896年前廊竞选','https://www.rbhayes.org/hayes/the-view-from-the-front-porch-william-mckinley-and-the-campaign-of-1896/')])
add('1896.bryan-nicknames','“伟大的平民”与“普拉特河的少年演说家”',[4,153,271],
    ['这些是布赖恩的政治绰号。“伟大的平民”强调他作为普通民众代言人的形象；“普拉特河的少年演说家”突出年轻与口才，并联系他的内布拉斯加背景。并非说他竞选时还是未成年少年。',
     '“普拉特河”是河名，不是柏拉图。游戏里听众发出嘘声，是在讽刺他的演说偏离支持者期待，译文保留这种挖苦。'],
    [('内布拉斯加州历史学会：布赖恩档案与政治绰号','https://history.nebraska.gov/collection_section/william-jennings-bryan-1860-1925-rg3198-am/'),
     ('国会图书馆：世纪之交的美国与布赖恩的演说形象','https://www.loc.gov/collections/early-films-of-new-york-1898-to-1906/articles-and-essays/america-at-the-turn-of-the-century-a-look-at-the-historical-context/')])
add('1896.wet-dry','Wet／Dry：反禁酒派与禁酒派',[10,32,83,84,85,138,139,140,141,250,358,362,395,404,405,406,416],
    ['禁酒政治中的wet通常指反禁酒或支持合法饮酒的一方，dry指支持禁酒的一方；不能直译成“湿的人”或“干的人”。节制饮酒、星期日限售与全面禁酒，也不是同一政策。',
     '1896年全国禁酒宪法修正案尚未通过。游戏中希望未来通过禁酒修正案，是政治主张；实际第十八修正案在1919年获批准，全国禁酒于1920年开始。'],
    [('国会图书馆：威尔逊档案中的禁酒争论与wet／dry称呼','https://www.loc.gov/collections/woodrow-wilson-papers/articles-and-essays/letters-from-ordinary-americans/prohibition/'),
     ('国会图书馆：全国禁酒开始的时间线','https://guides.loc.gov/this-month-in-business-history/january/prohibition')])
add('1896.pendleton-patronage','政党分赃制与官职酬庸',[40,119,356,359,360,363],
    ['政党分赃制指胜选后以官职报偿党内支持者，不是战场分赃。官职酬庸是分配职位的政治关系；也不意味着所有联邦职位都可由总统任意分给私人。',
     '1883年《彭德尔顿法》确立竞争考试等择优任用办法，但最初覆盖的职位有限，改革范围逐步扩大。因此游戏仍讨论酬庸官职，并不等于该法没有存在。'],
    [('美国国家档案馆：1883年《彭德尔顿法》原件与改革范围','https://www.archives.gov/milestone-documents/pendleton-act')])
add('1896.pullman-intervention','普尔曼罢工：邮件、禁令与联邦介入',[18,25,79,80,81,82,96,97,98,99,137,163,203,204,205],
    ['1894年普尔曼罢工及抵制普尔曼车厢，使铁路运输和邮政受到影响。法院禁令、州长与联邦政府的冲突、德布斯因违抗禁令被追究，属于相关但不同的问题。法院禁令不是工会自己发布的命令。',
     '原作把邮政车厢挂接安排归于联邦政府；国家公园管理局的叙述则特别记载铁路总经理协会鼓励挂接车厢，以利用邮件受阻争取干预。这里说明归责差别，保留原作问法，不据此认定当时每趟列车的安排。'],
    [('美国国家公园管理局：1894年罢工、铁路协会与联邦介入','https://home.nps.gov/pull/learn/historyculture/the-strike-of-1894.htm')])
add('1896.silver-repeal-date','《谢尔曼白银购买法》：原作1894年有误',[165,179,180,181],
    ['《谢尔曼白银购买法》属于1890年的货币立法，与同年的《谢尔曼反托拉斯法》不是同一部法律。支持铸银与反对企业垄断不能因名称相近而混为一谈。',
     '原问题把克利夫兰推动废法的年份写为1894年。参议院与众议院的官方历史均把废法争论放在1893年；正文保留原作的1894年，在旁注说明。此处所说的废法主要针对购银要求，不能简单概括为所有白银都从货币体系中消失。'],
    [('美国参议院：科罗拉多参议员与1893年废法争论','https://www.senate.gov/states/CO/timeline.shtml'),
     ('美国众议院历史：乔治·华盛顿·默里与1893年购银争论','https://history.house.gov/People/Detail/18709')])
add('1896.coxey-army','考克西“军队”：失业者进军华盛顿',[76,155,216,234,235,236,237],
    ['1894年，雅各布·考克西带领失业者赴华盛顿，要求通过公共工程创造工作。所谓“军队”是抗议队伍的政治称呼，不是联邦军队，也不是由将军指挥的军事单位。',
     '游戏对公共工程是否合宪、能否促进景气提供不同回答。支持公共工程、提高关税和扩大货币供给，是不同的政策路径，译文没有合并成同一种救济政策。'],
    [('国会图书馆：考克西军队与1894年失业者游行史料','https://blogs.loc.gov/teachers/2026/09/populism-and-coxeys-army-a-nineteenth-century-march-on-washington/')])
add('1896.pitchfork-tillman','“干草叉”本·蒂尔曼与南方州权话语',[268,302,303,304,348,349,350],
    ['蒂尔曼的绰号与他扬言用干草叉戳克利夫兰、迫其改变经济政策的攻击性修辞有关；不是他真的带着干草叉参加游戏中的会谈。',
     '在南方种族政治语境中，“尊重州权”和“自然秩序”可能被用来维护白人统治。原作某个选项直接宣称黑人及其他种族低等，译文保留其种族主义立场；旁注不把游戏中的可选发言当作布赖恩真实说过的引文。第十四和第十五修正案涉及平等保护、公民权及投票权，不能笼统译为一般性修宪。'],
    [('美国参议院：本杰明·蒂尔曼生平、绰号与种族主义政治','https://www.senate.gov/senators/FeaturedBios/Featured_Bio_Tillman.htm')])
add('1896.women-idaho-date','爱达荷妇女选举权：同年不等于已参与当届总统投票',[279,314,315,316,329],
    ['科罗拉多、犹他、爱达荷和怀俄明的妇女选举权，形成于不同的立法、建州与公投过程，不能都说成全国宪法修正案带来的权利。',
     '爱达荷的妇女选举权公投，在1896年十一月投票日才获批准。原作却以“如今已能投票”的说法，把它列入竞选期间的州名单；正文保留这个表述，但不应据此推断爱达荷妇女已经参与1896年总统投票。全国第十九修正案是后来的事件。'],
    [('美国国家公园管理局：西部各州妇女选举权时间线','https://www.nps.gov/articles/woman-suffrage-in-the-west.htm')])
add('1896.blue-laws','“蓝色法”：星期日营业与休息规定',[366,382,383,384],
    ['蓝色法通常指限制星期日营业、劳动或某些娱乐活动的法律，历史上与基督教的休息、礼拜观念相联系；名称不是说法律使用蓝色字体。',
     '是否限售酒类、强制商店停业，以及应由州还是联邦立法，是游戏中的不同选项，不等于都主张全国全面禁酒。'],
    [('国会图书馆法律博客：星期日蓝色法与营业限制','https://blogs.loc.gov/law/2018/08/baseball-blues-sunday-games-and-the-law/')])
add('1896.rural-mail','农村免费投递：把邮件送到住处',[367,376,377,378,392],
    ['农村免费投递指居民无需专程去邮局领取邮件，开始获得上门投递服务；“免费”不是所有寄信都免邮资。',
     '美国邮政史记载，实验性投递拨款于1893年获通过，随后追加经费，服务于1896年10月1日在西弗吉尼亚几个地点试行。原作把过程概括为克利夫兰当年签署的一部法律，旁注说明这涉及多年拨款及试验，并非1896年已覆盖全体农村居民。'],
    [('美国邮政：农村免费投递的拨款与服务时间线','https://about.usps.com/who/profile/history/rural-free-delivery.htm')])
add('1896.rail-funding-date','太平洋铁路融资法案：疑似提前引用1897年表决',[397,411,412,413,414],
    ['国会记录中，可识别的H.R. 8189太平洋铁路融资法案，涉及既有铁路债务和联邦债权的清偿，并不只是拨款新建一条铁路。1897年1月11日，它在众议院推进至三读的表决中遭到否决。',
     '原作在1896年竞选中提到该法案“最近遭否决”，存在明显的年代疑点。正文保留问法；此处不是声称铁路融资在1896年没有争论，也未排除原作者可能混用了其他提案。'],
    [('美国政府出版局：1897年1月11日国会记录与H.R. 8189表决','https://www.govinfo.gov/content/pkg/GPO-CRECB-1897-pt1-v29/pdf/GPO-CRECB-1897-pt1-v29-19-2.pdf')])
add('1896.effluence-source','effluence：原作措辞不协调',[306],
    ['原句使用with effluence。这个词通常表示流出或排放，放在鼓励南方竞选的句子里不协调。译文按上下文理解为“放开手脚去干”，没有把异常措辞当成一个美国政治术语。',
     '无法从原文确定作者本来想写哪一个词，故不宣称它一定是eloquence等词的笔误。英文原文完整保留；本条属于翻译判断与原作疑点，不是历史事件的考证。'],
    [('原版内置1896年布赖恩—苏厄尔剧本（用于核对措辞）','https://github.com/newcampaigntrail/newcampaigntrail.github.io/blob/d6655ef6ad80ab9a8fe5510d0fd43874e57dacbf/static/questionset/1896_Bryan_Sewall.html')])
add('1896.contingent-election','胶着选举与众议院按州选总统',[3,6],
    ['nail-biter与squeaker都在这里形容结果极其接近的选举，并非咬指甲的比赛或“输给吱吱声”。胜负标题与缺少选举人票多数的叙述应结合阅读。',
     '没有候选人得到选举人票过半数时，众议院从选举人票前三名中选总统，每州代表团一票；参议院另选副总统。游戏直接依据州代表团的党派控制预测结果，是简化叙事，而不是将普通众议员票数直接相加。1896年的州数与今日不同，不套用今日所需州票数。'],
    [('美国国家档案馆：选举人票不足多数时的国会选举规则','https://www.archives.gov/electoral-college/faq')])
add('1896.darwin-context','进化论、社会达尔文主义与后来“猴子审判”',[189,419,433,434,435,436,437,443],
    ['生物进化论、把竞争与弱肉强食套用到社会的社会达尔文主义，以及基于宗教的创造论，并不是同一个概念。原作有意让不同选项在这些问题上表态，译文保留这种区别。',
     '布赖恩与1925年斯科普斯审判的关联很有名；史密森尼档案保存了达罗盘问他的照片。但1925年不能当成1896年已经发生的事件。游戏把他后来的政治宗教形象带入较早的竞选，所提供的具体回答也不能自动视为当年真实演说原话。'],
    [('史密森尼档案：1925年7月20日斯科普斯审判照片与人物','https://siarchives.si.edu/collections/siris_sic_11723'),
     ('内布拉斯加州历史学会：布赖恩档案中的《达尔文主义的威胁》等著作','https://history.nebraska.gov/collection_section/william-jennings-bryan-1860-1925-rg3198-am/')])
add('1896.hawaii','推翻夏威夷君主制与美国吞并是两件事',[230,255,278,317,318,319],
    ['夏威夷君主制于1893年被推翻；美国于1898年吞并夏威夷。1896年讨论是否吞并，不是在讨论一个已经成为美国州的地方。多尔指政治人物桑福德·多尔，也不是水果本身。',
     '“带去秩序”“种植园收益”等是游戏人物的立场性说法，不能当作夏威夷人民一致同意的结论。伊奥拉尼宫资料保留了莉莉乌奥卡拉尼女王反对吞并的抗议；1898年总统咨文则记录了美国接收主权的程序，二者反映不同当事方。'],
    [('美国国家公园管理局：伊奥拉尼宫与夏威夷反对吞并的历史资料','https://www.nps.gov/articles/000/iolani-palace-a-hawaiian-place-of-history-power-and-prestige.htm'),
     ('美国国务院历史文献：1898年总统咨文中的夏威夷接收程序','https://history.state.gov/historicaldocuments/frus1898/message-of-the-president')])
old={n['id']:n for n in data['notes']};old.update({n['id']:n for n in notes})
data['notes']=list(old.values());data['checkedAt']='2026-10-09'
(ROOT/'localization/annotations/notes.zh-CN.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
gpath=ROOT/'localization/reviews/glossary-context.zh-CN.json';g=read(gpath)
new=[('wet / dry (Prohibition)','反禁酒派／禁酒派','湿人／干人','1896.wet-dry'),
    ('patronage jobs','酬庸官职','一般工作岗位','1896.pendleton-patronage'),
    ('Coxey’s Army','考克西抗议队伍／考克西军队','正规联邦军队','1896.coxey-army'),
    ('Blue Laws','蓝色法／星期日营业限制法','蓝色字体的法律','1896.blue-laws'),
    ('Rural Free Delivery','农村免费投递','农村寄信免邮资','1896.rural-mail'),
    ('injunction (labor dispute)','法院禁令','工会命令','1896.pullman-intervention'),
    ('nail-biter / squeaker (election)','极其胶着的选举','咬指甲比赛／吱吱声','1896.contingent-election')]
terms={t['en']:t for t in g['terms']}
for en,zh,avoid,noteId in new:terms[en]={'en':en,'zh':zh,'avoid':avoid,'noteId':noteId}
g['terms']=list(terms.values());g['checkedAt']='2026-10-09';g['era']='1844 / 1860 / 1896 / 1964 / 1968'
gpath.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched 1896 notes')
