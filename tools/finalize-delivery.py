"""Publish completion documentation only after fresh full runtime evidence."""
import datetime,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
write=lambda p,s:(ROOT/p).write_text(s,encoding='utf-8')
browser=read('tests/stories-browser-results.json')
notes=read('tests/annotations-results.json')
endings=read('tests/story-endings-results.json')
coverage=read('localization/annotations/coverage.json')
audit=read('localization/reviews/final-field-audit.json')
historical=read('localization/reviews/historical-review-report.json')
catalogue=read('localization/stories/catalogue.json')
assert {r['scope'] for r in browser['pairings']}=={s['scope'] for s in catalogue['scenarios']}
assert len(browser['pairings'])==105 and all(r['status']=='passed' and r['answers']==25 for r in browser['pairings'])
assert len(endings['fixtures'])==105 and sum(r['fixtures'] for r in endings['fixtures'])==20160
for report in [browser,notes,endings]:
    assert not report.get('failure')
    for key in ['errors','missing','external','warnings']:assert not report.get(key),key
assert notes['notes']==coverage['notes'] and notes['bindings']==coverage['boundFields']
assert notes['rendered']==notes['bindings']
assert not audit['unreviewed'] and audit['entries']==32770
assert len(historical['completeProseYears'])==15
epoch=lambda s:datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
packs=list((ROOT/'localization/stories').glob('*.pack.json'))
assert epoch(browser['date'])>=max(p.stat().st_mtime for p in packs),'Playthrough is older than packs'
assert epoch(endings['date'])>=max(p.stat().st_mtime for p in packs),'Ending test is older than packs'
assert epoch(notes['date'])>=(ROOT/'localization/annotations/index.json').stat().st_mtime,'Annotation test stale'
outputs=[]
for command in [['node','tests/syntax.cjs'],['node','tests/integrity.cjs'],['node','tests/stories-integrity.cjs'],['python','tools/audit-final-review.py']]:
    result=subprocess.run(command,cwd=ROOT,text=True,encoding='utf-8',capture_output=True)
    assert result.returncode==0,result.stdout+result.stderr
    outputs.append({'command':' '.join(command),'stdout':result.stdout.strip()})
