import sympy as sp

# 원래 문제 설정
A = sp.Matrix([0, 0])
B = sp.Matrix([6, 0])

# cos(∠CAB)=1/3, 반원(지름 AB) → ∠ACB=90°, AC=2
cos_A = sp.Rational(1, 3)
sin_A = sp.sqrt(1 - cos_A**2)  # 2√2/3
AC = 2
C = sp.Matrix([AC * cos_A, AC * sin_A])  # (2/3, 4√2/3)

# C가 반원 (x-3)^2+y^2=9 위에 있는지
assert sp.simplify((C[0]-3)**2 + C[1]**2 - 9) == 0, 'C not on semicircle'

# D: AB 위, DB=AC=2
D = sp.Matrix([4, 0])
assert sp.Abs(D[0] - B[0]) == 2  # DB=2

# CD 방향
dir_CD = D - C

# B를 지나고 CD에 평행한 직선의 반원 교점 E
t = sp.symbols('t', real=True)
Px = 6 + t * dir_CD[0]
Py = 0 + t * dir_CD[1]
eq = (Px - 3)**2 + Py**2 - 9
solns = sp.solve(eq, t)
t_E = [s for s in solns if s != 0][0]
E = sp.Matrix([sp.Rational(16, 11), 20*sp.sqrt(2)/11])

# 내 답 대입하여 검증
# 1) E가 반원 위
assert sp.simplify((E[0]-3)**2 + E[1]**2 - 9) == 0, 'E not on semicircle'
# 2) CE 거리 확인
CE_vec = E - C
CE_sq = sp.simplify(CE_vec.dot(CE_vec))
CE_val = sp.sqrt(CE_sq)
expected = 2*sp.sqrt(33)/11
if sp.simplify(CE_val - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
