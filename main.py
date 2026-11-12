import json,os,sys,time,urllib.request,urllib.error
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("E")
F="abcdefgh";V={"p":100,"n":320,"b":330,"r":500,"q":900,"k":0};N=[0];B=3000;T={}
def S(f,r):return f+r*8
def G(fen):
 p=fen.split();b={};r=7
 for w in p[0].split("/"):
  f=0
  for c in w:
   if c.isdigit():f+=int(c)
   else:b[S(f,r)]=c;f+=1
  r-=1
 return b,p[1],p[2]
def M(b,sd):
 ms=[];o="b"if sd=="w"else"w"
 for d,pc in list(b.items()):
  if(pc.isupper())!=(sd=="w"):continue
  f=d&7;r=d>>3;t=pc.lower()
  def a(x,y,pr=""):
   if 0<=x<8 and 0<=y<8:ms.append(F[f]+str(r+1)+F[x]+str(y+1)+pr)
  if t=="p":
   dr=1 if sd=="w"else-1;nr=r+dr
   if 0<=nr<8 and S(f,nr)not in b:
    if nr in(0,7):a(f,nr,"q")
    else:a(f,nr)
    if r==(1 if sd=="w"else 6)and S(f,nr)not in b and S(f,nr+dr)not in b:a(f,nr+dr)
   for df in(-1,1):
    x=f+df;y=r+dr
    if 0<=x<8 and 0<=y<8:
     cp=b.get(S(x,y))
     if cp and(cp.isupper())!=(sd=="w"):a(x,y,"q")if y in(0,7)else a(x,y)
  elif t=="n":
   for df,dr in((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)):a(f+df,r+dr)
  elif t=="k":
   for df in(-1,0,1):
    for dr in(-1,0,1):
     if df or dr:a(f+df,r+dr)
  else:
   ds={"b":(1,1,1,-1,-1,1,-1,-1),"r":(1,0,-1,0,0,1,0,-1),"q":(1,0,-1,0,0,1,0,-1,1,1,1,-1,-1,1,-1,-1)}[t]
   for i in range(0,len(ds),2):
    df,dr=ds[i],ds[i+1];x,y=f+df,r+dr
    while 0<=x<8 and 0<=y<8:
     cp=b.get(S(x,y))
     if cp:
      if(cp.isupper())!=(sd=="w"):a(x,y)
      break
     a(x,y);x+=df;y+=dr
 return ms
def A(b,sd,mo):
 f=F.index(mo[0]);r=int(mo[1])-1;t=F.index(mo[2]);u=int(mo[3])-1
 x=S(f,r);y=S(t,u);b=dict(b);pc=b.pop(x);cp=b.get(y)
 if len(mo)==5:pc="q"if pc.islower()else"Q"
 b[y]=pc
 return b,"b"if sd=="w"else"w"
def e(b,sd):
 t=0
 for d,pc in b.items():t+=(1 if pc.isupper()else-1)*V[pc.lower()]
 return t if sd=="w"else-t
def C(m,b):return bool(b.get(S(F.index(m[2]),int(m[3])-1)))or len(m)==5
def K(m,b):
 f=F.index(m[0]);r=int(m[1])-1;t=F.index(m[2]);u=int(m[3])-1
 cp=b.get(S(t,u));mv=V[b.get(S(f,r)).lower()]if b.get(S(f,r))else 0;cv=V[cp.lower()]if cp else 0
 return-(cv*16-mv*2)if cp else-mv
def s(b,sd,d,a,z):
 N[0]+=1
 if N[0]>B:raise TimeoutError
 if d<=0:return e(b,sd)
 best=-10**9
 for m in sorted(M(b,sd),key=lambda m:K(m,b)):
  b2,s2=A(b,sd,m);v=-s(b2,s2,d-1,-z,-a)
  if v>=z:return z
  if v>best:best=v
  if v>a:a=v
 return best
def P(fen,legal):
 b,sd,c=G(fen);ms=[m for m in legal if m in set(M(b,sd))]
 if not ms:return legal[0] if legal else None
 bm=ms[0]
 for depth in range(1,5):
  N[0]=0;db=-10**9;dm=bm;ok=1;t0=time.monotonic()
  for m in ms:
   if time.monotonic()-t0>0.7:ok=0;break
   b2,s2=A(b,sd,m)
   try:v=-s(b2,s2,depth-1,-10**9,10**9)
   except TimeoutError:ok=0;break
   if v>db:db=v;dm=m
  if ok:bm=dm
  else:break
 return bm
def p(path,body):
 req=urllib.request.Request(E+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(req)as res:return json.load(res)
 except urllib.error.HTTPError as ex:sys.exit(path+": HTTP "+str(ex.code))
while 1:
 g=p("/game",{})
 if g.get("status")=="done":break
 while g.get("status")=="your_move":
  m=P(g["fen"],g.get("legal_moves")or[])
  if m is None:break
  g=p("/move",{"game":g["game"],"move":m})
 print("game",g.get("game"),g.get("outcome"),g.get("reason"),file=sys.stderr)
print("done",g.get("wins"),g.get("draws"),g.get("losses"),file=sys.stderr)
