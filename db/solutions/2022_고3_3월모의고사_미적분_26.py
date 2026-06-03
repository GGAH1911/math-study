import sympy as sp
from sympy import symbols, limit, oo, Rational

n = symbols('n', positive=True, integer=True)
a1 = symbols('a_1', real=True)

# 주어진 조건에서 유도한 b_n
b_n = 1 / (2*n - 1)

# 수열 a_n: a_{n+1} - a_n = 3이므로 등차수열
a_n = a1 + 3*(n - 1)

# 검증: sum(1/b_k, k=1..n) = n^2 확인
# b_k = 1/(2k-1)이므로 sum(1/b_k) = sum(2k-1)
sum_result = sp.summation(2*sp.Symbol('k') - 1, (sp.Symbol('k'), 1, n))
if sum_result == n**2:
    verification1 = True
else:
    verification1 = False

# a_n * b_n의 극한 계산
product = a_n * b_n
limit_value = limit(product, n, oo)

if limit_value == Rational(3, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')