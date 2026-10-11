"""Build small, independently loadable runtime packs and readable reports."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'localization/stories'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
cat=read(BASE/'catalogue.json');index=read(BASE/'index.json')
for scope in index:
 en=read(BASE/(scope+'.en-US.json'));zh=read(BASE/(scope+'.zh-CN.json'))
 compact={collection:{pk:{field:[r['key'] for r in rows] for field,rows in fields.items()} for pk,fields in ids.items()} for collection,ids in index[scope].items()}
 events=[dict(key=r['key'],**{k:r['location'][k] for k in ['script','start','end','literal']}) for r in cat['records'] if r['scope']==scope and r['collection']=='event']
 presentations=next((s['presentations'] for s in cat['scenarios'] if s['scope']==scope),[])
 (BASE/(scope+'.pack.json')).write_text(json.dumps({'index':compact,'en':en,'zh':zh,'events':events,'presentations':presentations},ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
report=read(BASE/'coverage.json')
lines=['# 内置剧本清单与文本覆盖率','',f"统计：{len(cat['scenarios'])} 个组合，{report['entries']} 条命名空间条目，{report['translated']} 条有中文译文。",'',
 '重复文本按不同剧本分别计数；同一剧本的隐藏选项及反馈记录全部保留。`pk@位置` 用于区分原版重复 ID。',
 '', '本表统计“已有译文”，不代表所有译文已完成人工历史校对。译文生成与校订来源记录在 translation-memory.json。','',
 '| 年份 | 总统候选人 | 竞选搭档 | 数据来源 | 剧本条目 | 已翻译 | 覆盖率 |','|---|---|---|---|---:|---:|---:|']
for s in report['scenarios']:lines.append(f"| {s['year']} | {s['candidateName']} ({s['candidate']}) | {s['runningMateName']} ({s['runningMate']}) | `{s['file']}` | {s['entries']} | {s['translated']} | {s['coverage']}% |")
lines.extend(['','## 共用文本与原版重复 ID','','背景和人物：`base.*.json`。高级竞选资料：`staff.年份ID.候选人ID.*.json`。','',
 '翻译字段：summary、recommended_reading、人物姓名/党派/简介/结局、questions_json.description、answers_json.description、answer_feedback_json.answer_feedback、issues_json.name/description/stance_1..7/stance_desc_1..7、states_json.name、endingPicker 的自然语言片段、特殊打字剧情。','',
 '源代码：JSON.parse 的参数通过 AST 解码，字面量数组通过受限的字面量读取器解析，均不执行剧本代码。','',
 '以下重复 ID 来自上游；保留原有顺序、记录和查找行为：','', '```json',json.dumps(cat['diagnostics'],ensure_ascii=False,indent=2),'```',''])
(BASE/'COVERAGE_ZH.md').write_text('\n'.join(lines),encoding='utf-8')
print('Built',len(index),'offline packs')
