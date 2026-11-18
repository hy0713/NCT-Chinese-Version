# 典故正文改写验证

2026-11-18。

288 条典故统一改写为标题和两段正文。正文从人物、事件和制度讲起，然后解释它在对应的竞选题、顾问反馈、结局或页眉语录中所起的作用。打开卡片即可读到两段正文，资料来源在末尾按需展开。

新正文包括近 4.48 万字符，旧版默认可见的导语约 2.94 万字符。诸如「禁议规则」先讲众议院怎样搁置反奴隶制请愿，再讲废除规则的政治意义。「含着银脚出生」分开解释富家出身和失言两个习语，再说明安·理查兹为何把它们拼起来。「佛州 537 票」按顺序讲认证票数、重计和诉讼。

保留每条资料出处及原有考据文件。重写期间抽查了国会档案里的禁议规则、杜鲁门的竞选演说、肯尼迪联系科雷塔的资料及民权立法历程。[美国国家档案馆的众议院记录](https://www.archives.gov/legislative/guide/house/chapter-14.html) · [杜鲁门总统图书馆的竞选演说](https://www.trumanlibrary.gov/library/public-papers/183/rear-platform-and-other-informal-remarks-michigan-and-ohio) · [肯尼迪总统图书馆的竞选资料](https://www.jfklibrary.org/sites/default/files/2018-06/Presidents_Desk_Resource_Guide_Low_Res.pdf) · [美国众议院的民权立法资料](https://history.house.gov/Exhibitions-and-Publications/BAIC/Historical-Essays/Keeping-the-Faith/Civil-Rights-Movement/)。

实际验证结果如下。

- 对照发布前后的构建文件，288 个 ID、来源与顺序、5,916 处剧本绑定、47 个页眉语录键及结局关联完全一致。
- 通过 Chrome 在阻断外网的环境中打开 263 组剧本典故和 47 种页眉典故，覆盖全部 288 条新文案。两个段落默认显示，来源链接可展开。
- 390 像素窄屏、390×380 多条长文滚动和 80%、100%、125%、150% 缩放均通过。测过鼠标、Enter、Escape、关闭按钮以及中英文切换。
- 查看典故、展开资料和使用键盘后，选中答案、竞选状态与随机调用计数一致，随后也能正常作答并进入下一题。
- 原游戏 7 处算法、111 份原数据和 105 种组合的 32,770 个剧本翻译字段通过完整性检查。

[Chrome 浏览器测试记录](../../tests/annotations-rewrite-results.json) · [典故全文](NOTES_ZH.md)。

可运行 `python tools/build-annotations.py` 重新构建。在本地服务器运行时，通过 `NCT_ANNOTATION_UNIQUE=1` 的浏览器测试覆盖不同的典故组合。省略该环境变量可以逐一打开所有重复绑定，耗时更长。
