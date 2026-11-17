import json,glob,sys
cases=[json.load(open(f)) for f in sorted(glob.glob('cases/*.json'))]
for c in cases:
    s=c['scen']; n=len(c['stages'])
    assert len(c['ph'])==n and len(c['ced'])==n and len(c['water'])==n and len(c['heat'])==n, c['id']
    for g in s['g']: assert len(g)==n, (c['id'],'g')
    for k in 'names desc e w x'.split(): assert len(s[k])==len(s['g']),(c['id'],k)
    if 'rad' not in c:
        for k in 'lu': assert len(s[k])==len(s['g']),(c['id'],k)
    for sr in c['sens']['s']: assert len(sr['y'])==len(c['sens']['x']),(c['id'],'sens')
    for r in c['lci']: assert len(r)==7,(c['id'],r)
    for r in c['esrs']: assert len(r)==7,(c['id'],r)
    wf=c['wf']; tot=sum(s['g'][s['base']])
    assert abs(wf[0][1]-tot)<1e-6*max(1,abs(tot))+1e-9, (c['id'],'wf base',wf[0][1],tot)
    print(c['id'], 'baseline', round(tot,4), 'wf end', round(sum(x[1] for x in wf),4), 'scen', [round(sum(g),4) for g in s['g']], 'exec words', len(c['exec'].split()))
import csv as _csv, os
sys.path.insert(0,'.')
from lci_specs import CASES as SPECS
lcid=[]
for sp in SPECS:
    p={r['Property']:r['Value'] for r in _csv.DictReader(open(f"../lci/{sp['slug']}/dataset/{sp['slug']}_properties.csv"))}
    val='0 errors; ' + {9:'3 expected warnings (credits)',11:'1 expected warning (net N uptake)'}.get(sp['n'],'0 warnings')
    lcid.append(dict(n=sp['n'],slug=sp['slug'],fu=' | '.join(f[1] for f in sp['fu']),acts=p['Total Activities'],exch=p['Total Exchanges'],bio=p['Total Biosphere flows'],tech=p['Total Technosphere flows'],deps=p['Dataset dependencies'],val=val))
t=open('template.html').read().replace('/*DATA*/',json.dumps(cases,ensure_ascii=False)).replace('/*LCIDATA*/',json.dumps(lcid,ensure_ascii=False))
open('index.html','w').write(t.replace('/*HOSTED*/false','false'))
import pathlib; pathlib.Path('netlify/lca-portfolio/files').mkdir(parents=True,exist_ok=True)
open('netlify/lca-portfolio/index.html','w').write(t.replace('/*HOSTED*/false','true'))
print('ok',len(t))
