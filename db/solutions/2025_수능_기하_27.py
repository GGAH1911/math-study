from sympy import *
sqrt5=sqrt(5);sqrt3=sqrt(3);sqrt10=sqrt(10)
A=Matrix([4,0,0]);B=Matrix([0,0,2*sqrt5]);C=Matrix([0,0,-2*sqrt5]);D=Matrix([2,2*sqrt3,0]);M=Matrix([0,0,0])
assert simplify((A-B).norm()-6)==0
assert simplify((B-C).norm()-4*sqrt5)==0
assert simplify((B+C)/2-M)==Matrix([0,0,0])
nAMD=(A-M).cross(D-M)
assert simplify((B-C).cross(nAMD))==Matrix([0,0,0])
AM=simplify((A-M).norm());MD_v=simplify((M-D).norm());AD_v=simplify((A-D).norm())
assert AM==MD_v==AD_v==4
AC=simplify((A-C).norm());CD=simplify((C-D).norm());AD2=simplify((A-D).norm())
assert AC==6 and CD==6 and AD2==4
s=(AC+CD+AD2)/2
area_ACD=sqrt(s*(s-AC)*(s-CD)*(s-AD2))
r=simplify(area_ACD/s)
assert simplify(r-sqrt(2))==0
n_ACD=(A-C).cross(D-C);n_BCD=(B-C).cross(D-C)
cos_theta=simplify(Abs(n_ACD.dot(n_BCD))/(n_ACD.norm()*n_BCD.norm()))
assert simplify(cos_theta-sqrt10/8)==0
proj_area=simplify(pi*r**2*cos_theta)
if simplify(proj_area-sqrt10*pi/4)==0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')