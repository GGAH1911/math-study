import sympy as sp
from sympy import symbols, solve, simplify

# 직선 위의 점: (t+1, 2-t, 2t-1)
t = symbols('t')
x_line = t + 1
y_line = 2 - t
z_line = 2*t - 1

# 벡터 PA: (1,2,-1) - (2,0,5) = (-1, 2, -6)
PA = [-1, 2, -6]

# 직선의 방향벡터
d = [1, -1, 2]

# 외적 (법선벡터)
normal = [
    PA[1]*d[2] - PA[2]*d[1],
    PA[2]*d[0] - PA[0]*d[2],
    PA[0]*d[1] - PA[1]*d[0]
]
# normal = (2*2 - (-6)*(-1), (-6)*1 - (-1)*2, (-1)*(-1) - 2*1)
# normal = (4-6, -6+2, 1-2) = (-2, -4, -1)
normal = [2, 4, 1]  # 같은 법선

# 평면 방정식: 2(x-2) + 4(y-0) + 1(z-5) = 0
# 2x + 4y + z = 9

# x축 위의 점 (x, 0, 0)을 평면에 대입
x = symbols('x')
plane_eq = 2*x + 4*0 + 0 - 9
x_val = solve(plane_eq, x)[0]

# 검증: 직선이 평면에 포함되는가
plane_check = 2*(t+1) + 4*(2-t) + (2*t-1) - 9
plane_check_simplified = simplify(plane_check)

if x_val == sp.Rational(9, 2) and plane_check_simplified == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')