"""Source-backed context for every fully read 1964 batch, exact English keys."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/1964-{p}-source-snapshot.json') for p in 'abc'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'1964.'+id,'title':title,'category':'历史制度／政治修辞',
        'contains':[parts[p][i]['source'] for p,indices in bindings for i in indices],
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('economic-dates','1964年的通胀与失业：原文数值有疑点',
    [('a',[22,62,63,64,65,73]),('b',[44]),('c',[6,7,8])],
    ['原作问题写通胀超过4%，一个选项又写失业率3%。总统经济报告的历史统计表显示，1964年CPI-U年度平均涨幅为1.3%，民间失业率年度平均为5.2%；12月同比CPI涨幅为1.0%。这些并不支持原文作为1964年全国通常指标的概括。',
     '译文保留原数字，旁注说明史实差异，没有改动游戏数值或选项效果。年度平均、单月值、不同物价指数必须区分；将通胀完全归咎于某个候选人的政策，仍是选项中的政治论证，不是统计表直接证明的因果关系。'],
    [('总统经济报告：表B-64，消费者价格指数变化（数据来源BLS）','https://www.govinfo.gov/content/pkg/ERP-2003/html/ERP-2003-table64.htm'),
     ('总统经济报告：表B-43，民间失业率（数据来源BLS）','https://www.govinfo.gov/content/pkg/ERP-2003/html/ERP-2003-table43.htm')])
add('great-society','伟大社会与Medicare：承诺、倡导与实施的区别',
    [('a',[20,61,71,72,73]),('b',[2,3])],
    ['伟大社会是约翰逊的改革议程，涉及减贫、教育、医疗等领域；并不是所有项目在1964年竞选时就已经立法或实施。Medicare的1965年法律于7月30日签署，主要制度在1966年开始运行。',
     '原选项中“扩大Medicare”的说法保留，但此时应联系尚在争取通过的老年医疗保险方案理解。福利、社会保障现金给付、老年医疗保险也不是同一种项目。原文“执政头两年”另有时间概括问题：约翰逊在1963年11月继任，至1964年大选尚不到一年，不能按两个完整任职年理解。'],
    [('美国国家档案馆：1965年Medicare与Medicaid法律','https://www.archives.gov/milestone-documents/medicare-and-medicaid-act'),
     ('美国社会保障署：签署与筹备运行的历史','https://www.ssa.gov/history/ssa/lbjmedicare1.html'),
     ('美国国务院人物资料：肯尼迪任期至1963年','https://history.state.gov/historicaldocuments/frus1964-68v14/persons')])
add('school-prayer','学校祷告案：官方组织与个人信仰',
    [('a',[21,54,55,56,57])],
    ['1962年恩格尔诉维塔莱案涉及纽约公立学校采用官方制定的祷文。最高法院认为，政府组织的这种宗教活动违反第一修正案的政教分离原则，即便祷文声称不属于某一教派、学生可以不参加，也不能消除问题。',
     '原问题以“强制学校祷告”简写，不能扩写成法院禁止孩子所有私人祈祷、禁止信仰或禁止一切道德教育。选项中关于道德沦丧或宗教自由的说法，分别是候选人立场。'],
    [('美国联邦法院教育资料：恩格尔诉维塔莱案事实与理由','https://www.uscourts.gov/sites/default/files/freedom-religion_0.pdf'),
     ('美国判例汇编原件：370 U.S. 421','https://www.govinfo.gov/app/details/USREPORTS-370/USREPORTS-370-421')])
add('soviet-offices','赫鲁晓夫下台：党领导人与总理分由两人接任',
    [('a',[25,68]),('b',[11])],
    ['1964年10月，赫鲁晓夫被迫下台。勃列日涅夫接任苏共中央第一书记；柯西金接任部长会议主席，即总理。不能把党领导人与政府总理合并成勃列日涅夫一个职位。',
     '原问题用勃列日涅夫概括这次权力更替，正文保留其叙事，旁注说明两人的职务。勃列日涅夫的称号在1966年才改为总书记；“这损害戈德华特竞选”的说法是游戏判断，不是当时国务院文件证明的选票测量。'],
    [('美国国务院：1964年10月17日评估赫鲁晓夫更替的备忘录','https://history.state.gov/historicaldocuments/frus1964-68v14/d58'),
     ('美国国务院：勃列日涅夫、赫鲁晓夫与柯西金的职务时间','https://history.state.gov/historicaldocuments/frus1964-68v14/persons')])
add('reagan-speech','《抉择的时刻》：里根为戈德华特助选',
    [('a',[27,69]),('b',[5])],
    ['里根1964年10月27日的电视演说，后来通常以《抉择的时刻》闻名，支持戈德华特，阐述减小政府、个人自由、强硬反共和自由与集权对立的政治主张。此时他是演员和政治演说者，还不是总统。',
     '这些是演说者的立场，不是译者认定所有数据与指控都正确。游戏里“他该继续拍电影”的话，是对跨入政治领域的嘲讽，并非对后来里根政治生涯的历史结论。'],
    [('里根总统图书馆：1964年10月27日演说全文','https://www.reaganlibrary.gov/archives/speech/time-choosing-speech')])
add('baker','博比·贝克：国会调查不等于刑事审判',
    [('a',[11,16,51,52,53]),('b',[10,21,27,28,37,74]),('c',[26])],
    ['博比·贝克曾担任参议院多数党秘书，1963年辞职后受到调查。参议院规则与行政委员会在1963至1964年举行听证，调查利益冲突与财务不当行为。',
     '原反馈在1964年说“贝克审判”，正文保留，但国会听证不是法院刑事审判；参议院后来的调查史料把贝克的法院审判记在1967年。贝克、埃斯蒂斯与约翰逊的关联被用作竞选攻击，也不能只凭关联就推定总统本人参与了每项欺诈。游戏中对某个回答“撒谎”的评价是顾问反馈，旁注不扩写为独立司法定罪。'],
    [('美国参议院：1964年贝克案调查及听证日期','https://www.senate.gov/about/powers-procedures/investigations/select-investigations.htm'),
     ('美国参议院情报调查史料：贝克审判1967年开始','https://www.intelligence.senate.gov/sites/default/files/94intelligence_activities_VI.pdf')])
add('confessions-ad','《一个共和党人的自白》：竞选广告的角色发言',
    [('a',[17,49,50]),('b',[29])],
    ['这是约翰逊阵营1964年的电视广告，画面中的共和党选民角色表达对戈德华特的担忧，并表示宁愿投民主党候选人。广告用跨党派选民的叙述争取温和派，不是司法意义的认罪自白。',
     '广告原件与对白保存在影像博物馆的竞选广告档案中，影像来自约翰逊图书馆。游戏说它在北方“引起轰动”，是效果反馈，不能把一则广告推定为所有共和党选民的真实意见。'],
    [('影像博物馆Living Room Candidate：1964年广告原件与对白','https://livingroomcandidate.org/commercials/1964/confessions-of-a-republican')])
add('klan','三K党背书与候选人立场：不是会员身份的同义词',
    [('a',[23,28,66,67]),('b',[45,47]),('c',[9,10,11,12,38])],
    ['阿拉巴马州三K党领导人支持戈德华特，成为1964年竞选攻击的重要素材。但某个极端团体的支持，并不自动证明候选人是该团体成员；是否谴责、是否接受支持、是否赞同其主张也是不同问题。',
     '国家档案馆依据竞选史料讨论了戈德华特、米勒及团队对种族议题和背书的不同反应。选项可选择拒绝、沉默或辩护，保留其政治区别；顾问预测南方或北方选票得失，不当作所有当地选民态度一致的证明。'],
    [('美国国家档案馆Prologue：1964年白人反弹、背书与候选人的反应','https://www.archives.gov/publications/prologue/2001/spring/lbj-and-white-backlash-1'),
     ('影像博物馆：1964年三K党背书攻击广告原件','https://livingroomcandidate.org/commercials/1964/kkk')])
add('civil-rights-act','1964年民权法：民权、州权与执行现行法律',
    [('a',[12,13,14,31,32,33,44,45,46]),('b',[39,51,52,53,63,68]),('c',[16,30,34,36,45])],
    ['1964年《民权法案》针对公共设施、就业等领域的歧视，并扩展联邦执行权。它不等于当年已经通过1965年《投票权法》，也不能概括成一签字便解决所有种族隔离与投票障碍。',
     '反对某项法律、希望国会废除它、承诺总统依法执行它，是可以并存的立场。州权在这些段落里与种族隔离争论相联系，保留其政治含义；跨区校车接送则是学校融合手段，不是普通公共交通。原选项关于创建NAACP州分会的具体个人功绩仍需专门档案核对，本条法案来源不证明该个人传记细节。'],
    [('美国国家档案馆：1964年《民权法案》原件与各项保障','https://www.archives.gov/milestone-documents/civil-rights-act'),
     ('美国参议院：结束民权法案冗长辩论','https://www.senate.gov/about/powers-procedures/filibusters-cloture/civil-rights-filibuster-ended.htm')])
add('southern-geography','南方重组与“边界州”：原文地理概括',
    [('a',[0,12,36,60]),('b',[7,61]),('c',[19,27,44])],
    ['原背景说自重建以来首次让南方转向共和党，若理解为任何南方州首次投共和党，则不准确：1928年胡佛已赢得德克萨斯、佛罗里达、弗吉尼亚等南方州。戈德华特在深南部的突破，与整个南方同时转党不是一回事。',
     '原选项把阿肯色、田纳西和北卡罗来纳称为border states，保留这个称呼，但它们不是内战中留在联邦的典型蓄奴边界州；那些通常指特拉华、马里兰、肯塔基、密苏里及后来成立的西弗吉尼亚。这里应理解为竞选路线的较宽泛地域说法，不擅自改州名单或访问效果。'],
    [('美国国家档案馆：1928年各州选举结果','https://www.archives.gov/electoral-college/1928'),
     ('美国国家公园管理局：内战边界州的构成与历史','https://www.nps.gov/articles/the-border-states.htm')])
add('ending-rhetoric','结局的夸张、杜威典故与连任资格',
    [('a',[2,3,4,5,6])],
    ['“最好读读杜威的经历”借1948年民调看好杜威却最终败选的逆转，讽刺玩家丢掉巨大优势；不是说1964年真实历史也发生了戈德华特获胜。1948年真实败者与模拟胜者分别看待。',
     '原作“一个多世纪以来首次选举夜没有胜者”是夸张概括，1876年海斯与蒂尔登的争议就拖到次年。平局时众议院选总统按州代表团投票，参议院另选副总统，不能只用全院党派席位推出必然结果。',
     '第二十二修正案规定，为他人任期代任超过两年者只能再获选一次。约翰逊1963年11月继任至1965年1月不足两年，故1964年当选后仍可争取1968年提名；原作胜利结局不需要为此修改游戏规则。'],
    [('杜鲁门总统图书馆：1948年选举','https://www.trumanlibrary.gov/education/presidential-inquiries/election-1948'),
     ('美国国家档案馆：1876年争议选举','https://www.archives.gov/electoral-college/1876'),
     ('美国国家档案馆：第十二及第二十二修正案','https://www.archives.gov/founding-docs/amendments-11-27')])
path=ROOT/'localization/annotations/notes.zh-CN.json';data=read(path)
old={n['id']:n for n in data['notes']};old.update({n['id']:n for n in notes})
data['notes']=list(old.values());data['checkedAt']='2026-10-09'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched 1964 notes')
