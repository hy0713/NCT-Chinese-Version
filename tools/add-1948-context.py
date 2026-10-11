"""Source-backed 1948 notes attached to immutable, fully reviewed fields."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/1948-{p}-source-snapshot.json') for p in 'abcd'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'1948.'+id,'title':title,'category':'历史制度／政治修辞',
        'contains':[parts[p][i]['source'] for p,indices in bindings for i in indices],
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('buck-stops','“责任到我这里为止”：不是一美元停在桌上',
    [('a',[28])],
    ['杜鲁门桌上的名牌写着“The Buck Stops Here”，意为责任到此为止，不能再推给别人。这里的buck不是通常所说的一美元。',
     '杜鲁门图书馆解释它与“推卸责任”的说法及扑克牌中轮到谁发牌的标记有关，同时对词源使用“据说”的措辞。游戏借这个政治口头禅表达承担责任，并非把所有可选发言都认证为历史上的原话。'],
    [('杜鲁门总统图书馆：名牌原物、推责习语与词源说明','https://www.trumanlibrary.gov/education/trivia/buck-stops-here-sign')])
add('turnip-day','“无所作为的国会”与“萝卜日”特别会期',
    [('a',[11,14,44,50,51]),('b',[37,40]),('c',[13,35,36])],
    ['杜鲁门在1948年接受提名演说中，宣布召集国会于7月26日开特别会期，要求共和党议员用实际行动兑现本党党纲。他称国会无所作为，是竞选攻击，并非字面上指国会没有通过任何法律。',
     '“萝卜日”借用密苏里州夏季播种萝卜的俗语。原文put their money where their mouth is意为拿出行动兑现承诺，不是要求议员真的交钱。特别会期实际上通过了针对通胀和住房的两项法案。'],
    [('美国参议院：“萝卜日”会期的演说、两项法案与竞选争论','https://www.senate.gov/artandhistory/history/minute/Turnip_Day_Session.htm')])
add('whistle-stop','Whistle-stop：乘火车沿途停车演说',
    [('a',[12,43,46,47,48,49]),('b',[39,41]),('c',[40,64])],
    ['这里指候选人乘火车旅行，沿途停车，在车厢后部平台向群众演说的竞选方式。不能译成吹哨举报，也不是停止吹口哨。',
     '杜鲁门图书馆保存了1948年列车、站点和演说记录。游戏里夸口能亲自和当地三分之一选民交谈，是人物的竞选修辞，旁注不把这项比例当作实测史实。'],
    [('杜鲁门总统图书馆：1948年竞选列车与巡回地图档案','https://www.trumanlibrary.gov/library/online-collections/1948-election-campaign')])
add('dewey-headline','“杜威击败杜鲁门”：著名的错误头条',
    [('a',[0,4]),('b',[39,41,42]),('c',[65,66,67])],
    ['1948年《芝加哥论坛报》曾刊出“杜威击败杜鲁门”的错误头条。后来杜鲁门举着这份报纸的照片，成为政治预测失误的著名典故。',
     '这说明当时很多人看好杜威，但不能把民调领先等同于已经获胜。游戏如果产生杜威胜选，则是模拟的另一种结果，不能拿真实历史的错误头条去证明那个模拟结局也是假消息。'],
    [('国会图书馆：保存的1948年错误头条及其背景','https://blogs.loc.gov/loc/2012/11/stop-the-presses/'),
     ('美国国家档案馆：1948年政治讽刺画与错误头条','https://www.archives.gov/exhibits/running-for-office/assets/pages/45.html')])
add('israel-date','以色列：宣布独立、托管终止与美国承认的日期',
    [('a',[7,32,33]),('b',[25,26]),('c',[8,19,20,21,52,53])],
    ['原问题把宣布独立写为5月15日。杜鲁门图书馆的详细时间线区分：本·古里安在当地5月14日宣读宣言，英国托管于当地5月15日零时终止；美国在华盛顿时间5月14日傍晚给予事实上的承认。时差和不同事件不能混成同一个时间。',
     '正文保留原日期，旁注说明差别。事实承认与法律承认也不同；美国正式的法律承认在1949年。支持承认并不自动等于承诺派美军保卫这个国家。'],
    [('杜鲁门总统图书馆：宣布、托管终止与承认的详细时间线','https://www.trumanlibrary.gov/library/online-collections/recognition-of-state-of-israel'),
     ('美国国家档案馆：承认声明原件与事实／法律承认','https://www.archives.gov/milestone-documents/press-release-announcing-us-recognition-of-israel')])
add('taft-hartley','《塔夫脱—哈特利法》：否决不等于没有生效',
    [('a',[0,6,29,31]),('b',[9,23,24,53]),('c',[7,17,18,35,50])],
    ['这项限制工会权力的法律是在1947年通过的。杜鲁门否决后，国会推翻否决，使其生效。游戏中的“支持否决”和“法律已经通过”，因此并不互相矛盾。',
     '1948年竞选回顾此前的争论，并非同年第一次提出该法。原选项把它列入“过去十二个月”的政绩，是较宽泛的时间概括；距1948年党代会已经超过十二个月。工会是否认为它公平，与联邦政府有没有依法实施它，也是不同问题。'],
    [('美国参议院：杜鲁门否决与国会推翻否决的记录','https://www.senate.gov/legislative/vetoes/TrumanHS.htm'),
     ('美国参议院：罗伯特·塔夫脱与第八十届国会','https://www.senate.gov/about/parties-leadership/taft-a-robert.htm')])
add('civil-rights','民权条款、迪克西民主党人与军队种族隔离',
    [('a',[8,34,35,36,37]),('b',[27,28,29]),('c',[9,22,23,24,54])],
    ['汉弗莱1948年推动民主党民权条款时，尚是明尼阿波利斯市长和参议员候选人；不是已经在任的联邦参议员。民权争论引发南方种族隔离派的反抗，瑟蒙德成为另一个总统候选人。',
     '杜鲁门7月26日发布第9981号行政命令，确立军队不因种族等因素而区别待遇的政策。实施整合需要时间，并非签字当天所有单位就完成融合。支持党纲、行政命令和争取选票，是相关但不同的行为。'],
    [('美国参议院：汉弗莱的1948年演说与1949年起的参议员任期','https://www.senate.gov/senators/FeaturedBios/Featured_Bio_HumphreyHubert.htm'),
     ('美国国家档案馆：第9981号行政命令原件与执行过程','https://www.archives.gov/milestone-documents/executive-order-9981'),
     ('杜鲁门总统图书馆：1948年左右两翼挑战','https://www.trumanlibrary.gov/education/presidential-inquiries/election-1948')])
add('berlin-zones','柏林封锁：占领区、飞地与空中走廊',
    [('a',[10,40,41]),('b',[33,34]),('c',[11,28,29,30,48,59,60])],
    ['西柏林是处于苏联占领区之内、由西方盟国控制的城区。1948年封锁主要切断铁路、公路和水路，空中走廊仍可用于补给，所以不能把原文“任何物资都进不去”理解成不存在空运。',
     '游戏中的“东德”“西德”在这个年份应联系德国东西占领区理解；两个德国国家正式成立是在1949年。苏联接管西柏林的反馈是玩家选择导致的架空分支，不是现实中的柏林空运最终结局。'],
    [('美国国务院：1948—1949年封锁、空运与德国内部分区','https://history.state.gov/milestones/1945-1952/berlin-airlift')])
add('loyalty-huac','忠诚审查、非美活动委员会与麦卡锡的区别',
    [('a',[9,20,30,38,39]),('b',[5,6,7,30,31,32,51,52,73]),('c',[10,25,26,56,71]),('d',[0,1,2,7,8])],
    ['1947年第9835号行政命令规定行政部门雇员的忠诚审查程序；众议院非美活动调查委员会则属于国会。联邦调查局、行政机关和众议院委员会不是同一个机构。',
     '原作的反共指控有真实冷战背景，但选项里的指控不自动构成有罪事实。1948年的众议院调查，也不能直接说成由参议员麦卡锡主持；旁注区分机构，保留玩家支持加强审查或保护公民自由的不同立场。'],
    [('第9835号行政命令全文：行政部门忠诚审查程序（美国总统项目）','https://www.presidency.ucsb.edu/documents/executive-order-9835-prescribing-procedures-for-the-administration-employees-loyalty'),
     ('美国众议院：1948年阿尔杰·希斯传票与非美活动委员会记录','https://history.house.gov/Records-and-Research/Featured-Content/Alger-Hiss-Subpoena/')])
add('dewey-stassen','杜威—史塔森辩论：反共与禁党不是同一立场',
    [('c',[27,58,69]),('d',[3])],
    ['两人1948年5月17日在俄勒冈州通过广播辩论，核心问题是是否取缔美国共产党。史塔森赞成取缔，杜威反对用禁党解决问题。',
     '因此，杜威援引这场辩论，并不等于他支持共产主义，也不表示反对一切针对间谍、暴力或颠覆的法律。游戏给出史塔森作为替代搭档，是模拟组合，不是实际共和党票组。'],
    [('明尼苏达历史学会：1948年5月17日史塔森—杜威广播辩论原稿','https://www2.mnhs.org/library/findaids/00202/pdfa/00202-00055-1.pdf'),
     ('美国国会1948年5月18日记录：引用辩论中的现有法律论点','https://www.govinfo.gov/content/pkg/GPO-CRECB-1948-pt5/pdf/GPO-CRECB-1948-pt5-5.pdf')])
add('henry-wallace','1948年的华莱士与进步党',
    [('a',[36,45]),('b',[49,50,51,72]),('c',[49])],
    ['这里是富兰克林·罗斯福的前副总统亨利·华莱士，代表1948年的进步党参选；不是1968年的乔治·华莱士，也不能与1912年的罗斯福进步党简单视为同一个组织。',
     '该党支持民权等改革，并批评杜鲁门的冷战政策。游戏中民主党人说对手只是为满足虚荣而参选，是党派攻击；旁注不把这个动机判断当成已证实的史实。'],
    [('杜鲁门总统图书馆：1948年进步党党纲史料','https://www.trumanlibrary.gov/education/lesson-plans/1948-election'),
     ('杜鲁门总统图书馆：亨利·华莱士与1948年竞选','https://www.trumanlibrary.gov/education/presidential-inquiries/election-1948')])
add('two-terms','两届惯例、第二十二修正案与麦金莱的情况',
    [('a',[3,19,72,73,74]),('b',[0,46,47,70])],
    ['1948年，总统两届任期限制仍是拟议修宪问题；第二十二修正案在1951年才获批准，而且对当时在任总统有例外。惯例、获选次数和完整任职年数不能混为一谈。',
     '原作杜威胜选结局称可能成为格兰特以来首位two-term共和党总统。如果理解为赢得两次选举，麦金莱在1896和1900年已经做到；如果强调完成两个完整任期，麦金莱则在第二任期遇刺身亡。正文保留原作概括，旁注说明措辞歧义。'],
    [('美国国家档案馆：第二十二修正案全文及1951年批准日期','https://www.archives.gov/founding-docs/amendments-11-27'),
     ('美国参议院：麦金莱1900年成功连任','https://www.senate.gov/artandhistory/history/minute/Hanna_1896Election.htm'),
     ('美国国家档案馆：1900年选举结果及麦金莱遇刺日期','https://www.archives.gov/electoral-college/1900')])
add('nuclear-control','联合国核管制：不是已经签成的核裁军条约',
    [('c',[14,44,45,46])],
    ['1946年的艾奇逊—利林撒尔报告与巴鲁克计划，提出国际管制原子能、防止核扩散的安排。不同国家对机构权限、核武器处置与实施顺序存在分歧，并没有由此实现统一的国际核管制。',
     '游戏选项讨论无条件支持、先取得其他国家保证或拒绝，是不同的政策判断。不能把“国际管制”直接改写成美国已经单方面销毁全部核弹。'],
    [('美国国务院：艾奇逊—利林撒尔与巴鲁克计划','https://history.state.gov/milestones/1945-1952/baruch-plans')])
add('aid-distinction','杜鲁门主义与马歇尔计划：两种援助背景',
    [('a',[17,23,69,70,71]),('b',[1,2,3,4,49,50,71]),('d',[10,11,12,13,15])],
    ['杜鲁门主义以1947年援助希腊和土耳其的政策为重要起点，涉及军事与经济援助；马歇尔计划则以欧洲战后经济复兴为核心，1947年提出、1948年立法。',
     '两者与遏制共产主义扩张的冷战战略有关，但不是同一个法案或同一种援助。原作中关于援助会导致依赖、侵略或未来战争的说法，保留为候选人的政治判断，不冒充客观因果定论。'],
    [('美国国务院：1947年杜鲁门主义','https://history.state.gov/milestones/1945-1952/truman-doctrine'),
     ('美国国家档案馆：1948年马歇尔计划立法及1947年演说','https://www.archives.gov/milestone-documents/marshall-plan')])
add('contingent','众议院选总统、参议院选副总统',
    [('a',[2,5])],
    ['无人获得过半数选举人票时，宪法规定众议院从总统得票前三名中选总统，州代表团各一票；参议院从副总统得票前两名中选副总统。不是由众议院同时选出一整套搭档。',
     '游戏设想候选人达成交易或一方出任另一方副总统，是政治叙事的简化。协议仍需符合候选范围及各院程序，不能只凭普选领先或两人握手就自动转移职位。'],
    [('美国国家档案馆：第十二修正案与后续修正案全文','https://www.archives.gov/founding-docs/amendments-11-27')])
path=ROOT/'localization/annotations/notes.zh-CN.json';data=read(path)
old={n['id']:n for n in data['notes']};old.update({n['id']:n for n in notes})
data['notes']=list(old.values());data['checkedAt']='2026-10-09'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
gpath=ROOT/'localization/reviews/glossary-context.zh-CN.json';g=read(gpath)
terms={t['en']:t for t in g['terms']}
for en,zh,avoid,noteId in [
    ('The buck stops here','责任到我这里为止','一美元停在这里','1948.buck-stops'),
    ('whistle-stop tour','乘火车沿途停车演说','吹哨举报之旅','1948.whistle-stop'),
    ('civil rights plank','民权条款／党纲中的民权主张','木板','1948.civil-rights'),
    ('pay-as-you-go liberalism','量入为出的自由主义','随用随付服务／自由意志主义',''),
    ('de facto / de jure recognition','事实承认／法律承认','承认即承诺派兵保卫','1948.israel-date'),
    ('HUAC','众议院非美活动调查委员会','麦卡锡主持的参议院委员会','1948.loyalty-huac')]:
    terms[en]={'en':en,'zh':zh,'avoid':avoid,'noteId':noteId}
g['terms']=list(terms.values());g['checkedAt']='2026-10-09';g['era']='1844 / 1860 / 1896 / 1916 / 1948 / 1964 / 1968'
gpath.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched 1948 notes')
