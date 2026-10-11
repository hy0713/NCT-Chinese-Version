"""Reproducible coverage/provenance and an honest human proofreading queue."""
import collections,hashlib,json,re,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'localization/stories'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cat=read(BASE/'catalogue.json');memory=read(BASE/'translation-memory.json');full=read(BASE/'editorial-records.json');overrides=read(BASE/'editorial-overrides.json')
parts=runpy.run_path(str(ROOT/'tools/translate-stories.py'))['parts']
packs={scope:read(BASE/(scope+'.pack.json')) for scope in {r['scope'] for r in cat['records']}}
queue={};counts=collections.Counter();prose=collections.Counter();byScope={};residual=[]
for r in cat['records']:
 source=r['source'];zh=packs[r['scope']]['zh'].get(r['key'])
 if source in full or source in overrides:status='human-revised'
 else:
  methods={memory.get(hashlib.sha256(p.strip().encode()).hexdigest(),{}).get('method','missing') for p in parts(source)[::2] if re.search('[A-Za-z]',p)}
  status='needs-proofreading' if any(m.startswith('draft-') for m in methods) else 'reviewed-segments-or-terms' if 'missing' not in methods else 'missing'
 counts[status]+=1;byScope.setdefault(r['scope'],collections.Counter())[status]+=1
 if len(re.sub('<[^>]*>','',source))>=40:prose[status]+=1
 if status=='needs-proofreading':
  row=queue.setdefault(r['sha256'],{'source':source,'zh':zh,'keys':[],'reason':'Development-time machine draft, not fully historically proofread.'});row['keys'].append(r['key'])
 text=re.sub(r'<[^>]*>','',zh or '');text=re.sub(r'https?://\S+','',text)
 if re.search(r'[A-Za-z]{3,}(?:[ -]+[A-Za-z]{3,}){2,}',text):residual.append({'key':r['key'],'zh':text,'status':'proper-name-parenthesis' if re.search(r'\([A-Za-z ]{10,}\)',text) else 'review-needed'})
notes=[
 {'topic':'典故与网络梗校注','note':'来源说明及逐段修订持续更新，当前数量见 ../annotations/coverage.json，全文见 ../annotations/NOTES_ZH.md。全部105组合的完整字段审读范围、尚未审读字段及原文疑点见 ../reviews/HISTORICAL_REVIEW_ZH.md；固定英文快照及对应修订记录保留在该目录。疑似误署名、未找到最早载体及游戏虚构明确标记；原作人物观点与校注事实区分。全部长文本已有完整字段编辑，短术语与专名另行复核；这不是独立历史学者对每项原作主张的认证。'},
 {'topic':'原文史实与讽刺','note':'剧情含架空史、讽刺和原文笔误；译文不擅自更改为真实历史。2020 部分人物头衔及亲属关系、2016 法拉奇的时间指代等，已逐段校订，原作疑点与查证边界见 ../reviews/FINAL_RESEARCH_BOUNDARIES_ZH.md。'},
 {'topic':'术语','note':'已区分 liberal/Libertarian、decriminalization/legalization、州权/人民主权原则、自由铸银/金本位、竞选组合/入场券。较少见人物与利益团体音译仍建议人工复核。'},
 {'topic':'完整字段与短术语复核','note':'全部105内置组合的问题、全部回答、反馈、背景、人物、结局和团队简介已有完整字段审读；185项短术语与316项专名分别复核，原文SHA与具体键及当前包的对照见 ../reviews/final-field-audit.json。没有把机器草稿或规则替换冒充逐段审读。'},
 {'topic':'特殊打字剧情','note':'^ 延时控制与 < 换行控制完整保留。开始播放前按当前语言选择文本；播放中途切换语言不会重启动画，因此当前动画仍沿用启动时语言。'},
 {'topic':'失效媒体','note':'6 个远程媒体无法取得，使用本地替代。1968 隐藏视频用3秒黑色视频替代，原 onended/videoDone/nextTask 保留；影片内容和原时长未还原。'},
 {'topic':'上游问题','note':'原版重复 pk、330 条指向未加载集合的引用保持原样。1988 布什538票特殊路径原文返回空白叙事，未擅自增加剧情。'},
 {'topic':'随机与分支','note':'105 组合各完成一个固定随机序列下的中英文完整对局；边界结局采用合成结果测试。未穷尽所有随机事件、所有答案路径及每个特殊条件组合。'},
]
report={'schema':1,'entries':len(cat['records']),'missing':sum(not packs[r['scope']]['zh'].get(r['key']) for r in cat['records']),'recordReviewCounts':dict(counts),'longTextReviewCounts':dict(prose),'uniqueSourcesNeedingProofreading':len(queue),'segmentMethods':dict(collections.Counter(v['method'] for v in memory.values())),'fullFieldHumanOverrides':len(full),'segmentHumanOverrides':len(overrides),'scopes':{s:dict(c) for s,c in byScope.items()},'residualEnglish':residual,'notes':notes}
write(BASE/'quality-review.json',report);write(BASE/'review-queue.json',list(queue.values()))
lines=['# 译文校订状态与剩余风险','',f"已生成中文：{report['entries']} 条；空译文／缺失：{report['missing']} 条。",'',
 '全部内置长文本已完成完整字段校订，短术语与专名另行复核。没有把英文段落复制为中文来计算完成率。人名、URL、作品名和缩写可按原文保留。','',
 '## 实际来源统计','', '| 状态 | 命名空间条目数 | 长文本条目数（至少40字符） |','|---|---:|---:|']
for status,n in counts.items():lines.append(f'| {status} | {n} | {prose[status]} |')
lines.extend(['',f"剩余机器草稿待审独立原文：**{len(queue)}** 条。见 `review-queue.json`，每条包含英文、当前中文和全部对应键。",'',
 '完整字段人工修订记录：`editorial-records.json`；段落／片段修订：`editorial-overrides.json`；开发时初译来源和复用记录：`translation-memory.json`。', '',
 '仅使用术语、框架已审译文或人工片段构成的字段，列为 `reviewed-segments-or-terms`；这不意味着整段已经过独立历史学者审读。','', '## 剩余事项',''])
for note in notes:lines.append(f"- **{note['topic']}**：{note['note']}")
lines.extend(['','## 复现与人工修订','','优先在 `editorial-records.json` 中按完整英文原文添加中文；不要更改原文键。保留原始HTML标签、属性、实体、URL和占位符，随后执行：','','```powershell','python tools/translate-stories.py --offline','python tools/build-stories.py','python tools/review-stories.py','node tests/stories-integrity.cjs','```','',
 '运行时只读取本地 pack 文件。开发时的批量初译工具默认会联网；日常重建请使用 `--offline`。原作疑点与史料获取边界公开记录，不把编辑校订称为独立学术认证。',''])
(BASE/'REVIEW_ZH.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['entries','missing','recordReviewCounts','uniqueSourcesNeedingProofreading']},ensure_ascii=False))
