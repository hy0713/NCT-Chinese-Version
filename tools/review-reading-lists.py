"""Human-reviewed visible bibliography labels; preserve every tag and URL.
Titles are readable translations of the supplied English labels, not a claim
that a particular Chinese edition exists. Common media brand names stay intact.
"""
import hashlib,json,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'localization/stories'
cat=json.loads((BASE/'catalogue.json').read_text(encoding='utf-8'))
full=json.loads((BASE/'editorial-records.json').read_text(encoding='utf-8'))
parts=runpy.run_path(str(ROOT/'tools/translate-stories.py'))['parts']
# These are original text segments, not executable script substitutions.
pairs={
'Articles':'文章','Books':'书籍','Books and Links':'书籍与链接','Books by the Candidates':'候选人著作','By the Candidates':'候选人作品','Links':'链接','General Resources':'综合资料','Misceallany':'杂项','Political News and Analysis':'政治新闻与分析','Politics in 2012':'2012年的政治','The Financial Crisis':'金融危机','The Vietnam War':'越南战争',
'Real Clear Politics':'RealClearPolitics（政治新闻与民调网站）','The Atlantic':'《大西洋月刊》','Politico':'Politico（政治新闻网站）','Huffington Post':'《赫芬顿邮报》','Fox News Politics':'福克斯新闻：政治','FiveThirtyEight - ':'FiveThirtyEight（民调分析网站）— ',
'Our Case For Joe Biden':'我们支持乔·拜登的理由','The Case For Trump':'支持特朗普的理由','How Biden Won: Ramping Up The Base And Expanding Margins In The Suburbs':'拜登如何获胜：动员基本盘，扩大郊区领先幅度','Why Did Trump Almost Win?':'特朗普为何险些获胜？','No Evidence For Voter Fraud: A Guide To Statistical Claims About The 2020 Election':'没有选举舞弊的证据：解读关于2020年大选的统计论断',
' What Would It Take To Turn Blue States Red?':' 怎样才能让蓝州转为红州？','Anti-Trump forces seize on grim polls for Clinton match-up':'反特朗普阵营借其对阵克林顿时不利的民调展开攻势','Think Hillary Clinton Will Crush Donald Trump in the General Election? Don’t Be So Sure.':'以为希拉里·克林顿会在大选中碾压唐纳德·特朗普？别那么肯定。','How Team Clinton Is Planning to Defeat Trump':'克林顿团队打算如何击败特朗普','Here\'s Donald Trump\'s Best Strategy for Winning the White House':'唐纳德·特朗普入主白宫的最佳策略',
'Hard Choices':'艰难的抉择','Living History':'亲历历史','Crippled America: How to Make America Great Again':'受困的美国：如何让美国再次伟大','The Art of the Deal':'交易的艺术','Seven Principles of Good Government':'良好治理的七项原则',
'Dreams from My Father: A Story of Race and Inheritance':'父亲的梦想：关于种族与传承的故事','The Audacity of Hope: Thoughts on Reclaiming the American Dream (Vintage)':'无畏的希望：重拾美国梦的思考（Vintage版）','No Apology: Believe in America':'不必道歉：相信美国','The Amateur':'业余者','The Real Romney':'真实的罗姆尼','Republic, Lost: How Money Corrupts Congress--and a Plan to Stop It':'迷失的共和国：金钱如何腐蚀国会，以及制止它的方案','Confidence Men: Wall Street, Washington, and the Education of a President':'信心掮客：华尔街、华盛顿与一位总统的历练','Financial Fiasco: How America\'s Infatuation with Home Ownership and Easy Money Created the Economic Crisis':'金融惨败：美国对住房所有权和宽松信贷的迷恋如何酿成经济危机','The Great Financial Crisis: Causes and Consequences':'大金融危机：原因与后果',
'Al Gore - Earth in the Balance':'阿尔·戈尔 — 濒临失衡的地球','George W. Bush - A Charge to Keep: My Journey to the White House':'乔治·W.·布什 — 肩负使命：我的白宫之路','The Ralph Nader Reader':'拉尔夫·纳德文选','Larry Sabato - Overtime! The Election 2000 Thriller':'拉里·萨巴托 — 加时赛！2000年大选惊险纪实','Jeffrey Toobin - Too Close to Call: The Thirty-Six-Day Battle to Decide the 2000 Election':'杰弗里·图宾 — 胜负难分：决定2000年大选的三十六天之战','Andrew E. Busch & James W. Ceaser - The Perfect Tie: The True Story of the 2000 Presidential Election':'安德鲁·E.·布施与詹姆斯·W.·西瑟 — 势均力敌：2000年总统大选的真实故事','The Florida Recount / 2000 Election':'佛罗里达州重新计票／2000年大选','The Path to Florida':'走向佛罗里达','Digital History - The Disputed Election of 2000':'Digital History：争议中的2000年大选','Bush v. Gore':'布什诉戈尔案','Al Gore Concedes the 2000 Election':'阿尔·戈尔承认2000年大选败选',
'The Quest for the Presidency, 1988':'角逐总统宝座：1988年','Michael Dukakis: The Photo Op That Tanked':'迈克尔·杜卡基斯：惨败的坦克摆拍','How Presidential Race Was Won--and Lost : George Bush':'总统大选的胜负如何决定：乔治·布什','How Presidential Race Was Won-and Lost : Michael S. Dukakis':'总统大选的胜负如何决定：迈克尔·S.·杜卡基斯','L.A. Times, November 10, 1988 - ':'《洛杉矶时报》，1988年11月10日 — ',
'1976 Election Books and Biographies':'1976年大选书籍与人物传记','Jules Witcover - Marathon: The Pursuit of the Presidency, 1972-1976':'朱尔斯·维特科弗 — 马拉松：角逐总统宝座，1972—1976年','The Election of 1976 and the Administration of Jimmy Carter':'1976年大选与吉米·卡特政府','Craig Shirley - Reagan\'s Revolution: The Untold Story of the Campaign That Started It All':'克雷格·雪莉 — 里根的革命：开启一切的那场竞选鲜为人知的故事','Douglas Brinkley - Gerald R. Ford':'道格拉斯·布林克利 — 杰拉尔德·R.·福特','Julian E. Zelizer - Jimmy Carter':'朱利安·E.·泽利泽 — 吉米·卡特',
'Final 1968 Results':'1968年大选最终结果','The Making of the President 1968 (Landmark Political)':'总统的诞生：1968年（Landmark Political系列）','Nixonland: The Rise of a President and the Fracturing of America':'尼克松之国：一位总统的崛起与美国的分裂','The Memoirs of Richard Nixon':'理查德·尼克松回忆录','1948 Civil Rights speech':'1948年民权演说','1967 speech on dissent and intellectualism':'1967年关于异议与知识主义的演说','Vietnam: A History':'越南：一部历史','Secret of \'68':'1968年的秘密','Living Apart: How the Government Betrayed a Landmark Civil Rights Law':'隔离生活：政府如何背弃一部里程碑式民权法律','The G.O.P.\'s Journey From the Liberal Days of Nixon':'共和党走出尼克松自由派时代的历程','George Wallace and the 1968 Election':'乔治·华莱士与1968年大选',
'1960 Election Books and Links':'1960年大选书籍与链接','1960--LBJ vs. JFK vs. Nixon: The Epic Campaign That Forged Three Presidencies':'1960年：约翰逊、肯尼迪与尼克松之争——成就三位总统的史诗般竞选','The Making of the President 1960':'总统的诞生：1960年','The Real Making of the President: Kennedy, Nixon, and the 1960 Election':'总统的诞生真相：肯尼迪、尼克松与1960年大选','1960 Cast of Characters':'1960年大选人物一览','First Kennedy-Nixon Debate (video)':'肯尼迪与尼克松首次辩论（视频）','The Making of the President 1960 (video documentary, 1963)':'总统的诞生：1960年（1963年纪录片）',
'1948 Election Books and Links':'1948年大选书籍与链接','Truman':'杜鲁门','Truman\'s Triumphs: The 1948 Election and the Making of Postwar America':'杜鲁门的胜利：1948年大选与战后美国的形成','1948: Harry Truman\'s Improbable Victory and the Year that Transformed America':'1948年：哈里·杜鲁门出人意料的胜利与改变美国的一年','Thomas E. Dewey and His Times':'托马斯·E.·杜威和他的时代','The 1948 Democratic Convention (newsreel footage)':'1948年民主党全国大会（新闻纪录片片段）','The 1948 Republican Convention (newsreel footage)':'1948年共和党全国大会（新闻纪录片片段）','The 1948 Election Explained (video)':'解读1948年大选（视频）',
'Wilson':'威尔逊','Woodrow Wilson and the Progressive Era, 1910-1917':'伍德罗·威尔逊与进步时代，1910—1917年','Presidential Campaigns and Elections - 1916':'总统竞选与选举：1916年','Woodrow Wilson\'s Campaigns':'伍德罗·威尔逊的竞选','The Great GOP Spat -- of 1916':'共和党的大争执——1916年','German-Americans as Voters and Office-Seekers':'作为选民与公职竞逐者的德裔美国人','Woodrow Wilson, Irish-Americans, and the Election of 1916':'伍德罗·威尔逊、爱尔兰裔美国人与1916年大选','July 8, 1916: Alice Paul Pushes Presidential Nominee to Support Suffrage':'1916年7月8日：爱丽丝·保罗敦促总统候选人支持妇女选举权',
'Final 1896 Results':'1896年大选最终结果','1896 Election -- Overview and Political Cartoons':'1896年大选：概述与政治漫画','The First Battle: A story of the campaign of 1896':'第一场战役：1896年竞选纪事','"Cross of Gold" speech':'“黄金十字架”演说','"Front Porch" speech':'“前廊”演说','The Depression of 1893':'1893年经济萧条','The Panic of 1893':'1893年金融恐慌','The Panic of 1893 with Lawrence Reed':'劳伦斯·里德谈1893年金融恐慌','The Wonderful Wizard of Oz - A Monetary Reform Parable':'绿野仙踪：一个货币改革寓言','Pullman Strike of 1894':'1894年普尔曼罢工','Wilson-Gorman Tariff':'威尔逊—戈尔曼关税法','Plessy v. Ferguson':'普莱西诉弗格森案',
'Lincoln':'林肯','Abraham Lincoln, Stephen Douglas, and the Election of 1860':'亚伯拉罕·林肯、斯蒂芬·道格拉斯与1860年大选','Stephen A. Douglas':'斯蒂芬·A.·道格拉斯','Twelve Years a Slave':'为奴十二年','Incidents in the Life of a Slave Girl':'一个女奴的生平遭遇','How Lincoln Won the 1860 Republican Nomination':'林肯如何赢得1860年共和党提名','John Bell for President, 1860':'约翰·贝尔竞选总统，1860年','Running to Lose? The Candidacy of John C. Breckinridge':'注定败选的竞逐？约翰·C.·布雷肯里奇的参选',
'A Country of Vast Designs: James K. Polk, the Mexican War and the Conquest of the American Continent':'宏图之国：詹姆斯·K.·波尔克、对墨西哥战争与征服美洲大陆','Henry Clay: The Essential American':'亨利·克莱：不可或缺的美国人','Polk: The Man Who Transformed the Presidency and America':'波尔克：改变总统职位与美国的人',
' (video) ':'（视频）',
}
people={'David Heidler and Joanne Heidler':'戴维·海德勒与乔安妮·海德勒','Robert Merry':'罗伯特·梅里','Walter Borneman':'沃尔特·博恩曼','David Herbert Donald':'戴维·赫伯特·唐纳德','Harriet Jacobs':'哈丽雅特·雅各布斯','Robert W. Johannsen':'罗伯特·W.·约翰森','Solomon Northup':'所罗门·诺瑟普','William Jennings Bryan':'威廉·詹宁斯·布赖恩','William McKinley':'威廉·麦金莱','Edward Klein':'爱德华·克莱因','Johan Norberg':'约翰·诺伯格','Stanley Karnow':'斯坦利·卡诺','A. Scott Berg':'A.·斯科特·伯格','Andrew E. Busch':'安德鲁·E.·布施','Arthur Link':'阿瑟·林克','David McCullough':'戴维·麦卡洛','David Pietrusza':'戴维·皮特鲁萨','David Pietruza':'戴维·皮特鲁萨','George Wallace':'乔治·华莱士','Hubert Humphrey':'休伯特·汉弗莱','John Bellamy Foster & Fred Magdoff':'约翰·贝拉米·福斯特与弗雷德·马格多夫','Lawrence Lessig':'劳伦斯·莱斯格','Michael Kranish & Scott Helman':'迈克尔·克拉尼什与斯科特·赫尔曼','Peter Goldman':'彼得·戈德曼','Richard Nixon':'理查德·尼克松','Richard Norton Smith':'理查德·诺顿·史密斯','Rick Perlstein':'里克·珀尔斯坦','Ron Suskind':'罗恩·萨斯金德','Theodore White':'西奥多·怀特','W. J. Rorabaugh':'W.·J.·罗拉博','Barack Obama':'贝拉克·奥巴马','Mitt Romney':'米特·罗姆尼','Donald Trump':'唐纳德·特朗普','Gary Johnson':'加里·约翰逊','Hillary Clinton':'希拉里·克林顿'}
records=[]
for source in dict.fromkeys(r['source'] for r in cat['records'] if r['field']=='recommended_reading'):
    tokens=parts(source)
    for i in range(0,len(tokens),2):
        text=tokens[i]
        if text in pairs:tokens[i]=pairs[text];continue
        if not text.strip() or text==' -- ':continue
        # Exact author text nodes, including original CR/LF/space separators.
        author=text.strip().removesuffix(' -').strip()
        assert author in people,('Unreviewed reading-list node',repr(text))
        prefix=text[:len(text)-len(text.lstrip())]
        tokens[i]=prefix+people[author]+' — '
    zh=''.join(tokens);assert parts(zh)[1::2]==parts(source)[1::2]
    full[source]=zh;records.append({'sha256':hashlib.sha256(source.encode()).hexdigest(),'source':source,'zh':zh,'method':'human-full-field','keys':[r['key'] for r in cat['records'] if r['field']=='recommended_reading' and r['source']==source]})
