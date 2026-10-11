"""Cross-era political meanings, bound only to complete reviewed originals."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
rows=read(ROOT/'localization/reviews/political-terms-source-snapshot.json')
data=read(ROOT/'localization/annotations/notes.zh-CN.json')
notes=[]
def add(id,title,indices,body,sources):
    notes.append({'id':id,'title':title,'category':'政治术语／时代语境',
        'contains':[rows[i]['source'] for i in indices],'body':body,
        'sources':[{'title':t,'url':u} for t,u in sources]})
add('1860.know-nothing','一无所知党：这是党名，不是在骂人无知',[8,9,11],
    ['Know-Nothings指一无所知党人，与当时排外、反天主教的美国党运动有关。成员对组织活动的询问，常以“我对此一无所知”作答，因此得名。不能把他们译成一般的“一无所知的人”。',
     '游戏中声称这些人转投某党，是人物为了争取选民或攻击对手而说的话。译文保留这种政治修辞，不将其扩写为所有成员都以相同方式转党的史学结论。'],
    [('美国国会图书馆：美国党1854年入党审查问题原件','https://www.loc.gov/item/mcc.062/'),
     ('美国国会图书馆：一无所知名称与排外活动','https://www.loc.gov/classroom-materials/immigration/irish/religious-conflict-and-discrimination/')])
add('1860.popular-sovereignty','人民主权：由领地居民决定奴隶制',[6,7,10],
    ['在这段美国内战前的争论中，popular sovereignty主要指由领地居民决定是否允许奴隶制，而不是泛泛宣称一切权力属于人民。道格拉斯推动的1854年《堪萨斯—内布拉斯加法》，将这一原则用于新领地，并废除了密苏里妥协的地域限制。',
     'Southern bolters指脱离原有党派阵营的南方人，绝不是“南方爆弹手”。这个选项让玩家改弦更张、反对新州与领地的奴隶制，是游戏允许的立场选择，不能当作道格拉斯真实历史竞选纲领。'],
    [('美国参议院：堪萨斯—内布拉斯加法','https://www.senate.gov/artandhistory/history/minute/Kansas_Nebraska_Act.htm')])
add('1964.dixiecrat','迪克西民主党人与瑟蒙德转党',[1,3],
    ['Dixie是美国南方的传统称呼。Dixiecrats在这里指1948年反对民主党民权路线、支持种族隔离的州权民主党人。瑟蒙德曾以该党总统候选人身份参选，并于1964年9月加入共和党。',
     '这个名称指特定历史派系，不能泛指所有南方民主党人。1968年的反馈是在描述游戏中这些选民如何反应，不是断言他们在现实中必然采取同一种投票行为。'],
    [('美国参议院：斯特罗姆·瑟蒙德生平','https://www.senate.gov/senators/FeaturedBios/Featured_Bio_Thurmond.htm')])
add('1968.dog-whistle','政治“狗哨”：带有隐含指向的措辞',[2],
    ['政治狗哨是表面上可以作普通解释、却向特定群体传递另一层含义的措辞。这里的反馈明确说，黑人群体把人物的用词理解为种族主义暗示；它不是指真的吹狗哨。',
     '这是游戏叙述者对选项效果的描述。校注解释术语，不把所有相似词汇一概判为种族主义，也不声称这是1968年人物当时使用的固定术语。'],
    [('韦氏词典：dog whistle的政治含义','https://www.merriam-webster.com/dictionary/dog%20whistle')])
ids={n['id'] for n in notes}
add('1964.solid-south','“稳固南方”与南方战略',[0,4,5],
    ['Solid South在这里指传统上稳定支持民主党的南方票仓，也常称“南方基地”。“稳固”说的是党派选票格局，不是南方社会不存在冲突。南方战略则是共和党争取这批原民主党选民的竞选策略，两者不能混为同一个概念。',
     '1964年民权争论及白人反弹，是这种重组的重要背景。游戏所说“南方战略已充分奏效”是具体游戏结局的判断，不表示现实中的转变在一年内全部完成。'],
    [('PBS《美国历史》：稳固南方及其民主党票仓背景','https://www.pbs.org/wgbh/americanexperience/features/freedom-riders-solid-south/'),
     ('美国国家档案馆：1964年竞选中的种族政治','https://www.archives.gov/publications/prologue/2001/spring/lbj-and-white-backlash-1')])
ids={n['id'] for n in notes}
data['notes']=[n for n in data['notes'] if n['id'] not in ids]+notes
(ROOT/'localization/annotations/notes.zh-CN.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
context=read(ROOT/'localization/reviews/glossary-context.zh-CN.json')
context['era']='1844 / 1860 / 1964 / 1968'
added=[{'en':'Know-Nothings','zh':'一无所知党人','avoid':'一无所知的人','noteId':'1860.know-nothing'},
    {'en':'popular sovereignty','zh':'人民主权原则','avoid':'忽略领地奴隶制争论的泛泛表述','noteId':'1860.popular-sovereignty'},
    {'en':'Southern bolters','zh':'脱离党派的南方人','avoid':'南方爆弹手','noteId':'1860.popular-sovereignty'},
    {'en':'Dixiecrats','zh':'迪克西民主党人','avoid':'泛指所有南方民主党人','noteId':'1964.dixiecrat'},
    {'en':'dog whistle','zh':'政治狗哨（隐含暗示）','avoid':'不解释政治隐喻的字面吹哨','noteId':'1968.dog-whistle'},
    {'en':'Solid South','zh':'稳固南方（民主党南方票仓／南方基地）','avoid':'与共和党南方战略混同','noteId':'1964.solid-south'}]
context['terms']=[t for t in context['terms'] if t['en'] not in {a['en'] for a in added}]+added
(ROOT/'localization/reviews/glossary-context.zh-CN.json').write_text(json.dumps(context,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added',len(notes),'cross-era notes.')
