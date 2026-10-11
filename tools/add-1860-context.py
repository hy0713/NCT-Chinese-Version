"""Optional authoring step for researched, exact-source 1860 context notes."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
rows=read(ROOT/'localization/reviews/1860-source-snapshot.json')
base=read(ROOT/'localization/reviews/1860-base-source-snapshot.json')
supp=read(ROOT/'localization/reviews/1860-supplement-source-snapshot.json')
data=read(ROOT/'localization/annotations/notes.zh-CN.json');notes=[]
def add(id,title,indices,body,sources,extra=(),category='历史制度／政治术语'):
    notes.append({'id':id,'title':title,'category':category,
        'contains':[rows[i]['source'] for i in indices]+list(extra),'body':body,
        'sources':[{'title':t,'url':u} for t,u in sources]})
add('1860.dred-scott','德雷德·斯科特案：公民身份与领地奴隶制',[10,24,54,55,57,97,105,171,174,221],
    ['1857年的德雷德·斯科特诉桑福德案，否认被作为奴隶带入美国的非洲人后裔享有判决所说的联邦公民身份，并认定国会不得在联邦领地禁止奴隶制。这里的领地不能随意译成已加入联邦的州。',
     '游戏人物对判决的谴责、接受或担忧，是不同政治立场；不能把所有回答改写成同一种现代评价。某些选项让玩家主张黑人拥有公民身份与投票权，这也不等于林肯在1860年真实发表过相同承诺。'],
    [('美国国家档案馆：1857年斯科特案判决与原文','https://www.archives.gov/milestone-documents/dred-scott-v-sandford')])
add('1860.lemmon','莱蒙案：经过自由州，不等于逃奴案件',[20,74,75],
    ['莱蒙案涉及奴隶主从弗吉尼亚前往得克萨斯、途经纽约时带入的八名被奴役者。纽约法院判他们自由；纽约州上诉法院于1860年维持该结果。它与逃亡奴隶遭追捕的问题不同。',
     '游戏担心此案进一步上诉后，最高法院会要求自由州承认带入境内者的奴隶身份。这是人物对未来判决的担忧，不是已经发生的联邦判决。原作采用Lemmon v. New York这一名称；纽约正式判例也以Lemmon v. People记载。'],
    [('纽约法院历史学会：莱蒙奴隶案','https://history.nycourts.gov/resource/lemmon-slave-case/'),
     ('纽约州上诉法院2022年判决回顾Lemmon v. People（1860）','https://www.nycourts.gov/reporter/3dseries/2022/2022_03859.htm')])
add('1860.personal-liberty','个人自由法与《逃奴法》',[14,62,63,64,180,181],
    ['1850年《逃奴法》加强了联邦追捕、遣返逃亡奴隶的机制。北方一些州的个人自由法则提供州级程序保障，或限制州官员、监狱协助执行。它们不是泛指保障所有个人自由的法律。',
     '例如马萨诸塞1855年法对主张奴隶所有权者的举证提出要求，并限制使用州内拘禁设施。游戏选项分别主张支持、回避或服从联邦法，译文保留这一争论，不悄悄合并成一致立场。'],
    [('美国参议院：梅森与1850年《逃奴法》','https://www.senate.gov/senators/FeaturedBios/Featured_Bio_MasonJamesMurray.htm'),
     ('马萨诸塞州图书馆：1855年第489章个人自由法原件','https://archives.lib.state.ma.us/bitstream/handle/2452/97312/1855acts0489.pdf?sequence=3')])
add('1860.land-grant-source','赠地大学与“中等教育”的原文疑点',[19,72,73,234,235,236,237],
    ['赠地大学通过联邦赠予公共土地等方式支持办学。1862年《莫里尔法》资助以农业和机械技艺为重点的学院，属于高等教育。',
     '原问题却写成land grant universities for secondary education，即“用于中等教育的赠地大学”。正文保留这个不协调的说法，在此指出中等教育与高等教育之别；不能据此认为这些大学是中学，也不能把1862年法案当作1860年已经生效的法律。'],
    [('美国国家档案馆：1862年《莫里尔法》','https://www.archives.gov/milestone-documents/morrill-act')],category='原文疑点／教育制度')
add('1860.homestead','宅地法：土地分配与1860年否决',[11,50,51,166,167,168,219],
    ['宅地政策讨论以公共土地支持定居与耕作，不能直接套用中国宅基地制度。1860年国会曾通过宅地法案，但布坎南总统否决了它。著名的《宅地法》直到1862年5月20日才由林肯签署。',
     '因此，游戏在1860年讨论是否支持宅地立法，有真实背景；不能把支持这一主张译成已经落实1862年法案。对自由劳动者与种植园主购买西部土地的不同表述，也分别保留。'],
    [('美国国家档案馆：1860年否决与1862年《宅地法》','https://www.archives.gov/legislative/features/homestead-act')])
add('1860.black-republicans','“黑色共和党”：种族化的竞选攻击',[129,142,158,159,160,187,188,189],
    ['“Black Republicans”是当时对共和党的种族化贬称，用来攻击其反对奴隶制扩张的政策、煽动对白人与黑人关系改变的恐惧。这里不能译成单纯表示族裔身份的“黑人共和党人”。',
     '1860年讽刺画就曾把所谓“Black Republicanism”与一名夸张描绘的黑人候选人联系起来。游戏选项是在重现这种攻击话术，校注解释其含义，不认可这类指控，也不把“反扩张”和“立即废奴”混为一谈。'],
    [('美国国会图书馆：1860年反共和党讽刺画及编目说明','https://www.loc.gov/item/2003674574/')],category='政治贬称／竞选修辞')
add('1860.john-brown','约翰·布朗突袭与1859年恐慌',[17,37,38,155,156,216],
    ['1859年10月16日，约翰·布朗及其追随者突袭哈珀斯费里的联邦军械库，试图推动反奴隶制起义。事件激化了南北恐惧与相互指责。',
     '原问题的late in 1859在这里指1859年后期，不应理解为12月发生。玩家可以谴责其违法行为，也可以批评南方的挑衅；这类可选立场不是每位候选人在现实中逐字说过的史料。'],
    [('美国国家公园管理局：约翰·布朗突袭经过','https://www.nps.gov/articles/john-browns-raid.htm'),
     ('美国国家公园管理局：布朗突袭与1860年选举','https://www.nps.gov/articles/000/john-brown-1860-election.htm')])
add('1860.freeport-doctrine','自由港学说：地方立法如何影响奴隶制',[172],
    ['1858年自由港辩论中，道格拉斯主张：即使最高法院承认将奴隶带入领地的权利，领地居民仍可通过不提供支持奴隶制的地方立法，使它难以维持。这个回答后来被称为自由港学说。',
     '这解释了游戏里他为什么一面不否认斯科特案判决，一面坚持居民反对就能阻止奴隶制发展。它不等于法院已经撤销原判，也不是联邦政府直接禁止奴隶制。'],
    [('美国国家公园管理局：自由港学说及1858年辩论','https://www.nps.gov/liho/learn/historyculture/freeport-doctrine.htm')])
add('1860.corwin-background','永久保护奴隶制的修宪主张',[7,67,68,69,182,183,184,224],
    ['危机中的妥协方案可能保护既有蓄奴州的制度，同时限制其扩张。1861年提出的科温修正案，试图禁止未来修宪赋予国会干预州内奴隶制的权力，但没有获得所需批准、成为宪法。',
     '1860年游戏问题是在询问一种尚待形成的妥协，并未指名这就是科温修正案。不能把它译成已经通过的法律，也不能把人物质疑“以后能否再修宪”的台词当作对永久性条款的确定法律裁判。'],
    [('美国国会访客中心：1861年科温修正案原件','https://www.visitthecapitol.gov/artifact/hj-res-80-proposing-amend-constitution-united-states-corwin-amendment-february-28-1861')],
    extra=[base[6]['source'],base[8]['source']])
add('1860.atlantic-slave-trade','禁止进口奴隶，不等于废除奴隶制',[12,58,59,175,176,222],
    ['美国禁止从海外输入奴隶的联邦法律于1808年1月1日生效，但奴隶制与美国境内的奴隶买卖继续存在。游戏讨论“重启跨大西洋奴隶贸易”，针对的是海外输入这一禁令。',
     '因此，反对重启贸易不必然意味着赞成立即废奴。译文把进口禁令、国内奴隶贸易和奴隶制本身区分开来。'],
    [('美国国家档案馆：奴隶贸易及1808年进口禁令','https://www.archives.gov/education/lessons/slave-trade.html')])
add('1860.naturalization-source','移民与入籍：nationalization的语境疑点',[15,53,169,170],
    ['原问题用的是nationalization，通常可指国有化；但上下文讨论外国移民，实际选项明确谈naturalization laws（入籍法）。本译文据此按“入籍”理解，并在这里公开说明，而不是另造一个国有化政策议题。',
     '入籍是取得公民身份的程序，不等同于入境或移民本身。1802年法律恢复了入籍所需的五年等待要求，这是当时讨论现行入籍法的历史背景。'],
    [('美国国家档案馆：1802年恢复入籍等待要求','https://www.archives.gov/exhibits/treasures_of_congress/Images/page_5/18a.html')],category='原文疑点／公民身份')
add('1860.fire-eaters','“喷火派”：激进的南方分离主义者',[],
    ['Fire-Eaters不是表演吞火的人，而是内战前激进维护奴隶制、鼓吹蓄奴州脱离联邦的一批南方人物。他们也有人要求恢复跨大西洋奴隶贸易。',
     '约翰逊介绍中反对“喷火派”，并不表示他反对一切奴隶制；格思里虽然是奴隶主并主张州权，也反对脱离联邦。奴隶主、州权派与分离主义者不能当作完全相同的标签。'],
    [('美国国家公园管理局：喷火派与南方分离运动','https://www.nps.gov/fosu/learn/historyculture/confederates.htm')],
    extra=[base[10]['source'],base[13]['source']])
add('1860.hunkers','Hunkers与“烧谷仓派”',[],
    ['Hunkers是纽约民主党内部较保守的派系，译文保留英文并说明为“保守派”；不宜把它当作全国统一的另一个政党。与之相对的Barnburners，则是更反对奴隶制扩张的一派。',
     'Barnburners的绰号借用了“为除掉老鼠，连谷仓也烧掉”的故事，用来讥讽改革过于激烈。这是政治派系之间的比喻性攻击，不是说这些人真的烧毁了谷仓。'],
    [('美国国家公园管理局：纽约民主党的Hunkers与Barnburners','https://www.nps.gov/mava/learn/historyculture/the-election-of-1848-free-soil-free-labor-free-men.htm')],
    extra=[base[14]['source']],category='政治派系／历史绰号')
ids={n['id'] for n in notes}
add('1860.fusion-electors','联合选票：不只是总统与副总统搭档',[107,126,150,151,152,153,154,200,212,213,231],
    ['1860年的fusion ticket在这些问题里，指反林肯阵营联合推出选举人名单，以减少分散选票；不是把不同总统候选人简单组成总统、副总统搭档。联合名单中的选举人可以支持不同的总统人选。',
     '新泽西的实际结果就分给林肯四张选举人票、道格拉斯三张。各州联合安排与选票细节不同，游戏的简化呈现不能当作一套全国统一的法律程序；译文解释术语，原有票数算法完全保留。'],
    [('马凯特大学法学院：1860年联合选票与新泽西结果','https://law.marquette.edu/facultyblog/2013/09/could-lincoln-have-been-defeated-in-1860/'),
     ('美国国家档案馆：1860年选举人票结果','https://www.archives.gov/electoral-college/1860')],extra=[supp[0]['source']])
add('1860.contingent-election','“国会选择”：总统实际由众议院选出',[],
    ['依据宪法第十二修正案，无人获得已任命选举人票的过半数时，总统由众议院从选举人票最多的至多三名候选人中选出。每个州代表团只有一票；副总统另由参议院按规则选出。',
     '原结局笼统说“国会选择”，应当结合这一制度理解。候选人位列前三只获得被选择的资格，并不自动获胜；仅仅阻止林肯获胜，也不一定意味着无人取得过半数。游戏的具体架空结局不等于历史上实际发生过这一轮投票。'],
    [('美国国家档案馆：第十二修正案及选举人团法律条文','https://www.archives.gov/electoral-college/provisions')],extra=[base[0]['source'],base[4]['source'],base[5]['source'],base[8]['source']])
ids={n['id'] for n in notes}
data['checkedAt']='2026-10-09'
data['notes']=[n for n in data['notes'] if n['id'] not in ids]+notes
(ROOT/'localization/annotations/notes.zh-CN.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
context=read(ROOT/'localization/reviews/glossary-context.zh-CN.json')
context['checkedAt']='2026-10-09'
added=[{'en':'Dred Scott v. Sandford','zh':'德雷德·斯科特诉桑福德案','avoid':'把联邦领地与已入联邦的州混同','noteId':'1860.dred-scott'},
    {'en':'personal liberty laws','zh':'个人自由法','avoid':'忽略其对逃奴遣返程序的历史语境','noteId':'1860.personal-liberty'},
    {'en':'land grant universities','zh':'赠地大学','avoid':'把原作secondary education错置当成高等教育事实','noteId':'1860.land-grant-source'},
    {'en':'Black Republicans','zh':'“黑色共和党人”（当时的贬称）','avoid':'单纯按族裔译成黑人共和党人','noteId':'1860.black-republicans'},
    {'en':'Fire-Eaters','zh':'喷火派','avoid':'吞火表演者／泛指所有南方人','noteId':'1860.fire-eaters'},
    {'en':'Hunkers','zh':'纽约民主党保守派（Hunkers）','avoid':'另一个全国性政党','noteId':'1860.hunkers'},
    {'en':'fusion ticket (1860)','zh':'联合竞选组合／联合选举人名单','avoid':'只按总统／副总统搭档理解','noteId':'1860.fusion-electors'}]
context['terms']=[t for t in context['terms'] if t['en'] not in {a['en'] for a in added}]+added
(ROOT/'localization/reviews/glossary-context.zh-CN.json').write_text(json.dumps(context,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched 1860 context notes.')
