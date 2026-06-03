from sympy import symbols, binomial, expand, Rational, solve

x, a = symbols('x a')

expr = (x**2 + a/x)**5
expanded = expand(expr)

# coefficient of x^(-2)
coeff_neg2 = expanded.coeff(x, -2)
# coefficient of x^1
coeff_pos1 = expanded.coeff(x, 1)

a_val = 2  # our answer

c1 = coeff_neg2.subs(a, a_val)
c2 = coeff_pos1.subs(a, a_val)

if c1 == c2 and c1 != 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: coeff(1/x^2)={c1}, coeff(x)={c2}')
