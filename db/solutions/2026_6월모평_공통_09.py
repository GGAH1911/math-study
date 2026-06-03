import sympy as sp
from sympy import symbols, integrate, solve

a = symbols('a', real=True)
x = symbols('x', real=True)

# f(x) = x^2 + ax
f = x**2 + a*x

# 좌변: ∫(x+1)f(x)dx from -3 to 3
lhs = integrate((x + 1) * f, (x, -3, 3))

# 우변: 36 + ∫f(x)dx from -3 to 3
rhs = 36 + integrate(f, (x, -3, 3))

# 방정식: lhs = rhs
eq = sp.Eq(lhs, rhs)
sol = solve(eq, a)

if sol and sol[0] == 2:
    # a = 2로 검증
    a_val = 2
    f_val = x**2 + a_val*x
    lhs_check = integrate((x + 1) * f_val, (x, -3, 3))
    rhs_check = 36 + integrate(f_val, (x, -3, 3))
    if lhs_check == rhs_check:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')