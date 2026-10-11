# 1968年完整字段校订与史料边界

本批固定全集492条；a至f各75条，g42条。全部英文已逐条实际读出，中文逐行编写；不复制机器初译、不改原始英文数据。原作共享的完整英文通过键与SHA对应复用，候选人及搭档独有文本没有跳过。构建后的覆盖与实际测试见历史报告和tests目录，本文不预先宣称尚未执行的测试通过。

## 史料与旁注

23条新增离线说明的来源和绑定由`tools/add-1968-context.py`保存。解释按钮与正文分离，保持所有原始数值、选项关系和标签。重点核对：

- [约翰逊图书馆的陈香梅事件资料](https://www.lbjlibrary.org/media-kit/chennault-affair?type=document)：停止轰炸、秘密联络、未公开情报与否认。谈判失败的游戏分支不是真实定罪；[Diplomatic History对南越动机的研究](https://academic.oup.com/dh/article/48/5/633/7758644)提醒不能把南越一切决定归因于美国竞选联络。
- [总统辩论委员会](https://www.debates.org/about-cpd/overview/)：1964、1968、1972年没有主要候选人大选辩论。游戏1968辩论是架空选择；结局与1964的比较原样保留，未伪造尼克松1964参选史。
- [国务院六日战争资料](https://history.state.gov/milestones/1961-1968/arab-israeli-war-1967)：战前危机、占领土地和以土地换和平；人物关于先开战与自卫的论断不是同一个命题。
- [哥伦比亚大学档案展](https://exhibitions.library.columbia.edu/exhibits/show/1968/causes/gym)：校园占领包括国防研究关系、体育馆与哈莱姆社区的问题。候选人贬损学生的语言保留。
- [国会调查背景资料](https://www.archives.gov/research/jfk/select-committee-report/part-2-king-findings.html)及[克纳报告原件](https://www.hud.gov/sites/dfiles/FHEO/documents/kerner_commission_full_report.pdf)：1967年骚乱与1968年金遇刺后的动荡分开，不能将所有骚乱归给黑豹党或所有黑人。
- [吉迪恩案](https://www.uscourts.gov/about-federal-courts/educational-resources/educational-activities/sixth-amendment-activities/gideon-v-wainwright/facts-and-case-summary-gideon-v-wainwright)、[米兰达案](https://www.uscourts.gov/about-federal-courts/educational-resources/educational-activities/fifth-amendment-activities/miranda-v-arizona/facts-and-case-summary-miranda-v-arizona)、[洛文案](https://prologue.blogs.archives.gov/2021/02/11/the-fight-for-the-right-to-marry-the-loving-v-virginia-case/)区分律师、讯问与婚姻保障。Wainright是原拼写错误，中文用通行案名。
- [参议院任职表](https://www.senate.gov/senators/senators-who-served-as-vice-president.htm)：尼克松1957年为副总统、兼任参议院议长，不是当时参议员。原1957表功保留，配合[约翰逊传记](https://www.senate.gov/senators/FeaturedBios/Featured_Bio_JohnsonLyndonBaines.htm)说明职务不同。
- [1965年移民改革](https://prologue.blogs.archives.gov/2015/09/17/fifty-year-later-a-brief-history-of-the-immigration-act-of-1965/)与[第11246号行政命令原版](https://www.eeoc.gov/history/executive-order-no-11246)：取消旧来源配额不是取消所有入境限制；平权行动不是原文规定雇用不合格者。歧视性台词与制度事实分开。
- [启蒙计划项目历史](https://www.headstart.gov/about-us/article/head-start-history)与[环保署历史](https://www.epa.gov/history/origins-epa)：1965年儿童发展项目、1970年环保署成立，避免把1968年的提议写成已成立机构。
- [1968年黄金会议记录](https://history.state.gov/historicaldocuments/frus1964-68v08/d191)实际读到公报及两层市场说明；1968黄金危机与1971停止美元兑换分开，不套用1896年的普通金币兑换语境。
- [春节攻势](https://history.state.gov/milestones/1961-1968/tet)：军事结果与美国国内政治后果分开。[多米尼加原始评估](https://history.state.gov/historicaldocuments/frus1964-68v32/d60)与[同期国会批评](https://www.govinfo.gov/content/pkg/GPO-CRECB-1965-pt8/pdf/GPO-CRECB-1965-pt8-1-2.pdf)说明反共论证的争议，而非将恢复博什政府阵营全部定为共产党。[肯尼迪回合会议材料](https://history.state.gov/historicaldocuments/frus1964-68v08/d362)核对贸易授权与行政、国会的权限区别。
- [儿童营养法原件80 Stat. 885](https://www.govinfo.gov/content/pkg/STATUTE-80/pdf/STATUTE-80-Pg885.pdf)实际读取第3、4节及免费／减价条件；早餐是试点、牛奶为独立项目，原题的免费概括保留。不要拿1998年新试点证明1966年的制度。
- [格里斯沃尔德1965判决原文](https://www.law.cornell.edu/supremecourt/text/381/479)：已婚夫妇避孕隐私不是当时已经有1973年的堕胎判例。[宪法第三条](https://www.archives.gov/founding-docs/constitution-transcript)实际读取叛国定义与证据要求；政治指控不等于刑事定罪。
- [沃克报告摘要原文转载](https://chicago68.com/ricsumm.html)实际读出警察暴力、示威者挑衅及警方暴乱结论；报告1968年12月公布，不能倒写成大选前已公布报告。转载有个别拼写错误，未逐字引用，不据此改原游戏。

## 政治梗与修辞

Dump the Hump利用Humphrey的缩写押韵，译为甩掉汉弗莱；[佐治亚数字图书馆标语牌记录](https://dlg.usg.edu/record/gsu_labor_873)检索摘要证实文字，完整页抓取失败，未声称已读取其完整档案或确认所有使用者身份。

Jumbo借约翰逊给自己阴茎起的绰号代指他，译为巨无霸并旁注解释。[MEL传记轶事汇集](https://melmagazine.com/en-us/story/lyndon-b-johnson-penis)实际读出，但此次未逐项检查其引述的原始口述证据；不将尺寸、曝光场景或越战动机当作认证史实。

尖脑袋知识分子是反精英嘲讽，[1970年国会记录收录的华莱士采访](https://www.govinfo.gov/content/pkg/GPO-CRECB-1970-pt2/pdf/GPO-CRECB-1970-pt2-7-1.pdf)有相关提问。一角钱的差别、房间里的大猩猩、拍马屁式示好、抱树嬉皮士、被人利用的有用的傻瓜均按语境处理；未把最后一词无证归于列宁，也不凭网络梗判断真实人物逐字说过这些台词。

## 原文异常与证据限制

尼克松1964比较、1957职务、Wainright拼写、crusader语法与虚构庭审均记入metadata／旁注。crusader按上下文译为针对民权法案的讨伐，不声称已确定作者漏字。种族主义、排外、恐同及反民权台词仍明确保留观点，例如mongrelize译为“杂种化”，没有把立场改成温和政策。

隐藏动画第9条的星号、所有连串插入号及小于号命令完全保持，新增校验逐项比较命令序列；JSON和HTML校验外不能漏掉这些动画控制符。

仍未独立逐项核实约翰逊威胁割喉是否为真实逐字引语、1968年的所有即时民调判断、各选项给出的具体经济因果及政党支持预测。这些按原作人物台词或游戏效果保留，不伪称历史档案已经证明。HeadStart、部分大学和史密森检索未成功完整抓取，已用明确可读的官方检索摘要／其他资料区分证明范围；未把搜索失败当成证据。全部项目还未完成其他年份，不发最终完成通知。