(BASE/'editorial-records.json').write_text(json.dumps(full,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report={'checkedAt':'2026-10-08','uniqueSourcesReviewed':len(records),'recordPositions':sum(len(r['keys']) for r in records),'scope':'All native recommended_reading labels; readable title translations, not certification of published Chinese editions or linked articles.','revisions':records}
report['titleChoices']=[{'title':'Confidence Men','zh':'信心掮客','note':'依据作者介绍的市场信心与华尔街／华盛顿关系，保留confidence与confidence men骗局含义的双关；属于本项目意译，不宣称官方中文书名。','source':'https://ronsuskind.com/portfolio/confidence-men/'}]
(ROOT/'localization/annotations/reading-editorial-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
person_path=ROOT/'localization/glossary_people_zh.json'
person_terms=json.loads(person_path.read_text(encoding='utf-8'))
for source,zh in people.items():
    if '&' not in source and ' and ' not in source:person_terms[source]=zh
person_terms.update({'David Heidler':'戴维·海德勒','Joanne Heidler':'乔安妮·海德勒','John Bellamy Foster':'约翰·贝拉米·福斯特','Fred Magdoff':'弗雷德·马格多夫','Michael Kranish':'迈克尔·克拉尼什','Scott Helman':'斯科特·赫尔曼'})
person_path.write_text(json.dumps(person_terms,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Reviewed',len(records),'native reading lists;',report['recordPositions'],'record positions; tags/URLs intact.')
