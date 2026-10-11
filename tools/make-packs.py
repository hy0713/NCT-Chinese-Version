from pathlib import Path
import json,re,hashlib,html
root=Path(__file__).resolve().parents[1]
loc=root/'localization'; loc.mkdir(exist_ok=True)
en={}; zh={}; source={}
for line in '\n'.join((root/'tools'/name).read_text(encoding='utf8') for name in ['translations.tsv','extra-translations.tsv','staff-effects.tsv']).splitlines():
 if not line.strip(): continue
 a,b=line.split('\t',1); a=re.sub(r'\s+',' ',a).strip()
 key='ui.'+re.sub(r'[^a-z0-9]+','_',a.lower()).strip('_')
 if key in en and en[key]!=a: key+='_alternate'
 en[key]=html.unescape(a); zh[key]=html.unescape(b); source[a]=key
extra={
 'game.progress':('Question {current} of {total}','第 {current} 题，共 {total} 题'),
 'game.visit':('You have chosen to visit {state} -- is this correct?','你选择访问{state}，确认访问吗？'),
 'game.election_night':('Election night has arrived. Settle in and wait for the returns, however long it may take. Best of luck!','选举之夜到了。请耐心等待各州计票结果。祝你好运！'),
 'game.win':("Congratulations! You won this year's election! Click OK to view the rest of the returns, or skip straight to the final results. We hope you have a nice victory speech prepared for your supporters.",'恭喜，你赢得了本次选举！点击“确定”继续查看计票，或直接查看最终结果。准备好向支持者发表胜选演说吧！'),
 'game.loss':('Sorry. You have lost the election this time. Click OK to view the rest of the returns, or skip straight to the final results. We hope you have a nice concession speech prepared.','遗憾，这次你未能赢得选举。点击“确定”继续查看计票，或直接查看最终结果。准备向支持者发表败选演说吧。'),
 'game.result_win':('You won the election.','你赢得了选举。'), 'game.result_loss':('You lost the election.','你未能赢得选举。'), 'game.result_tie':('No candidate won an electoral majority.','没有候选人取得选举人票的过半多数。'),
 'menu.language':('Language','语言'), 'menu.mod_notice':('Community mods are outside this localization project. Click Mod Loader to open the original library.','社区模组不属于本次汉化范围。点击“模组加载器”可打开原版模组库。'),
 'error.load':('Unable to load local game data. Please run start.bat and reload.','无法加载本地游戏数据。请运行 start.bat 后刷新页面。'),
 'ui.link_directly_to_the_image':('Link directly to the image.','请输入图片的直接地址。'), 'ui.numbering_starts_from_0':('Numbering starts from 0!','题目编号从0开始。'),
 'ui.disable_christmas':('Disable Christmas','关闭圣诞主题'),'ui.enable_christmas':('Enable Christmas','启用圣诞主题'),
 'ui.last_updated':('Last updated: {date}','最近更新：{date}'),
 'ui.close':('Close','关闭'),
 'ui.scenario_credit':('This scenario was made by {author}.','本剧本作者：{author}。'),
 'error.skip_high':('You are trying to go over the question limit. This will likely break unless the mod maker specifically made questions for this (possibly for CYOA). Are you sure?','跳转题号超出了剧本范围，可能导致游戏无法继续。确定跳转吗？'),
 'error.skip_low':('You are trying to go below question 1. This will almost certainly break. Are you sure?','跳转题号小于第一题，极可能导致游戏无法继续。确定跳转吗？'),
 'error.rng':('NormSInv: Argument out of range.','随机数函数参数超出范围。'),
}
extra.update(json.loads((root/'tools/ui-extra.json').read_text(encoding='utf8')))
for k,(a,b) in extra.items(): en[k]=a;zh[k]=b;source[re.sub(r'\s+',' ',a).strip()]=k
quotes=re.search(r'nct_stuff\.quotes = \[(.*?)\]\s*\n', (root/'static/js/indexCode.js').read_text(encoding='utf8'), re.S).group(1)
quotes=re.findall(r'`([^`]*)`|\'([^\']*)\'',quotes)
translations=json.loads((root/'tools/quotes-zh.json').read_text(encoding='utf8'))
assert len(quotes)==len(translations)==48
for i,((a,b),translation) in enumerate(zip(quotes,translations)):
 original=a or b; key='quote.'+re.sub(r'[^a-z0-9]+','_',original.lower()).strip('_')
 en[key]=original;zh[key]=translation;source[re.sub(r'\s+',' ',original).strip()]=key
