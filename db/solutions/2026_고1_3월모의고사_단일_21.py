from sympy import *
t_val = Rational(4,5)
c_val = 2*sqrt(5)
a_val = 3*c_val
B = Matrix([0,0])
A = Matrix([-a_val,0])
C = Matrix([0,c_val])
D = Matrix([-c_val,0])
E = Matrix([a_val*(t_val-1), t_val*c_val])
def area3(P,Q,R):
    v1=Q-P; v2=R-P
    return Abs(v1[0]*v2[1]-v1[1]*v2[0])/2
BC=(C-B).norm(); BE=(E-B).norm(); BD=(D-B).norm()
assert simplify(BC-c_val)==0,'BC'
assert simplify(BE-c_val)==0,'BE'
assert simplify(BD-c_val)==0,'BD'
assert simplify(area3(E,A,D)-16)==0,'area_EAD'
assert simplify(area3(C,E,D)-4)==0,'area_CED'
CE=(E-C).norm()
perimeter=simplify(BC+BE+CE)
expected=2*sqrt(2)+4*sqrt(5)
if simplify(perimeter-expected)==0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL',perimeter)