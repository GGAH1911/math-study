import sympy as sp
CANDIDATE = sp.Rational(4,3)
sqrt2=sp.sqrt(2)
s=-sqrt2/2+sp.sqrt(6)/2
O1=(sp.Integer(0),sp.Integer(0)); M1=(sqrt2,sp.Integer(0)); O2=(sp.Integer(0),sqrt2)
C1=(sqrt2+s,s); A2=(s,sqrt2+s)
def area(p):
    a=0;n=len(p)
    for i in range(n):
        x1,y1=p[i];x2,y2=p[(i+1)%n];a+=x1*y2-x2*y1
    return sp.simplify(a/2)
def ccw(p): return p if area(p)>0 else p[::-1]
def clip(sub,cl):
    out=sub
    for i in range(len(cl)):
        A=cl[i];B=cl[(i+1)%len(cl)];inp=out;out=[]
        f=lambda p:(B[0]-A[0])*(p[1]-A[1])-(B[1]-A[1])*(p[0]-A[0])
        isin=lambda p: sp.simplify(f(p))>=0
        for j in range(len(inp)):
            cur=inp[j];prv=inp[(j-1)%len(inp)]
            def it(p,q):
                d1=f(p);d2=f(q);t=d1/(d1-d2);return (p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1]))
            if isin(cur):
                if not isin(prv):out.append(it(prv,cur))
                out.append(cur)
            elif isin(prv):out.append(it(prv,cur))
    return out
A1=area(clip(ccw([O2,M1,C1,A2]),ccw([O1,C1,A2])))
r=sp.sqrt((A2[0]-O2[0])**2+(A2[1]-O2[1])**2)/2
S=sp.simplify(A1/(1-r**2))
print('VERIFY_PASS' if sp.simplify(S-CANDIDATE)==0 else 'VERIFY_FAIL')