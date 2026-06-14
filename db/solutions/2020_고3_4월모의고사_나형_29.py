CANDIDATE = 40
from itertools import combinations
def ne(a,b): return tuple(sorted([a,b]))
def mono(start,end):
    sx,sy=start;ex,ey=end;dx=ex-sx;dy=ey-sy;n=abs(dx)+abs(dy)
    sX=(1 if dx>0 else -1,0);sY=(0,1 if dy>0 else -1);ps=[]
    for c in combinations(range(n),abs(dx)):
        seq=[sY]*n
        for i in c: seq[i]=sX
        cur=start;e=set()
        for s in seq:
            nx=(cur[0]+s[0],cur[1]+s[1]);e.add(ne(cur,nx));cur=nx
        ps.append(frozenset(e))
    return ps
fwd=mono((0,0),(3,3));ret=mono((3,3),(0,0))
def sq(x,y):
    c=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
    return [ne(c[0],c[1]),ne(c[1],c[2]),ne(c[2],c[3]),ne(c[3],c[0])]
S={(x,y):sq(x,y) for x in range(3) for y in range(3)}
cnt=0
for f in fwd:
    for r in ret:
        cov=f|r
        full=[s for s,es in S.items() if all(e in cov for e in es)]
        if full==[(2,2)]: cnt+=1
print('VERIFY_PASS' if cnt==CANDIDATE else 'VERIFY_FAIL')