"""Attach researched 1960 context to exact immutable reviewed originals."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/1960-{p}-source-snapshot.json') for p in 'abcd'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'1960.'+id,'title':title,'category':'历史制度／政治修辞',
        'contains':[parts[p][i]['source'] for p,indices in bindings for i in indices],
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('religion','天主教候选人与休斯敦演说',
    [('a',[15,19,40,41,42,43,44,45]),('b',[47,48,49,50,51,52]),('d',[20,21,22,23,43])],
    ['肯尼迪在1960年9月12日对大休斯敦牧师协会发表演说，明确主张政教分离，总统不接受教会对公共政策的指令。这里的Catholic是天主教，新教牧师与天主教神职人员不能混成一个教派。',
     '游戏里的反天主教指控是当时的竞选偏见或玩家可选攻击，不是证明天主教总统必定服从教宗的事实。原问题关于150名牧师及皮尔的具体说法仍保留；这篇演说本身不能单独证实那个精确人数，也不把所有选项当作肯尼迪真实说过的原话。'],
    [('肯尼迪总统图书馆：1960年9月12日休斯敦演说全文','https://www.jfklibrary.org/learn/about-jfk/historic-speeches/address-to-the-greater-houston-ministerial-association')])
add('king-call','金博士被捕：旧交通案、缓刑与慰问电话',
    [('a',[28,73,74]),('b',[0,74]),('c',[0,1])],
    ['1960年10月，金博士参与亚特兰大静坐后被捕。研究所整理的时间线区分静坐指控与此前交通案：静坐指控撤销后，他仍因被认定违反旧案缓刑而转押。不能把这简化成静坐本身获判四个月，或新发现驾照问题后立即入狱。',
     '肯尼迪打电话给科雷塔表达关切，罗伯特·肯尼迪也联系司法官员。这里的condolences按活着的丈夫遭监禁的语境译为慰问，不是丈夫死亡后的哀悼。金博士获释后的采访表示感谢，但仍公开保持不为候选人背书的立场；支持肯尼迪的父亲与金博士本人不能混同。'],
    [('斯坦福金研究所：基于金的文字整理的亚特兰大被捕章节','https://kinginstitute.stanford.edu/publications/autobiography-martin-luther-king-jr/chapter-15-atlanta-arrest-and-presidential'),
     ('斯坦福金研究所：1960年10月27日获释后的采访原稿','https://kinginstitute.stanford.edu/king-papers/documents/interview-after-release-georgia-state-prison-reidsville')])
add('quemoy-matsu','Quemoy、Matsu、Formosa：金门、马祖与台湾',
    [('a',[22,56,57,58,59]),('b',[63,64,65,66])],
    ['Quemoy与Matsu指金门和马祖，Formosa是当时英语中对台湾的称呼。选项争论离大陆较近的外岛与台湾防卫之间的关系，不能把三者译成同一个地点。',
     '1958年国务院电报区分条约对台湾、澎湖的共同防卫承诺，以及总统判断保卫相关阵地是否有助于台湾、澎湖防卫的权限。保卫台湾并不等于条约已经无条件要求保卫每一座外岛；派驻美军、维持承诺、征询军事意见分别保留。'],
    [('美国国务院外交文件：1958年9月28日电报及共同防卫范围','https://history.state.gov/historicaldocuments/frus1958-60v19/d139')])
add('missile-gap','“导弹差距”：竞选指控与后来情报',
    [('a',[9,65]),('b',[28,29,30]),('c',[30,31,32,33])],
    ['“导弹差距”在这里指美国被认为落后于苏联的战略导弹能力，不是两枚导弹之间的距离。这个说法是冷战焦虑与1960年竞选争论的一部分。',
     '中央情报局对CORONA项目的历史说明指出，1960年8月开始成功回收的卫星影像，随后帮助纠正对苏联导弹及轰炸机实力的高估。正文保留候选人的指控，不把它当作已经验证的军事现状；这些资料也不能单独证明每个候选人在发言时掌握了哪些机密情报。'],
    [('中央情报局博物馆：CORONA影像与导弹差距评估','https://www.cia.gov/legacy/museum/exhibit/corona-americas-first-imaging-satellite-program/')])
add('u2','U-2事件：遗憾、道歉与侦察政策',
    [('a',[16]),('b',[14,15,16]),('c',[15,16,17,18])],
    ['1960年5月1日，美军情报体系使用的U-2侦察机在苏联领空被击落，飞行员鲍尔斯被捕。美国最初的气象飞行解释遭到证据反驳，随后承认侦察活动。',
     '艾森豪威尔拒绝正式道歉，巴黎峰会最终破裂。表达遗憾、正式道歉、停止特定飞越行动与彻底停止所有间谍活动，是不同承诺。选项对苏联责任的判断是候选人立场，旁注不把所有指责当作客观定论。'],
    [('美国国务院：U-2飞越、鲍尔斯被捕与巴黎峰会','https://history.state.gov/milestones/1953-1960/u2-incident')])
add('little-rock','小石城：执行法院裁决与联邦用兵',
    [('a',[17,18,46,47,48]),('b',[17,18,19]),('c',[19,20])],
    ['1957年9月，艾森豪威尔将阿肯色州国民警卫队置于联邦指挥之下，并派遣第101空降师，保护黑人学生进入小石城中央高中，执行取消学校种族隔离的法院裁决。',
     '1960年的问题是在评价此前事件及民权运动。支持法院判决、赞成动用联邦军队、支持静坐与担心擅入私人场所的法律争议，不能合并成一个立场；以州权为种族隔离辩护的选项也保留其政治含义。'],
    [('美国国家公园管理局：小石城九人与1957年干预时间线','https://www.nps.gov/people/the-little-rock-nine.htm')])
add('health','老年医疗：保险方案失败不等于所有援助失败',
    [('a',[10,52,53,54,55]),('b',[55,56,57,58,59,60,61,62])],
    ['社会保障署1960年时间线说明：8月23日，参议院否决肯尼迪—安德森的医疗保险修正案，同时通过经修改的克尔—米尔斯方案；9月签署的法律向州提供符合条件的老年人医疗援助。',
     '因此，原问题的“一项提案被否决”不能扩写为当年没有任何老年医疗法案通过。社会保障筹资的保险、经经济状况审查的援助、自愿保险和全国全民医疗覆盖，都是不同制度；也不能提前把1965年Medicare的最终制度套到每个1960年选项上。'],
    [('美国社会保障署：1960年保险修正案、克尔—米尔斯方案及立法','https://www.ssa.gov/history/1960.html')])
add('right-to-work','“工作权法”：不是政府保证人人有工作',
    [('a',[21]),('b',[24,25,26,27]),('c',[23,24,25,26,27,28])],
    ['美国劳资争论中的right-to-work，涉及就业能否以加入或支持工会为条件，并不是赋予每个人由政府提供工作的权利。原选项要求全国性法律，比现有州层面的限制更进一步。',
     '《国家劳资关系法》第14(b)节允许州或领地禁止将工会会员资格作为就业条件的协议。限制这类协议并不等于禁止工会或所有集体谈判；废除《塔夫脱—哈特利法》与支持全国工作权法也不是同一方向。'],
    [('美国国家劳资关系委员会：《国家劳资关系法》第14(b)节','https://www.nlrb.gov/guidance/key-reference-materials/national-labor-relations-act')])
add('union-inquiries','霍法与工会调查：反腐不等于反对所有工人组织',
    [('a',[21]),('b',[24,25,26]),('c',[23,24,25,26])],
    ['这里的霍法是卡车司机工会领导人吉米·霍法。参议院1957年成立调查劳资不当行为的特别委员会，由麦克莱伦主持，罗伯特·肯尼迪担任首席法律顾问，调查工会及劳资领域腐败和犯罪影响。',
     '约翰·肯尼迪、罗伯特·肯尼迪、委员会与工会本身是不同主体。支持调查腐败、赞成劳工组织、限制工会权力、要求霍法下台，是可以分别表态的议题，不把选项简化成所有工会一律犯罪。'],
    [('美国参议院国土安全与政府事务委员会：调查小组历史及1957年特别委员会','https://www.hsgac.senate.gov/media/reps/permanent-subcommittee-on-investigations-historical-background/')])
add('congress','国会党派与未承诺选举人',
    [('a',[3,6]),('b',[35,36,42,58])],
    ['1959—1961年的第86届众议院由民主党占多数，不能把原文Republican Congress误读成当时共和党控制整个国会。医疗方案反馈按上下文译为国会中的共和党人，并在校订记录中披露这一理解。',
     'Unpledged指没有预先承诺支持特定总统候选人的选举人，不是尚未决定投票的普通选民。1960年实际有15张总统选举人票投给哈里·伯德；游戏中的交易是模拟叙事。众议院在无人取得选举人票多数时选总统，按州代表团一州一票，不能仅凭全院某党席位多数就断定结果。'],
    [('美国众议院史料：第86届党派席位','https://history.house.gov/Institution/Party-Divisions/Party-Divisions/'),
     ('美国国家档案馆：1960年选举人团计票','https://www.archives.gov/electoral-college/1960'),
     ('美国国家档案馆：第十二修正案','https://www.archives.gov/founding-docs/amendments-11-27')])
add('tv','“上镜”与1960年电视辩论',
    [('a',[0,38,39]),('b',[44,45,46]),('d',[18,19,40,41,42])],
    ['telegenic指在电视镜头前形象、表达效果良好，不是拥有电视技术。1960年9月26日的首场总统候选人电视辩论，使两人的镜头表现成为广受关注的竞选因素。',
     '肯尼迪图书馆记述两人的健康、服装、对镜头的表达方式，以及尼克松后来几场的改善。这并不能证明所有观众意见相同，也不能把游戏里“赢下辩论”的反馈理解为正式裁判结果或只凭化妆就决定选举。替代搭档的剧情仍是架空选择。'],
    [('肯尼迪总统图书馆：1960年竞选与电视辩论','https://www.jfklibrary.org/learn/about-jfk/jfk-in-history/campaign-of-1960')])
add('dixie','《迪克西》：歌曲与南方政治暗示',
    [('d',[33])],
    ['这里的Dixie是歌曲《迪克西》，不是1948年迪克西民主党人的党名。歌曲有黑脸滑稽歌舞演出背景，后来与南部邦联及南方白人身份产生强烈联系。',
     '乔治梅森大学的史料解读同时指出，它的使用并不只限于南部，林肯也喜欢这支曲子；在民权运动语境中，它会让黑人联想到奴隶制与种族主义。游戏暗示竞选场合播放歌曲有政治信号，不据此断言每个演奏者动机相同，或把所有模拟场景认证为真实行程。'],
    [('乔治梅森大学History Matters：以史料分析《迪克西》的多重意义','https://historymatters.gmu.edu/mse/songs/model.html')])
add('nixon-future','尼克松落选结局：当时的预判与真实后来',
    [('a',[5])],
    ['原作落选结局认为尼克松当总统的机会已经过去，这是剧情在1960年的预判，并非真实历史的最终结论。',
     '尼克松在1962年加利福尼亚州长选举中再次失利，但1968年重新取得共和党提名并赢得总统选举。正文保留原作叙述，不擅自用后来发生的事实改写玩家的模拟结局。'],
    [('尼克松总统图书馆：1960、1962年的失利与1968年当选','https://www.nixonlibrary.gov/president-nixon')])
add('dallas','达拉斯抗议与伯德夫人的称呼',
    [('a',[29,37]),('b',[43]),('c',[35])],
    ['Lady Bird是克劳迪娅·约翰逊的昵称，译作伯德夫人；不是在讲一种鸟。第六层博物馆保存的1960年11月4日达拉斯竞选照片，记录约翰逊夫妇遭遇支持者与反对者人群，进入阿道弗斯酒店会场。',
     '这份照片及馆藏说明能支持围堵、抗议的背景，不能单独证实原问题“向她吐口水”的具体动作。正文保留原作说法，细节仍需进一步档案核对；“反而获得宣传好处”也是顾问的政治判断，并非照片证明的因果关系。'],
    [('第六层博物馆：1960年11月4日达拉斯竞选照片及馆藏说明','https://emuseum.jfk.org/objects/44649/lyndon-and-lady-bird-johnson-surrounded-by-a-crowd-during-a')])
add('economic-terms','紧缩货币、整笔拨款与最高边际税率',
    [('a',[65,68]),('b',[1,2,3]),('c',[38,58,65,66])],
    ['hard money在这些降低利率、刺激就业的选项中译为紧缩货币政策，不是字面上的硬币或1844年的金属货币制度。联储历史资料记录1960年衰退及货币政策变化，但候选人把经济问题归咎于艾森豪威尔，是竞选论证，不能据此证明一切责任都在总统。',
     'block grants译为整笔拨款，指为较宽泛用途提供资金并给接受者较大使用裁量，并非街区建设补助。国会研究处的定义用于解释术语，不把后来的具体制度全部套到1960年的提议上。',
     '最高91%的所得税率是边际档税率，不是所有收入都扣掉91%，也不是所有纳税人的实际平均税负。同期国会记录讨论这一最高税档；这里保留原数值，不替玩家计算税务。'],
    [('联邦储备历史：1951至1960年代中期的货币制度','https://www.federalreservehistory.org/essays/treas-fed-accord-to-mid1960s'),
     ('国会研究处：整笔拨款的定义与受款者裁量','https://www.congress.gov/crs_external_products/R/PDF/R40486/R40486.18.pdf'),
     ('1960年国会记录：最高91%税率的争论','https://www.govinfo.gov/content/pkg/GPO-CRECB-1960-pt2/pdf/GPO-CRECB-1960-pt2-1-1.pdf')])
path=ROOT/'localization/annotations/notes.zh-CN.json';data=read(path)
old={n['id']:n for n in data['notes']};old.update({n['id']:n for n in notes})
data['notes']=list(old.values());data['checkedAt']='2026-10-09'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
gpath=ROOT/'localization/reviews/glossary-context.zh-CN.json';g=read(gpath)
terms={t['en']:t for t in g['terms']}
for en,zh,avoid,noteId in [
    ('Quemoy / Matsu / Formosa','金门／马祖／台湾','将台湾与外岛混为一处','1960.quemoy-matsu'),
    ('missile gap','导弹差距','两枚导弹间距／已验证的苏联优势','1960.missile-gap'),
    ('right-to-work law','工作权法','政府保证人人有工作的法律','1960.right-to-work'),
    ('condolences (King imprisonment)','慰问','丈夫已死的哀悼','1960.king-call'),
    ('block grants','整笔拨款','街区补助','1960.economic-terms'),
    ('hard money (1960 campaign)','紧缩货币政策','金属硬币／1844金属货币制度','1960.economic-terms'),
    ('unpledged electors','未承诺支持特定候选人的选举人','尚未决定投票的普通选民','1960.congress'),
    ('telegenic','上镜／镜头表现良好','电视技术','1960.tv')]:
    terms[en]={'en':en,'zh':zh,'avoid':avoid,'noteId':noteId}
g['terms']=list(terms.values());g['checkedAt']='2026-10-09';g['era']='1844 / 1860 / 1896 / 1916 / 1948 / 1960 / 1964 / 1968'
gpath.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched 1960 notes')
