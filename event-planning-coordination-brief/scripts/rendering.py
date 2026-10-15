"""Draft-only serialization plus verification of the files actually written."""
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event, Todo, Timezone
from planning import aware, programme_checks
from sources import digest, integer

ARTIFACTS = ('vendor-comparison.csv', 'event-plan.md', 'event-calendar.ics', 'draft-communications.md')
CSV_FIELDS = ('option_id','quote_ids','planning_people','cost_twd','currency','feasibility','availability_status','evidence_ids','tradeoffs','unresolved','approval_status')
ZONE = ZoneInfo('Asia/Taipei')


def money(value):
    return 'unknown' if value is None else format(value, ',')


def context(model, options, selected, run_id):
    bases = [o for o in options if o['option_id'] in ('BASE-260','BASE-300')]
    amounts = '; '.join(o['option_id']+' total TWD '+money(o['cost_twd'])+', remaining headroom TWD '+money(o['headroom_twd']) for o in bases)
    return ('Run: '+run_id+'. Planning people: '+str(model['people'])+'. Recommended option: '+str(selected)+'. Stakeholder approvals: pending. '+amounts+'. Included communications TWD '+money(model['policy']['communications_allowance_twd'])+'; included contingency TWD '+money(model['policy']['contingency_allowance_twd'])+'.')


