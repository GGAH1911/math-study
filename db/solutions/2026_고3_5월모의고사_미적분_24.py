import sympy as sp
from sympy import symbols, limit, oo

# b_n을 정의: b_n = a_n / 3^n
# 급수가 수렴하므로 lim b_n = 0
# a_n = b_n * 3^n으로 표현

n = symbols('n', integer=True, positive=True)
b_n = symbols('b_n', real=True)

# 극한식: (a_n + 3^(n+1)) / (a_n + 3^(n-1))
# = (b_n * 3^n + 3^(n+1)) / (b_n * 3^n + 3^(n-1))
# 분자와 분모를 3^n으로 나누면:
# = (b_n + 3) / (b_n + 1/3)

# b_n -> 0 일 때의 극한
result = (0 + 3) / (0 + 1/3)
print(result)

# 검증
if result == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')