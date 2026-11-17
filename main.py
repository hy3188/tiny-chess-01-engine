import os,json as J,urllib.request as U
V=(0,100,320,330,500,950,0)
D8=(-16,-15,1,17,16,15,-1,-17);DR=D8[::2];DB=D8[1::2];DN=(-33,-31,-18,-14,14,18,31,33);SQ=[s for s in range(128)if not s&136]
def P(fen):
 a=fen.split();b=[0]*128;r=7;f=0
 for c in a[0]:
  q='PNBRQKpnbrqk'.find(c)
  if c=='/':r-=1;f=0
  elif c.isdigit():f+=int(c)
  else:b[r*16+f]=q+1 if q<6 else 5-q;f+=1
 return[b,1 if a[1]=='w'else-1,sum((c in a[2])<<i for i,c in enumerate('KQkq'))]
def A(b,sq,by):
 for d in DN:
  t=sq+d
  if not t&0x88 and b[t]==2*by:return 1
 for i,d in enumerate(D8):
  t=sq+d
  while not t&0x88:
   p=b[t]
   if p:
    if p*by>0:
     ap=abs(p)
     if(ap in(4,5)and(ap==5 or i%2==0))or(ap==3 and i%2)or(t==sq+d and(ap==6 or(ap==1 and i%2 and d*by<0))):return 1
    break
   t+=d
 return 0
def G(pos,cap=0):
 b=pos[0];tm=pos[1];res=[]
 for sq in SQ:
  p=b[sq]
  if not p or(p>0)!=(tm>0):continue
  ap=abs(p)
  if ap==1:
   up=16*tm;one=sq+up;pr=5 if one>>4 in(0,7)else 0
   if not cap and not b[one]:
    res.append((sq,one,pr))
    if sq>>4==1+5*(tm<0)and not b[sq+2*up]:res.append((sq,sq+2*up,0))
   for d in(up-1,up+1):
    t=sq+d
    if not t&0x88 and b[t]and(b[t]>0)!=(tm>0):res.append((sq,t,pr))
  else:
   for d in(DN if ap==2 else DB if ap==3 else DR if ap==4 else D8):
    t=sq+d
    while not t&0x88:
     q=b[t]
     if q:
      if(q>0)!=(tm>0):res.append((sq,t,0))
      break
     if not cap:res.append((sq,t,0))
     if ap in(2,6):break
     t+=d
 if not cap and pos[2]:
  home=0 if tm==1 else 112
  for bit,rf,emp,dst in((1,7,(5,6),6),(2,0,(1,2,3),2)):
   if pos[2]&(bit if tm==1 else bit*4)and b[home+4]==6*tm and b[home+rf]==4*tm and all(not b[home+e]for e in emp)and all(not A(b,home+e,-tm)for e in(4,(4+dst)//2,dst)):res.append((home+4,home+dst,0))
 return res
def M(pos,m):
 b=pos[0][:];frm,to,pro=m;p=b[frm];tm=pos[1];cap=b[to]
 b[to]=pro*tm if pro else p;b[frm]=0
 if abs(p)==6 and abs(to-frm)==2:
  rf,rt=(frm+3,frm+1)if to>frm else(frm-4,frm-1)
  b[rt]=b[rf];b[rf]=0
 return[b,-tm,pos[2]],cap
def E(pos):
 b=pos[0];s=0
 ph=sum((0,0,1,1,2,4,0)[abs(x)]for x in b if x)
 for sq in SQ:
  p=b[sq]
  if not p:continue
  ap=abs(p);r,f=sq>>4,sq&7;w=p>0;c=min(r,7-r)+min(f,7-f);y=r if w else 7-r
  if ap==1:v=(y*y*3)//2+min(f,7-f)*3-3
  elif ap in(2,3):v=c*4-16
  elif ap==4:v=min(f,7-f)*2-6
  elif ap==5:v=c*2-8
  else:v=c*7-30 if ph<=6 else-30-y*10
  s+=(V[ap]+v)*(1 if w else-1)
 return s*pos[1]
TT={};HP=set();ND=[0];BUD=100000
def KEY(pos):return(tuple(pos[0]),pos[1],pos[2])
def OM(pos,moves,ttm,ply):
 b=pos[0]
 moves.sort(key=lambda m:(1<<30)if m==ttm else(1<<24)+10*V[abs(b[m[1]])]-V[abs(b[m[0]])]if b[m[1]]else 0,reverse=True);return moves
def S(pos,d,a,be,ply):
 ND[0]+=1
 assert ND[0]<BUD
 q=d<=0;ttm=None
 if q:
  a=max(a,E(pos))
  if a>=be:return a
 else:
  key=KEY(pos)
  if ply>0 and key in HP:return 0
  if ent:=TT.get(key):
   ttm=ent[3]
   if ent[0]>=d:
    if ent[1]==0:return ent[2]
    if ent[1]==1 and ent[2]>a:a=ent[2]
    if ent[1]==2 and ent[2]<be:be=ent[2]
    if a>=be:return ent[2]
 best=-10**9;bm=None;a0=a;n=0
 for m in OM(pos,G(pos,1 if q else 0),ttm,ply):
  np,cap=M(pos,m)
  if cap and abs(cap)==6:return 100000-ply
  n+=1
  if not q and n>1:
   sc=-S(np,d-2 if(d>=3 and n>3 and not cap and not m[2])else d-1,-a-1,-a,ply+1)
   if a<sc<be:sc=-S(np,d-1,-be,-a,ply+1)
  else:sc=-S(np,d-1,-be,-a,ply+1)
  if sc>best:best=sc;bm=m
  if sc>a:a=sc
  if a>=be:break
 if q:return a
 if bm is None:return 0
 TT[key]=(d,0 if a0<best<be else(2 if best<=a0 else 1),best,bm);return best
def BM(pos):
 ND[0]=0
 HP.add(KEY(pos));bm=G(pos)[0];d=1
 try:
  while ND[0]<BUD:
   S(pos,d,-10**9,10**9,0)
   if e:=TT.get(KEY(pos)):bm=e[3]
   d+=1
 except AssertionError:pass
 return bm
env=os.environ['MAKEFUN_ENV_URL']
post=lambda pa,bo:J.load(U.urlopen(U.Request(env+pa,data=J.dumps(bo).encode())))
while True:
 g=post('/game',{});s=g['status']
 if s=='done':break
 while s=='your_move':
  m=BM(P(g['fen']));frm,to,pro=m
  u=''.join(chr(97+(x&7))+chr(49+(x>>4))for x in(frm,to))
  if pro:u+='qrbn'[5-pro]
  g=post('/move',{'game':g['game'],'move':u});s=g['status']