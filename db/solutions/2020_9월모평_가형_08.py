import sympy as sp
x, h = sp.symbols('x h', real=True, positive=True)
e_val = sp.E

# 함수 정의
f = sp.ln(x) / x**2

# f(e+h)와 f(e-2h) 정의
f_e_plus_h = f.subs(x, e_val + h)
f_e_minus_2h = f.subs(x, e_val - 2*h)

# 극한 계산
limit_expr = (f_e_plus_h - f_e_minus_2h) / h
limit_value = sp.limit(limit_expr, h, 0)

# f'(x) 계산
f_prime = sp.diff(f, x)
f_prime_e = f_prime.subs(x, e_val)

# 검증
expected = -3 / e_val**3

if sp.simplify(limit_value - expected) == 0 and sp.simplify(3*f_prime_e - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')