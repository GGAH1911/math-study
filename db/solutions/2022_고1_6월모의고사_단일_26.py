import sympy as sp

# 주어진 방정식: x^4 - (2a-9)x^2 + 4 = 0
# a = 7일 때
a = 7
x = sp.Symbol('x')
eq = x**4 - (2*a - 9)*x**2 + 4

# 근 구하기
roots = sp.solve(eq, x)
roots = sorted([float(r) for r in roots])

alpha, beta, gamma, delta = roots

# 조건 검증
sum_sq = alpha**2 + beta**2
print(f'alpha={alpha}, beta={beta}, gamma={gamma}, delta={delta}')
print(f'alpha^2 + beta^2 = {sum_sq}')

if abs(sum_sq - 5) < 1e-10 and abs(eq.subs(x, alpha)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')