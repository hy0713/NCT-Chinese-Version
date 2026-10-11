"""Source-bounded annotations for the last full-field reviews; no game edits."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/2020-{p}-source-snapshot.json') for p in 'abcdefg'}
staff=read(ROOT/'localization/reviews/final-supplement-source-snapshot.json')
notes=[]
def add(id,title,bindings,body,sources,staff_ids=()):
    sources_text=[parts[p][i]['source'] for p,ids in bindings for i in ids]+[staff[i]['source'] for i in staff_ids]
    notes.append({'id':id,'title':title,'category':'历史事件／政治修辞',
      'contains':list(dict.fromkeys(sources_text)),'body':body,
      'sources':[{'title':t,'url':u} for t,u in sources]})
add('2020.reversed-election','“阻止偷窃”与角色互换的架空结局',[('a',[20,28,30])],
 ['国家档案馆记录，真实2020年选举人票为拜登306票、特朗普232票，538票中的获胜多数为270票。国会计票因国会大厦内外的暴力骚乱而延迟，到2021年1月7日凌晨3时44分才完成确认。',
  '游戏中让败选拜登指责现场投票、筹备一月六日集会的段落，是把现实政治话术换给另一角色的架空讽刺，不是拜登真实行动的历史记录。特朗普结局中的引号也带讽刺意味，不能按字面当成旁注赞同。原作“一票之差”保留；获胜所需多数与两名候选人之间的票差是两个概念。'],
 [('国家档案馆：2020年选举人团结果','https://www.archives.gov/electoral-college/2020')])
add('2020.impeachment-timeline','众议院弹劾与参议院审判跨两个年份',[('a',[50,52]),('e',[26,28])],
 ['众议院历史办公室记载，特朗普首次被弹劾是在2019年12月18日，指控为滥用职权和妨碍国会；参议院审判在2020年1月16日至2月5日进行，结果为无罪。',
  '因此，原作“2019年的弹劾审判”压缩了弹劾和审判两个阶段。正文保留年份，旁注说明区别。无罪判决不等于从未遭众议院弹劾，候选人有关拜登家族或调查动机的指控也不自动成为已证实事实。'],
 [('众议院历史办公室：历次弹劾与审判清单','https://history.house.gov/Institution/Impeachment/Impeachment-List/')])
add('2020.historical-masks','2020年的口罩建议与竞选台词',[('e',[22]),('f',[25,26])],
 ['CDC保存的2020年4月3日说明建议，在其他社交距离措施难以维持的公共场所，特别是社区传播显著的地区，使用布制面部覆盖物；同时仍强调保持六英尺距离。该说明把布制覆盖物与供医疗人员使用的外科口罩、N95区分。',
  '因此，“完全没有证据”等回答是原作角色的政治说法，并非旁注认定的医学结论。这里只解释当时的史料，不把2020年指导当成今天的医疗建议，也不认可题目选项中的治疗或隔离主张。'],
 [('CDC历史存档：2020年4月3日布制面部覆盖物建议','https://stacks.cdc.gov/view/cdc/86440/cdc_86440_DS1.pdf')])
add('2020.court-expansion','扩充最高法院与法官任命',[('a',[59]),('c',list(range(17,24))),('f',[5,6,7,8]),('g',[10,11])],
 ['最高法院的官方说明指出，国会通过法律确定大法官人数；1869年法律确定为九人。总统提名填补空缺的人选，参议院表决确认。',
  'Court-packing在这里是通过增设席位改变法院政治构成的争论，不是重新任命所有现有法官。正文中的扩充计划或拒绝回答立场各自保留；总统不能仅凭个人宣告就增加四个法定席位。'],
 [('美国最高法院：一般事项常见问题','https://www.supremecourt.gov/about/faq_general.aspx')])
add('2020.ghosts-past','败选幽灵与《圣诞颂歌》',[('a',[45])],
 ['狄更斯《圣诞颂歌》中的幽灵分别带主人公回顾过去、观察现在、面对未来。这里把他们换成兰登、胡佛和麦戈文三位大败的总统候选人，并笑称选举幽灵只管过去。',
  '这是根据原文明确提到过去、现在、未来而作的文学典故解读，不是经游戏作者认证的创作访谈，也不是特朗普真实遇见幽灵的记载。三人的安慰和特朗普的拒绝构成讽刺，人物姓名与剧情均保留。'],
 [('狄更斯：《圣诞颂歌》原文，Project Gutenberg','https://www.gutenberg.org/files/46/46-h/46-h.htm')])
add('2020.lagoa-service','州最高法院与州上诉法院不能混为一谈',[('f',[14]),('g',[14])],
 ['联邦司法中心传记列出，拉戈阿在佛罗里达州第三地区上诉法院任职为2006—2019年，州最高法院任职为2019年；2019年12月6日收到联邦第十一巡回上诉法院任命状。',
  '原作把她在州最高法院的任职说成“多年”，与这份履历不符。正文保留角色说法，不能把较长的州上诉法院经历错移到州最高法院。这份旁注不声称已从成功获取的州法院页面核准每个交接日。'],
 [('联邦司法中心：芭芭拉·拉戈阿法官传记','https://www.fjc.gov/history/judges/lagoa-barbara')])
add('2020.harris-vaccine','哈里斯疫苗回答的前后条件',[('f',[20]),('g',[18])],
 ['2020年10月7日副总统辩论的PBS节目存档字幕中，哈里斯先表示，公共卫生专业人员、福奇或医生建议接种时，她会首先排队接种；随后表示不会仅因特朗普叫她接种而接种。',
  '不能把整段简化成她反对任何疫苗。游戏顾问以CDC背书概括她的条件，也不完全等同于存档里的具体措辞。存档注明字幕来自第三方或计算机且未经逐字验证，本旁注据其清楚的条件关系说明语境，不冒充重新核对过音频的逐字稿。'],
 [('美国公共广播档案：PBS NewsHour，2020年10月7日辩论存档','https://americanarchive.org/catalog/cpb-aacip-311cf321c01')])
add('2020.kung-flu','Kung-flu：带族裔指向的谐音攻击语',[('d',[53]),('e',[14])],
 ['Kung-flu把kung fu（功夫）与flu（流感）拼成谐音，借与中国的文化联系称呼疫情；它是带族裔指向的攻击语，不是正式疾病名称。译为“功夫流感”，保留角色措辞及题干对煽动性言论的批评。',
  '美国总统项目保存的2020年6月23日凤凰城演说记录中，观众喊出该词，特朗普随后重复。此出处证明当时确有此种修辞，不证明游戏里有关制造病毒或操纵选举的指控。'],
 [('美国总统项目：2020年6月23日凤凰城集会演说记录','https://www.presidency.ucsb.edu/documents/remarks-turning-point-action-students-for-trump-rally-phoenix-arizona')])
add('staff.castro-twins','朱利安与华金·卡斯特罗的职务',[ ],
 ['HUD履历和华金·卡斯特罗的议员官网分别确认：朱利安曾任圣安东尼奥市长，2014年7月28日就任住房与城市发展部长；他的双胞胎兄弟华金2012年当选联邦众议员。',
  '本段的名字写朱利安，职务却写国会议员，且英文名字有乱码。译文按名字保留朱利安，并公开说明职务混淆；不把正文悄悄改成另一人，更不改变竞选团队ID、德克萨斯州加成或任用机制。'],
 [('HUD历史档案：朱利安·卡斯特罗履历','https://archives.hud.gov/secretaries/castrobio.cfm'),('华金·卡斯特罗议员官网：传记','https://castro.house.gov/about')],[28])
add('staff.bauer-spelling','Bob Baur与白宫法律顾问',[ ],
 ['白宫2011年6月2日公告把奥巴马的白宫法律顾问写作Bob Bauer，并说明他返回私人执业后为总统连任竞选和民主党全国委员会担任法律顾问。',
  '游戏姓名Baur疑似遗漏字母；中文统一鲍尔。白宫法律顾问是法律职务，不是竞选一般政策顾问。对本段竞选辩论辅导身份的推断保留为游戏安排，不以这份公告证实每项2016年或2020年的实际团队职务。'],
 [('奥巴马白宫档案：2011年6月2日白宫法律顾问人事公告','https://obamawhitehouse.archives.gov/realitycheck/the-press-office/2011/06/02/president-obama-announces-new-white-house-counsel-kathryn-ruemmler')],[22])
add('staff.adc-name','ADC的正式名称与游戏概称',[ ],
 ['ADC的自述名称为American-Arab Anti-Discrimination Committee，即美国阿拉伯裔反歧视委员会，1980年创立；不是把Committee改成League后的另一组织。',
  '本段对以色列政策的概括是游戏描述，不能代替组织全部宗旨或各个时期的具体声明。中文正文按原作League保留“联盟”，这里说明正式组织名；英文与团体ID原样保留。'],
 [('ADC官网：组织介绍','https://adc.org/about/')],[33])
add('staff.mcenany-date','麦克纳尼任命与疫情时间指代',[ ],
 ['白宫2020年4月8日公告宣布，原竞选团队全国新闻秘书麦克纳尼将出任白宫新闻秘书。两种新闻秘书职务与任职起点应区别。',
  '原作“几乎整个疫情期间”的说法是概括性叙事，不代表她在疫情出现前已经任白宫新闻秘书。正文保留措辞，也不把竞选团队技能名称当成真实人物具有改变随机数的能力。'],
 [('特朗普白宫档案：2020年4月8日新增白宫工作人员公告','https://trumpwhitehouse.archives.gov/briefings-statements/president-donald-j-trump-announces-additions-white-house-staff/')],[40])
add('staff.alternative-facts','“另类事实”与2016年叙事的时间错位',[ ],
 ['NBC于2017年1月22日发布的《Meet the Press》片段标题与说明，记录康韦以alternative facts为新闻秘书斯派塞的首次声明辩护。中文保留“另类事实”的讽刺意味，不把它译成事实已经获得另一套证据支持。',
  '本段用于2016年竞选团队时，是后来出名的修辞被放进较早背景。这里只核对NBC公开片段的日期和说明；页面与视频正文未成功获取，不宣称已重新播放或逐字复核完整采访。'],
 [('NBC News官方片段：2017年1月22日，公开标题与说明','https://www.youtube.com/watch?v=VSrEEDQgFc8')],[45])
add('staff.brexit-year','“去年脱欧公投”与2016年竞选背景',[ ],
 ['英国选举委员会2016年报告记载，英国与直布罗陀的欧盟成员资格公投在2016年6月23日举行，离开欧盟一方获51.9%。',
  '把这次公投称为2016年竞选中的“去年”存在时间错位，正文保留并另作说明。公投决定离开与英国正式退出欧盟是不同事件；这份资料也不独立证实原作给予法拉奇的全部功劳或其他个人头衔。'],
 [('英国选举委员会：2016年欧盟公投报告','https://www.electoralcommission.org.uk/sites/default/files/pdf_file/2016-EU-referendum-report.pdf')],[50])
add('staff.guilfoyle-relationship','女友与“新婚妻子”的原作差异',[],
 ['政府印刷局保存的白宫2021年1月公告摘要，在一月四日及二十日行程中都称金伯莉·吉尔福伊尔为小唐纳德·特朗普的女友。',
  '这与游戏2020年简介中的“新婚妻子”不符。正文按原作保留，旁注指出差异；不会据较晚时期的婚姻或订婚报道倒推她在游戏时间已经结婚，也不声称检查过婚姻登记档案。'],
 [('GovInfo：2021年1月白宫其他公告摘要，第1、4页','https://www.govinfo.gov/content/pkg/DCPD-2021DIGEST-TRUMP/pdf/DCPD-2021DIGEST-TRUMP.pdf')],[39])
early=read(ROOT/'localization/reviews/2016a-d-source-snapshot.json')
notes.append({'id':'2016a.spoonful-sugar','title':'一勺糖与苦药：文学比喻和出处推断',
 'category':'文学典故／政治修辞','contains':[early[30]['source']],
 'body':['《欢乐满人间》的歌曲《一勺糖》由理查德与罗伯特·谢尔曼创作，朱莉·安德鲁斯演唱。把糖与吞下苦药相连，用于暗示先用讨喜的主张吸引选民，再让他们接受不喜欢的政策。',
         '原文没有点名影片。这里说明可帮助理解的对应典故，属于文本解读，不是作者已经确认引用该歌；不摘录完整歌词。'],
 'sources':[{'title':'迪士尼D23：A Spoonful of Sugar歌曲资料','url':'https://d23.com/a-to-z/spoonful-of-sugar-a/'}]})
notes.append({'id':'2016a.iraq-authorization','title':'2002年授权使用武力与2003年入侵',
 'category':'历史事件／立法程序','contains':[early[39]['source']],
 'body':['参议院记录显示，2002年10月11日以77票对23票通过H.J.Res.114，授权对伊拉克使用武力；希拉里·克林顿投赞成票。',
         '因此，2002年支持的是授权决议，不能把实际2003年入侵的时间挪到2002年。原作围绕战争判断的辩护和批评保留，投票本身不能独立证明所有角色对战争原因的说法。'],
 'sources':[{'title':'美国参议院：2002年10月11日第237次唱名表决','url':'https://www.senate.gov/legislative/LIS/roll_call_votes/vote1072/vote_107_2_00237.htm'}]})
path=ROOT/'localization/annotations/notes.zh-CN.json'
data=read(path);byid={n['id']:n for n in data['notes']};byid.update({n['id']:n for n in notes})
data['notes']=list(byid.values());data['checkedAt']='2026-10-10'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'source-bounded final notes')
