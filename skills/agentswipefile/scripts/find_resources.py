#!/usr/bin/env python3
"""Search the public Agent Swipe File catalog. Python standard library only."""
import argparse
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

PRIMARY = 'https://agentswipefile.com/catalog.json'

def load_catalog(path=None):
    if path:
        return json.loads(Path(path).read_text()),'local file'
    try:
        request=urllib.request.Request(PRIMARY,headers={'User-Agent':'AgentSwipeFile-Skill/1.1'})
        with urllib.request.urlopen(request,timeout=20) as response:
            catalog=json.loads(response.read(4_000_000))
        if not isinstance(catalog.get('resources'),list):
            raise ValueError('The response has no resource list')
        return catalog,PRIMARY
    except (urllib.error.URLError,ValueError,TimeoutError) as exc:
        raise RuntimeError('The public catalog is unavailable. Do not invent live resource facts.') from exc

def shortlist(catalog,query='',asset=None,requires=None,platform=None,free=False,limit=3):
    tokens=set(re.findall(r'[a-z0-9]+',query.lower()))-{'a','an','and','for','the','to','with','i','need'}
    results=[]
    for resource in catalog['resources']:
        workflow=resource.get('workflow',{})
        if asset and asset not in resource.get('categories',[]):continue
        if requires and workflow.get('capabilities',{}).get(requires,{}).get('status')!='documented':continue
        if platform and not any(x.get('platform','').casefold()==platform.casefold() and x.get('status')=='documented' and x.get('scope')=='resource' and (not free or x.get('freeAccess') is True) for x in workflow.get('platforms',[])):continue
        if free and workflow.get('pricing',{}).get('freeAccess') is not True:continue
        if free and requires and workflow.get('capabilities',{}).get(requires,{}).get('freeAccess') is not True:continue
        fields=[resource.get('name',''),resource.get('description',''),' '.join(resource.get('bestFor',[])),' '.join(resource.get('categories',[])),workflow.get('primaryJob','')]
        score=sum(sum(token in field.lower() for token in tokens)*weight for field,weight in zip(fields,[2,3,4,2,2]))
        if tokens and score==0:continue
        results.append((score,resource))
    results.sort(key=lambda x:(-x[0],x[1]['name'].casefold()))
    return [dict(r,keywordScore=score) for score,r in results[:limit]]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query',default='')
    parser.add_argument('--asset',choices=['ads','ugc','emails','sms','websites','apps','social','presentations','context','design'])
    parser.add_argument('--requires',choices=['mcp','api','figmaPlugin','browserExtension','markdown'])
    parser.add_argument('--platform')
    parser.add_argument('--free',action='store_true',help='Require documented free access, which may be a limited preview. This does not establish free full-library or connector access.')
    parser.add_argument('--limit',type=int,default=3)
    parser.add_argument('--catalog-file')
    args=parser.parse_args()
    if not 1<=args.limit<=20:parser.error('--limit must be between 1 and 20')
    try:
        catalog,source=load_catalog(args.catalog_file)
        results=shortlist(catalog,args.query,args.asset,args.requires,args.platform,args.free,args.limit)
    except (OSError,ValueError,RuntimeError) as exc:
        print(str(exc),file=sys.stderr);return 1
    print(json.dumps({'catalogSource':source,'usedTemporaryFallback':False,'updatedAt':catalog.get('updatedAt'),'matches':results,'note':'Keyword shortlist only. Free access can be a limited preview; read all relevant pricing plans, billing periods and connector entitlements before recommending.'},indent=2,ensure_ascii=False))
    return 0

if __name__=='__main__':sys.exit(main())
