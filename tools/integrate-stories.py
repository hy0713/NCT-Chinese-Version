"""Idempotent presentation-site patch with explicit match counts.

No scenario source, JSON data or calculation function is rewritten.
"""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'static/js/campaign_trail.js'
s=p.read_text(encoding='utf-8')
patches=[
 ('substitutePlaceholders(e.answers_json[i[a].key].fields.description)',"NCTStory.html('answers_json', e.answers_json[i[a].key].pk, 'description', e.answers_json[i[a].key].fields.description)",1),
 ('substitutePlaceholders(e.questions_json[e.question_number].fields.description)',"NCTStory.html('questions_json', e.questions_json[e.question_number].pk, 'description', e.questions_json[e.question_number].fields.description)",1),
 ('substitutePlaceholders(e.answer_feedback_json[s].fields.answer_feedback)',"NCTStory.html('answer_feedback_json', e.answer_feedback_json[s].pk, 'answer_feedback', e.answer_feedback_json[s].fields.answer_feedback)",1),
 ('+ e.candidate_json[t].fields.description +',"+ NCTStory.html('candidate_json', e.candidate_json[t].pk, 'description', e.candidate_json[t].fields.description, 'base') +",1),
 ('+ e.candidate_json[t].fields.description_as_running_mate +',"+ NCTStory.html('candidate_json', e.candidate_json[t].pk, 'description_as_running_mate', e.candidate_json[t].fields.description_as_running_mate, 'base') +",1),
 ('+ e.election_json[inX].fields.summary +',"+ NCTStory.html('election_json', e.election_json[inX].pk, 'summary', e.election_json[inX].fields.summary, 'base') +",1),
 ('+ e.election_json[t].fields.summary +',"+ NCTStory.html('election_json', e.election_json[t].pk, 'summary', e.election_json[t].fields.summary, 'base') +",1),
 ('+ e.election_json[t].fields.recommended_reading +',"+ NCTStory.html('election_json', e.election_json[t].pk, 'recommended_reading', e.election_json[t].fields.recommended_reading, 'base') +",2),
 ('${NCTI18n.describe(targ.description)}',"${NCTStory.staff('staff', targ, 'description')}",1),
 ('${targ.description}',"${NCTStory.staff('lobby', targ, 'description')}",1),
 ('<td><h4>${targ.name}</h4>',"<td><h4>${NCTStory.staff('staff', targ, 'name')}</h4>",1),
 ('issueDescription.textContent = issue.fields.description;',"NCTStory.bind(issueDescription, 'issues_json', issue.pk, 'description', issue.fields.description);",1),
 ('stanceDesc.textContent = stanceDescription;',"NCTStory.bind(stanceDesc, 'issues_json', issue.pk, `stance_desc_${i}`, stanceDescription);",1),
 ("+ s + '</div> '","+ NCTStory.ending(s) + '</div> '",2),
]
# Staff and lobby use the same source expression; disambiguate by the surrounding
# updater function rather than replacing both names with one collection.
old='<td><h4>${targ.name}</h4>'
if s.count(old)==2:
 a=s.index('const update_lobby_table') if 'const update_lobby_table' in s else s.index('for (let i in our_info.lobby)')
 pos=s.index(old,a);s=s[:pos]+s[pos:].replace(old,"<td><h4>${NCTStory.staff('lobby', targ, 'name')}</h4>",1)
for old,new,count in patches:
 if new in s and old not in s:continue
 actual=s.count(old)
 if actual!=count:raise RuntimeError(f'Expected {count} presentation sites, got {actual}: {old}')
 s=s.replace(old,new)
p.write_text(s,encoding='utf-8',newline='\n')
print('Integrated explicit native presentation sites')
