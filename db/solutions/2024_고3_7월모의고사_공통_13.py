from sympy import *
sqrt7=sqrt(7); sqrt21=sqrt(21)
B=Matrix([0,0]); C=Matrix([Rational(36,7)*sqrt7,0])
A=Matrix([Rational(27,14)*sqrt7,Rational(45,14)*sqrt21])
O=Matrix([Rational(18,7)*sqrt7,Rational(9,7)*sqrt21])
D=Matrix([3*sqrt7,0])
Op=Matrix([Rational(57,14)*sqrt7,Rational(25,14)*sqrt21])
R_sq=simplify((O-A).dot(O-A)); assert R_sq==81
Rp_sq=simplify((Op-A).dot(Op-A)); assert Rp_sq==75
assert simplify((Op-D).dot(Op-D))==75
assert simplify((Op-C).dot(Op-C))==75
t=symbols('t'); sol=solve(A+t*(O-A)-D,t); assert simplify(sol[t]-Rational(5,3))==0
OO2=simplify((Op-O).dot(Op-O))
print('VERIFY_PASS' if OO2==21 else f'VERIFY_FAIL: {OO2}')