def write_plan(path, model, options, selected, run_id, mode):
    population = model['population']
    forecast = population.get('walk_ins',{})
    content = [
        '# Fellowship Demo Day — UNSENT PLANNING DRAFT','',context(model,options,selected,run_id),'',
        'Source mode: '+mode+'. Business clock: 2026-08-26 12:00 Asia/Taipei. Actual retrieval timestamps, versions and hashes remain in stage02.',
        '', '## Objective and attendance basis','',
        'Present every supplied team demonstration, give partners a useful programme overview and support accessible participation.',
        'Source basis: E-ATTENDEES supplies populations and overlapping needs; E-BUDGET supplies allocations, commitments and limits; E-VENDORS supplies packages; E-CALENDAR supplies dates and dependencies. E-BRIEF supplies the exercise requirements and fictional venue confirmations. E-ACCESS/E-FLOOR supply official spatial evidence only. The source registry in snapshots/evidence records URLs, retrieval results, versions and hashes. Learner choices come from the recorded conversation, separate from source facts and approvals.',
        '', '| Population | People | Confidence | Source record |', '|---|---:|---|---|',
        *['|'+name+'|'+str(row['people'])+'|'+row['confidence']+'|'+row['signal_id']+'|' for name,row in sorted(population.items())],
        '',
        'Registered people: '+str(model['registered'])+'. The 80% registered check-in success target is '+str(model['checkin_target'])+'; it does not reduce service capacity.',
        'Current forecast walk-ins: '+str(forecast.get('people'))+'; confidence: '+str(forecast.get('confidence'))+'. Forecast walk-ins are already included in the current population sum. Accessibility, companion and dietary needs overlap these people.',
        'The recorded learner baseline was 245, including 35 medium-confidence walk-ins, with no extra margin. Source changes are displayed as current observations and require recorded policy review; that historical reason does not establish the changed attendance.',
        '', '## Budget and supported alternatives','',
        'Overall ceiling TWD '+money(model['ceiling_twd'])+'; planned allocations TWD '+money(model['planned_twd'])+'; existing commitments TWD '+money(model['committed_twd'])+'.',
        'Communications and contingency above are already included in each full total. Remaining headroom is separate, not contingency counted twice. Current commitments consume headroom in addition to newly proposed packages. A category approval limit cannot override the overall ceiling.',
        '', '| Option | Full amount TWD | Remaining headroom TWD | Feasibility | Approval |','|---|---:|---:|---|---|'
    ]
    for row in options:
        content.append('|'+row['option_id']+'|'+money(row['cost_twd'])+'|'+money(row['headroom_twd'])+'|'+row['feasibility']+'|pending|')
    for row in options:
        content += ['', '### '+row['option_id'],'',row['tradeoffs'],
                    'Quotes: '+', '.join(row['quote_ids'])+'. Categories TWD: '+json.dumps(row['categories'],sort_keys=True)+'.',
                    'Allocation variances TWD: '+json.dumps(row['allocation_variances_twd'],sort_keys=True)+'. Approval-limit breaches TWD: '+json.dumps(row['approval_limit_breaches_twd'],sort_keys=True)+'.',
                    'Reasons: '+('; '.join(row['reasons']) or 'none')+'. Unresolved: '+('; '.join(row['unresolved']) or 'none beyond pending review approvals')+'.']
    content += ['', '## Budget allocation and approval limits (E-BUDGET)', '', '| Category | Allocation TWD | Existing commitments TWD | Approval limit TWD | Owner |', '|---|---:|---:|---:|---|']
    for row in model['budget']:
        content.append('|'+row['category']+'|'+money(integer(row['planned_amount_twd']))+'|'+money(integer(row['committed_amount_twd']))+'|'+money(integer(row['approval_limit_twd']))+'|'+row['owner']+'|')
    content += ['', '## Quote identity, capacity and conditions (E-VENDORS)','', '| ID | Category | Package TWD | Capacity | Service date | Valid until | Conditions |','|---|---|---:|---:|---|---|---|']
    for q in sorted(model['quotes'].values(),key=lambda r:r['quote_id']):
        content.append('|'+q['quote_id']+'|'+q['category']+'|'+money(integer(q['quote_amount_twd']))+'|'+str(integer(q['capacity']))+'|'+q['available_date'][:10]+'|'+q['valid_until'][:10]+'|'+q['status']+': '+q['notes']+'|')
    content += ['', 'Quote amounts are fixed packages, not per-person multipliers. Date-only quote/hold expiries remain date-only; no expiry hour is inferred from spreadsheet midnight formatting. Held/available is not booked or approved.', '', '## Recommendation for review','',
                'Recommended option: '+str(selected)+'.' if selected else 'Recommendation deferred: no option currently passes all hard-constraint checks.',
                'The learner preliminarily preferred Q-003 for baseline coverage and greater headroom. Q-004 remains an extra-capacity comparison. Final recommendation follows current capacity, timing, evidence, quote and budget checks.',
                'Current catering capacities/margins: '+json.dumps({k:{'capacity':q['capacity'],'margin':int(float(q['capacity']))-model['people'] if model['people'] is not None else None} for k,q in model['quotes'].items() if k in ('Q-003','Q-004')},sort_keys=True)+'. No package multiplication or extension is inferred.',
                'Livestream is excluded from the base by learner choice; its current cost, production-limit and ceiling reasons and unmet network-test/venue-confirmation conditions are retained above. No test is presumed complete.',
                'The October 24 fallback loses the keynote under the retained records; it is not an equivalent fallback. Programme/Operations own resolution and date-specific replacement evidence.',
                '', '## Complete proposed programme','',
                'The meal, two refreshment breaks, networking and setup/check allocations are planner choices within source-supported windows, not invented mandatory vendor durations. R2 supplies exercise aggregate readiness/clearance support only.',
                '', '| Block | Start Asia/Taipei | End Asia/Taipei | Dependencies |','|---|---|---|---|']
    for row in model['programme']:
        content.append('|'+row['event_id']+' '+row['summary']+'|'+row['start_at']+'|'+row['end_at']+'|'+', '.join(row['dependencies'])+'|')
    if not model['programme']:
        content.append('No supported event timing: programme/calendar deferred.')
    content += ['', 'Each explicit demo identity appears once with its presentation and separate changeover. Team slots add no attendance population.', '', '## All source calendar records','', '| ID | Meaning | Start | End | Owner and conditions |','|---|---|---|---|---|']
    for row in model['calendar']:
        content.append('|'+row['constraint_id']+'|'+row['constraint_type']+'|'+row['start_at']+'|'+row['end_at']+'|'+row['owner']+': '+row['notes']+'|')
    content += ['', 'Venue confirmation must precede the accessibility walkthrough; it has not occurred. Rehearsal retains its remote-backup option. CAL-005 is a deadline represented by VTODO DUE at its exact source instant, with no invented duration. Source windows/holds are constraint envelopes, not overlapping programme activities.', '', '## Accessibility evidence and limits','']
    if model.get('media_verified'):
        content.append('E-FLOOR page1: Plenary Hall at right, V.I.P. Room at left, Room401 between, wheelchair-area markers and accessible elevator/restroom symbols interpreted with the legend. Retained bytes match the previously visually inspected PDF hash; the source record preserves that observation provenance. These symbols are locations, not an exact usable-space count.')
    else:
        content.append('Required official image evidence is unavailable, invalid, changed or unreviewed. Current image-dependent spatial/accessibility claims are withheld. Operations must obtain/review the correct bytes; historical observations cannot masquerade as current image evidence.')
    if model['brief_text']:
        content += ['Fictional VEN allocation: '+str(model['venue_capacity'])+' usable places, '+str(model['wheelchair_places'])+' wheelchair spaces and '+str(model['quiet_capacity'])+' quiet-room occupancy. Current concurrent quiet-room demand: '+str(model['quiet_users'])+'. Companions use ordinary places already in the population.',
                    'Step-free/readiness and dietary coordination are fictional exercise facts, not official current certification. The diagram cannot prove current elevator operation, unobstructed routes, widths, acoustic separation or selected seating configuration. Real deployment requires current Operations/venue confirmation. Room401 is not selected.',
                    'Current aggregate service needs: '+json.dumps(model['needs'],sort_keys=True)+'. Both caterers have the exercise dietary/allergy response; named contacts remain privately with Operations. No personal medical/contact details are published.']
    else:
        content.append('Venue allocation, route/readiness and dietary-response facts are unverified because the current brief/venue source is unavailable; dependent claims are withheld, with Operations as resolution owner.')
    content += ['', '## Risks, owners and review requests','']
    for item in model['unknowns']:
        content.append('- '+item['id']+': '+item['summary']+'. Owner: '+str(item.get('owner'))+'.')
    for sid in model['source_failures']:
        content.append('- '+sid+': source unavailable/invalid; affected dependent claims remain conditional. Owner: Operations / source owner; see actual captured attempt.')
    content += ['- Operations reviews the versioned plan, date, room, headcount policy and unresolved issues. Budget owners review category amounts, allocation variances, limit breaches, quote validity and ceiling headroom. All actual approvals remain pending.',
                '- Attendance, dates, quotes, access needs and owner-direction changes revisit the earliest affected basis and all dependent options, decisions, review requests and drafts. History retains evidence/failed attempts. Recovery grants no approval.',
                '- No booking, payment, vendor commitment, invitation delivery, sent communication or production-calendar mutation has occurred.']
    path.write_text('\n'.join(content)+'\n')