paths=packs+[ROOT/'localization/annotations/index.json',ROOT/'localization/stories.js',ROOT/'localization/i18n.js',ROOT/'localization/annotations.js']
frozen={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
report={'finishedAt':now,'status':'passed','nativePairings':105,'bilingualGames':210,'endingFixtures':20160,
        'annotations':coverage,'fieldAudit':audit['counts'],'unreviewedFields':0,
        'browser':browser['browser'],'service':'Windows Python 3.12, http://127.0.0.1:8000',
        'runtimeReports':{p:read(p)['date'] for p in ['tests/stories-browser-results.json','tests/annotations-results.json','tests/story-endings-results.json']},
        'staticChecks':outputs,'testedArtifactSha256':frozen,
        'limits':['One seeded answer path per pairing; not every RNG and answer permutation.',
                  'Synthetic ending fixtures are not all naturally reached endings.',
                  'Final rerun in Chrome; previous Edge and extended checks are dated 2026-10-08.',
                  'Six inaccessible media have replacements; original Wallace movie not restored.',
                  'Original historical claims and uncertainty are disclosed, not independently certified.']}
write('localization/reviews/final-acceptance.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# 最终校订与实际验收','',f'完成时间（UTC）：{now}。全部15个年份／版本、105组合校订完成。','',
       '## 文本与来源','',
       f'- 全32770字段有中文并通过对应校验；完整字段{audit["counts"]["human-full-field"]}位置、专名{audit["counts"]["human-proper-name-verification"]}位置、短术语{audit["counts"]["human-short-terminology"]}位置，另2个党派上下文键。待审与缺失均0。',
       f'- 本轮历史批次累计5362个独立原文／23125位置；此前人物简介与其他完整字段也保留手写编写源。所有正文均不使用运行时在线翻译。',
       f'- {coverage["notes"]}条离线来源解释、{coverage["boundFields"]}个剧本字段、{coverage["noteBindings"]}个说明绑定。另含47语录键、48原版位置及14份阅读标题列表。','',
       '## 实际执行','',
       '| 测试 | 结果 | 报告起始时间（UTC） |','|---|---|---|',
       f'| 全组合断网双语通关 | 105×2＝210局，每局25题，数值、答案、访问及RNG完全一致 | {browser["date"]} |',
       f'| 旁注和交互 | 全绑定渲染、鼠标／键盘、语言切换、390px及四档CSS缩放通过 | {notes["date"]} |',
       f'| 结局边界及特殊事件 | 105组合／20160合成夹具；华莱士视频结束、中文动画、nextTask实际完成 | {endings["date"]} |','',
       f'最终浏览器：Chrome {browser["browser"]}，Windows；仅放行回环／data／blob请求，其余全部拦截。错误、资源缺失、外部请求和结局警告数组均为空。',
       '最终服务由Windows Python3.12实际运行在默认127.0.0.1:8000；早先8000沙箱服务超时，重启本项目服务到浏览器所在环境后默认端口成功完成全量回归。未修改系统网络或选举算法。','',
       '### 最后执行的静态检查','']
lines += ['- `'+o['command']+'`：'+o['stdout'] for o in outputs]
lines += ['', '## 真实剩余边界','',
          '一次固定随机序列与首个答案路径不能穷尽随机事件、全部答案组合。所有记录可显示中文，不等于每个排列都自然通关。合成结局也不替代所有自然触发。',
          '最终重跑是Chrome；旧Edge／扩展报告的日期为2026-10-08，未伪称这次重跑。缩放为CSS zoom，不是全部浏览器原生菜单测试。',
          '6个失效媒体替代、330条上游集合外引用、重复PK及1988布什538票空叙事保留。原华莱士电影与时长未还原。',
          '原作事实疑点、误署名、首发载体与史料获取失败详见[来源边界](FINAL_RESEARCH_BOUNDARIES_ZH.md)。不把编辑校订冒充独立学术认证。','',
          '原始英文111文件与7段计算AST检查通过。测试输入与原版基线没有为通过验收而重新生成。`final-acceptance.json`记录实际命令、时间及最终包SHA，供后续维护辨别测试是否过期。','']
write('localization/reviews/FINAL_TEST_REPORT_ZH.md','\n'.join(lines))
readme=(ROOT/'README_ZH.md').read_text(encoding='utf-8')
start=readme.index('**全部');end=readme.index('\n\n## 1.',start)
readme=readme[:start]+'**全部15个内置年份／版本、105种候选人与搭档组合已完成简体中文完整字段校订，缺失和待审均为0；最后重新执行210局断网双语通关与20160个结局夹具。** 原英文与机制保持一致。详见[最终验收](localization/reviews/FINAL_TEST_REPORT_ZH.md)与[史料边界](localization/reviews/FINAL_RESEARCH_BOUNDARIES_ZH.md)。'+readme[end:]
start=readme.index('首批逐句修订' if '首批逐句修订' in readme else '最终提供 **');end=readme.index('## 2.',start)
readme=readme[:start]+f'''最终提供 **{coverage['notes']}条有来源的离线解释**，绑定{coverage['boundFields']}个剧本文本字段及全部页眉语录位置。现实事件、角色攻击、原作错误、架空情节与典故推断分别说明；只有主动点击来源链接才联网。

已逐段校订全部背景、人物、问题、所有回答、反馈、结局及竞选团队资料；少见短术语和专名另行复核，未把机器草稿或规则替换冒充审读。历史批次累计5362条独立原文／23125复用位置，早期人物与共用字段另保留人工编写源。全部字段对应检查见[final-field-audit.json](localization/reviews/final-field-audit.json)，各组合统计见[历史报告](localization/reviews/HISTORICAL_REVIEW_ZH.md)。

典故包括独立国库、人民主权、金本位与自由铸银、工作权法、迪克西民主党人、政治狗哨、互联网竞选梗、另类事实、功夫流感、文学幽灵和“阻止偷窃”的角色互换。正文保留原作立场；无法认证的首发载体或政治指控明确记录。14份推荐阅读列表仅翻译可见标题与作者标签，保留链接，不宣称相应中文书籍已经出版。

说明全文见[NOTES_ZH.md](localization/annotations/NOTES_ZH.md)，剩余查证边界见[FINAL_RESEARCH_BOUNDARIES_ZH.md](localization/reviews/FINAL_RESEARCH_BOUNDARIES_ZH.md)。早期阶段进度为历史记录，保存在[PROGRESS_ZH.md](localization/reviews/PROGRESS_ZH.md)。

'''+readme[end:]
glossary=read('localization/glossary_zh.json')
readme=readme.replace('273个人名部分、602个术语／完整名称',f"{len(glossary['names'])}个人名部分、{len(glossary['terms'])}个术语／完整名称")
start=readme.index('初译在开发时由Google' if '初译在开发时由Google' in readme else '开发时初译曾用于起草');end=readme.index('## 6.',start)
readme=readme[:start]+'''开发时初译曾用于起草；现有全部内置长文本已经完整字段读写校订，短术语与姓名州名另有复核记录。最终包缺失0条、未审0条。保留初译来源记录，不改标签伪造专家审定。

原文事实疑点不直接改写：正文保留年代、数字和人物说法，旁注解释实际史料与推断边界。文件名含RESEARCH_PENDING的年代报告为兼容旧元数据保留，开头已更新最终状态，其旧启动记录明确标为归档。

'''+readme[end:]
start=readme.index('## 7. 实际测试');end=readme.index('## 8.',start)
readme=readme[:start]+f'''## 7. 实际测试

最终实际验收于2026-10-10执行，Windows／Chrome {browser['browser']}，默认本地服务8000。全部105组合分别中英文通关，共210局，每局25题；相同种子和选择的全国／州票数、答案、访问与随机调用完全相同。外网请求在浏览器中拦截，错误、缺失与外部请求为空。

{coverage['notes']}条旁注及全部绑定真实渲染；鼠标、键盘、语言切换、390px视口及80／100／125／150% CSS缩放通过。全部105组合的20160个合成结局夹具、华莱士本地视频回调及中文打字剧情实际通过。111原数据字节、7计算AST、全部32770字段的HTML／变量完整性通过。

报告与真实时间：[最终验收](localization/reviews/FINAL_TEST_REPORT_ZH.md)、[双语通关](tests/stories-browser-results.json)、[结局](tests/story-endings-results.json)、[旁注](tests/annotations-results.json)、[静态完整性](tests/stories-integrity-results.json)。最终包哈希保存于[final-acceptance.json](localization/reviews/final-acceptance.json)。

边界：每组合一个固定随机序列与首个答案路径，未穷尽所有随机与答案排列；结局夹具不是全部自然触发。旧Edge及扩展界面报告为2026-10-08，没有伪称本次重跑。此前8000服务超时后，将本项目服务在实际浏览器所在环境重启，默认8000完成全量验收；未修改系统网络。

上游330条集合外引用、重复PK、1988布什538票空叙事保持。六个失效媒体替代及中文打字时长差异见第6节。独立史料未确认的细节公开记录，测试通过不等于所有原作主张已获学术认证。

'''+readme[end:]
readme=readme.replace('python tools/build-annotations.py\nnode tests/stories-integrity.cjs','python tools/build-annotations.py\npython tools/report-historical-reviews.py\npython tools/audit-final-review.py\nnode tests/stories-integrity.cjs')
readme=readme.replace('当前批次为 `1844`、`1844-supplement`、`1844-base`、`political-terms`、`1860`、`1860-base`、`1860-supplement`、`1896-a`至`1896-f`及`1896-labels`。','批次涵盖1844至2020全部年份及final-supplement，清单与数量见historical-review-report.json。短术语和专名复核分别见final-terms-review.json、final-names-review.json。')
readme=readme.replace('`editorial-records.json` 和','`editorial-records.json` 和')
write('README_ZH.md',readme)
progress=(ROOT/'localization/reviews/PROGRESS_ZH.md').read_text(encoding='utf-8')
progress=progress.split('\n\n## 最终收尾（2026-10-10，历史记录以上保留）')[0]
progress+='\n\n## 最终收尾（2026-10-10，历史记录以上保留）\n\n'+f'- 全部15版本／105组合完整字段完成，剩余0。最后补齐2000、2012、2016a、2016、2020及65个团队／短结局等字段。历史批次5362独立原文／23125位置；185短术语、316专名另行复核。全32770字段对应审计通过。\n- {coverage["notes"]}来源旁注／{coverage["boundFields"]}剧本字段／{coverage["noteBindings"]}绑定。全部快照、中文、元数据及原作疑点保留。\n- 最新全量双语通关：{browser["date"]}，105组合210局；旁注：{notes["date"]}；结局：{endings["date"]}，105组合20160夹具。所有错误、缺失、外部请求和警告为空。\n- 默认8000实际通过：重启此前沙箱中的本项目服务，在浏览器所在环境运行Python，未改系统网络。具体结果与包SHA见final-acceptance.json、FINAL_TEST_REPORT_ZH.md。\n- 仅固定种子首答案路径，随机未穷尽；失效媒体、上游引用与原作未认证细节如实记录。此前未完成说明均为过去批次记录，当前审读已收尾。\n'
write('localization/reviews/PROGRESS_ZH.md',progress)
print('Final documentation generated from fresh passed evidence')
