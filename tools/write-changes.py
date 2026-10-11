"""List actual deliverable workspace changes; exclude ignored test caches."""
import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8').splitlines()
modified=git('ls-files','-m');added=git('ls-files','--others','--exclude-standard')
added=sorted(set(added+['CHANGES_ZH.md','CHANGES_ZH.json']))
report={'baseCommit':git('rev-parse','HEAD')[0],'modified':modified,'added':added}
historical=json.loads((ROOT/'localization/reviews/historical-review-report.json').read_text(encoding='utf-8'))
annotation=json.loads((ROOT/'localization/annotations/notes.zh-CN.json').read_text(encoding='utf-8'))
header_annotation=json.loads((ROOT/'localization/annotations/header-notes.zh-CN.json').read_text(encoding='utf-8'))
annotation_count=len({n['id'] for source in (annotation,header_annotation) for n in source['notes']})
(ROOT/'CHANGES_ZH.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 实际修改文件清单','',f'基于 `{report["baseCommit"]}`；本表覆盖本地化、历史校订与可选攻略的工作区。','',
 f'原有文件修改{len(modified)}份；新增{len(added)}份。原版JSON、105份questionset和人员能力代码均保留原始字节。','',
 '`.tools/`、`.test-artifacts/` 和Python缓存为已忽略的开发产物，不参与交付。未提交或推送Git。','',
 '## 主要新增内容','',
 '- `localization/stories.js`：显式剧本展示适配。',
 '- `localization/guide/`：可选双语攻略、独立原作预测器、访问建议、机制说明和UI文本维护源。',
 f'- `localization/annotations.js`、`localization/annotations/`：{annotation_count}条离线典故与政治术语旁注（含页眉）、研究来源和48个语录位置校订记录。',
 f'- `localization/reviews/`：历史批次累计{historical["uniqueSourcesThisRound"]}条完整原文校订、{historical["positionsThisRound"]}个复用位置、固定英文快照、逐行中文、原文疑点及按时代解释的术语表。',
 '- `localization/stories/`：110个离线包及双语源包、提取目录、索引、覆盖与校订报告。',
 '- `localization/glossary_zh.json`：统一术语；独立人物译名维护输入。',
 '- `tools/`：AST提取、离线构建、人工修订、覆盖及质量报告工具。',
 '- `tests/`：原版完整性、105组合双语通关、结局边界、语法、扩展回归及结果。',
 '- `static/vendor/story-assets/`：本地结局媒体与来源／失效记录。',
 '- `README_ZH.md`、`THIRD_PARTY_ZH.md`：使用、实测、校订限制与资源差异。','',
 '## 修改的原有文件','']
lines.extend('- `'+p+'`' for p in modified)
lines.extend(['','## 新增文件（完整列表）',''])
lines.extend('- `'+p+'`' for p in added)
(ROOT/'CHANGES_ZH.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Deliverables:',len(modified),'modified,',len(added),'added')
