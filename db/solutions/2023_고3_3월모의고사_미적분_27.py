import sympy as sp
from sympy import symbols, limit, oo, summation, simplify

n = symbols('n', positive=True, integer=True)
k = symbols('k', positive=True, integer=True)

# 등차수열 b_n = 3n - 2
b_n = 3*n - 2

# 일반항 a_n (n >= 2)
a_n = -6*(3*n - 2) / (n * (n + 1))

# a_n * b_n 계산
product = a_n * b_n
product_simplified = simplify(product)

# 극한 계산
result = limit(product_simplified, n, oo)

# 검증: n=2일 때 a_2 = -4 확인
a_2_check = -6*(3*2 - 2) / (2 * 3)
if a_2_check == -4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')