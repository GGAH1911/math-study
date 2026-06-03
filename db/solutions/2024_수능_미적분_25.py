from sympy import symbols, diff, integrate, ln, simplify
t, a = symbols('t a', positive=True)
f = lambda u: 4*u**2*(u+1)
# f(1)=8 조건 확인
assert f(1) == 8
# g는 f의 역함수 -> g'(f(x)) = 1/f'(x); 적분식 좌변 = f'(x)/f(x)
fp = diff(f(t), t)
integrand = fp / f(t)
lhs = integrate(integrand, (t, 1, a))
rhs = 2*ln(a) + ln(a+1) - ln(2)
if simplify(lhs - rhs) == 0 and f(2) == 48:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
