"""Author researched offline notes against the immutable 1916 review snapshots."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/1916-{p}-source-snapshot.json') for p in 'abcd'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'1916.'+id,'title':title,'category':'历史制度／政治修辞',
        'contains':[parts[p][i]['source'] for p,indices in bindings for i in indices],
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('hyphenated','“带连字符的美国人”：族裔身份与忠诚争论',
    [('a',[22,26]),('b',[16,17,18,26,27,28,74]),('c',[23,24,28]),('d',[47])],
    ['英文中的族裔称呼常用连字符连接，例如German-American。“带连字符的美国人”在战争时期的争论中，被用来质疑移民及其后裔的忠诚，并不是一个法律上的国籍类别。',
     '国会图书馆保存的1916年讽刺画，直接讽刺以这种称呼攻击不投票支持威尔逊的人。游戏里的“美国人身份优先”和“铁血爱国”带有当时民族主义、排外争论的色彩；不能把德裔或爱尔兰裔整体描述成已经被证实的不忠者。'],
    [('国会图书馆：1916年关于威尔逊与hyphen的政治讽刺画','https://loc.gov/pictures/item/2016685411/')])
add('revenue-date','1916年税法与“超额利润税”的时间差',
    [('a',[14,59,60,61]),('b',[53,54,55])],
    ['原作把1916年收入法中的遗产税与“超额利润税”并列，正文保留这一说法。美国税务局1918年的报告则区分：1916年对军火制造净所得征税，第一项一般性的超额利润税来自1917年3月3日的法律。',
     '因此，不宜把1916年的军火制造税与后来的一般超额利润税混为一谈。这里是原作的年代／分类问题，并非允许汉化调整税率、选项效果或事件时间。'],
    [('美国税务局：1918年局长报告中的1916及1917税法沿革','https://www.irs.gov/pub/irs-soi/1918dbfullar.pdf')])
add('literacy','移民识字测试：不是只准考英语',
    [('a',[27]),('b',[19,20,21,25,26])],
    ['原问题将拟议的移民测试写成英语识字测试，正文保留原文。1917年实际生效的识字条款允许用某种语言或方言阅读，并有若干豁免，并非一律要求读英语。',
     '国务院保存的1917年劳工部长函件明确讨论这项测试及配偶豁免。游戏发生在1916年竞选期间，支持或反对拟议法案，与已经实施后的法律规定需要分开理解。'],
    [('美国国务院：1917年6月27日关于识字测试及豁免的函件','https://history.state.gov/historicaldocuments/frus1917/d1063')])
add('child-labor','《基廷—欧文法》：州际贸易限制与后来的判决',
    [('a',[13,62,63]),('b',[56,57]),('c',[44]),('d',[6,7,8,32])],
    ['1916年的《基廷—欧文法》借联邦监管州际贸易的权限，限制使用某些童工的工厂、矿场等产品流通；不是联邦已经永久、全面禁止所有未成年人工作的法律。',
     '最高法院在1918年的哈默诉达根哈特案中判该法违宪。游戏的1916年人物讨论支持、州权或联邦权限时，尚不能把这个后来的判决当成已经发生。原问题的Keating-Owens拼写对应通常所称的Keating-Owen Act。'],
    [('美国国家档案馆：1916年法案原件、限制范围与1918年判决','https://www.archives.gov/milestone-documents/keating-owen-child-labor-act')])
add('brandeis','布兰代斯提名：进步主义与犹太身份争论',
    [('a',[7,43,44]),('b',[42]),('c',[40,61]),('d',[20])],
    ['威尔逊1916年提名布兰代斯，引发强烈争议和长时间公开听证。他成为最高法院第一位犹太裔大法官，进步主义立场和职业经历也卷入提名争论。',
     '原作选项提到“犹太人问题”，保留了当时带有偏见的政治措辞；旁注不认同这种偏见，也不把游戏中每一句可选的反对发言都当作休斯的真实引语。'],
    [('美国参议院：司法提名史中的1916年布兰代斯听证','https://www.senate.gov/about/powers-procedures/nominations/judicial-nominations-overview.htm'),
     ('美国参议院：布兰代斯获确认的历史','https://www.senate.gov/artandhistory/history/common/briefing/Nominations.htm')])
add('jones-philippines','1916年的《琼斯法》：菲律宾自治与独立承诺',
    [('a',[28,64,65,66]),('b',[58,59]),('c',[5])],
    ['此处指1916年菲律宾自治立法，扩大民选政府并表达未来独立的方向；不是1920年美国沿海航运中也俗称《琼斯法》的法律。',
     '更大的自治权、立即独立和以后独立是不同政策。菲律宾实际于1946年独立，不能把游戏中“立即独立”的可选主张当成1916年已完成的历史事实。'],
    [('美国众议院：菲律宾相关立法与1916年自治法','https://history.house.gov/Exhibitions-and-Publications/APA/Historical-Data/Legislation/'),
     ('美国国务院：美菲战争及自治、独立的后续时间线','https://history.state.gov/milestones/1899-1913/war')])
add('villa-expedition','潘兴远征：抓捕比利亚与墨西哥主权',
    [('a',[20,50,51,52]),('b',[46,47]),('c',[39]),('d',[0,1,2,28])],
    ['潘乔·比利亚的部队1916年袭击新墨西哥州哥伦布镇后，美国派潘兴率军进入墨西哥追捕。比利亚并不等于卡兰萨政府，美军与该政府之间也有主权和军事行动的冲突。',
     '远征最终未能抓到比利亚。游戏中限制行动区域、增强边境防卫、支持墨西哥合法政府与全面深入追捕，是不同的选项，译文保留这些差别。'],
    [('美国国家公园管理局：哥伦布镇、卡兰萨与远征','https://www.nps.gov/places/village-of-columbus-and-camp-furlong-columbus-new-mexico.htm'),
     ('国会图书馆：袭击之后的美墨关系','https://www.loc.gov/exhibits/mexican-revolution-and-the-united-states/us-mexico-relations-post-columbus-nm.html')])
add('easter-rising','复活节起义：爱尔兰问题与美国竞选',
    [('d',[35,38,39,40,44,45,46,47])],
    ['1916年4月24日至29日，爱尔兰独立派在都柏林发动起义，随后面临拘押、军事审判及处决。它不是宗教节庆活动引发的小规模纠纷。',
     '美国竞选涉及爱尔兰裔选民、对英关系以及是否应呼吁宽大处理。支持起义者、避免得罪英国与将它视为英国内政，是原作不同的政治立场。'],
    [('国会图书馆：复活节起义的同期报刊研究指南','https://guides.loc.gov/chronicling-america-1916-easter-rising/?loclr=bloglaw'),
     ('英国国家档案馆：起义、军事审判及减刑档案','https://www.nationalarchives.gov.uk/help-with-your-research/research-guides/ireland-easter-rising-1916')])
add('california-snub','休斯与约翰逊：“怠慢”传闻不等于唯一败因',
    [('c',[43,66,67,68]),('d',[21,22])],
    ['原作以州长海勒姆·约翰逊是否感到遭到怠慢，表现加利福尼亚共和党传统派与进步派之间的裂痕。同期报刊中确有“怠慢”说法及否认它的辩解，不能把这个争议压缩成已经证实的一句因果结论。',
     '加利福尼亚最终投给威尔逊，其13张选举人票对结果很重要。但“若见了一面就必定胜选”是反事实推断，并非票数档案能够证明的事实。'],
    [('俄勒冈大学同期报刊档案：1916年11月11日关于怠慢说的争论','https://oregonnews.uoregon.edu/lccn/sn85042444/1916-11-11/ed-1/seq-3/ocr/'),
     ('美国国家档案馆：1916年各州选举人票结果','https://www.archives.gov/electoral-college/1916')])
add('hughes-court','休斯离开最高法院：失去席位并非终身无法返回',
    [('a',[4,5]),('c',[63])],
    ['休斯在1916年离开最高法院参加总统竞选，落选后没有自动恢复原来的大法官席位。原作结局讨论这次选择的代价。',
     '他后来出任国务卿，又于1930年出任首席大法官。因此“这次失去席位”不能被理解为他此后从未重返最高法院。游戏的胜选叙事和替代搭档情节，属于模拟结果。'],
    [('美国国务院：查尔斯·埃文斯·休斯的任职经历','https://history.state.gov/departmenthistory/people/hughes-charles-evans')])
add('burkett-name','伯克特人名：原作的Haskett与档案不符',
    [('d',[33,37])],
    ['这一搭档分支的原问题称Elmer Haskett，后续选项称Burkett。美国众议院人物档案记载的内布拉斯加州前参议员，是埃尔默·雅各布·伯克特（Elmer Jacob Burkett）。正文保留原问题的哈斯克特写法，在此说明原作人名不一致。',
     '这不表示游戏新增了另一位副总统候选人。1916年实际共和党搭档是费尔班克斯，伯克特分支是可选的模拟组合。'],
    [('美国众议院：埃尔默·雅各布·伯克特人物档案','https://history.house.gov/People/Detail/10198'),
     ('美国国家档案馆：1916年总统与副总统选举结果','https://www.archives.gov/electoral-college/1916')])
add('early-succession','威尔逊提前交权：不是胜选者自动继任',
    [('a',[2,4])],
    ['国务卿罗伯特·兰辛在回忆录中记述：威尔逊考虑过，如果休斯胜选，就先任命休斯为国务卿，再由总统和副总统马歇尔辞职，借当时的继任安排提前交权。这是一项未实施的预案。',
     '正文简略说“辞职，让你马上就职”，不应理解为总统一辞职，尚未就任的胜选者便自动接任。替代搭档分支也不能据此认定所有人物都会接受这套安排。'],
    [('罗伯特·兰辛《战争回忆录》：1916年竞选章，第165—166页（公开转录）','https://dokumen.pub/war-memoirs-of-robert-lansing.html')])
add('peace-slogan','“他让我们置身战争之外”：1916年的竞选口号',
    [('a',[34,36,37,38,39,40,41,42]),('b',[35,37,38,39,40]),('c',[37,52,53,54,55,56,57])],
    ['“他让我们置身战争之外”强调威尔逊此前任内没有使美国参战，是1916年民主党竞选的重要口号。不能把它自动改写成无论情况如何、永不参战的法律保证。',
     '兰辛的回忆录记述了口号传播及共和党对中立政策的批评。游戏中的“投休斯就是投战争”是人物的可选攻击话术，这里不将它认证为某位候选人的逐字史实引语。'],
    [('罗伯特·兰辛《战争回忆录》：1916年竞选章，第160—162页（公开转录）','https://dokumen.pub/war-memoirs-of-robert-lansing.html')])
add('workers-compensation','工伤赔偿：联邦雇员与危险行业的范围差别',
    [('d',[34,41,42,43])],
    ['工伤赔偿针对因工作受伤或职业病等情形提供补偿，不是普遍加薪。1916年《联邦雇员赔偿法》扩展了联邦文职雇员的保护。',
     '原作分别提供建立更广泛的危险行业制度、仅支持联邦雇员措施及反对的选项。它们的适用范围不同，不能在中文中合并成一句“支持工人福利”。'],
    [('美国劳工部：1916年联邦雇员赔偿立法沿革','https://www.dol.gov/sites/dolgov/files/owcp/dfec/icstraining/fecaoverview/historical_overview.html')])
add('league-future','国际联盟：1916年仍是未来设想',
    [('a',[23,70,71,72]),('c',[7,8])],
    ['1916年已有关于战后国际组织的倡议，但国际联盟正式开始活动是在1920年1月10日。游戏所说“若战后成立”，讨论的是未来设想，不是1916年已存在的组织。',
     '反对干预欧洲、暂缓判断与支持未来组织，表达的是不同的外交立场；国际联盟也不能直接译成后来的联合国。'],
    [('联合国日内瓦办事处：国际联盟设想与正式成立时间','https://www.ungeneva.org/en/about/league-of-nations/background')])
path=ROOT/'localization/annotations/notes.zh-CN.json';data=read(path)
old={n['id']:n for n in data['notes']};old.update({n['id']:n for n in notes})
data['notes']=list(old.values());data['checkedAt']='2026-10-09'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
gpath=ROOT/'localization/reviews/glossary-context.zh-CN.json';g=read(gpath)
terms={t['en']:t for t in g['terms']}
for en,zh,avoid,noteId in [
    ('hyphenated American','带族裔前缀的美国人／带连字符的美国人','独立法律国籍类别','1916.hyphenated'),
    ('workers’ compensation','工伤赔偿','工人工资补贴',''),
    ('Jones Act (1916 Philippines)','《琼斯法》／菲律宾自治法','1920年沿海航运法','1916.jones-philippines'),
    ('political machine','政治机器／政党组织网络','机械设备',''),
    ('Preparedness (1916)','备战／加强国防准备','已正式参战',''),
    ('Easter Rising','复活节起义','宗教节日纠纷','1916.easter-rising')]:
    terms[en]={'en':en,'zh':zh,'avoid':avoid,'noteId':noteId}
g['terms']=list(terms.values());g['checkedAt']='2026-10-09';g['era']='1844 / 1860 / 1896 / 1916 / 1964 / 1968'
gpath.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched 1916 notes')
