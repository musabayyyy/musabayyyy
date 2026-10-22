import os, json, urllib.request, pathlib
from html import escape
query = 'query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount color}}}}}}'
body = json.dumps({'query':query,'variables':{'login':'musabayyyy'}}).encode()
req = urllib.request.Request('https://api.github.com/graphql', data=body, headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Content-Type':'application/json'})
with urllib.request.urlopen(req, timeout=45) as response:
    data = json.load(response)
if data.get('errors'):
    raise RuntimeError(data['errors'])\ncalendar = data['data']['user']['contributionsCollection']['contributionCalendar']
parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280"><rect width="800" height="280" rx="12" fill="#020805"/>']
for c, week in enumerate(calendar['weeks']):
    for r, day in enumerate(week['contributionDays']):
        x, y = 20+c*14, 30+r*17
        n = day['contributionCount']
        color = '#102419' if n == 0 else '#14532d' if n < 3 else '#166534' if n < 6 else '#22c55e' if n < 10 else '#86efac'
        title = escape(str(day['date'])+': '+str(n)+' contributions')
        parts.append(f'<rect x="{x}" y="{y}" width="10" height="12" rx="2" fill="{color}"><title>{title}</title></rect>')
        if n:
            parts.append(f'<path d="M{x+5} {y+6} Q{x+5} 190 400 225" stroke="#22c55e" stroke-width="0.4" fill="none" opacity="0.1"/>')
parts.append('<rect y="25" width="2" height="130" fill="#bbf7d0"><animate attributeName="x" values="20;770;20" dur="14s" repeatCount="indefinite"/></rect><circle cx="400" cy="225" r="7" fill="#86efac"><animate attributeName="r" values="5;10;5" dur="3s" repeatCount="indefinite"/></circle>')
parts.append(f'<text x="400" y="267" text-anchor="middle" font-family="monospace" font-size="12" fill="#86efac">Contribution Observatory | {calendar["totalContributions"]} contributions | past year</text></svg>')
pathlib.Path('assets').mkdir(exist_ok=True)
pathlib.Path('assets/observatory.svg').write_text(''.join(parts), encoding='utf-8')
