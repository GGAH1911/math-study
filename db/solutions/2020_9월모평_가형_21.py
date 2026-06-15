import sympy as sp

# 2020 9월모평 가형 21: A(-2,0),B(2,0). 직사각형 위 P 에 대해 PA+PB 가 (0,6)에서 최대,
# (5/2,3/2)에서 최소. 직사각형 넓이의 최댓값?  (보기 ⑤=240/19)
# 최소점 (5/2,3/2) 의 등거리타원 접선 = x+y=4 → 한 변이 이 직선. (0,6)은 x+y=6 위 정점.
# 변 방향 (1,±1). 최대 넓이는 반대 정점이 최댓값 타원(PA+PB=4√10: x^2/40+y^2/36=1) 위일 때.
CANDIDATE = sp.Rational(240, 19)
A, B = sp.Matrix([-2, 0]), sp.Matrix([2, 0])
def papb(P):
    return (P - A).norm() + (P - B).norm()
smax = papb(sp.Matrix([0, 6]))          # 4√10
a2 = (smax / 2) ** 2                      # 40
b2 = a2 - 4                               # 36  (c=2)
u = sp.symbols('u', real=True)
V = sp.Matrix([(6 + u) / 2, (6 - u) / 2]) # x+y=6, x-y=u 정점
d2 = max(s for s in sp.solve(V[0] ** 2 / a2 + V[1] ** 2 / b2 - 1, u) if s != -6)
area = d2 + 6                             # 폭 √2 × 길이 (d2+6)/√2
print('VERIFY_PASS' if sp.nsimplify(area) == CANDIDATE else 'VERIFY_FAIL')
