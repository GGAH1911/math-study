import sympy as sp
# y=2^{x-3}+1, y=2^{x-1}-2 교점 A. 직선 y=-x+k 가 두 곡선과 만나는 B,C, BC=√2, x_B>x_A. △ABC 넓이? (③=5/2)
CANDIDATE = sp.Rational(5, 2)
x = sp.symbols('x')
xA = sp.solve(sp.Eq(2**(x-3)+1, 2**(x-1)-2), x)[0]            # 3
A = (xA, 2**(xA-3)+1)
# B on curve1, C=(x_B-1) on curve2 (BC=√2, |Δx|=1): y_B+1 = 2^{x_B-2}-2 → 2^{x_B-3}=4
xB = sp.solve(sp.Eq(2**(x-3)+2, 2**(x-2)-2), x)[0]            # 5
B = (xB, 2**(xB-3)+1)
C = (xB-1, 2**((xB-1)-1)-2)
assert sp.simplify((B[0]-C[0])**2+(B[1]-C[1])**2 - 2) == 0    # BC=√2
area = sp.Rational(1,2)*abs(A[0]*(B[1]-C[1])+B[0]*(C[1]-A[1])+C[0]*(A[1]-B[1]))
print('VERIFY_PASS' if sp.simplify(area-CANDIDATE) == 0 else 'VERIFY_FAIL')
