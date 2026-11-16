# 零基础典故说明改写与验证

日期：2026-11-16。

## 阅读方式

全部288条典故都有重新撰写的入门主说明。默认先读一小段，说明人物是谁、发生了什么、当时在争什么，以及为什么会影响选票或形成笑点。需要进一步了解时，再展开原有的“补充背景”和“资料来源”。

主说明输入为 `beginner-notes.zh-CN.json`，按既有典故ID独立维护；原有详细背景仍保存在 `notes.zh-CN.json` 和 `header-notes.zh-CN.json`。构建时组合两层，不覆盖英文、剧本文本或游戏数据。

例如，自由铸银先讲货币供应与农民债务；“银脚出生”先拆开富家子和说错话两层双关；“满文件夹的女性”先还原女性人才招聘语境，再解释为什么措辞会被嘲笑。

## 具体检查

- 288个原典故ID全部对应一条新主说明，无空值、漏项或额外ID。
- 逐条比较构建前后：原标题、类别、详细背景、来源地址及其顺序全部保留。
- 5916个剧本原文绑定、全部页眉绑定、原文校验值及结局关联不变。
- 浏览器实际打开263组不同典故组合及47个页眉键，覆盖全部288条入门主说明；每条弹窗的默认首段与语言包逐字一致。
- 14份推荐阅读、48个原始页眉位置，以及原文改变时不套用旧注释的检查通过。
- 点击、回车、空格、方向键、关闭、切换语言不改变当前游戏数据、已选答案或随机调用次数。
- 打开典故后，正常选择回答、阅读反馈并继续游戏的流程通过。
- 390像素视口及80%、100%、125%、150%缩放检查通过。
- 浏览器阻断所有非回环请求；本轮没有脚本错误、缺失资源或来源网站请求。
- 原始算法、原始数据、105种组合及32770个剧本字段的静态完整性检查通过。

本轮验证的是文字展示和既有数据完整性，没有重跑全部105种组合的完整通关。

## 史料与记录

此次是面向初学者的AI逐条文字改写，不把它记作全部史料重新完成了独立学术考证。原有史料与待查细节保持原样；新说明也保留了必要的不确定语气，尤其是出处尚未确认的名言和推测性的网络用典。

为避免把入门解释写错，另抽查了[国家档案馆的选举人团说明](https://www.archives.gov/electoral-college/faq)、[参议院瑟蒙德传记](https://www.senate.gov/senators/FeaturedBios/Featured_Bio_Thurmond.htm)、[CMS医保制度历史](https://www.cms.gov/about-cms/who-we-are/history)与[水门事件时间线](https://www.archives.gov/education/lessons/watergate-constitution/chronology.html)。史密森尼自由铸银条目此次读取了检索摘要，全文请求超时；没有将该次全文访问记为成功。

逐条改写及原文对照：[beginner-review-2026-11-16.json](beginner-review-2026-11-16.json)。浏览器实际记录：[annotations-beginner-results.json](../../tests/annotations-beginner-results.json)。

## 重建与复现

```powershell
python tools/build-annotations.py
python server.py --port 18081
```

另开终端，在游戏目录运行：

```powershell
$env:NCT_BASE_URL='http://127.0.0.1:18081'
$env:NCT_ANNOTATION_UNIQUE='1'
$env:NCT_ANNOTATION_REPORT='tests/annotations-beginner-results.json'
node tests/annotations.cjs
node tests/integrity.cjs
node tests/stories-integrity.cjs
```

浏览器测试需要开发依赖；正常游玩不需要Node.js或联网。
