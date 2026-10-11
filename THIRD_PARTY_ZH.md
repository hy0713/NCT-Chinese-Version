# 第三方资源、来源与离线差异

本地化没有给上游游戏、图片或音乐添加新的授权，也不改变原作者的权利。请保留仓库原有作者信息、源代码中的注释和各资源许可证。本项目面向个人本地游玩与学习。

## 新缓存的库

| 库 | 来源 | 本地授权文件 |
|---|---|---|
| jQuery 3.7.1 | https://code.jquery.com/jquery-3.7.1.min.js | `static/vendor/LICENSE.jquery.txt`，MIT |
| jQuery UI 1.14.1、CSS、图标 | https://code.jquery.com/ui/1.14.1/ | `static/vendor/LICENSE.jquery-ui.txt`，MIT |
| jQuery BlockUI 2.70 | https://malsup.github.io/jquery.blockUI.js | `static/vendor/LICENSE.blockUI.txt`；原文件注明 MIT／GPL 双重授权，本地保留原头部并附 MIT 全文 |

上述脚本保持原始下载内容；文件来源及 SHA-256 见 `static/vendor/manifest.json`。已有 Raphael、地图、MD5 和渐变库继续使用仓库原文件，未改写、未升级；保留其原有注释和作者来源。本地化不对这些原文件补充无法确认的授权声明。

## 原生 1964 年图片

原始远程地址继续保留在原版 JSON 中；仅在展示时解析成以下本地路径：

| 原始地址文件名（i.imgur.com） | 本地使用 |
|---|---|
| `cBPk43V.png` | 仓库的 `static/images/lyndon-johnson-1964.png` |
| `Biigves.png` | 仓库的 `static/images/barry-goldwater-1964.png` |
| `fpPVcOI.png` | 仓库的 `static/images/hubert-humphrey-1968.jpg` |
| `r3llYzE.png` | `static/vendor/theme-assets/135828388a1945.png`，William E. Miller 的美国众议院肖像 |
| `zHVrIgV.png` | 仓库的 `static/images/1964-election-photo.png` |
| `RsnpYGz.png` | 仓库的 `static/images/carville-rove.jpg`，通用顾问替代图片 |

米勒肖像作者为美国众议院，文件页面标记为美国联邦政府职务作品、公有领域。来源与授权记录：[Representative William E. Miller.png](https://commons.wikimedia.org/wiki/File:Representative_William_E._Miller.png)。照片不是对失效 Imgur 文件的逐像素还原。

## 可选主题图片与配乐

- 已取得的卡特主题背景／横幅、Omori 背景及米勒肖像，见 `static/vendor/theme-assets/manifest.json`。
- 失效的 Discord 横幅使用已有 `banner_1.png`；无法取得的澳大利亚、彩虹、两洋主题背景使用已有 `black.jpg`。原版主题名称、配色、窗口图片和可取得的横幅继续保留。
- 原版 `newcampaigntrail/resources` 中的 14 首配乐已缓存，来源、路径、哈希见 `static/vendor/soundtracks/manifest.json`。原版演奏者／曲目名称保持不变；资源存放在上游仓库并不代表可以任意再发行。
- Discord 的 `e1.mp3` 地址已失效，本地使用生成的一秒静音 WAV，记录在 `localization/assets.json`。生成的静音文件不含原曲内容。
- 原仓库随附的其他图片、音乐与字体选择保持原有权利状态。

## 第二阶段特殊结局媒体

- 额外缓存6份原生结局资源：Boston Globe照片、CloudFront背景图、3份Imgur图片／动图、Archive.org戈尔庆祝音轨。
- 来源、SHA-256和下载结果见 `static/vendor/story-assets/manifest.json`。这些素材沿用原作者权利，公开可下载不代表可自由再发行。
- 5个失效Discord图片／动图／音频使用已有尼克松照片、黑色背景或生成静音替代。
- OneDrive原版隐藏视频无法取得。`unavailable.mp4` 是本地生成的3秒黑色视频，不含原影片内容。保留原版播放结束回调与后续文字，未还原影片和时长。
- `tools/generate-story-video.py` 使用开发机FFmpeg，FFmpeg没有加入运行时交付；游玩不需要安装它。

用户填写的远程主题、社区模组和外部链接未承诺离线还原。正常竞选、访问、民调、结算和已测特殊剧情无需联网。

## 公开仓库的额外媒体排除

上述缓存清单描述本地交付历史。公开仓库没有附带权限未确认的额外配乐、主题背景或特殊结局媒体；清单中这些项标记 omitted-from-public-distribution，运行时使用 public-media-fallbacks.json 记录的本地替代。米勒公有领域肖像与自行生成的静音／黑色视频保留。
