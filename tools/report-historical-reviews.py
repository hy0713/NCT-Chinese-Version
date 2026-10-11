"""Audit reviewed batches against immutable source catalogue and current packs."""
import collections,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'localization/reviews'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
cat=read(ROOT/'localization/stories/catalogue.json')
full=read(ROOT/'localization/stories/editorial-records.json')
records={r['key']:r for r in cat['records']};seen={};batches={};dates=[]
for path in sorted(BASE.glob('*-editorial-review.json')):
    batch=read(path);batches[batch['batch']]={'uniqueSources':batch['uniqueSourcesReviewed'],'positions':batch['recordPositions']}
    dates.append(batch['checkedAt'])
    for r in batch['revisions']:
        assert hashlib.sha256(r['source'].encode()).hexdigest()==r['sha256']
        assert r['zh']==full[r['source']],f'Stale review: {path.name}:{r["index"]}'
        assert all(records[k]['source']==r['source'] for k in r['keys'])
        seen[r['source']]=r
scenarios=[]
for scenario in cat['scenarios']:
    rows=[r for r in cat['records'] if r['scope']==scenario['scope']]
    # Initial menu data come from the base namespace, including every ending.
    pks={scenario['candidate'],scenario['runningMate']}
    rows += [r for r in cat['records'] if r['scope']=='base' and
        ((r['collection']=='candidate_json' and r['location']['pk'] in pks) or
         (r['collection']=='election_json' and r['location']['pk']==scenario['election']))]
    pack={}
    for scope in {r['scope'] for r in rows}:pack.update(read(ROOT/'localization/stories'/f'{scope}.pack.json')['zh'])
    counts=collections.Counter();remaining=[]
    for r in rows:
        assert pack.get(r['key']),r['key']
        if r['source'] in full:status='human-full-field'
        elif len(re.sub(r'<[^>]*>','',r['source']))<=40:status='short-label-or-name'
        else:status='needs-full-field-review';remaining.append(r['key'])
        counts[status]+=1
    if scenario['year'] in {'1844','1860','1896','1916','1948','1960','1964','1968','1976','1988','2000','2012','2016a','2016','2020'}:assert not remaining,(scenario['scope'],remaining)
    scenarios.append({'scope':scenario['scope'],'year':scenario['year'],'candidate':scenario['candidateName'],
        'runningMate':scenario['runningMateName'],'entriesIncludingBase':len(rows),
        'reviewCounts':dict(counts),'remainingProse':remaining})
completeYears=[year for year in dict.fromkeys(s['year'] for s in scenarios)
    if all(not s['remainingProse'] for s in scenarios if s['year']==year)]
report={'checkedAt':max(dates),'uniqueSourcesThisRound':len(seen),
    'positionsThisRound':sum(r['source'] in seen for r in cat['records']),
    'batches':batches,'scenarios':scenarios,'completeProseYears':completeYears,
    'remainingProjectDraftSources':read(ROOT/'localization/stories/quality-review.json')['uniqueSourcesNeedingProofreading'],
    'limits':['Short labels and person/state names retain glossary review; full prose was read in complete fields.',
        'No independent historian certification. Preserve original partisan claims and disclose source errors.',
    'Only years listed in completeProseYears have complete prose-field coverage; segment review alone does not qualify.']}
(BASE/'historical-review-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 美国历史、政治术语与政治梗校订','',
    f'历史批次累计完整字段校订：{len(seen)}条独立原文，覆盖{report["positionsThisRound"]}个复用位置。原英文、数据ID与游戏数值保持原样。','',
    '全部15个内置年份／版本、105种可玩候选人与搭档组合均已完成完整字段审读。最后复核竞选团队、短结局、议题、党派、七级立场及人名州名。短术语与专名复核和长篇审读分开统计；推荐阅读标题已单独校订。完整32770字段校验见final-field-audit.json。',
    f'完整长文本审读的年份：{", ".join(completeYears)}。下表涵盖全部105组合；待逐段校订数由实际完整字段记录判定，不能仅凭译文已有中文判定。','',
    '| 组合 | 含菜单／人物／结局条目 | 完整字段人工修订 | 短标签／人名州名 | 待逐段校订 |',
    '|---|---:|---:|---:|---:|']
for s in scenarios:
    counts=s['reviewCounts'];lines.append(f'| {s["scope"]} | {s["entriesIncludingBase"]} | {counts.get("human-full-field",0)} | {counts.get("short-label-or-name",0)} | {len(s["remainingProse"])} |')
