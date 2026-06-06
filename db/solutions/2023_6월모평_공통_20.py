import sympy as sp
x = sp.Symbol('x')
f = 2*x**2 - 12*x + 13

# 조건 검증
f0 = f.subs(x, 0)
f1 = f.subs(x, 1)
f2 = f.subs(x, 2)
f4 = f.subs(x, 4)
f5 = f.subs(x, 5)

# g'(1) = 0 확인: |f(2)| = |f(1)|
cond1 = abs(f2) == abs(f1)
# g'(4) = 0 확인: |f(5)| = |f(4)|
cond2 = abs(f5) == abs(f4)
# 최고차 계수 확인
coeff_check = sp.Poly(f, x).LC() == 2

if cond1 and cond2 and coeff_check and f0 == 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')