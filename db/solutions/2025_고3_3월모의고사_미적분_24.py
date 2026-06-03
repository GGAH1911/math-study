import sympy as sp
from sympy import symbols, limit, oo

n = symbols('n', positive=True, integer=True)

# 주어진 조건에서 a_n의 점근 형태
a_n = 3*n**2 / (2*n + 3)

# 주어진 조건 검증
condition = limit((2*n + 3)*a_n / n**2, n, oo)
if condition == 3:
    # 구하는 극한값 계산
    result = limit(n*a_n / (3*n**2 + 1), n, oo)
    if result == sp.Rational(1, 2):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')