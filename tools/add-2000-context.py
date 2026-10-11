"""Sourced 2000 notes; exact reviewed sources, no game data mutation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts={p:read(ROOT/f'localization/reviews/2000-{p}-source-snapshot.json') for p in 'abcde'}
notes=[]
def add(id,title,bindings,body,sources):
    notes.append({'id':'2000.'+id,'title':title,'category':'历史制度／政治典故',
        'contains':list(dict.fromkeys(parts[p][i]['source'] for p,ids in bindings for i in ids)),
        'body':body,'sources':[{'title':t,'url':u} for t,u in sources]})
add('florida','佛州537票：计票与诉讼不是同一道程序',[('a',[0,11,12])],
    ['众议院书记员公布的2000年选举统计中，佛州共和党总统选举人得票2912790，民主党2912253，相差537票。这个数字来自认证计票结果，不是最高法院亲自数出的票数。',
     '布什诉戈尔判词回顾了不足半个百分点触发机器重计，随后申请手工重计、认证和诉讼的过程。游戏将这些程序压缩为结局；不要把小差距直接等同于平票，或把司法裁判译成选举人团投票。'],
    [('众议院书记员：2000年选举统计佛州表','https://clerk.house.gov/member_info/electionInfo/2000/2000Stat.htm'),
     ('康奈尔大学转载：布什诉戈尔案判词，2000年12月12日','https://www.law.cornell.edu/supct/html/00-949.ZPC.html')])
add('funding','纳德的5%目标与公共资助',[('a',[9,10,36,37,38,43]),('e',[28,30])],
    ['联邦选举委员会2000年年报区分初选配套资助和大选公共资助：小党依据上次总统选举的全国普选票比例取得部分大选资助；新党候选人达到5%可取得选后部分资助。',
     '所以5%目标有制度背景，但赢下哥伦比亚特区或一个州，不会自动保证全国比例达标。原作把多种公共资助概称matching funds，正文保留联邦配套资助说法；需用这条说明区分初选配套款与大选拨款。候选人还须满足其他资格条件。'],
    [('联邦选举委员会：2000年年报第16—17页，PDF第20—21页','https://www.fec.gov/resources/about-fec/reports/ar00.pdf')])
add('veto-comedy','纳德喊否决：架空喜剧与真实程序',[('a',[39])],
    ['这一结局是纳德当总统的架空喜剧。总统不是靠在参议院书记员身后大喊一声，就完成法定否决；宪法规定将法案连同反对理由退回原提出的院，推翻否决须两院各有三分之二赞成。',
     '真实的2001财年国防授权立法是2000年10月30日的公法106-398，由H.R.4205承载并引入H.R.5408内容。原作的H.R.5411、81比19、74次否决与五分钟都保留，不拿真实编号替换或改变触发条件。'],
    [('美国国家档案馆：宪法第一条第七款','https://www.archives.gov/founding-docs/constitution-transcript'),
     ('GovInfo：公法106-398正式文本开篇','https://www.govinfo.gov/content/pkg/PLAW-106publ398/html/PLAW-106publ398.htm')])
add('internet','戈尔发明互联网：缩略转述形成的政治梗',[('d',[69,74]),('e',[0,1])],
    ['CNN在2003年节目逐字稿中重放了1999年采访片段：戈尔谈的是在国会任职时主动推动互联网的创建。节目随后明确谈到，简化转述把这变成了“我创造了互联网”。不是声称亲自写出全部技术。',
     '互联网协会由早期建设者撰写的历史也记述了研究报告对戈尔及高速网络政策的影响。游戏中的问题采用广为流传的攻击说法，回答则可解释政府研究与经费支持；中文保留这一区别，不把传闻写成技术史结论。'],
    [('CNN：2003年1月19日节目重放原采访片段','https://transcripts.cnn.com/show/le/date/2003-01-19/segment/00'),
     ('互联网协会：互联网简史，政府政策与研究网络','https://www.internetsociety.org/internet/history-internet/brief-history-internet/')])
add('kyoto-vote','克里与京都：决议不等于条约批准票',[('a',[62]),('b',[30,31,32]),('c',[40,41])],
    ['1997年7月25日，参议院以95票赞成通过伯德—黑格尔决议，克里投赞成票。决议反对不同时要求发展中国家承担指定减排承诺、或严重损害美国经济的协定。这不是对后来《京都议定书》的批准表决。',
     '议定书第三条将量化目标放在附件一国家，另有其他合作义务。原作把克里的投票概括为反对议定书、把差别义务概括为80%免于履约；正文保留竞选语境，旁注指出制度区别，不把这些概括认证为完整法条。'],
    [('参议院：1997年第205号唱名表决及克里票向','https://www.senate.gov/legislative/LIS/roll_call_votes/vote1051/vote_105_1_00205.htm'),
     ('美国国会：第105届参议院第98号决议原文','https://www.congress.gov/bill/105th-congress/senate-resolution/98/text'),
     ('联合国气候框架公约：京都议定书原文第三条','https://unfccc.int/resource/docs/convkp/kpeng.html')])
add('milosevic','米洛舍维奇下台与移交法庭的时间',[('b',[17,18])],
    ['前南刑庭的案件历史记载，1999年发出逮捕令，2000年9月选举及10月群众抗议使米洛舍维奇下台；实际移交海牙是在2001年6月。',
     '因此，2000年竞选中说已经让独裁者接受司法制裁，超前概括了后来的过程。原作这句话与对轰炸效果的赞许仍保留；不能把起诉、下台、逮捕、移交和定罪当成同一个事件。'],
    [('联合国前南刑庭：逮捕与移交历史','https://www.icty.org/en/content/arrest-and-transfer')])
add('cole','科尔号袭击：当时疑问与后来的调查',[('a',[54]),('b',[24,25,26])],
    ['2000年10月12日，科尔号驱逐舰在也门亚丁港补给燃料时遭载有炸药的小艇袭击，17名美国水兵遇难。FBI后来确认基地组织策划并实施袭击。',
     '题目及回答处于竞选当时，可以要求先调查责任人。不能把后来调查的结论强行写进每个选项，抹去克制、调查后打击和推翻庇护政府三种政策立场的差别。'],
    [('FBI：科尔号袭击案件历史','https://www.fbi.gov/history/cases-and-criminals/uss-cole-bombing')])
add('elian','埃利安：监护与移民争议',[('a',[49]),('b',[13,14,15]),('c',[12])],
    ['埃利安·冈萨雷斯案涉及古巴男孩在美国亲属与古巴父亲之间的监护、移民和庇护申请争议。克林顿图书馆档案说明，联邦人员于2000年4月22日接走男孩，同年6月28日他与父亲返回古巴。',
     '正文的支持或反对遣返，是候选人的政治选择；不把两党立场简单归成赞成或反对某种族，也不把政府说明当成所有争论已经消失。'],
    [('克林顿总统图书馆：埃利安案档案导读','https://www.clintonlibrary.gov/research/archives/finding-aids/elian-gonzalez')])
add('anwr','ANWR：北极保护区的名称',[('a',[58]),('b',[43])],
    ['ANWR指位于阿拉斯加的北极国家野生动物保护区。鱼类与野生动物管理局说明，其前身建立于1960年，1980年扩大并改称现名。',
     '题干原作写成Alaska National Wildlife Refuge，正文保留阿拉斯加措辞；含ANWR的回答使用规范译名。地名不改原始资源与州数据，钻探支持和反对仍按原作立场表达。'],
    [('美国鱼类与野生动物管理局：北极保护区历史','https://www.fws.gov/refuge/arctic/about-us')])
add('petroleum','战略石油储备：2000年交换放油',[('d',[4,14,15,16,20,22,23])],
    ['克林顿在2000年9月23日讲话中宣布，前一日指示能源部长在30天内交换3000万桶战略储备原油，理由是取暖油库存不足、原油昂贵，尤其影响东海岸与新英格兰。',
     '交换安排不是永远免费赠送库存。游戏对是否只应在紧急情况下动用储备、以及临近选举的动机有不同判断，中文保留这些争议，不把所有批评者统称不关心冬季取暖。'],
    [('美国国家档案馆：克林顿2000年9月23日讲话','https://clintonwhitehouse6.archives.gov/2000/09/2000-09-23-rrmarks-upon-departure-on-strategic-petroleum-reserve.html')])
add('impeachment','弹劾不等于免职',[('a',[15,16,17]),('b',[9,10,11,12])],
    ['众议院在1998年12月19日弹劾克林顿，参议院于1999年2月12日审判后作无罪裁决，他并未因此被免职。弹劾是提出正式指控，免职还涉及审判定罪，不能互译。',
     '候选人可以主张他本应被免职，也可以赞许其政策、批评其私生活；这些立场原样保留，不把“应该”改成已经发生的事实。'],
    [('美国众议院历史办公室：弹劾名单与克林顿审判结果','https://history.house.gov/Institution/Impeachment/Impeachment-List/')])
add('raiders','纳德突击队：消费者权益研究者',[('a',[40])],
    ['纳德在自己的回顾文章中记述，第一批年轻研究者于1969年调查并推动改革联邦贸易委员会，后续团队调查公司与政府机构。这就是Nader’s Raiders称号的背景。',
     '正文译为纳德突击队，指政策调查与消费者权益行动者，不是军队、橄榄球队或游戏中的袭击部队。“三十年走到白宫”则是本局架空胜选结局，不是纳德现实中曾当选总统。'],
    [('纳德本人：2021年回顾早期Nader’s Raiders','https://nader.org/2021/11/24/thanksgiving-thanks-for-the-early-nader-raiders/')])
catalogue=read(ROOT/'localization/stories/catalogue.json')
danforth=[r['source'] for r in catalogue['records'] if r['scope']=='base' and 'John Danforth served four terms' in r['source']]
assert len(danforth)==1
notes.append({'id':'2000.danforth-terms','title':'丹福思的四届：补缺与完整任期','category':'历史制度／人物资料',
    'contains':danforth,'body':[
        '参议院手册记载，丹福思于1976年12月27日就任，任至1995年1月2日；脚注说明，他先当选1977年1月3日开始的任期，随后获州长任命补完此前任期的最后几天。',
        '因此，原作的四届可以将极短的补缺任期与三个完整六年任期分别计数。正文保留四届，不应据此推断他任职24年或四次当选；也不能确定作者是否有意采用这种计数。'],
    'sources':[{'title':'GovInfo：第110届参议院手册，密苏里州历任参议员表及脚注（PDF第26页）','url':'https://www.govinfo.gov/content/pkg/SMAN-110/pdf/SMAN-110-pg1165.pdf'}]})
path=ROOT/'localization/annotations/notes.zh-CN.json';data=read(path)
byid={n['id']:n for n in data['notes']};byid.update({n['id']:n for n in notes})
data['notes']=list(byid.values());data['checkedAt']='2026-10-09'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'researched 2000 notes')
