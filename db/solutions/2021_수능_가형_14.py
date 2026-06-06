from fractions import Fraction as F
# Re-derive from original problem statement
A=(F(0),F(2)); B1=(F(0),F(0)); C1=(F(4),F(0)); D1=(F(4),F(2))
E1=(F(3),F(2))  # AE1:E1D1 = 3:1, AD1=4 horizontal
# F1 inside, right angle at F1, |F1E1|=|F1C1|
F1=(F(5,2),F(1,2))
# verify F1 conditions
d1=(F1[0]-E1[0])**2+(F1[1]-E1[1])**2
d2=(F1[0]-C1[0])**2+(F1[1]-C1[1])**2
dot=(E1[0]-F1[0])*(C1[0]-F1[0])+(E1[1]-F1[1])*(C1[1]-F1[1])
assert d1==d2 and dot==0
# inside rectangle
assert 0<=F1[0]<=4 and 0<=F1[1]<=2
# Shoelace for quadrilateral E1 F1 C1 D1
def sh(P):
    s=F(0)
    for i in range(len(P)):
        x1,y1=P[i]; x2,y2=P[(i+1)%len(P)]
        s+=x1*y2-x2*y1
    return abs(s)/2
S1=sh([E1,F1,C1,D1])
assert S1==F(9,4)
# New rectangle AB2C2D2: AB2:AD2=1:2, A=(0,2), B2 on AB1 (x=0), D2 on AE1 (y=2), C2 on E1F1
# Line E1F1: from (3,2) to (5/2,1/2): y = 3x - 7
# AB2=a (vertical), AD2=2a (horizontal). C2=(2a, 2-a) on line
# 2 - a = 3(2a) - 7  =>  a = 9/7
a=F(9,7)
C2=(2*a, 2-a)
assert C2[1]==3*C2[0]-7
# Containment: D2=(2a,2) on AE1 segment => 0<=2a<=3
assert F(0)<=2*a<=F(3)
assert F(0)<=a<=F(2)  # B2 inside
# Linear ratio = AB2/AB1
r=a/2
assert r==F(9,14)
# Geometric series sum
S_inf=S1/(1-r*r)
ans=F(441,115)
if S_inf==ans:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
