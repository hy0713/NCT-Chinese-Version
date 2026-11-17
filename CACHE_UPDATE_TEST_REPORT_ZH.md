# 本地化资源更新验证

日期：2026-11-17。

`server.py`对`/localization/`目录下的JavaScript、JSON和CSS返回`Cache-Control: no-cache`。浏览器可保留缓存，但使用前向本机服务确认是否更新；断网游玩无需外部服务。带查询参数的资源地址适用同一策略。自动退出模式的游戏入口继续返回`no-store`。

`python tests/server_start.py`实际通过8项检查，新增检查启动真实本机HTTP服务，读取脚本、带查询参数的语言包、样式和游戏入口，并断言响应头。既有端口选择、参数与生命周期检查亦通过。

本轮另执行`node tests/integrity.cjs`和`node tests/stories-integrity.cjs`：7处原算法、111份原数据、645个双语界面键、105组合、32770个剧本文本条目及HTML结构检查通过。没有更改游戏计算或原始剧本。

攻略插件独立仓库另提供内容版本号，刷新后加载对应新版入口与后台规划器；详见[NCT-Guide的缓存回归报告](https://github.com/hy0713/NCT-Guide/blob/main/guide/CACHE_REFRESH_TEST_REPORT_ZH.md)。本仓库不内置该插件。
