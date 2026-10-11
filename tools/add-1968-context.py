"""Bind researched 1968 context to immutable complete originals, never game data."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/1968-{p}-source-snapshot.json') for p in 'abcdefg'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'1968.'+id,'title':title,'category':'历史制度／政治典故',
        'contains':list(dict.fromkeys(parts[p][i]['source'] for p,indices in bindings for i in indices)),
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('chennault','陈香梅事件：秘密联络与游戏分支',
    [('a',[57]),('b',[59,60]),('c',[9,10,11]),('d',[38,66,67]),('e',[73,74]),('f',[0]),('g',[28,32])],
    ['约翰逊1968年10月31日宣布停止轰炸北越，推动和平谈判。约翰逊图书馆说明，尼克松竞选阵营中的一些人与南越政府秘密联络，劝其延缓谈判，并暗示尼克松当选后会提供更好的条件；重要中间人陈香梅是陈纳德的遗孀。',
     '约翰逊把这件事称为叛国，但未在大选前公开相关情报，尼克松否认参与。政治上的叛国指责不等于法院已经定罪。游戏允许玩家选择是否参与、是否公开指控，并给出不同成败结果；这些分支及票数变化不是已经发生的历史。不能把南越政府自身的考虑全部简化为美国竞选阵营的指令。'],
    [('约翰逊总统图书馆：陈香梅事件及X档案','https://www.lbjlibrary.org/media-kit/chennault-affair?type=document'),
     ('Diplomatic History：越南方面的动机与既有解释的局限','https://academic.oup.com/dh/article/48/5/633/7758644')])
add('debates','1968辩论是架空选择，1964比较另有疑点',
    [('a',[13]),('b',[61,62]),('c',[12,13,14,15]),('d',[32,60,61]),('e',[21,22,23,24])],
    ['真实历史中，1960年肯尼迪与尼克松辩论后，1964、1968和1972年均未举行主要总统候选人之间的大选辩论。游戏允许尼克松与汉弗莱辩论，是玩家可改变历史的分支，胜负评价也属于模拟。',
     '原结局另写“与1964年相比”的翻身。1964年共和党总统候选人是戈德华特，不能把这句话当成尼克松1964年参选或参加辩论的证据。正文保留原比较年份，旁注指出其含混之处，不改分支条件。'],
    [('总统辩论委员会：1964、1968和1972年没有大选辩论','https://www.debates.org/about-cpd/overview/'),
     ('美国国家档案馆：1964年各候选人结果','https://www.archives.gov/electoral-college/1964')])
add('six-day','六日战争与以土地换和平',
    [('a',[54]),('b',[5,6,7,8]),('e',[65,66,67,68])],
    ['1967年6月以色列击败埃及、约旦和叙利亚，占领西奈半岛、加沙、约旦河西岸、东耶路撒冷和戈兰高地。战前有封锁蒂朗海峡、撤出联合国部队及军事集结等危机；不能只凭选项“四面受敌”就认定战争的开火顺序。',
     '约翰逊政府寻求撤军与和平安排相结合。联合国安理会第242号决议将撤军与承认各国主权、和平安全相联系，各方对措辞有不同解释。无条件先归还、先获得和平保证、主张继续占领和美国不介入，是四种不同立场，译文没有抹平它们。'],
    [('美国国务院：1967年战争、危机及第242号决议','https://history.state.gov/milestones/1961-1968/arab-israeli-war-1967')])
add('columbia','哥伦比亚大学：越战、国防研究与社区争议',
    [('a',[43]),('b',[29,30,31]),('f',[32,33,34])],
    ['1968年春的校园占领不只是抽象的学生不满。抗议涉及学校与国防分析研究所的关系，以及晨边公园体育馆项目对哈莱姆社区的影响；建筑入口安排引发种族不平等的批评。',
     '学生占领校园建筑后，校方请求警察清场，出现逮捕与伤害。候选人关于煽动者、共产主义或校方纵容的台词是其政治判断，不是将所有抗议者定为同一种人。原选项中的同性恋、吸毒和焚旗指控保留，不增添译者的道德判决。'],
    [('哥伦比亚大学档案展：体育馆建设与社区抗议','https://exhibitions.library.columbia.edu/exhibits/show/1968/causes/gym'),
     ('哥伦比亚大学：1968年抗议的多重背景','https://news.columbia.edu/content/new-perspective-1968')])
add('summer','漫长炎热的夏季：1967年城市骚乱',
    [('a',[6,56]),('b',[20,22,23,26,27,28,44]),('d',[33,42,43,44,45]),('e',[34]),('g',[3,4,5,6])],
    ['这里的漫长炎热夏季指1967年的城市骚乱，纽瓦克和底特律尤其突出。1968年金博士遇刺后又发生了另一波骚乱，二者不能混成同一事件。',
     '克纳委员会调查关注种族歧视、贫困、居住隔离和警民关系等因素。选项把骚乱归因于融合、黑豹党或法院判决，是候选人的论证，不能作为委员会的结论；也不应把所有黑人或所有抗议者当作参与暴力的人。金的非暴力运动、黑人激进组织及各地骚乱分别理解。'],
    [('美国国家档案馆：众议院调查所述1967年骚乱、克纳委员会与金的反战立场','https://www.archives.gov/research/jfk/select-committee-report/part-2-king-findings.html'),
     ('美国住房与城市发展部保存：克纳委员会报告原件','https://www.hud.gov/sites/dfiles/FHEO/documents/kerner_commission_full_report.pdf')])
add('court-rights','沃伦法院：律师权、讯问权与婚姻自由',
    [('b',[9,10,11,12]),('c',[24,48,49,50]),('d',[11,19,20,21,42]),('f',[9,10,11,12,54,55,56])],
    ['吉迪恩案1963年确立贫困重罪被告获得指定律师的保障；米兰达案1966年涉及羁押讯问时的权利告知与程序保障，不是法院一概禁止执法。原文把Wainwright误拼为Wainright，中文采用通行案名。',
     '洛文案1967年裁定弗吉尼亚州禁止跨种族婚姻的法律违宪。它涉及平等保护与正当程序，不能译成一般的通婚习俗争论。司法能动主义是对法院积极运用司法审查的称呼；选项批评其越权，保留批评语气，但不替候选人证明判决造成犯罪。'],
    [('美国联邦法院：吉迪恩案事实与判决','https://www.uscourts.gov/about-federal-courts/educational-resources/educational-activities/sixth-amendment-activities/gideon-v-wainwright/facts-and-case-summary-gideon-v-wainwright'),
     ('美国联邦法院：米兰达案事实与判决','https://www.uscourts.gov/about-federal-courts/educational-resources/educational-activities/fifth-amendment-activities/miranda-v-arizona/facts-and-case-summary-miranda-v-arizona'),
     ('国家档案馆：洛文夫妇与跨种族婚姻案','https://prologue.blogs.archives.gov/2021/02/11/the-fight-for-the-right-to-marry-the-loving-v-virginia-case/')])
add('nixon-1957','尼克松1957年的角色：副总统与参议员不同',
    [('a',[70]),('c',[32])],
    ['尼克松1950至1953年担任参议员，1953至1961年担任副总统，依法兼任参议院议长；1957年已经不是参议员。原选项的“推动在参议院过关”应与其副总统职务区分，不能据此把他写成1957年的参议员或多数党领袖。',
     '约翰逊当时作为多数党领袖，也在法案通过中发挥重要作用。汉弗莱另一个选项提到1948年民权运动，是不同人物的政治经历，不应把两人的自我表功合并成同一条传记。'],
    [('美国参议院：曾任副总统的参议员及任职年代','https://www.senate.gov/senators/senators-who-served-as-vice-president.htm'),
     ('美国参议院：约翰逊与1957年民权法','https://www.senate.gov/senators/FeaturedBios/Featured_Bio_JohnsonLyndonBaines.htm')])
add('immigration','1965年移民改革：取消歧视性来源配额',
    [('a',[47]),('b',[16,17,18,19])],
    ['1965年改革废除旧的国籍来源配额体系，改以家庭联系、技能等因素安排优先次序。取消旧配额不等于取消一切人数限制，更不等于任何人都可以无条件入境。',
     '原选项使用Negro、Orientals等当时的族群称呼，并带有明确的排外语气。中文保留其针对黑人、墨西哥人和东方人的指责，不把它改写成中性的技术移民政策，也不把这种台词视为译者观点。'],
    [('美国国家档案馆：1965年移民改革背景','https://prologue.blogs.archives.gov/2015/09/17/fifty-year-later-a-brief-history-of-the-immigration-act-of-1965/')])
add('affirmative','平权行动不等于强制雇用不合格者',
    [('a',[69,71]),('c',[21,51,52,53,54]),('d',[14,22,23,24,25]),('f',[24,25,26,27])],
    ['1965年第11246号行政命令的原始文本要求联邦承包商反歧视并采取积极措施，促进平等就业机会。原选项声称法律要求雇用不合格者，是反对者的说法，不能当作行政命令的原文规定。',
     '招聘中的平权行动、配额、学校种族融合的跨区校车接送，是有关联但不同的制度。校车接送在这里是改变学校种族构成的措施，不是所有学生日常乘校车。命令1965年原始版本与后来增列性别歧视的修订，也应区分。'],
    [('美国平等就业机会委员会：第11246号行政命令原始文本','https://www.eeoc.gov/history/executive-order-no-11246')])
add('head-start','启蒙计划：学前教育与减贫',
    [('f',[73,74]),('g',[0,1])],
    ['启蒙计划是伟大社会减贫议程中的儿童发展项目，1965年从八周示范项目起步，结合学前教育、健康与家庭支持。它不是小学课程的另一个名称，也不是大学提前录取。',
     '选项“唯一办法”“知识精英浪费钱”分别是支持与反对的竞选修辞，不能当作经评估证明的唯一政策答案。'],
    [('HeadStart.gov：项目历史','https://www.headstart.gov/about-us/article/head-start-history')])
add('environment','环保署尚未成立：1968年的政策提议',
    [('c',[23,33,34,35]),('d',[13,26,27,28]),('f',[6,7,8,51,52,53])],
    ['环境保护署1970年才正式成立。1968年问题问的是是否支持建立这个联邦机构，不能写成扩建已存在的环保署。1963年《清洁空气法》与1970年强化后的法律，也不能混为同一个版本。',
     '反对者把环保监管与失业联系起来，支持者强调污染危害，温和选项强调执行与经济的平衡；译文分别保留。抱树嬉皮士是嘲笑环保人士的政治标签，不是说人物真的正在抱树。'],
    [('美国环保署：机构起源与成立','https://www.epa.gov/history/origins-epa'),
     ('美国环保署：清洁空气法的演变','https://www.epa.gov/clean-air-act-overview/evolution-clean-air-act')])
add('gold','1968年的黄金危机：不同于19世纪金币本位',
    [('a',[64,65,66,67]),('b',[32,33,34,35])],
    ['此时的美元与黄金联系属于布雷顿森林国际货币体系，不能按19世纪公众日常持有纸币兑换金币的金本位理解。1968年3月黄金总库危机后，官方黄金交易和私人市场形成两层市场。',
     '官方市场维持每盎司35美元，私人价格浮动；停止美元对黄金兑换则发生在1971年。充分就业也不是每个成年人都必定有工作。原选项对通胀、利率和失业的因果判断保留，没有改任何经济或选举数值。'],
    [('美国国务院：1968年3月黄金两层市场的会议与公报','https://history.state.gov/historicaldocuments/frus1964-68v08/d191'),
     ('联邦储备历史：美元黄金兑换至1971年终止','https://www.federalreservehistory.org/essays/gold-convertibility-ends')])
add('tet','春节攻势：战场结果与政治影响并非一回事',
    [('d',[12,15,16,17,18]),('f',[40,41,42,43])],
    ['1968年春节攻势未达到北越与越共预期的普遍起义和军事目标，但严重冲击了美国公众对战争进展及政府乐观表态的信任。说其军事上失利，不等于说美国国内政治也因此毫发无损。',
     '游戏中的胜利、灾难、应加强戒备和根本不该参战，是不同政治论证。越共与北越相互协作，但并非同一个组织；译文没有把两个名称任意互换。'],
    [('美国国务院：春节攻势与美方政策转变','https://history.state.gov/milestones/1961-1968/tet'),
     ('美国国防部：军事胜利与舆论转折','https://www.defense.gov/News/Feature-Stories/Story/Article/3291950/highlighting-history-how-tet-began-the-end-of-vietnam/')])
add('dominican','1965年多米尼加干预：反共理由与争议',
    [('c',[29,55,56,57,58]),('f',[28,29,30,31])],
    ['多米尼加内战中，争取恢复被推翻的博什政府的力量与其对手交战。约翰逊政府以保护人员、担忧共产主义势力掌权等理由出兵，但恢复宪政的阵营不能全部等同于共产党。',
     '国务院当时的情报评估强调共产主义影响，同期美国国会议员则质疑干预的依据与民主承诺。原选项支持、审慎支持和谴责干预的区别均保留；“最低伤亡”是人物评价，不意味着没有多米尼加平民伤亡。'],
    [('美国国务院：1965年5月7日情报评估','https://history.state.gov/historicaldocuments/frus1964-68v32/d60'),
     ('美国海军历史：博什、内战与干预全过程','https://www.history.navy.mil/research/library/online-reading-room/title-list-alphabetically/c/caribbean-tempest.html'),
     ('美国国会记录：1965年5月11日的批评','https://www.govinfo.gov/content/pkg/GPO-CRECB-1965-pt8/pdf/GPO-CRECB-1965-pt8-1-2.pdf')])
add('kennedy-round','肯尼迪回合：贸易谈判与授权之争',
    [('a',[52]),('b',[36,37,38]),('f',[36,37])],
    ['肯尼迪回合是关贸总协定框架下的多边贸易谈判，由肯尼迪时期的1962年《贸易扩展法》授权推动，后来在约翰逊任内完成。它不是肯尼迪本人在1967年主持的会议，也不是已经成立世界贸易组织。',
     '行政部门谈判权限、关税让步、国会后续立法及劳动者利益，是不同问题。支持贸易和批评某项协议偏向一方可以并存。'],
    [('美国国务院：1967年5月对国会领导层说明的谈话要点','https://history.state.gov/historicaldocuments/frus1964-68v08/d360'),
     ('美国国务院：贸易授权与各方权限争论','https://history.state.gov/historicaldocuments/frus1964-68v08/d362')])
add('hump','Dump the Hump：拒绝汉弗莱的押韵口号',
    [('f',[66])],
    ['Hump是Humphrey的戏谑缩写，与dump押韵。这里应理解为甩掉汉弗莱、别投他，不是字面上的丢掉驼峰。佐治亚数字图书馆的标语牌档案保存了这一口号。',
     '口号曾被不同反对者使用，单凭这句话不能认定说话者必定属于同一政党或反战组织。中文传达拒绝投票的意思，没有编造原文不存在的押韵口号。'],
    [('佐治亚数字图书馆：带Dump the Hump字样的原始标语牌记录','https://dlg.usg.edu/record/gsu_labor_873')])
add('jumbo','Jumbo：把约翰逊变成粗俗网络绰号',
    [('f',[42])],
    ['Jumbo字面意为巨大的东西，在约翰逊相关轶事和网络梗中指其给自己阴茎起的名字；游戏这里借它代指约翰逊，带有粗俗嘲讽，而不是另一名政治人物。中文保留“巨无霸”的绰号，并在此解释双关。',
     '下列文章汇集传记作者转述的轶事。此次未读到这些轶事对应的原始口述档案，不能把每个场景、尺寸或所谓越战动机当作已独立证实的史实，也不能推定当时鸽派普遍这样称呼他。'],
    [('MEL：约翰逊绰号的传记转述汇集及证据限制','https://melmagazine.com/en-us/story/lyndon-b-johnson-penis')])
add('pointy-heads','尖脑袋知识分子：华莱士的反精英修辞',
    [('d',[26]),('f',[74]),('g',[24])],
    ['尖脑袋是把学者与官僚讥为只会纸上谈兵、脱离普通人生活的政治称呼，不能误译成某种生理疾病。1970年国会记录收录的采访，直接问华莱士此前贬低北方记者与知识分子的言论。',
     '“两党差别连一角钱都不值”则用很小的货币单位夸张地表示两党毫无差别。这里保留修辞，不把其理解为客观测量的政策相似度。'],
    [('美国国会记录：1970年2月5日所载华莱士采访','https://www.govinfo.gov/content/pkg/GPO-CRECB-1970-pt2/pdf/GPO-CRECB-1970-pt2-7-1.pdf')])
add('deadlock-fiction','未决选举与隐藏结局：游戏叙事不是历史判决',
    [('a',[2,5,8,9,11,30]),('b',[64]),('g',[13,23,24,25,35,41])],
    ['没有候选人取得选举人票过半数时，众议院从总统得票前三名中选总统，按州代表团一州一票；参议院另从副总统得票前两名中选副总统。全院民主党席位多，不自动等于每个州代表团会投汉弗莱。',
     '华莱士讨价还价、赢下全国、隐藏打字动画和尼克松庭审，属于原作架空或恶搞结局。尼克松1968年并未接受这种庭审，“我只是在闭目养神”是为睡着找借口的笑点，不是法院史料。原文民权法案crusader一句语法不通，按上下文译为针对法案的讨伐，公开记录这一解释。'],
    [('美国国家档案馆：宪法第十二修正案','https://www.archives.gov/founding-docs/amendments-11-27'),
     ('美国国家档案馆：真实1968年选举结果','https://www.archives.gov/electoral-college/1968')])
add('nutrition','儿童营养法：试点早餐与牛奶项目分别理解',
    [('a',[41]),('b',[24,25])],
    ['1966年《儿童营养法》第3节授权特殊牛奶项目，第4节授权学校早餐试点。早餐资助由州教育机构分配，优先考虑经济困难地区及学生通学距离较远的学校；不能理解成1966年所有学生已经普遍享有免费早餐。',
     '法案规定，无力支付全价的儿童可免费或减价用早餐。原问题把早餐与牛奶简写为免费提供，译文保留问题，旁注区分具体条款与资格安排，不改候选人立场。'],
    [('美国成文法原件：80 Stat. 885，第3至4节','https://www.govinfo.gov/content/pkg/STATUTE-80/pdf/STATUTE-80-Pg885.pdf')])
add('privacy','避孕与堕胎：1968年不能倒套后来的判例',
    [('c',[25,66,67]),('d',[7,8,9,73]),('f',[13,14,15,16,38,39])],
    ['1965年格里斯沃尔德诉康涅狄格州案涉及向已婚夫妇提供避孕建议和手段，法院从宪法保障中阐释婚姻隐私。它不是已经判决所有人的堕胎权，也不是1968年已经发生了1973年的罗诉韦德案。',
     '是否通过联邦法律、是否维持州立法、是否只准许危急情况下的手术，是不同政策选择。反对避孕药的宪法修正案提议也须与普通法律区分。'],
    [('康奈尔法律信息研究所：1965年判决原文381 U.S. 479','https://www.law.cornell.edu/supremecourt/text/381/479')])
add('treason','叛国：宪法限定与政治指控',
    [('b',[26]),('d',[67]),('a',[11])],
    ['美国宪法第三条将叛国限于对美国发动战争，或依附其敌人并给予援助；定罪还设有明确证据要求。仅仅具有激进观点或加入某个政治组织，不等于已经构成宪法意义的叛国。',
     '原选项要求监禁甚至处决，是候选人的强硬政治主张。旁注区分指控与定罪，不替角色增加新的犯罪事实，也不改变原回答效果。'],
    [('美国国家档案馆：宪法第三条第三节','https://www.archives.gov/founding-docs/constitution-transcript')])
add('chicago','芝加哥大会：警察制造的暴乱与调查报告',
    [('d',[29,37,53,54,62,63,64,65,74]),('e',[25,26,27])],
    ['1968年民主党大会期间，芝加哥街头警察与示威者发生严重冲突。沃克调查报告承认挑衅与示威者的暴力，也记录警察对和平示威者、记者和旁观者使用无差别及过度武力，并用警察制造的暴乱概括某些警察行动。',
     '这份报告在1968年12月才公开。游戏中大选前角色说出类似表述，可以是其政治立场，但不能写成当时已经引用12月发布的报告。这里警察是被指责发动暴力的一方，不是“警察镇压暴乱”的缩写；将责任完全归给某一方和双方皆有责任的选项保留区别。'],
    [('沃克报告原始摘要转载：1968年12月发布的Rights in Conflict','https://chicago68.com/ricsumm.html')])
path=ROOT/'localization/annotations/notes.zh-CN.json';data=read(path)
byid={n['id']:n for n in data['notes']};byid.update({n['id']:n for n in notes})
data['notes']=list(byid.values());data['checkedAt']='2026-10-09'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# The hidden animation uses carets, stars and '<' as non-HTML timing commands.
zh=(ROOT/'localization/reviews/1968-a-revised.txt').read_text(encoding='utf-8').splitlines()[9]
commands=lambda s:re.findall(r'\^+|\*|<',s)
assert commands(parts['a'][9]['source'])==commands(zh)
exceptions={
 'a':[{'index':13,'reason':'1968 debate is playable counterfactual; original 1964 turnaround comparison retained and annotated.'},
      {'index':30,'reason':'Malformed a crusader against civil rights bill interpreted contextually as a campaign against the law; original unchanged.'},
      {'index':70,'reason':'Nixon was Vice President/presiding Senate officer in 1957, not serving Senator; preserve claim and distinguish offices.'}],
 'd':[{'index':11,'reason':'Original Wainright misspelling retained in English; Chinese uses conventional Wainwright case name.'}],
 'f':[{'index':42,'reason':'Jumbo interpreted as vulgar LBJ nickname; anecdote evidence is secondary, original oral-history material not independently examined.'},
      {'index':66,'reason':'Dump the Hump rhyme explained using original placard catalogue; full page fetch failed, catalogue search extract read.'}]}
for p in parts:
    metadata={'checkedAt':'2026-10-09','sourceExceptions':exceptions.get(p,[]),
              'research':'1968-RESEARCH_ZH.md','animationCommandsPreserved':p=='a'}
    (ROOT/f'localization/reviews/1968-{p}-metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'1968 notes; original hidden-animation command sequence preserved')
