from sympy import symbols, simplify, Rational

# 이항분포 B(n, p)의 기댓값 E(X) = n*p
n = 45
p = Rational(1, 3)
expected_value = n * p

# 주어진 조건 E(X) = 15인지 확인
if expected_value == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')