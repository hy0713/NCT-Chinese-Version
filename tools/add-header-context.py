"""Authoring record for the remaining native header allusions, researched 2026-10-08.
Normal maintenance edits the JSON directly; this script records the authored batch.
Only exact original header sources are bound, never live DOM text.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'localization/annotations/header-notes.zh-CN.json'
data=json.loads(path.read_text(encoding='utf-8'))
quotes=json.loads((ROOT/'localization/annotations/header-editorial-review.json').read_text(encoding='utf-8'))['records']
rows=[
('ford.snl','gerald ford,','福特回应《周六夜现场》','电视喜剧梗',[
'切维·蔡斯在《周六夜现场》中模仿福特，也以“我是切维·蔡斯，你不是”作为开场白。1976年福特借用句式回应这位模仿者，随后还以预录片段参与节目。笑点是被模仿的人反过来模仿喜剧演员。'],
[('福特1976年3月26日回忆前一晚与蔡斯的互动','https://www.presidency.ucsb.edu/documents/remarks-president-ford-committee-fundraising-dinner-los-angeles-california'),('TIME：福特与1976年《周六夜现场》','https://time.com/4292027/gerald-ford-saturday-night-live/')]),
('carville.economy','economy stupid','“笨蛋，问题是经济”','竞选内部口号',[
'1992年克林顿团队的策略师詹姆斯·卡维尔用这句话提醒团队把注意力放在经济上。Stupid是对自己团队的粗直提醒，不是指称选民愚蠢；它也不应自动署名为克林顿本人在演说中说的原话。'],
[('弗吉尼亚大学米勒中心：克林顿竞选与选举','https://millercenter.org/president/clinton/campaigns-and-elections')]),
('machiavelli.attribution','politics have no','马基雅维利署名尚未核实','署名存疑／思想概括',[
'游戏把“政治与道德无关”署名为马基雅维利。本次没有在所查《君主论》英译全文中定位到这句逐字表述，不能仅凭名言网站确认出处。','《君主论》第十五章讨论统治者如何面对现实中的善恶与权力维持；这能解释常见的“马基雅维利主义”联想，却不足以证明该短句就是作者原话。保留游戏署名，并明确列为待考。'],
[('《君主论》W. K. Marriott英译全文，第十五章','https://www.gutenberg.org/files/1232/1232-h/1232-h.htm')]),
('bush.iraq-wmd','weapons of mass destruction','伊拉克大规模杀伤性武器说法','战前主张／事后调查',[
'这是对小布什政府伊拉克战争论述的概括。2003年政府以萨达姆政权的大规模杀伤性武器威胁为重要理由；2005年美国调查委员会随后认定，战前情报对伊拉克此类武器的判断几乎全错。','旁注区分当时政府的主张与后来的调查结论；页眉不能当作今天已经证实的事实。这段游戏短句也不是已核实日期的逐字演说引文。'],
[('2003年3月17日总统对伊拉克问题的全国讲话','https://2001-2009.state.gov/p/nea/rls/rm/18789.htm'),('2005年大规模杀伤性武器情报调查委员会报告','https://www.govinfo.gov/content/pkg/GPO-WMD/pdf/GPO-WMD.pdf')]),
('grant.judgment','my failures','“判断失误，并非蓄意”','历史文献／游戏简写',[
'格兰特在1876年最后一次年度咨文中承认政府犯过错误，尤其谈到任命助手时对人选缺乏了解，并为自己的主观用意辩护。游戏用了原句的简写，中文保留“判断”与“意图”的区别。','这是一位总统对自己任期的辩解，不是旁注替他证明所有决定正确，也不是对再建时期争议的完整评价。'],
[('格兰特1876年12月5日第八次年度咨文','https://www.presidency.ucsb.edu/documents/eighth-annual-message-3')]),
('nixon.frost','when the president does','尼克松与弗罗斯特访谈','访谈名场面',[
'尼克松在1977年弗罗斯特访谈中说过这句话。相关问答讨论1970年“休斯顿计划”及总统权限；影视作品后来将它移入水门掩盖事件的讨论，容易使观众记错原始提问。','解释访谈语境不等于认同这项法律主张。游戏短句保留其震撼效果，不能用它概括总统在法律上可以任意行事。'],
[('尼克松基金会：原访谈与《福斯特对话尼克松》的语境差异','https://www.nixonfoundation.org/2008/12/further-notes-on-frostnixon/')]),
('lincoln.law-lecture','leave nothing','林肯谈律师的勤勉','历史文献',[
'这句劝人不要拖延的话可追溯到约1850年的法律讲课笔记，处于对律师勤勉工作的劝告中。它与另一个署名林肯的“磨斧头”故事不同，所查资料给出了明确的文献归属。'],
[('林肯协会：语录及法律讲课笔记出处','https://www.abrahamlincoln.org/features/speeches-writings/abraham-lincoln-quotes/index.html')]),
('king.birmingham','injustice anywhere','《伯明翰狱中书简》','民权文献',[
'马丁·路德·金在1963年的《伯明翰狱中书简》中用这句话说明不同地方的正义相互关联，并回应把民权行动者视作“外来煽动者”的指责。它强调共同责任，不能缩成对某一地方的孤立评论。'],
[('萨姆福德大学：神职人员公开信与金的回复全文','https://www.samford.edu/arts-and-sciences/files/History/Statement-and-Response-King-Birmingham.pdf')]),
('kennedy.dream','the dream shall','“梦想永不消逝”','落选演说／政治修辞',[
'爱德华（泰德）·肯尼迪在1980年民主党全国大会上，经历提名之争失败后发表这篇演说。结束语强调，自己的竞选告一段落，但关心社会与经济正义的事业仍应继续。','这里的“梦想”是政治理想的延续，不是在预言他赢得总统提名。'],
[('爱德华·肯尼迪研究所：1980年大会演说','https://emkinstitute.org/senator-kennedy/senator-kennedy-speeches/')]),
('eisenhower.principle','change based on','有原则的改变与混乱','竞选演说',[
'艾森豪威尔在1956年接受共和党提名的演说中，用这对句子区分有原则的进步与没有原则的反复变动。它强调他对稳定和改革的理解，不是宣称任何改变都会造成混乱。'],
[('艾森豪威尔图书馆：语录及1956年8月23日出处','https://www.eisenhowerlibrary.gov/eisenhowers/quotes')]),
('reagan.freedom','freedom is never','自由不能自动传给下一代','政治修辞',[
'里根在多个场合重复这个表述，强调自由需要每一代人维护，而不是自动继承。这里“一代人”是修辞警告，并非经过计算得出的消亡期限；1983年纪念马丁·路德·金时，他也用过同一句话。'],
[('里根图书馆：1983年1月15日纪念马丁·路德·金讲话','https://www.reaganlibrary.gov/archives/speech/remarks-anniversary-birth-martin-luther-king-jr')]),
('roosevelt.bull-moose-shot','just been shot','西奥多·罗斯福中枪后演说','历史轶事／硬汉形象',[
'1912年10月14日，正在以进步党候选人身份竞选的西奥多·罗斯福在密尔沃基遭枪击，仍坚持演说。他开头告诉听众自己刚中枪，接着借“公麋鹿”形象逞强；这是实际枪击后的话，不是比喻性抱怨。','游戏开头称呼略有改写。这里是西奥多·罗斯福，不是新政时期的富兰克林·罗斯福。'],
[('1912年10月14日密尔沃基演说全文','https://www.presidency.ucsb.edu/documents/the-progressive-cause-greater-than-any-individual-remarks-milwaukee-wi')]),
('vietnam.wont-go',"hell no, we won't go",'“我们不去”：拒绝征兵','反战口号',[
'这是越战时期反征兵、反战示威的著名喊话。“不去”指拒绝被征召参与战争，并非拒绝去投票。原句有强烈粗口，中文保留愤怒的抗议口吻。'],
[('洛杉矶公共图书馆：1968年拒绝征兵横幅馆藏','https://www.lapl.org/vi/event/11275')]),
('vietnam.hey-lbj','hey, hey, lbj','“LBJ，你今天害死了多少孩子？”','反战口号',[
'LBJ指林登·约翰逊。这句越战反战喊话通过押韵和重复，把战争造成的死亡直接归责于总统，目的在于强烈施压。','这是示威者的指控性修辞，不是逐日死亡统计，也不是游戏报告的选举数据。中文保留质问和指责。'],
[('LIFE／TIME：1968年反战示威及约翰逊家人的回忆','https://time.com/5106608/protest-1968/')]),
('edwards.crook','vote for the crook','“投给贪腐的家伙”为什么还很重要？','1991年选举黑色幽默',[
'1991年路易斯安那州州长决选中，埃德温·爱德华兹面对曾任三K党头目的戴维·杜克。反对杜克的人用这个非正式口号，承认对爱德华兹廉洁声誉的疑虑，同时认为阻止杜克更为迫切。','Crook在这里影射政治腐败，单译成普通“骗子”会丢失背景。它表达的是特定选举中的两害相权，并非普遍提倡腐败。'],
[('TIME：1991年11月25日路易斯安那决选报道','https://time.com/archive/6719072/louisiana-the-no-win-election/')]),
('long.every-man-king','every man a king','人人为王，但无人戴王冠','财富再分配口号',[
'“人人为王”与休伊·朗的“分享财富”运动相连。1934年的广播演说提出限制巨额财富、保障家庭基本生活，King在这里表示普通人也应拥有生活尊严，不是倡议人人建立君主制。','“但无人戴王冠”强化了这种平等意象。本次来源直接支持“人人为王”演说和纲领；不将更长版本的最早出现时间认定为已查实。'],
[('美国参议院：休伊·朗1934年“人人为王”广播演说','https://www.senate.gov/artandhistory/history/resources/pdf/EveryManKing.pdf')]),
('coolidge.keep-cool','keep cool with','Cool与Coolidge的双关','竞选口号',[
'这个1924年口号把“保持冷静”的Cool与柯立芝的姓Coolidge拼在一起，也呼应他沉着寡言的公众形象。中文难以照搬同音双关，因此说明保留英文拆词帮助理解；不是让玩家给电脑降温。'],
[('Richard F. Brush美术馆：1924年竞选贴纸馆藏（JSTOR）','https://www.jstor.org/stable/community.28445738')]),
('lincoln.swap-horses',"don't swap horses",'渡河中途不要换马','1864年竞选比喻',[
'林肯在1864年回应支持提名的代表时引用过这个渡河比喻，表达战争尚未结束时不宜更换领导者。游戏采用口号形式；Horses指承担重任的政治领导人，不是游戏中的骑马行动。'],
[('迪金森学院：1864年6月9日回应联邦派代表的文字','https://housedivided.dickinson.edu/sites/lincoln/letter-to-union-delegation-june-9-1864/')]),
('kennedy.dare-fail','only those who','敢于失败，才可能成就大事','演说改写',[
'罗伯特·肯尼迪在1966年开普敦大学演说中谈到面对危险坚持理想的勇气，随后说敢于承受重大失败才可能取得重大成就。游戏的courage版本改写了原句的dare，意思接近，但不是逐字引用。','这句话出自围绕个人责任、自由与社会变革的演说；不能据此添加原文没有的竞选策略或胜率承诺。'],
[('肯尼迪图书馆：1966年6月6日开普敦演说','https://www.jfklibrary.org/learn/about-jfk/the-kennedy-family/robert-f-kennedy/robert-f-kennedy-speeches/day-of-affirmation-address-university-of-capetown-june-6-1966')]),
('goldwater.heart','in your heart','“内心深处，你知道他是对的”','竞选口号',[
'这是戈德华特1964年竞选使用的口号，可见于当年的竞选徽章。Right既可指“正确”，也容易让人联想到他的右翼立场；它是争取认同的动员语，不是游戏对他的政策作出的客观判定。'],
[('爱达荷大学图书馆：1964年戈德华特徽章','https://www.lib.uidaho.edu/digital/buttons/items/mg660_box1_9-0452.html')]),
('henry.liberty-death','give me liberty','“不自由，毋宁死”的文本来源','革命演说／事后重构',[
'帕特里克·亨利1775年的演说与弗吉尼亚准备对抗英国有关；这句成为美国革命的经典号召。它没有留下当场逐字稿，今天通行的全文由威廉·沃特在1817年传记中根据回忆重构。','因此应区分真实演说事件与后世流传的确切措辞，不把重构文本当作当年的完整速记记录。'],
[('弗吉尼亚图书馆：1775年演说与1817年重构说明','https://www.lva.virginia.gov/collections/educator-resources/dbva/items/show/324')]),
('taft.bryan-again','vote for taft','布赖恩怎么“哪次都能投”？','竞选讽刺／出处待细查',[
'笑点是布赖恩反复获得民主党总统提名：1896、1900年失利后，1908年又与塔夫脱竞争。意思是“这次先投塔夫脱，布赖恩往后还会再来”，不是投票规则允许随时投票。','这句话被后来的选举史资料列作共和党的讽刺口号。本次没有定位到当年载有完全相同措辞的印刷品，因此最早载体与具体作者仍待考。'],
[('1908年布赖恩竞选资料及提名史','https://en.wikipedia.org/wiki/William_Jennings_Bryan_1908_presidential_campaign')]),
('blaine.continental-liar','blaine, blaine','“举国大骗子”：反布莱恩顺口溜','1884年竞选攻击',[
'1884年针对共和党候选人詹姆斯·G.·布莱恩的顺口溜，把Blaine与Maine押韵。Continental强调全美国范围，不是在说他来自欧洲大陆；译为“举国大骗子”保留夸张的辱骂力度。','这是对手的竞选攻击，不是旁注已经裁定的事实。中文押韵难以完全对应，说明同时保留英文词尾的联系。'],
[('美国国会图书馆：1884年选举与反布莱恩歌谣','https://blogs.loc.gov/folklife/2016/11/election-week-special-the-dodger-and-the-election-of-1884/')]),
('eisenhower.like-ike','i like ike','I Like Ike：简短又押韵','竞选口号',[
'Ike是艾森豪威尔的昵称。1952年“我喜欢艾克”口号借Like与Ike押韵，广泛用于徽章、海报和歌曲；核心是把战时将领的亲切形象转化为对候选人的支持。中文使用昵称并在这里解释它的指代。'],
[('美国国会图书馆：1952年竞选歌曲与口号','https://www.loc.gov/exhibits/presidential-songs/issues-and-slogans.html')])
]
assert len(rows)==24
existing={n['id']:n for n in data['notes']}
for ident,fragment,title,category,body,sources in rows:
    matches={r['source'] for r in quotes if fragment.casefold() in r['source'].casefold()}
    assert len(matches)==(2 if ident=='edwards.crook' else 1),(ident,matches)
    existing[ident]={'id':ident,'title':title,'category':category,'contains':sorted(matches),'body':body,'sources':[{'title':t,'url':u} for t,u in sources]}
data['notes']=list(existing.values())
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added 24 source-linked header contexts, with attribution limitations stated explicitly.')