def write_calendar(path,model,selected,run_id):
    calendar=Calendar();calendar.add('prodid','-//Quillhaven//Draft event planning//EN');calendar.add('version','2.0');calendar.add('method','PUBLISH')
    if model['programme']:
        calendar.add_component(Timezone.from_tzinfo(ZONE))
    stamp=datetime.now(timezone.utc)
    def add(identity,summary,start,end=None,kind='constraint',description='',source_id=None,block_id=None):
        item=Todo() if end is None else Event();item.add('uid','quillhaven-'+identity.lower()+'@event-coordination.example');item.add('dtstamp',stamp)
        if end is None:
            item.add('due',start.astimezone(ZONE));item.add('status','NEEDS-ACTION')
        else:
            item.add('dtstart',start.astimezone(ZONE));item.add('dtend',end.astimezone(ZONE));item.add('status','TENTATIVE')
        item.add('summary',summary);item.add('description','UNSENT DRAFT;run='+run_id+';planning_people='+str(model['people'])+';recommended='+str(selected)+';'+description);item.add('X-RECORD-KIND',kind)
        if source_id:item.add('X-SOURCE-RECORD',source_id)
        if block_id:item.add('X-PLANNING-BLOCK',block_id)
        calendar.add_component(item)
    if model['programme']:
        for row in model['calendar']:
            a,b=aware(row['start_at']),aware(row['end_at']);add(row['constraint_id'],row['constraint_id']+' '+row['constraint_type'],a,None if a==b else b,description=row['notes']+';source constraint,not a booking',source_id=row['constraint_id'])
        for row in model['programme']:
            add(row['event_id']+'-'+row['start_at'][:10],row['summary'],aware(row['start_at']),aware(row['end_at']),row['kind'],'Proposed allocation;dependencies='+','.join(row['dependencies']),block_id=row['event_id'])
    path.write_bytes(calendar.to_ical())


