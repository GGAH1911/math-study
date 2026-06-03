from sympy import symbols, limit, oo, Rational

n = symbols('n', positive=True, integer=True)

# 주어진 조건을 만족하는 a_n
# lim(3*a_n - 5*n) = 2 => a_n = (5*n + 2)/3 + epsilon/3
a_n = (5*n + 2) / 3

# 조건 확인
check = limit(3*a_n - 5*n, n, oo)
assert check == 2, f'Condition failed: got {check}'

# 극한값 계산
target = limit((2*n + 1) * a_n / (4*n**2), n, oo)

if target == Rational(5, 6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')