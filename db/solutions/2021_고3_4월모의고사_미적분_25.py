import sympy as sp

n = sp.Symbol('n', positive=True, integer=True)

# 조건: sum_{n=1}^{infty} (a_n/n - 2) = 5
# 이 급수가 수렴하므로 lim_{n->infty} (a_n/n - 2) = 0
# 따라서 lim_{n->infty} a_n/n = 2, 즉 a_n ~ 2n

# 극한 계산
# lim_{n->infty} (2n^2 + 3n*a_n)/(n^2 + 4)
# a_n ~ 2n을 사용
numerator = 2*n**2 + 3*n*(2*n)
denominator = n**2 + 4

limit_value = sp.limit(numerator / denominator, n, sp.oo)

expected_answer = 8

if limit_value == expected_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')