def write_messages(path,model,options,selected,run_id):
    common=context(model,options,selected,run_id)
    window=next((r for r in model['calendar'] if r['constraint_type']=='preferred_event_window'),None)
    timing=window['start_at']+' to '+window['end_at'] if window else 'unverified;timing deferred'
    drafts=[('Operations and category budget owners','Review plan,date,venue and spending','Review source validity,category allocation variances,approval limits and overall ceiling before commitment','Operations and relevant category budget owners','Please review the versioned plan and both catering alternatives. Included contingency and remaining headroom are separate in the current amounts below.'),
            ('Attendees','Prepare programme and accessibility information','Send only after actual Operations/date/venue approval and supported service arrangements','Operations / Learner Experience','Proposed timing: '+timing+'. Captioning,quiet-space and dietary responses remain subject to source conditions in the event plan. Individual access/dietary details must use the future private Operations route.'),
            ('Vendors via Operations','Verify package scope and conditions','Send only after actual Operations and category spending approval;recheck date,capacity,expiry and readiness','Operations and category budget owners','Draft request to verify packages for '+str(model['people'])+' planning people,source-supported setup/readiness and clearance windows,and caption/loop/quiet-room coordination. No booking or payment has occurred.'),
            ('Programme / Operations','Resolve rejected alternatives and prerequisites','New evidence and recorded decisions required before reconsideration','Programme / Operations','Fallback keynote conflict remains unresolved. Livestream stays excluded with current ceiling/production reasons and unmet network/venue conditions. Venue confirmation must precede walkthrough;no prerequisite is marked completed.')]
    text=['# Communication drafts','',common]
    for audience,purpose,conditions,owner,body in drafts:
        text+=['','## UNSENT DRAFT — '+purpose,'','Intended audience: '+audience+'.','Purpose: '+purpose+'.','Conditions: '+conditions+'.','Approval owner: '+owner+'.',common,'',body,'This is an unsent draft;no message,invitation,booking,payment or vendor commitment has been sent/made.']
    path.write_text('\n'.join(text)+'\n')


def render(root,run_id,model,options,selected,mode):
    output=Path(root)/'deliverables';output.mkdir(parents=True,exist_ok=True)
    with (output/ARTIFACTS[0]).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=CSV_FIELDS);writer.writeheader()
        for row in options:
            data={key:row.get(key) for key in CSV_FIELDS}
            for key in ('quote_ids','evidence_ids'):data[key]=json.dumps(data[key])
            data['tradeoffs']=row['tradeoffs']+'; '+ '; '.join(row['reasons'])
            data['unresolved']=json.dumps(row['unresolved']+(['Cost unknown: incomplete budget/quote source'] if row['cost_twd'] is None else []));writer.writerow(data)
    write_plan(output/ARTIFACTS[1],model,options,selected,run_id,mode)
    write_calendar(output/ARTIFACTS[2],model,selected,run_id)
    write_messages(output/ARTIFACTS[3],model,options,selected,run_id)
    return [{'id':'ART-'+str(i+1),'path':'deliverables/'+name,'sha256':digest((output/name).read_bytes()),'validation_status':'valid'} for i,name in enumerate(ARTIFACTS)]


