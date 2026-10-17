# The New Campaign Trail 简体中文本地版

入口：`campaign-trail/index.html`。源码来自 [NCT官方仓库](https://github.com/newcampaigntrail/newcampaigntrail.github.io)，基于提交 `d6655ef6ad80ab9a8fe5510d0fd43874e57dacbf`。第二阶段保留第一阶段的部署与界面汉化，没有覆盖英文数据，没有引入前端框架。本项目用于个人本地游玩与学习。

**全部15个内置年份／版本、105种候选人与搭档组合已完成简体中文完整字段校订，缺失和待审均为0；最后重新执行210局断网双语通关与20160个结局夹具。** 原英文与机制保持一致。详见[最终验收](localization/reviews/FINAL_TEST_REPORT_ZH.md)与[史料边界](localization/reviews/FINAL_RESEARCH_BOUNDARIES_ZH.md)。

## 1. Windows启动与语言切换

Windows限制8000端口时自动选择其他可用端口，并在本地 .nct-port 记住地址。该文件不上传。浏览器按端口区分成就与偏好，换地址不会删除旧地址数据。显式 --port 仍使用指定端口；不指定时自动恢复。

电脑需要Python3；本次使用Windows上的Python3.12。游玩不需要Node.js、npm、pip包或互联网。

1. 双击 **start.bat**，启动本地服务并自动打开游戏。默认优先使用localhost:8000，不可用时以窗口实际显示的地址为准。
2. 点击“开始游戏”，选择年份、总统候选人、副总统、模式和难度。
3. 选择答案并继续，可访问州、查看民调，直至选举之夜与结算。
4. 在启动脚本窗口按 `Ctrl+C` 停止服务。

PowerShell启动：

```powershell
cd <PROJECT>
python server.py --open
```

默认仅监听 `127.0.0.1:8000`。端口被占用时执行 `start.bat --port 8001`，入口相应变为 `http://localhost:8001/campaign-trail/index.html`。不要用 `file://` 直接打开HTML，游戏需要通过HTTP加载JSON。

- 默认简体中文；顶部 **English／简体中文** 按钮即时切换。
- 语言保存在 `localStorage` 的 `nct.language` 中。
- 切换不重置题目、答案、访问、民调、票数或结果，不重新计算或调用随机数。
- 刷新页面按原版规则重新开始；语言持久化不等于保存进度。浏览器、主机名和端口不同，存储也不同。
- 1968隐藏打字动画在启动时选择语言；播放中途切换不会重启当前动画。

### 历史典故与网络梗旁注

中文模式中，已校注的句子和页眉语录旁有 **“典故”** 按钮。点击后在对应文字旁展开解释；可点“关闭”或按 `Esc` 收起。按钮不会替你选择回答，回车、空格和方向键操作旁注时也不会触发游戏快捷键。

最终提供 **288条有来源的离线解释**，绑定5916个剧本文本字段及全部页眉语录位置。现实事件、角色攻击、原作错误、架空情节与典故推断分别说明；只有主动点击来源链接才联网。

已逐段校订全部背景、人物、问题、所有回答、反馈、结局及竞选团队资料；少见短术语和专名另行复核，未把机器草稿或规则替换冒充审读。历史批次累计5362条独立原文／23125复用位置，早期人物与共用字段另保留人工编写源。全部字段对应检查见[final-field-audit.json](localization/reviews/final-field-audit.json)，各组合统计见[历史报告](localization/reviews/HISTORICAL_REVIEW_ZH.md)。

典故包括独立国库、人民主权、金本位与自由铸银、工作权法、迪克西民主党人、政治狗哨、互联网竞选梗、另类事实、功夫流感、文学幽灵和“阻止偷窃”的角色互换。正文保留原作立场；无法认证的首发载体或政治指控明确记录。14份推荐阅读列表仅翻译可见标题与作者标签，保留链接，不宣称相应中文书籍已经出版。

说明全文见[NOTES_ZH.md](localization/annotations/NOTES_ZH.md)，剩余查证边界见[FINAL_RESEARCH_BOUNDARIES_ZH.md](localization/reviews/FINAL_RESEARCH_BOUNDARIES_ZH.md)。早期阶段进度为历史记录，保存在[PROGRESS_ZH.md](localization/reviews/PROGRESS_ZH.md)。

## 2. 全部内置剧本清单

原生菜单共有 **15个年份选项、32名可玩总统候选人、105种总统／竞选搭档组合**：2020、2016、2016a、2012、2000、1988、1976、1968、1964、1960、1948、1916、1896、1860、1844。2016a是原生替代历史选项。

范围依据：`election_list.json` 的年份 → `candidate.json` 中同一选举且 `is_active === 1` 的候选人 → `running_mate.json` 的搭档关联 → 原版实际加载的 `static/questionset/年份_候选人姓氏_搭档姓氏.html`。

逐个组合的ID、来源、记录数量、文本数量和覆盖率见 [COVERAGE_ZH.md](localization/stories/COVERAGE_ZH.md)、[catalogue.json](localization/stories/catalogue.json)。没有使用 `mods.json` 的 `historical` 标签判定原生范围。`static/mods/` 和社区专属内容保持原样。

生成 **32,770条中文命名空间条目、6,061条独立完整原文、6,536个去重文本片段**，缺失0条。重复内容按所属剧本分别计数。提取也保留初始数据库中的部分未开放人物资料，不将它们计为额外可玩组合。

## 3. 源码结构与加载

| 文件／目录 | 作用 |
|---|---|
| `campaign-trail/index.html` | 原版页面、语言按钮、本地库与语言模块入口 |
| `static/js/indexCode.js` | 主题、标语、初始JSON；开始按钮等待数组就绪 |
| `static/js/campaign_trail.js` | 配置、问题、反馈、访问、地图、民调、管理、选举之夜与结算，在原渲染位置接入翻译 |
| `campaign_trail_other.js`、`bigshot.js`、`christmas.js` | 辅助控件、答案效果分析、配乐和主题 |
| `static/js/sea_to_sea.js` | 管理数据与人员能力，整份未修改 |
| `static/json/`、`static/questionset/` | 原版数据库及105份组合剧本，未修改 |
| `static/js/us-map-1.0.1/` | 美国地图及1844、1860年版图变体 |
| `static/css/` | 原版样式；中文适配单独放在 `localization/layout.css` |
| `static/vendor/` | 离线库、主题、配乐和结局媒体，含来源及授权 |
| `server.py`、`start.bat` | 标准库HTTP服务与Windows启动脚本 |

加载次序：框架语言模块 → 旁注模块 → 剧本展示模块 → 本地jQuery/UI/BlockUI → 原版脚本 → 初始JSON → 配置 → 内置questionset → 原版竞选与结算。

主要函数：年份／总统／搭档为 `gameStart`、`candSel`、`vpSelect`；模式／难度为 `s`；问题／答案／下一题为 `o`、`n`、`nextQuestion`；地图／访问／民调为 `openMap`、`rFunc`、`switchPV`、`evest`；管理为 `shining_menu`；结算包括 `electionNight`、`f`、`p`、`h`、`g`、`b`、`w`。计算函数 `A`、`F`、`divideElectoralVotesProp`、`dHondtAllocation` 等保持原样。

## 4. 语言包与机制保护

| 文件 | 用途 |
|---|---|
| `localization/en-US.json`、`zh-CN.json` | 645个界面键（含26个攻略键），变量与英文回退 |
| `localization/i18n.js` | 存储、插值、显式标记更新、本地资源解析 |
| `localization/stories.js` | 原生文本的展示适配器，不写回英文数据 |
| `localization/annotations.js`、`localization/annotations/` | 显式原文匹配的离线旁注、来源、编译索引与校订记录 |
| `localization/glossary_zh.json` | 273个人名部分、745个术语／完整名称 |
| `localization/glossary_people_zh.json` | 其他人物和组织的译名维护输入 |
| `localization/stories/组合.en-US.json`、`组合.zh-CN.json` | 按组合组织的可编辑语言包 |
| `组合.pack.json` | 游戏实际按需读取的离线包 |
| `base.*.json`、`staff.选举ID.候选人ID.*.json` | 共用背景／人物与高级竞选资料 |
| `catalogue.json`、`index.json` | 字段、原文、SHA-256、结构位置与索引 |
| `translation-memory.json` | 片段原文、译文和生成／修订来源 |
| `editorial-records.json`、`editorial-overrides.json` | 完整字段和段落片段的人工修订 |
| `coverage.json`、`untranslated.json` | 覆盖率及未翻译报告，当前缺失0条 |
| `quality-review.json`、`review-queue.json` | 历史校订状态及待复核文本 |

键示例：`1968_Nixon_Agnew/questions_json/321@0/description`。命名空间包含剧本、集合、PK、数组位置和字段，匹配还要求英文原文一致。上游重复PK与原始顺序保留，不删除、合并或重排游戏记录。

提取通过JavaScript AST定位 `JSON.parse` 字符串，再用JSON解析器解码；普通字面量数组用受限读取器。提取不执行剧本代码，不回写原文件。全部结局片段和特殊打字参数也以AST定位。

动态问题、选项、反馈、简介、议题、团队与结算在原版展示流程生成明确的 `data-story-*` 标记。切换语言仅更新这些标记，计算对象仍为英文，没有全局DOM文本替换或运行时在线翻译。

特殊打字参数与明确的媒体展示字面量加载时由原文校验适配器包装。测试解包适配器后对比105剧本全部脚本AST，执行逻辑相同。HTML标签、属性、实体、URL、占位符和打字控制字符均校验保留。缺少中文时回退原文。

## 5. 覆盖范围与历史质量

提供中文：全部原生固定界面、年份背景、总统与搭档资料、全部问题／回答／顾问反馈记录（包括隐藏与专属记录）、议题名称及七级立场、常规与特殊结局文字、管理团队和利益团体资料、辅助模式显示的上述文本。

图片内文字、歌曲原声、外部文章正文和社区模组不属于文本语言包。人名、数字、URL、作品名和专有缩写不会冒充未翻译段落；也没有把英文段落直接复制到中文包来计算完成率。

开发时初译曾用于起草；现有全部内置长文本已经完整字段读写校订，短术语与姓名州名另有复核记录。最终包缺失0条、未审0条。保留初译来源记录，不改标签伪造专家审定。

原文事实疑点不直接改写：正文保留年代、数字和人物说法，旁注解释实际史料与推断边界。文件名含RESEARCH_PENDING的年代报告为兼容旧元数据保留，开头已更新最终状态，其旧启动记录明确标为归档。

## 6. 离线资源与还原限制

脚本、CSS、地图、JSON、语言包与人物图均在本地，中文字体使用Windows系统字体回退。保留jQuery3.7.1、jQueryUI1.14.1、BlockUI2.70版本及许可证，缓存14首原版配乐与可取得的主题资源。本地运行不向旧ngrok服务提交结果，保留本局计算和结算。

第二阶段额外缓存6个结局媒体；另6个无法取得的媒体使用本地替代。见 `static/vendor/story-assets/manifest.json`。1968隐藏视频原链接失效，用3秒黑色视频接续原版 `onended → videoDone → runDialogue → nextTask`；**原影片内容与播放时长没有还原**。失效音轨用静音替代，图片用已有图片或黑色背景。

1964六个失效Imgur图、主题／音乐的其他差异及授权见 [THIRD_PARTY_ZH.md](THIRD_PARTY_ZH.md)。Mod Loader仅主动打开时加载社区库。外部文章、博客、Discord和用户自填远程主题仍需网络。

## 7. 实际测试

最终实际验收于2026-10-10执行，Windows／Chrome 155.0.8059.39，默认本地服务8000。全部105组合分别中英文通关，共210局，每局25题；相同种子和选择的全国／州票数、答案、访问与随机调用完全相同。外网请求在浏览器中拦截，错误、缺失与外部请求为空。

288条旁注及全部绑定真实渲染；鼠标、键盘、语言切换、390px视口及80／100／125／150% CSS缩放通过。全部105组合的20160个合成结局夹具、华莱士本地视频回调及中文打字剧情实际通过。111原数据字节、7计算AST、全部32770字段的HTML／变量完整性通过。

报告与真实时间：[最终验收](localization/reviews/FINAL_TEST_REPORT_ZH.md)、[双语通关](tests/stories-browser-results.json)、[结局](tests/story-endings-results.json)、[旁注](tests/annotations-results.json)、[静态完整性](tests/stories-integrity-results.json)。汉化验收当时的包哈希保存于[final-acceptance.json](localization/reviews/final-acceptance.json)；攻略作为独立插件发布，测试记录在 NCT-Guide 仓库。

边界：每组合一个固定随机序列与首个答案路径，未穷尽所有随机与答案排列；结局夹具不是全部自然触发。旧Edge及扩展界面报告为2026-10-08，没有伪称本次重跑。此前8000服务超时后，将本项目服务在实际浏览器所在环境重启，默认8000完成全量验收；未修改系统网络。

上游330条集合外引用、重复PK、1988布什538票空叙事保持。六个失效媒体替代及中文打字时长差异见第6节。独立史料未确认的细节公开记录，测试通过不等于所有原作主张已获学术认证。

## 8. 复现、重建与维护

开发可选，需要Node.js、Python和Playwright。测试默认使用已安装Chrome，以 `NCT_BROWSER` 指定其他路径；提取使用锁定Playwright附带的Babel解析器。游玩不需要这些工具。

```powershell
cd <PROJECT>
npm install
# 另一窗口保持 python server.py 运行；测试按顺序执行
npm run test:integrity
npm run test:stories:integrity
npm run test:stories
npm run test:endings
npm run test:extended
npm run test:annotations
```

`npm test` 执行完整测试；`npm run test:stories:smoke` 只测5组合，单独写报告，不覆盖全组合结果。

`npm run test:stories:review` 根据 `localization/reviews/*-editorial-review.json` 自动选取所有受修订影响的组合，写入 `tests/stories-review-results.json`。复用原文也会计入，不只测试默认竞选搭档。

离线重新提取与构建：

```powershell
node tools/extract-stories.cjs
python tools/translate-stories.py --offline
python tools/build-stories.py
python tools/review-stories.py
python tools/build-annotations.py
python tools/report-historical-reviews.py
python tools/audit-final-review.py
node tests/stories-integrity.cjs
```

人工修改优先写入 `editorial-records.json`：以完整英文原文为键，中文为值，保留HTML与占位符，然后重建。`editorial-overrides.json` 和 `translation-memory.json` 维护片段。不要只编辑生成的pack，下一次构建会覆盖它。

历史校订批次的固定英文快照为 `localization/reviews/批次-source-snapshot.json`，逐行中文为 `批次-revised.txt`。执行 `python tools/apply-historical-review.py 批次`，会核对原文键、SHA、HTML和占位符，然后写入独立完整字段语言包并记录来源。批次涵盖1844至2020全部年份及final-supplement，清单与数量见historical-review-report.json。短术语和专名复核分别见final-terms-review.json、final-names-review.json。可选 `批次-metadata.json` 记录日期及原作疑点；默认日期按香港时区生成。离线重建后运行 `python tools/report-historical-reviews.py` 更新覆盖报告；各时代术语定义和禁用误译见 `localization/reviews/glossary-context.zh-CN.json`，通过noteId关联带来源的解释。持续全项目校订的接续说明见 `localization/reviews/PROGRESS_ZH.md`。

旁注维护输入为 `localization/annotations/notes.zh-CN.json` 与 `header-notes.zh-CN.json`。按稳定ID编写中文解释与HTTPS来源；`contains`只在构建时筛选提取目录，运行时按稳定键及完整原文精确匹配。页眉原文中的空白／标点变体单独记录并校验，原文变化不会套用旧旁注。修改后运行 `python tools/build-annotations.py` 和 `npm run test:annotations`。英文模式不显示中文旁注。

本轮修订编写工具为 `review-annotations-texts.py`、`review-header-quotes.py`、`add-header-context.py`、`review-reading-lists.py`，记录最初批次；一般维护直接修改对应JSON，不必重新执行这些编写工具，以免覆盖后续人工调整。页眉中文输入在 `tools/quotes-zh.json`，修改后执行 `python tools/make-packs.py`，保持英文数组不变。

`translate-stories.py` 不带 `--offline` 时会使用开发时联网初译，代理使用系统 HTTPS_PROXY 设置；它不是游戏运行依赖，也不保证历史质量。新增原文未缓存时离线构建会报告缺失、退出失败，运行时回退英文。

术语输入在 `prepare-story-glossary.py` 与 `glossary_people_zh.json`。人工修订的编写源在 `editorial-stories.py`、`review-candidate-biographies.py`、`review-running-mates.py`。一般校订直接修改修订JSON，不必重新执行这些初始编写工具。资源缓存工具仅用于维护，游玩无需重新下载。

## 9. 交付

完整源码、双语包、术语表、校订记录与测试工具均在本仓库。攻略独立发布于 https://github.com/hy0713/NCT-Guide 。

## 10. 公开版差异

上面的全量验收记录对应原始本地交付。公开版独立移除攻略，并保留语言按钮的键盘隔离。未包含社区 MOD 和额外缓存的授权未确认音乐／图片；这些展示资源映射到已有黑色图片、生成静音等本地替代，详见 `localization/public-media-fallbacks.json`。原版剧本数据、计算函数、中文正文和旁注不变。公开版新增验证见 `PUBLICATION_TEST_REPORT_ZH.md`。