ach=json.loads((root/'tools/native-achievements.json').read_text(encoding='utf8'))
original=json.loads((root/'tests/data-text-inventory.json').read_text(encoding='utf8'))
for item in original['achievements']:
 if item[0] in ach:
  for i,field in enumerate(['name','description']):
   key=f'achievement.{item[0]}.{field}';en[key]=item[i+1];zh[key]=ach[item[0]][i];source[item[i+1]]=key
states='Alabama|阿拉巴马州;Alaska|阿拉斯加州;Arizona|亚利桑那州;Arkansas|阿肯色州;California|加利福尼亚州;Colorado|科罗拉多州;Connecticut|康涅狄格州;Delaware|特拉华州;District of Columbia|哥伦比亚特区;Florida|佛罗里达州;Georgia|佐治亚州;Hawaii|夏威夷州;Idaho|爱达荷州;Illinois|伊利诺伊州;Indiana|印第安纳州;Iowa|艾奥瓦州;Kansas|堪萨斯州;Kentucky|肯塔基州;Louisiana|路易斯安那州;Maine|缅因州;Maryland|马里兰州;Massachusetts|马萨诸塞州;Michigan|密歇根州;Minnesota|明尼苏达州;Mississippi|密西西比州;Missouri|密苏里州;Montana|蒙大拿州;Nebraska|内布拉斯加州;Nevada|内华达州;New Hampshire|新罕布什尔州;New Jersey|新泽西州;New Mexico|新墨西哥州;New York|纽约州;North Carolina|北卡罗来纳州;North Dakota|北达科他州;Ohio|俄亥俄州;Oklahoma|俄克拉何马州;Oregon|俄勒冈州;Pennsylvania|宾夕法尼亚州;Rhode Island|罗得岛州;South Carolina|南卡罗来纳州;South Dakota|南达科他州;Tennessee|田纳西州;Texas|得克萨斯州;Utah|犹他州;Vermont|佛蒙特州;Virginia|弗吉尼亚州;Washington|华盛顿州;West Virginia|西弗吉尼亚州;Wisconsin|威斯康星州;Wyoming|怀俄明州'
terms={}
for pair in states.split(';'):
 a,b=pair.split('|'); k='state.'+a.lower().replace(' ','_');en[k]=a;zh[k]=b;terms[a]=k
more='Democrat|民主党;Republican|共和党;Independent|独立候选人;Libertarian|自由意志党;Green|绿党;Whig|辉格党;Democratic|民主党;Democratic-Republican|民主共和党;Constitution|宪法党;Reform|改革党;Socialist|社会党;Populist|人民党;Dixiecrat|南方民主党;Prohibition|禁酒党;Northern Democrat|北方民主党;Southern Democrat|南方民主党;Constitutional Union|宪法联盟党;Cakewalk|轻而易举;Very Easy|非常简单;Easy|简单;Normal|普通;Hard|困难;Impossible|极难;Unthinkable|不可思议;Blowout|惨败;Disaster|灾难;Other|其他;Others|其他候选人;Unknown|未知;Unpledged electors|未承诺选举人;Unpledged elector|未承诺选举人;Name|姓名;NCT|新竞选之路;New Campaign Trail|新竞选之路;Custom|自定义;Old NCT|旧版新竞选之路'
for pair in more.split(';'):
 a,b=pair.split('|');k='term.'+re.sub(r'[^a-z0-9]+','_',a.lower()).strip('_');en[k]=a;zh[k]=b;terms[a]=k
if (loc/'guide/messages.json').exists():
 guide_messages=json.loads((loc/'guide/messages.json').read_text(encoding='utf8'))
 en.update(guide_messages['en-US']);zh.update(guide_messages['zh-CN'])
for name,obj in [('en-US.json',en),('zh-CN.json',zh),('source-keys.json',source),('term-keys.json',terms)]:
 (loc/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
protected={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['static/json','static/questionset'] for p in (root/folder).glob('*') if p.is_file()}
if not (root/'tests/original-data-sha256.json').exists(): (root/'tests/original-data-sha256.json').write_text(json.dumps(protected,indent=2),encoding='utf8')
print(len(en),'language keys')
