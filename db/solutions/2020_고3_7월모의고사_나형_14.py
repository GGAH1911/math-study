import sympy as sp

x = sp.Symbol('x')

# 짝함수 부분: f_e(x) = (3/2)x^2 - 1
f_e = sp.Rational(3, 2) * x**2 - 1

# 조건 (가) 검증: lim_{x->inf} (f_e(x) + f_e(-x)) / x^2 = 3
numerator = f_e + f_e.subs(x, -x)
limit_cond = sp.limit(numerator / x**2, x, sp.oo)

# 조건 (나) 검증: f_e(0) = -1
f_e_zero = f_e.subs(x, 0)

# 적분값 계산
integral_val = sp.integrate(f_e, (x, -3, 3))

# 모든 조건이 만족되는지 확인
if limit_cond == 3 and f_e_zero == -1 and integral_val == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')