lines += ['', '## 已修正的语义问题','',
    '- annexation：吞并，不是“附上”；acceptance letter：接受提名的公开信，不是“录取信”。',
    '- sectional：地域／地区之间，不是阶层；state politics：州级政治，不是国家政治。',
    '- internal improvements：国内公共工程；国家银行与独立国库不混同于现代央行。',
    '- Southern Whigs：批评其仍效忠立场激进化的政党，纠正原译的立场颠倒。',
    '- nativism：排外的本土主义，不是原住民；自由党与自由意志党区分。',
    '- 入籍、投票等待期、奴隶主补偿与非洲殖民安置分别保留，未弱化选项立场。',
    '- 利维·伍德伯里沿用项目统一译名；达拉斯／弗里林海森的参议员职务明确为联邦参议员。','',
    '## 原作疑点与旁注','',
    '“Thomas Birney”正文保留原名，旁注说明实际候选人为James G. Birney；“does derive”疑似漏not，不悄悄颠倒含义；“some of all”按上下文理解为部分或全部，并公开说明。1844年使用“天定命运”固定措辞的年代问题另作旁注。',
    '众议院选总统按州代表团一州一票；原作以席位多数预测结果是简化叙事，未修改其算法。',
    '本轮另审读12段跨年代高风险术语文本：1860年的一无所知党、人民主权与脱党者，1964／1968年的迪克西民主党人、稳固南方、南方战略和政治狗哨。Southern bolters曾被初译为“南方爆弹手”，已改为脱离党派的南方人；vindicated critics意为印证批评者的说法，而不是为他们辩护。','',
    '## 1860年补充校订','',
    '- 区分限制奴隶制扩张、立即废奴、社会平等、公民身份与投票权，保留各个选项的政治差异。人民主权涉及居民决定奴隶制问题；不等同于现代一般民主口号。',
    '- 黑色共和党是带有种族主义意味的政治攻击语，不是对黑人共和党成员的称呼；喷火派指拥护奴隶制及脱离联邦的激进派，州权立场与脱离联邦不能简单画等号。',
    '- 补充斯科特案、莱蒙案、弗里波特学说、个人自由法、科温修正案、联合选举人名单及Hunkers／Barnburners政治绰号的来源旁注。',
    '- 原文把赠地大学写成提供中等教育，正文保留而旁注解释其高等教育背景；nationalization按答案及法律语境理解为入籍，并公开记录这一判断。没有改动原作英文。',
    '- 非洲殖民安置保留其历史政治含义，避免误称所有获释奴隶此前都来自非洲；1808年海外奴隶输入禁令与国内奴隶制、奴隶买卖分别说明。','',
    '所有来源、史料原文及政治绰号解释见 [校注](../annotations/NOTES_ZH.md)。按年代区分术语的输入见 `glossary-context.zh-CN.json`，通过noteId关联完整来源。','',
    '## 1896年补充校订','',
    '- 完整区分金本位、自由铸银、有限购银、固定或浮动金银比价、关税保护、工伤赔偿、联邦监管与州权立场。',
    '- 政治语境中的wet译为反禁酒派；Gold Democrats是支持金本位的民主党人，不是黄金制成的党。patronage jobs译为酬庸官职；nail-biter／squeaker译为胶着的选举。',
    '- 修正J. P. 摩根被初译成现代公司“摩根大通”、坎顿被误译为广州、sectional unity被误译为“部门团结”等问题；“反对关税”的强调没有颠倒。',
    '- 原作1894年购银法废止、爱达荷妇女投票、农村邮政与铁路融资法案的时间线疑点保留正文，旁注以参议院、国会记录、邮政及国家公园管理局资料说明。effluence的原意无法确定，明确记录上下文翻译判断。',
    '- 保留反工会、排外、白人至上、创造论与社会达尔文主义选项的具体立场；不把玩家可选台词当作真实历史人物的逐字引文。','',
    '## 1916年补充校订','',
    '- 完整区分备战与参战、中立国权利与限制航运、提高关税与税收改革、联邦监管与州权、工伤赔偿与工资、族裔身份与忠诚指控。',
    '- 新增15条离线说明，包括族裔连字符、和平口号、威尔逊提前交权预案、布兰代斯、菲律宾自治、墨西哥远征、复活节起义、工伤赔偿、国际联盟及休斯生涯。',
    '- 原作1916年超额利润税、英语识字测试与伯克特人名疑点保留并解释；小笔误的上下文解读记在metadata。相关查证判断和来源边界见`1916-RESEARCH_ZH.md`。','',
    '## 1948年补充校订','',
    '- 保留杜鲁门、杜威及替代搭档的劳工、反共、民权、医疗、预算、住房和外交政策差异。量入为出的自由主义不是自由意志主义，工伤赔偿不是工资，党纲条款不是木板。',
    '- 新增15条来源说明：责任到此为止、火车竞选、无所作为的国会、错误报纸头条、以色列时区、军队整合、柏林占领区、忠诚审查、杜威—史塔森辩论、亨利·华莱士、总统任期、核管制及不同援助政策。',
    '- 保留原作日期与two-term措辞，说明宣布独立／托管终止／事实承认、赢得两次选举／完成两届任期、东西占领区／1949年建国之间的差别。未改游戏时间或数值。','',
    '## 1960年补充校订','',
    '- 肯尼迪的约翰逊／赛明顿／汉弗莱、尼克松的洛奇／德克森／洛克菲勒／戈德华特七种搭档组合全部纳入。逐段保留民权、医疗、工会、税收、农业、外交及国防选项的立场区别。',
    '- 修正金博士遭监禁时的condolences为慰问而非哀悼；Quemoy／Matsu为金门／马祖；hard money按本段利率语境译为紧缩货币；block grants为整笔拨款；right-to-work不是政府提供工作的保证。',
    '- 新增15条离线旁注，包括宗教偏见、金被捕的缓刑背景、导弹差距、U-2、外岛防卫、工会调查、医疗方案、未承诺选举人、电视辩论、《迪克西》及尼克松1968年当选。',
    '- 原作150名牧师的精确人数及达拉斯吐口水细节尚未从所查资料独立证实，明确保留为待核细节。Republican Congress按语境理解为共和党议员，避免虚构共和党控制第86届众议院。详见`1960-RESEARCH_ZH.md`与metadata。','',
    '## 1964年补充校订','',
    '- 约翰逊／汉弗莱与戈德华特／米勒的全部剩余200原文逐段审读，保留反对、废除、依法执行民权法案的差别，以及候选人针对工会、联邦项目和州权的立场。',
    '- 新增11条说明：经济数值年代、Medicare、学校祷告、苏联两种领导职务、里根演说、贝克调查、共和党人自白广告、三K党背书、民权法、南方地理与结局修辞。原数值、州名单及结局条件不变。',
    '- 原作4%通胀／3%失业、执政两年、贝克审判、重建后首次转向及一个世纪未决选举均另注明史实边界；NAACP分会个人功绩仍待核。来源与查证异常见`1964-RESEARCH_ZH.md`。','',
    '## 1968年补充校订','',
    '- 全部十一种组合的剩余492原文实际读写，覆盖2309复用位置；同一原文共享不跳过独有搭档问答。完整保留原作歧视性台词、政策差别与架空结局。',
    '- 新增23条离线说明：陈香梅、辩论架空、六日战争、哥伦比亚、城市骚乱、沃伦法院、1957年尼克松职务、移民、平权、启蒙、环保、黄金、春节攻势、多米尼加、贸易、汉弗莱口号、Jumbo、尖脑袋修辞、未决选举、营养、避孕与叛国、芝加哥调查。',
    '- 1964比较年份、Wainright拼写与crusader歧义公开记录；Jumbo轶事原始口述及割喉台词等未独立认证。隐藏动画的所有控制命令序列一致。详见`1968-RESEARCH_ZH.md`。','',
    '## 1976年补充校订','',
    '- 八种原生搭档组合的366条剩余完整原文逐段读写并应用，覆盖2189个复用位置。福特未获全国选举进入白宫、最后任期、粮食起始日期、Roe案拼写及竞选途中语法疑点均公开记录。',
    '- 新增25条离线说明：Playboy、卡特乌托邦、福特摔倒、玫瑰园、斯克鲁奇、斯库普、教会会籍、充分就业提案、工作权、核试验、石油、纽约贷款、布朗、彻奇调查、巴茨、巴拿马及死刑程序。',
    '- 教会报纸全文抓取失败，仅查搜索文本并说明边界；贝蒂75%与麦戈文方案细节等未独立核准。回归状态与连接失败记录见PROGRESS_ZH.md及tests实际报告。详见1976-RESEARCH_ZH.md。','',
    '## 最后五个版本与补充字段','',
    '- 1988：325条完整原文／1408位置；2000：337条加丹福思1条补充；2012：523条；2016a：391条；2016：501条；2020：388条。每批均保留固定英文快照、逐行中文、元数据与键映射。',
    '- 最后补充65个完整字段／740位置，包括竞选团队简介及短结局。185项短术语与316项专名另有独立复核清单；党派Progressive与意识形态Progressive通过具体字段键区分。',
    '- 2016／2020的邮件、民事和解、枪击统计、弹劾程序、最高法院、口罩历史、疫苗条件、族裔谐音、卡斯特罗兄弟和脱欧时间错位等均附有来源的离线旁注。余下原作事实疑点与获取失败明确列在FINAL_RESEARCH_BOUNDARIES_ZH.md。',
    '## 复现与边界','',
    '每批固定英文快照和逐行中文放在本目录；`tools/apply-historical-review.py 批次名`校验原文SHA、键、HTML及占位符后合并到独立语言包。不要用变化后的待审队列作为行号依据。执行离线构建，再运行 `tools/report-historical-reviews.py`可重建本报告。','',
    f'整个项目剩余独立机器草稿待审数：**{report["remainingProjectDraftSources"]}**。当前报告不会把术语修订或技术覆盖当作所有年份已获历史质量认证。','']
(BASE/'HISTORICAL_REVIEW_ZH.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['uniqueSourcesThisRound','positionsThisRound','remainingProjectDraftSources']},ensure_ascii=False))
