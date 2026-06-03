from sympy import symbols, solve, Poly
x, a = symbols('x a')
eq = x**2 + 4*x + a - 5
# 중근 조건: 판별식 = 0
a_val = 9
eq_substituted = eq.subs(a, a_val)
# x^2 + 4x + 4 = 0을 풀면 중근인지 확인
roots = solve(eq_substituted, x)
if len(roots) == 1 or (len(roots) == 2 and roots[0] == roots[1]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')