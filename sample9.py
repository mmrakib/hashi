import sys,re,copy
A=sys.stdin.read()
W=A.find('\n')+1
r=range
V={}
E=[]
for i in r(len(A)):
 if'0'<A[i]<'9':V[i]=int(A[i])
 for d in(1,W):m=re.match('[1-8]( +)[1-8]',A[i::d]);E+=[[i,i+len(m.group(1))*d+d,d,r(3)]]if m else[]
def S(E):
 q,t=0,1
 while q!=t:
  for e in E:
   if any(d[0]and e[3][0]==0and any(i in r(a+c,b,c)for i in r(e[0]+e[2],e[1],e[2]))for a,b,c,d in E):e[3]=[0]
  for i in V:
   m=sum(min(e[3])for e in E if i in e[:2]);n=sum(max(e[3])for e in E if i in e[:2])
   if m>V[i]or n<V[i]:return
   for e in E:
    if m+2>V[i]and i in e[:2]:e[3]=e[3][:V[i]-m+1]
    if n-2<V[i]and i in e[:2]:e[3]=e[3][V[i]-n-1:]
  t=q;q=sum(len(e[3])for e in E)
 Q=[min(V)]
 i=0
 while Q[i:]:
  x=Q[i];i+=1
  for e in E:
   if x in e[:2]:
    if sum(e[3]):
     for y in e[:2]:
      if y not in Q:Q+=[y]
 if len(Q)!=len(V):return
 U=[e for e in E if e[3][1:]]
 if U:
  for w in U[0][3]:U[0][3]=[w];S(copy.deepcopy(E))
 else:
  B=A
  for a,b,c,d in E:
   if d[0]:
    for i in r(a+c,b,c):B=B[:i]+[{1:'─',W:'│'},{1:'═',W:'║'}][d[0]-1][c]+B[i+1:]
  print(B)
  sys.exit(0)
S(E)