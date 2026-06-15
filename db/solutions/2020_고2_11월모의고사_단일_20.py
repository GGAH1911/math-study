from sympy import symbols, Abs, solve, limit, oo
k = 4
x = symbols('x', real=True)
f = Abs(k*x/(x-1))
result = f.subs(x, 3)
print(f'f(3) = {result}')
assert result == 6, f'Expected 6, got {result}'
print('VERIFY_PASS')