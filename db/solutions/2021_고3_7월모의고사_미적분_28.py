import sympy as sp
theta = sp.Symbol('theta', positive=True)
A = sp.Matrix([-5, 0])
B = sp.Matrix([5*sp.cos(theta), -5*sp.sin(theta)])
C = sp.Matrix([5*sp.cos(theta), 5*sp.sin(theta)])
D = sp.Matrix([5, 0])
E = sp.Matrix([5/sp.cos(theta), 5*sp.tan(theta)])
# 검증 1: BD ⊥ AB
AB = B - A
BD = D - B
assert sp.simplify(AB.dot(BD)) == 0, 'BD not perp AB'
# 검증 2: D가 원 위
assert sp.simplify(D.dot(D)) == 25, 'D not on circle'
# 검증 3: E가 직선 AC 위
AC = C - A
check_ac = sp.simplify((E[0]-A[0])*AC[1] - (E[1]-A[1])*AC[0])
assert check_ac == 0, 'E not on line AC'
# 검증 4: E가 직선 BD 위
check_bd = sp.simplify((E[0]-B[0])*BD[1] - (E[1]-B[1])*BD[0])
assert check_bd == 0, 'E not on line BD'
# 넓이 계산
def area(P,Q,R):
    v1=Q-P; v2=R-P
    return sp.Rational(1,2)*sp.Abs(v1[0]*v2[1]-v1[1]*v2[0])
f_th = sp.simplify(area(A,B,C))
g_th = sp.simplify(area(C,D,E))
ratio = sp.simplify(g_th / (theta**2 * f_th))
lim_val = sp.limit(ratio, theta, 0, '+')
if lim_val == sp.Rational(1,4):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {lim_val}')
