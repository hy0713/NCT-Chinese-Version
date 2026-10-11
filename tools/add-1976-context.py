"""Bind historical context to immutable 1976 full-field snapshots only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/1976-{p}-source-snapshot.json') for p in 'abcde'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'1976.'+id,'title':title,'category':'历史制度／政治典故',
        'contains':list(dict.fromkeys(parts[p][i]['source'] for p,indices in bindings for i in indices)),
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
app='https://www.presidency.ucsb.edu/documents/interview-with-playboy-magazine'
ford='https://www.fordlibrarymuseum.gov/exhibits/1976election/election.html'
constitution='https://www.archives.gov/founding-docs/amendments-11-27'
add('playboy','心里犯奸淫：宗教自省与竞选风波',
    [('a',[13,14,15,41,42]),('c',[3,4,5,6,7]),('d',[71]),('e',[20,21])],
    ['卡特在《花花公子》访谈中谈基督教的谦卑、欲念与不应自以为比别人优越。“心里犯奸淫”援引耶稣关于欲念的教导，不是承认实际婚外情。“干”和“姘居”保留原文口语的粗俗程度，不能改成他真的干过这些事。',
     '他随后批评尼克松和约翰逊撒谎、欺骗及歪曲真相；原作只突出约翰逊与得克萨斯选票。资料页的11月1日是编辑按杂志11月号设置的日期，不代表采访当天；游戏的票数后果及道歉选择属于模拟。'],
    [('加州大学圣巴巴拉分校：1976年《花花公子》访谈全文及日期说明',app)])
add('ford-offices','福特未经选举进入白宫，不是从未当选公职',
    [('a',[23,24,25])],
    ['福特曾多次当选联邦众议员。1973年按第二十五修正案程序获任命并经国会确认出任副总统，1974年尼克松辞职后继任总统；他没有在全国大选中当选总统或副总统。',
     '原文“从未当选进入职位”措辞过宽，中文按本段总统身份译为“从未通过选举进入白宫”，并在这里保留这一解释的依据。不能把它理解为他整个政治生涯都未赢过选举。'],
    [('福特总统图书馆：1973—1974年副总统档案与任命背景','https://www.fordlibrarymuseum.gov/digital-research-room/finding-aids/gerald-r-ford-vice-presidential-papers-1973-74'),('国家档案馆：第二十五修正案',constitution)])
add('last-term','福特最后一届任期与未决选举',
    [('a',[4,5,7])],
    ['福特继任后至1977年1月已任职超过两年。第二十二修正案规定，若在他人当选的任期内任职超过两年，之后只能再当选总统一次；因此1976年赢得选举将开启他的最后一届，而非还可以赢下1980年。',
     '若总统候选人都未获选举人票多数，第十二修正案规定众议院按州投票，每州一票，从前三名中选总统。原作把民主党议员占多数写成卡特必胜，属于机制简化；议员总人数多数不等于州代表团票数多数。'],
    [('国家档案馆：第十二与第二十二修正案',constitution)])
add('utopia','卡特乌托邦：花生、果酱与873票',
    [('a',[10,11])],
    ['这是原作的夸张架空结局：全民务农吃花生酱三明治、苏联解散并让出国土、卡特电视直播痛打尼克松、共和党解散，都不是历史事实。花生联系卡特的务农形象，全文故意把政治成功写成荒诞童话。',
     '蒙代尔“873比0”的选举人票不是1976年的真实票数。国家档案馆列出当年总计538票；译文保留873这个笑点，不改票数计算，也不把游戏中的1984年份强行认证为某个特定文学梗。'],
    [('国家档案馆：1976年真实选举人票','https://www.archives.gov/electoral-college/1976'),('《花花公子》访谈：卡特花生农场主的形象',app)])
add('rose-garden','玫瑰园战略：利用现任总统身份',
    [('a',[26,27,28,29]),('e',[0])],
    ['玫瑰园战略指福特更多留在白宫履行公务，突出总统的经验与可靠形象，由多尔外出竞选，也节省差旅预算。它不是园艺政策，也不意味着总统从不外出。',
     '游戏写“战略奏效”是相应胜利分支的评价；真实1976年福特输给卡特。建国二百周年庆典中的总统形象也服务于现任者优势。'],
    [('福特总统图书馆：1976年大选与玫瑰园战略',ford)])
add('europe-gaffe','东欧口误：辩论中的冷战措辞',
    [('b',[74])],
    ['福特在第二场总统辩论中否认苏联主宰东欧，引发争议。这里并不是东欧国家已经摆脱苏联影响；他的后续解释强调当地人民追求自由。',
     '游戏中有关赢得辩论或从口误中获益的反馈是模拟结果，不替任何候选人证明东欧当时的实际政治独立程度。'],
    [('福特总统图书馆：三场总统辩论及东欧争议',ford)])
add('grain','对苏粮食贸易：1972年已签大额协议',
    [('a',[51]),('b',[39,40,41]),('c',[38,39,40])],
    ['国务院《美国对外关系文件》记录，美国与苏联于1972年7月8日签署三年粮食采购协议。原问题写大量销售始于1973年，年代概括有误；中文正文保留1973，不暗改原始问题。',
     '农产品出口、缓和外交关系以及贸易导致国内价格变动的争论应分别理解。游戏关于农民支持或物价效果的评价是竞选反馈，不是从这份协议即可推出的定量结论。'],
    [('美国国务院：1972年7月粮食采购协议','https://history.state.gov/historicaldocuments/frus1969-76v15/d7')])
add('humphrey-hawkins','充分就业：1976年提案与1978年法律不同',
    [('a',[36]),('b',[50,51,52,53]),('c',[47,48,49,50])],
    ['1976年争论的是汉弗莱—霍金斯就业立法提议，不能写成当时已生效的1978年法律。充分就业并非绝对零失业。',
     '最终1978年法律包含20岁以上人员失业率不超过3%、通胀降至3%或更低及更长期零通胀等目标，并附带就业目标约束。原选项把3%失业、0%通胀、预算平衡和无贸易逆差并列，是反对者的讥讽论证，不能当作所有1976年版本的逐字条文。'],
    [('联邦储备历史：1978年充分就业与平衡增长法','https://www.federalreservehistory.org/essays/humphrey-hawkins-act')])
add('draft','逃避征兵者与军中逃兵不同',
    [('a',[39]),('b',[10,11,12,13])],
    ['逃避征兵者指未按征兵制度要求服役的人；军中逃兵则已进入军队后擅离职守。卡特在1976年访谈中支持普遍赦免前者，并明确不把军中逃兵纳入同一范围。',
     '这里保留完全反对、附条件与普遍赦免的政治立场差别；不能把draft evaders一律译成逃兵，也不能把所有反战者等同于违法者。'],
    [('卡特1976年访谈：分别讨论逃避征兵者与军中逃兵',app)])
add('era','ERA是宪法修正案；贝蒂的沙发是玩笑',
    [('a',[40]),('b',[14,15,16,17]),('c',[18,19,20,64,65,66,67])],
    ['平等权利修正案由国会于1972年提出，尚须足够州批准才能成为宪法的一部分。1976年的支持与反对不能译成国会准备首次通过一项普通法律；工会对妇女保护立法与平等待遇也并非始终有同一立场。',
     '贝蒂·福特公开支持ERA，并在1975年访谈表达期待。反馈里总统只能睡白宫沙发，是借夫妻观点冲突开玩笑，不是已查证的白宫生活记录。原文关于“许多工会反对”的范围和75%支持率尚未独立核准。'],
    [('国家档案馆：ERA的国会通过与州批准程序','https://www.archives.gov/women/era'),('福特总统图书馆：贝蒂1975年8月10日访谈','https://www.fordlibrarymuseum.gov/the-fords/betty-ford/key-speeches-first-lady-betty-ford')])
add('betty','贝蒂的坦率：不等于替丈夫宣布政纲',
    [('e',[51,52,53,54])],
    ['贝蒂1975年《60分钟》访谈涉及堕胎、年轻人的性关系及尝试大麻，引来赞成与反对。她表达自己的观点，也强调与丈夫可以有政治分歧。',
     '原问答中“劝她低调”“她不听”是可选竞选台词，不是访谈逐字实录；75%支持率在本批资料中尚未独立验证。图书馆正式访谈页标注8月10日，避免把另一份文件标题中的10月日期误当首次播出时间。'],
    [('福特总统图书馆：贝蒂《60分钟》完整访谈','https://www.fordlibrarymuseum.gov/the-fords/betty-ford/key-speeches-first-lady-betty-ford')])
add('work','工作权法：工会保障协议，而非政府保证就业',
    [('a',[47]),('b',[33,34,35]),('c',[33,34])],
    ['这里的工作权法涉及州是否禁止把缴纳工会费用等工会保障安排作为就业条件。它不是国家保证人人获得工作的权利，也不能与充分就业法案混为一谈。',
     '《塔夫脱—哈特利法》及其第14(b)条保留州在相关安排上的限制权限。支持工会与反对强制缴费的选项保留不同立场；现代机构页面中的州数量不能倒填到1976年。'],
    [('美国国家劳资关系委员会：工会保障协议与工作权法','https://www.nlrb.gov/about-nlrb/rights-we-protect/your-rights/employer-union-rights-and-obligations'),('美国国家劳资关系委员会：劳动关系法第14(b)条','https://www.nlrb.gov/guidance/key-reference-materials/national-labor-relations-act')])
add('oil','石油禁运：阿拉伯产油国与以色列政策',
    [('a',[50]),('b',[29,30,31,32]),('c',[31,32])],
    ['1973年阿拉伯—以色列战争期间，阿拉伯产油国针对支持以色列的国家实施禁运，并削减产量，禁运于1974年3月结束。不能把它写成所有石油输出国或所有阿拉伯国家一致的行动。',
     '美国对以色列的支持、与沙特等国的关系、国内能源开发及节能政策相互牵制。原选项的石油独立、调整外交立场和增加生产是不同路线，译文没有合并。'],
    [('美国国务院：1973—1974年石油禁运','https://history.state.gov/milestones/1969-1976/oil-embargo')])
add('panama','巴拿马运河：1976年谈判并未完成移交',
    [('d',[21,40,41,55,56])],
    ['福特时期已在谈判新的运河安排；1977年卡特与托里霍斯签署两个条约，1978年参议院批准。运河区于1979年10月停止存在，运河本身到1999年12月才移交巴拿马。',
     '1976年选项讨论的是将来的政策选择，不能当作已经完成的卡特条约。保留继续控制、谈判和主权移交的差别，也不把运河与整个运河区当作同一个日期移交的对象。'],
    [('美国国务院：托里霍斯—卡特条约及分阶段移交','https://history.state.gov/milestones/1977-1980/panama-canal')])
add('church-committee','彻奇委员会：情报监督，不是教会委员会',
    [('d',[20,24,25,26,27,28,29,30,31,44])],
    ['Church在这里是参议员弗兰克·彻奇的姓。1975年成立的调查委员会查究情报机关的非法、不当或不道德行动，1976年4月提出最终报告；并不是调查宗教组织的委员会。',
     '游戏把公开政府、约束军方及情报活动与国家安全之间的争议写入搭档分支。批评调查削弱安全，是角色的政治判断；调查发现的权利侵害不能被这一台词抹去。'],
    [('美国参议院：彻奇委员会调查与最终报告','https://www.senate.gov/about/powers-procedures/investigations/church-committee.htm')])
add('scoop','斯库普·杰克逊：绰号与鹰派民主党人',
    [('d',[61,62,63,64,65,66,67])],
    ['斯库普是亨利·杰克逊的绰号，参议院简介记述他年幼卖报时获得这个称呼。不是名字叫“独家新闻”的另一个人，也不是安德鲁·杰克逊。',
     '他是华盛顿州民主党参议员，国内政策上的自由派倾向与国防外交上的强硬态度可以并存。不能因为鹰派立场就把他的党籍、工会关系或全部国内政纲改成共和党保守派。'],
    [('美国参议院：亨利·斯库普·杰克逊生平','https://www.senate.gov/artandhistory/history/minute/Henry_Scoop_Jackson.htm')])
add('butz','巴茨辞职：真实事件与可选应对',
    [('d',[73]),('e',[8,9,10,11])],
    ['真实历史中，农业部长厄尔·巴茨于1976年10月4日辞职，福特当天公开接受。巴茨在辞职信中为被公开报道的言语致歉；不能把游戏中继续留任的选择当成真实最后结果。',
     '原问答概述粗俗且带种族主义的笑话，没有给出逐字引语，中文不额外编造辱骂内容。这里的总统称赞与支持者反应仍是相应原作台词。'],
    [('福特1976年10月4日讲话与巴茨辞职信','https://www.presidency.ucsb.edu/documents/remarks-upon-accepting-the-resignation-earl-l-butz-secretary-agriculture')])
add('scrooge','斯克鲁奇：吝啬冷酷的文学比喻',
    [('d',[16])],
    ['斯克鲁奇是狄更斯《圣诞颂歌》中的人物，成为吝啬、缺乏同情心的代称。这里说反对政策时不要显得像他，是顾问对竞选形象的讥讽，不是美国政客的姓名。'],
    [('美国国会图书馆：《圣诞颂歌》及斯克鲁奇的广播改编','https://blogs.loc.gov/now-see-hear/2014/12/our-favorite-scrooge/')])
add('nyc','纽约救助：贷款、条件与政治形象',
    [('a',[33]),('b',[6,7,8,9]),('c',[15,16,17])],
    ['问题所称23亿美元救助涉及联邦贷款，不是无偿向城市赠送同额资金。福特最初反对为避免违约而进行联邦救助，后来在纽约州、市及相关机构采取措施后支持贷款方案。',
     '福特竞选阵营的资料汇编记录了这一转变，但它本身是竞选宣传材料，不能把其中赞扬政策效果的说法当作中立经济评估。游戏保留赞成、附条件与拒绝的选项区别。'],
    [('福特总统图书馆保存：1976年竞选资料汇编','https://www.fordlibrarymuseum.gov/president-ford-76-fact-book')])
add('test-ban','有限禁试与全面禁试不是同一政策',
    [('a',[48]),('b',[36,37,38]),('c',[35,36,37])],
    ['1963年《部分禁止核试验条约》禁止大气层、外层空间和水下核试验，没有禁止地下核试验。1976年再讨论全面禁试并不意味着过去从未有过禁试安排。',
     '继续研制武器、与苏联谈判限制以及全面禁止核试验，是不同立场。译文不把停止试验擅自扩大为立即销毁所有核武器。'],
    [('美国国务院：1963年有限禁试条约的范围','https://history.state.gov/milestones/1961-1968/limited-ban')])
add('brown','布朗的以色列负担论：军事供给与外交争议',
    [('a',[45]),('b',[2,3,4,5]),('c',[12,13,14])],
    ['这里是参谋长联席会议主席乔治·布朗，不是副总统候选人或地方议员。1976年同期报道记录，福特回应有关布朗“军事负担”的说法，解释1973年战争援助曾动用美国在欧洲的军备储备，并强调已补足、美国支持以色列安全。',
     '批评援助成本、支持盟友及反犹指控不是同一种主张。原顾问反馈担忧选民把候选人立场理解为反对犹太人，中文保留这一竞选风险，不把所有对援助的批评直接判定为反犹。'],
    [('犹太电讯社1976年10月21日报道：福特回应布朗','https://www.jta.org/archive/ford-israel-not-a-military-burden')])
add('church-race','普莱恩斯教会与克伦农·金：礼拜不等于会籍',
    [('a',[53,72,73,74]),('c',[8,9,10])],
    ['克伦农·金是一名黑人牧师和民权活动人士，不是已于1968年遇刺的马丁·路德·金。同期美联社报道记载，卡特家乡教会后来以120比66表决向所有愿意参加礼拜的人开放。',
     '参加礼拜、申请加入教会、获准成为成员是不同程序。原问题把入会与礼拜取消放在一起，保留其剧情；“共和党特务”是选项的攻击说法，不是译者认证的身份。此次档案PDF全文读取失败，表决及身份依据为报纸档案的搜索文本，具体事发日和会籍程序仍待原页核对。'],
    [('得克萨斯理工大学报纸档案：1976年11月15日Pampa News所载美联社报道','https://newspapers.swco.ttu.edu/bitstreams/30146fa6-ab06-4543-a7a4-e7bf47f667ca/download')])
add('ford-falls','福特摔倒梗：电视讽刺中的笨拙总统',
    [('a',[9])],
    ['原作让玩家想象福特摔下飞机舷梯的动图，联系其在奥地利摔倒及切维·切斯在《周六夜现场》模仿笨拙福特的形象。电视讽刺不等于对其身体能力的医学判断，也不能据此否定他的运动经历。'],
    [('TIME历史专栏：福特、切维·切斯与1976年电视讽刺','https://time.com/4292027/gerald-ford-saturday-night-live/')])
add('bayh-celler','贝赫—塞勒：全国直选的宪法改革提议',
    [('a',[16,21])],
    ['贝赫—塞勒提议以总统全国直选取代选举人团。1969年众议院通过相关修宪方案，但它未完成参议院和州批准程序，并未成为宪法。',
     '游戏出现选举人票胜利而普选票落败的分支后，再谈推动改革，是架空政治后续。不能把这个分支当作卡特1976年真实地输了普选票。'],
    [('印第安纳大学图书馆：贝赫生平及选举人团改革史','https://libraries.indiana.edu/birch-bayh-biography'),('国家档案馆：1976年选举结果','https://www.archives.gov/electoral-college/1976')])
add('gregg','格雷格案：有程序限制的死刑合宪',
    [('a',[46]),('b',[58,59,60,61]),('c',[55,56])],
    ['1976年格雷格诉佐治亚州案审查新的死刑制度，并认可该案所涉、对判刑裁量加以约束的程序。不能把“死刑不当然违宪”写成任何罪名、任意程序的处决都合法。',
     '候选人可赞成、反对或限定死刑适用，译文保留立场差异；法院判决与人物道德赞许不是同一件事。'],
    [('美国政府出版局：格雷格案428 U.S.153判词原件，第153—156页概要','https://www.govinfo.gov/content/pkg/USREPORTS-428/pdf/USREPORTS-428-153.pdf')])
path=ROOT/'localization/annotations/notes.zh-CN.json';data=read(path)
byid={n['id']:n for n in data['notes']};byid.update({n['id']:n for n in notes})
data['notes']=list(byid.values());data['checkedAt']='2026-10-09'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
exceptions={
 'a':[{'index':23,'reason':'Never elected to office interpreted as President/VP entering White House; Ford had won House elections. Same reading at 24 and 25.'},{'index':51,'reason':'1973 grain-start year retained despite July 1972 agreement; annotated.'},{'index':11,'reason':'873 electoral votes and fantastical events retained as original absurdist ending, not historical results.'}],
 'b':[{'index':28,'reason':'Original Roe v. Wave typo retained in English; Chinese uses conventional Wade case name.'},{'index':53,'reason':'1976 proposal critique preserved; not presented as verbatim final 1978 statute.'}],
 'c':[{'index':14,'reason':'On the trial read contextually as campaign trail, not a court trial; English unchanged.'}],
 'e':[{'index':26,'reason':'On the fence out his politics read contextually as about his politics; English unchanged.'}]}
for p in parts:
    (ROOT/f'localization/reviews/1976-{p}-metadata.json').write_text(json.dumps({'checkedAt':'2026-10-09','sourceExceptions':exceptions.get(p,[]),'research':'1976-RESEARCH_ZH.md'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'1976 context notes')
