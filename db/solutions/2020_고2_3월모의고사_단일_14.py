from sympy import symbols, solve, simplify
a = symbols('a')
x = symbols('x')
f = lambda t, a_val: t**2 - 2*t + a_val
f_comp = lambda t, a_val: f(f(t, a_val), a_val)
eq = f_comp(2, a) - f_comp(4, a)
a_val = solve(eq, a)[0]
assert a_val == -3
result = f(6, a_val)
assert result == 21
print('VERIFY_PASS')