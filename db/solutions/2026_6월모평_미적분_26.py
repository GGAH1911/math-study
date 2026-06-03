import sympy as sp

x = sp.Symbol('x')
f_expr = sp.exp(3*x) - 3*sp.exp(2*x) + 4*sp.exp(x)
f_prime = sp.diff(f_expr, x)

# g(a) = ln2 이므로 검증
x_val = sp.log(2)
a_val = f_expr.subs(x, x_val)          # a = f(ln2)
fp_val = f_prime.subs(x, x_val)        # f'(g(a)) = f'(ln2)
g_prime_a = sp.Rational(1, 1) / fp_val  # g'(a) = 1/f'(g(a))
result = a_val + fp_val                 # a + f'(g(a))

ok1 = sp.simplify(g_prime_a - sp.Rational(1, 8)) == 0  # g'(a) == 1/8
ok2 = sp.simplify(result - 12) == 0                    # answer == 12

if ok1 and ok2:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: g_prime_a={g_prime_a}, result={result}')
