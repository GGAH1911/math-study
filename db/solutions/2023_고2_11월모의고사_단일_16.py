import sympy as sp
from sympy import symbols, Abs, limit, solve, simplify

t = symbols('t', positive=True, real=True)
x = symbols('x', positive=True, real=True)

# 교점 찾기
# 왼쪽 부분: 2/x - 3 = t
x1 = 2 / (t + 3)

# 오른쪽 부분: 3 - 2/x = t
x2 = 2 / (3 - t)

# 거리 함수
f_t = x2 - x1
f_t_simplified = simplify(f_t)

# 극한값 계산
result = limit(f_t / t, t, 0, '+')

# 검증
if result == sp.Rational(4, 9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')