def validate_outputs(root):
    root=Path(root);state=json.loads((root/'deliverables/snapshots/evidence/planning-state.json').read_text());model,options,selected,run_id=state['model'],state['options'],state['selected_option'],state['run_id'];errors=[]
    for name in ARTIFACTS:
        p=root/'deliverables'/name
        if not p.is_file() or not p.stat().st_size:errors.append('Missing/empty artifact:'+name)
    if errors:return {'valid':False,'errors':errors,'checks':[]}
    with (root/'deliverables/vendor-comparison.csv').open(newline='') as f:rows=list(csv.DictReader(f))
    expected={o['option_id']:o for o in options}
    if len(rows)!=len(expected) or {r['option_id'] for r in rows}!=set(expected):errors.append('CSV option identity mismatch')
    for row in rows:
        option=expected.get(row['option_id'])
        if not option:continue
        for key in ('cost_twd','planning_people'):
            if row[key]!=(str(option[key]) if option[key] is not None else ''):errors.append('CSV value mismatch:'+row['option_id']+':'+key)
        if json.loads(row['quote_ids'])!=option['quote_ids'] or row['feasibility']!=option['feasibility'] or row['approval_status']!='pending':errors.append('CSV quote/feasibility/approval mismatch')
    calendar=Calendar.from_ical((root/'deliverables/event-calendar.ics').read_bytes())
    if str(calendar.get('VERSION'))!='2.0' or str(calendar.get('METHOD'))!='PUBLISH':errors.append('Calendar envelope invalid')
    events=list(calendar.walk('VEVENT'));todos=list(calendar.walk('VTODO'));uids=set();actual_blocks={};source_records={}
    for item in events+todos:
        uid=str(item.get('UID'))
        if uid in uids or not item.get('DTSTAMP') or item.get('ATTENDEE'):errors.append('Calendar UID/stamp/attendee error')
        uids.add(uid)
        if run_id not in str(item.get('DESCRIPTION')) or 'planning_people='+str(model['people']) not in str(item.get('DESCRIPTION')):errors.append('Calendar run/headcount mismatch')
        if item.name=='VEVENT':
            a,b=item['DTSTART'].dt,item['DTEND'].dt
            if a.tzinfo is None or b.tzinfo is None or b<=a or str(item.get('STATUS'))!='TENTATIVE':errors.append('Calendar event timestamp/status failure')
        elif item['DUE'].dt.tzinfo is None or str(item.get('STATUS'))!='NEEDS-ACTION':errors.append('Calendar deadline failure')
        if item.get('X-PLANNING-BLOCK'):
            key=str(item['X-PLANNING-BLOCK'])
            if key in actual_blocks:errors.append('Duplicate programme identity')
            actual_blocks[key]=item
        if item.get('X-SOURCE-RECORD'):source_records[str(item['X-SOURCE-RECORD'])]=item
    if {r['event_id'] for r in model['programme']}!=set(actual_blocks):errors.append('Actual calendar programme identities mismatch')
    for row in model['programme']:
        item=actual_blocks.get(row['event_id'])
        if item and (item['DTSTART'].dt!=aware(row['start_at']) or item['DTEND'].dt!=aware(row['end_at']) or str(item['SUMMARY'])!=row['summary']):errors.append('Actual calendar block times/summary mismatch:'+row['event_id'])
    if model['programme']:
        if set(source_records)!={r['constraint_id'] for r in model['calendar']}:errors.append('Source calendar record lost')
        for row in model['calendar']:
            item=source_records.get(row['constraint_id'])
            if item is None:continue
            a,b=aware(row['start_at']),aware(row['end_at'])
            if a==b:
                if item.name!='VTODO' or item['DUE'].dt!=a:errors.append('Exact source deadline mismatch')
            elif item.name!='VEVENT' or item['DTSTART'].dt!=a or item['DTEND'].dt!=b:errors.append('Source calendar interval mismatch')
    programme=sorted([item for item in events if str(item.get('X-RECORD-KIND'))=='programme'],key=lambda x:x['DTSTART'].dt)
    if any(a['DTEND'].dt>b['DTSTART'].dt for a,b in zip(programme,programme[1:])):errors.append('Actual ICS programme overlap')
    demo_ids=[re.search(r'\bDEMO-\d{2}\b',str(item['SUMMARY'])).group(0) for item in events if re.search(r'\bDEMO-\d{2}\b',str(item['SUMMARY']))]
    if model['programme'] and sorted(demo_ids)!=sorted(model['demo_ids']):errors.append('Actual ICS demo identities mismatch')
    common=context(model,options,selected,run_id)
    for name in ('event-plan.md','draft-communications.md'):
        text=(root/'deliverables'/name).read_text()
        if common not in text or 'UNSENT' not in text:errors.append('Actual draft amount/headcount/approval binding:'+name)
    plan=(root/'deliverables/event-plan.md').read_text()
    for option in options:
        expected_row='|'+option['option_id']+'|'+money(option['cost_twd'])+'|'+money(option['headroom_twd'])+'|'+option['feasibility']+'|pending|'
        if expected_row not in plan:errors.append('Actual plan option amount/status mismatch:'+option['option_id'])
    for row in model['programme']:
        if '|'+row['event_id']+' '+row['summary']+'|'+row['start_at']+'|'+row['end_at']+'|' not in plan:errors.append('Actual plan programme mismatch')
    errors+=programme_checks(model) if model['programme'] else []
    return {'valid':not errors,'errors':errors,'checks':['Reopened CSV identities,amounts,quotes,headcounts,feasibility and approvals','Parsed actual ICS exact source records,deadline,programme identities,timestamps,UIDs,timezone,status and nonoverlap','Actual Markdown current amounts,headcounts,approvals and programme match serialized state']}
