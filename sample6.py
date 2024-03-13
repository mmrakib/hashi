import sys
from itertools import product,combinations

def convert(c):
    if (c == '0'):
        return 0
    if (c == '1'):
        return 1
    if (c == '2'):
        return 2
    if (c == '3'):
        return 3
    if (c == '4'):
        return 4
    if (c == '5'):
        return 5
    if (c == '6'):
        return 6
    if (c == '7'):
        return 7
    if (c == '8'):
        return 8
    if (c == '9'):
        return 9
    if (c == 'a'):
        return 10
    if (c == 'b'):
        return 11
    if (c == 'c'):
        return 12

e=[]
p=[[[0,(c,r,o,[])][c!='.'] for o,c in enumerate(l.strip())] for r,l in enumerate(open(sys.argv[1]))]
r=range(len(p))
c=range(len(p[0]))
for i,j in combinations(product(r,c),2):
 if p[i[0]][i[1]] and p[j[0]][j[1]]:
  if i[0]==j[0] and abs(i[1]-j[1])>1:
    b=1
    g=range(min(i[1],j[1])+1,max(i[1],j[1]))
    for x in g:
     if p[i[0]][x]:b=0
    if b:e+=[(i,j,[i[0]],g,1)]
  if i[1]==j[1] and abs(i[0]-j[0])>1:
    b=1
    g=range(min(i[0],j[0])+1,max(i[0],j[0]))
    for x in g:
     if p[x][i[1]]:b=0
    if b:e+=[(i,j,g,[i[1]],0)]
def s(v,i,m):
 if i>=len(v):
  return None
 for j in [3,2,1,0]:
  v[i]=j
  q=dict(m)
  b=1
  for l in [0,1]:
   n=e[i][l]
   if not n in q:q[n]=0
   q[n]+=j
   y=convert(p[n[0]][n[1]][0])
   if q[n]>y:b=0
  if not b:continue
  a=[d for b in range(i+1) for d in product(e[b][2],e[b][3]) if v[b]>0]
  if len(a)!=len(set(a)):continue
  if i==len(v)-1:
   g=1
   for l,z in product(r,c):
    n=p[l][z]
    if not n:continue
    if q[(n[1],n[2])]!=convert(n[0]):g=0
   if g:return v
  u=s(v,i+1,q)
  if u:return u
for i,v in zip(e,s([None]*len(e),0,{})):
 if v > 0:
    for j, k in product(i[2], i[3]):
        if v == 3:
            p[j][k] = '#' if i[4] == 1 else 'E'
        else:
            p[j][k] = [['|', '$'][v - 1], ['-', '='][v - 1]][i[4]]
for l in p:
 for c in l:
  if not c:c=[' ']
  sys.stdout.write(c[0])
 print('')