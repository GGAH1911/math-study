from sympy import *
sqrt3 = sqrt(3)
A1=Matrix([4,4*sqrt3]); B1=Matrix([0,0]); C1=Matrix([8,0])
D1=(A1+B1)/2; E1=(B1+C1)/2; F1=(C1+A1)/2
G1=(A1+D1)/2; H1=(B1+E1)/2; I1=(C1+F1)/2
A2=(G1+D1)/2; B2=(H1+E1)/2; C2=(I1+F1)/2
def shoelace(pts):
    n=len(pts); area=S.Zero
    for i in range(n):
        j=(i+1)%n
        area+=pts[i][0]*pts[j][1]-pts[j][0]*pts[i][1]
    return Abs(area)/2
area1=shoelace([A2,C2,F1,G1])
area2=shoelace([B2,A2,D1,H1])
area3=shoelace([C2,B2,E1,I1])
S1=area1+area2+area3
side=sqrt((B2-A2).dot(B2-A2))
r=(side/8)**2
limit_S=simplify(S1/(1-r))
expected=Rational(112,15)*sqrt3
if simplify(limit_S-expected)==0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL got',limit_S,'expected',expected)
