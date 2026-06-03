import sympy as sp
x, a = sp.symbols('x a', real=True)

a_val = sp.Rational(1, 2)
inequality = sp.Rational(1, 2) * (x + 5) - x <= a_val

lhs = sp.Rational(1, 2) * (x + 5) - x
rhs = a_val
simplified = sp.simplify(lhs - rhs)

result = sp.solve(simplified <= 0, x)
if result == sp.S('4') <= x or str(result) == 'x >= 4':
    print('VERIFY_PASS')
else:
    critical_val = sp.solve(lhs - rhs, x)[0]
    if critical_val == 4:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')