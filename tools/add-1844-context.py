"""Optional authoring step: researched notes bind exact reviewed full sources."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
snapshot=read(ROOT/'localization/reviews/1844-source-snapshot.json')
data=read(ROOT/'localization/annotations/notes.zh-CN.json')
notes=[]
def add(id,title,indices,body,sources,category='历史制度／术语'):
    notes.append({'id':id,'title':title,'category':category,
        'contains':[snapshot[i]['source'] for i in indices],'body':body,
        'sources':[{'title':t,'url':u} for t,u in sources]})
add('1844.american-system','国内公共工程与克莱的“美国体系”',[7,13,44,45,51,62,63,166,195,196,200],
    ['这里的internal improvements指运河、道路等交通与公共工程，不是泛指改善内政。克莱的“美国体系”把保护性关税、国家银行和联邦资助的公共工程结合起来，主张通过交通和市场联系促进各地区经济。',
     '电报是否应由政府购买专利并管理，是游戏把新技术放进这场政府权限争论中的具体选项。译文保留赞成政府主导与支持私人建设的区别。'],
    [('美国参议院：克莱1832年“美国体系”演说','https://www.senate.gov/artandhistory/history/common/generic/Speeches_ClayAmericanSystem.htm'),
     ('美国众议院：1824年“美国体系”演说','https://history.house.gov/Historical-Highlights/1800-1850/The-1824-American-System-speech-by-Speaker-Henry-Clay-of-Kentucky/')])
add('1844.bank-war','国家银行、银行战争与独立国库',[19,64,65,66,67,79,80,81,82,85,86,87,88,117,118,127,130,230,231,233],
    ['1844年语境中的national bank，是围绕是否恢复类似美国第二银行的全国性银行而展开的争论。第二银行的联邦特许期限于1836年届满；“已撤销”指其全国性特许地位，并非说其当时立即停止一切州级业务。杰克逊1832年否决续约，是“银行战争”的关键事件。',
     '独立国库是让政府自行保管公共资金、减少对私人银行依赖的制度，不是设立现代中央银行。1846年沃克任财政部长时，该制度重新确立。自由银行制度也不是免费银行服务。这些概念不能套用1863年的全国银行法或1913年成立的美联储。'],
    [('美联储历史：美国第二银行','https://www.federalreservehistory.org/essays/second-bank-of-the-us'),
     ('美国财政部：罗伯特·沃克与1846年独立国库','https://home.treasury.gov/about/history/prior-secretaries/robert-j-walker-1845-1849'),
     ('美国参议院：1863年全国银行法','https://www.senate.gov/artandhistory/history/common/civil_war/NationalBankActs.htm')])
add('1844.nativist-riots','本土主义与1844年费城暴乱',[11,16,39,52,53,76,77,78,103,104,126,138,162,165,180,182,183,185,218,220],
    ['此处nativism指反移民、反天主教的本土主义或排外主义，与美国原住民无关。许多爱尔兰移民信奉天主教，这使宗教与移民冲突相互交织。1844年费城发生暴乱，天主教教堂遭焚毁。',
     '游戏分别提供谴责本土主义者和谴责爱尔兰人的题目，这是政治立场不同的两段原文，不能合并成同一个温和表态。入籍法决定成为公民的条件；选项中的新公民投票等待期另行译明，避免与一般入境等待混淆。'],
    [('美国国会图书馆：爱尔兰移民的宗教冲突与歧视','https://www.loc.gov/classroom-materials/immigration/irish/religious-conflict-and-discrimination/'),
     ('美国国会图书馆：1844年费城暴乱版画与编目说明','https://www.loc.gov/pictures/item/2003654121/')])
add('1844.gag-rule','禁议规则：不是普通的维持议事秩序',[170,203,204,205,208],
    ['众议院1836年开始采用禁议规则，把涉及奴隶制的请愿自动搁置，不予进一步处理。约翰·昆西·亚当斯反对它，认为它侵害请愿权；规则最终在1844年12月3日被废除。',
     '因此，支持禁议规则的选项是在支持压下反奴隶制请愿。它不只是一般性的议会纪律要求。游戏在竞选期间询问是否支持废除，译文没有把大选后的结果写进人物当时的回答。'],
    [('美国众议院：禁议规则及其废除','https://history.house.gov/Historical-Highlights/1800-1850/House-Gag-Rule/')])
add('1844.manifest-destiny-date','“天定命运”的年代问题',[72],
    ['“天定命运”以天意和民族使命为领土扩张辩护。约翰·L.·奥沙利文在1845年的《吞并》文章中使用了这一著名措辞。',
     '这一选项位于1844年剧本，因而存在用后来成名的术语概括较早扩张观念的年代错置。译文保留原作说法；不能据此认定人物在1844年已经使用了这个固定口号。'],
    [('奥沙利文1845年《吞并》原文及史料导读','https://teachingamericanhistory.org/document/annexation/')],category='年代校注／政治修辞')
add('1844.calhoun-pakenham','卡尔霍恩致帕肯纳姆信',[145,148,149,150],
    ['卡尔霍恩1844年4月18日写给英国驻美公使理查德·帕肯纳姆的信，为奴隶制辩护，并把吞并得克萨斯与保护奴隶制免受英国废奴政策影响联系起来。这里的“积极的福祉”是他的政治主张，不是校注认可的事实判断。',
     '游戏原文写作Packenham，收信人的规范拼写是Pakenham。中文按帕肯纳姆处理，原始英文数据保持不变。选项之间对奴隶市场、全国扩张和南方利益的不同表态也完整保留。'],
    [('卡尔霍恩1844年致理查德·帕肯纳姆信原文','https://teachingamericanhistory.org/document/letter-to-richard-pakenham-british-minister-to-the-united-states/')])
add('1844.princeton','普林斯顿号事故与国务卿更替',[146],
    ['1844年2月28日，普林斯顿号在波托马克河试航时，“和平缔造者”舰炮爆炸，国务卿阿贝尔·厄普舒尔、海军部长托马斯·吉尔默等人遇难。这里说的是军舰事故，不是普林斯顿大学发生爆炸。'],
    [('美国海军历史与遗产司令部：普林斯顿号舰史','https://www.history.navy.mil/research/histories/ship-histories/danfs/p/princeton-i.html')])
add('1844.birney-name','伯尼：原作的人名误写',[193,194],
    ['1844年自由党的总统候选人是詹姆斯·吉莱斯皮·伯尼（James G. Birney）。游戏这个攻击选项却写成Thomas Birney，正文按原文保留为“托马斯·伯尼”，在此说明实际人物。',
     '“民主党的傀儡”“把大选送给波尔克”属于玩家角色的竞选攻击，不是对伯尼真实动机的史学定论。自由党是当时的废奴第三党，不是现代自由意志党的另一译名。'],
    [('美国国会图书馆：1844年自由党候选人詹姆斯·伯尼肖像','https://www.loc.gov/pictures/item/2002699741/')],category='原文错误／竞选攻击')
add('1844.sectional-source','地域偏见：原句可能漏了否定词',[71],
    ['原文确实写的是“this does derive from sectional prejudice”（这确实源于地域偏见）。但紧接着说既反对得克萨斯扩张，也反对俄勒冈等地扩张，可能本想表达“不因地域偏见而反对”，疑似漏写not。',
     '译文保留现有英文的肯定含义，不擅自补成否定。这里的sectional指美国不同地区之间的利益分歧，不是社会阶层。得克萨斯与俄勒冈涉及不同的领土及奴隶制争论，这也解释了原句为何可疑；漏词只是校订判断，并未获作者确认。'],
    [('美国国务院历史办公室：得克萨斯吞并','https://history.state.gov/milestones/1830-1860/texas-annexation'),
     ('美国国务院历史办公室：俄勒冈领地争端','https://history.state.gov/milestones/1830-1860/oregon-territory')],category='原文疑点／译法说明')
add('1844.oregon-source','俄勒冈边界与原文语病',[206,207],
    ['这里的俄勒冈领地是美英争议地区，范围不能等同于今天的俄勒冈州。1846年条约主要沿北纬49度划界，并保留温哥华岛归英国。哥伦比亚河曾是谈判中的另一种边界构想。',
     '原选项写作“some of all”，语法不通。本译文根据上下文按“some or all”（部分或全部）理解，明确记录这一解释，而不声称原文无误。另一选项把Columbia River拼成Colombia River；中文采用通行译名“哥伦比亚河”。游戏中的政策选择和实际历史最终条约分开说明。'],
    [('美国国务院历史办公室：1846年俄勒冈领地协议','https://history.state.gov/milestones/1830-1860/oregon-territory')],category='原文疑点／边界术语')
add('1844.african-colonization','非洲殖民安置与附条件废奴',[186],
    ['这里的recolonized to Africa指把获释黑人送往非洲建立殖民定居点，不能译成一般的国内再安置。美国殖民协会推动自由黑人迁往非洲，亨利·克莱是其中的重要人物。',
     '选项同时要求补偿奴隶主、给予提前通知和非洲殖民安置。这是附带条件的废奴主张，与立即、无条件废奴不同；译文保留这些限制，不把它改写为现代平等权利宣言。'],
    [('美国国会图书馆：殖民安置及亨利·克莱','https://www.loc.gov/collections/african-american-perspectives-rare-books/articles-and-essays/colonization/')])
base=read(ROOT/'localization/reviews/1844-base-source-snapshot.json')
notes.append({'id':'1844.contingent-election','title':'众议院选总统：按州投票，不是按议员人数',
    'category':'选举制度／原作简化','contains':[base[4]['source'],base[8]['source']],
    'body':['如果没有总统候选人获得已任命选举人票的过半数，宪法第十二修正案规定，由众议院从选举人票最多的至多三名候选人中选出总统。每个州的代表团只有一票；副总统另由参议院按相应规则选出。',
        '游戏结局只说民主党在众议院占多数，所以波尔克很可能获选。这是原作的简化叙事：议员席位总数占多数，并不必然等于掌握多数州代表团。译文保留“很可能”的语气，不把这一结果说成自动产生的法律规则。'],
    'sources':[{'title':'美国国家档案馆：选举人团相关宪法条文（第十二修正案）','url':'https://www.archives.gov/electoral-college/provisions'}]})
supplement=read(ROOT/'localization/reviews/1844-supplement-source-snapshot.json')
notes.append({'id':'1844.young-hickory','title':'“小山核桃”：杰克逊的政治传人',
    'category':'政治绰号／竞选修辞','contains':[supplement[0]['source']],
    'body':['杰克逊被称为“老山核桃”（Old Hickory）；波尔克因支持杰克逊的政策而获得“小山核桃”（Young Hickory）的称号。这里的“年轻”强调政治传承，不是在谈一种树的树龄。',
        '问题是在问：应该利用杰克逊的声望，还是避免被视为缺乏独立立场的门生。称号本身是真实的历史竞选用语，不是后来网上杜撰的昵称。'],
    'sources':[{'title':'美国国会图书馆：波尔克生平时间线','url':'https://www.loc.gov/collections/james-k-polk-papers/articles-and-essays/timeline/'},
        {'title':'美国国会图书馆：1844年民主党竞选旗帜','url':'https://www.loc.gov/pictures/item/2003674555/'}]})
ids={n['id'] for n in notes}
data['notes']=[n for n in data['notes'] if n['id'] not in ids]+notes
(ROOT/'localization/annotations/notes.zh-CN.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
context={'schema':1,'checkedAt':'2026-10-08','era':'1844','terms':[
    {'en':'internal improvements','zh':'国内公共工程','avoid':'内部改进／内政改革','noteId':'1844.american-system'},
    {'en':'national bank','zh':'国家银行','avoid':'直接等同于现代美联储或1863年全国银行制度','noteId':'1844.bank-war'},
    {'en':'Independent Treasury','zh':'独立国库','avoid':'独立央行','noteId':'1844.bank-war'},
    {'en':'free banking','zh':'自由银行制度','avoid':'免费银行服务','noteId':'1844.bank-war'},
    {'en':'nativism','zh':'本土主义（排外主义）','avoid':'美国原住民主义','noteId':'1844.nativist-riots'},
    {'en':'Gag Rule','zh':'禁议规则','avoid':'普通议事纪律／禁止所有发言','noteId':'1844.gag-rule'},
    {'en':'Manifest Destiny','zh':'天定命运','avoid':'忽略固定措辞的1845年背景','noteId':'1844.manifest-destiny-date'},
    {'en':'sectional','zh':'地域的／地区间的','avoid':'阶层的','noteId':'1844.sectional-source'},
    {'en':'recolonized to Africa','zh':'送往非洲殖民安置','avoid':'国内安置／移民归化','noteId':'1844.african-colonization'},
    {'en':'Liberty Party','zh':'自由党','avoid':'自由意志党','noteId':'1844.birney-name'}]}
(ROOT/'localization/reviews/glossary-context.zh-CN.json').write_text(json.dumps(context,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched context notes; all matching originals reviewed in full.')
