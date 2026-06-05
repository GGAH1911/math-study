import sympy as sp
x, k = sp.symbols('x k')
k_val = 18
# 원래 방정식 x^2 - 6x + k = 0 의 근을 구함
roots = sp.solve(x**2 - 6*x + k_val, x)
# 두 허근이 서로 다른지 확인
if len(roots) != 2 or roots[0] == roots[1]:
    print('VERIFY_FAIL'); raise SystemExit
# 두 근이 모두 허수인지 확인 (실수부만 있는 경우 아님)
if all(sp.im(r) == 0 for r in roots):
    print('VERIFY_FAIL'); raise SystemExit
# alpha*i + beta = 0 을 만족하는 (alpha, beta) 순서쌍 존재 확인
I = sp.I
found = False
for a in roots:
    for b in roots:
        if a == b:
            continue
        if sp.simplify(a*I + b) == 0:
            found = True
print('VERIFY_PASS' if found else 'VERIFY_FAIL')
