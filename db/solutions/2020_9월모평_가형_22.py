from sympy import symbols, solve, Rational

# 2020 9월모평 가형 22: X ~ B(n, 1/4), V(X)=6. n?
CANDIDATE = 32
n = symbols('n', positive=True)
p = Rational(1, 4)
sol = solve(n * p * (1 - p) - 6, n)[0]   # 이항분포 분산 np(1-p)=6
print('VERIFY_PASS' if sol == CANDIDATE else 'VERIFY_FAIL')
