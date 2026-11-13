import json,os,sys,urllib.request,urllib.error
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit()
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':9000}
F='abcdefgh'
def b(f):
 d={}
 for i,r in enumerate(f.split()[0].split('/')):
  x=0
  for c in r:
   if c.isdigit():x+=int(c)
   else:d[F[x]+str(8-i)]=c;x+=1
 return d
def e(d,w):
 r=0
 for x,c in d.items():
  v=V[c.lower()]
  r+=v if c.isupper()==w else -v
 return r
def c(f,t,d):
 pc=d.get(f);vc=d.get(t)
 if vc is None:return 0
 if pc and pc.lower()=='p' and abs(ord(f[0])-ord(t[0]))==1 and t not in d:vc='p'
 return V[vc.lower()]
while 1:
 g=json.load(urllib.request.urlopen(urllib.request.Request(E+'/game',data=b'{}',headers={'content-type':'application/json'}),timeout=5))
 if g.get('status')=='done':break
 while g.get('status')=='your_move':
  d=b(g['fen']);w=g['colour']=='white';l=g['legal_moves'];bm=None;bv=-1e9
  for mv in l:
   f,t=mv[:2],mv[2:4];n=d.copy();n.pop(f);n[t]=mv[4] if len(mv)==5 else d[f]
   val=e(n,w)-c(f,t,d)
   if val>bv:bv=val;bm=mv
  if bm is None:break
  g=json.load(urllib.request.urlopen(urllib.request.Request(E+'/move',data=json.dumps({'game':g['game'],'move':bm}).encode(),headers={'content-type':'application/json'}),timeout=5))
 print(g.get('outcome','?'),file=sys.stderr)
