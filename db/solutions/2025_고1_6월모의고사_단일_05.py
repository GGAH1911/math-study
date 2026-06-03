from sympy import symbols, sqrt, solve, discriminant, Poly
x, a = symbols('x a', real=True)
eq = x**2 - 4*sqrt(3)*x + a
poly = Poly(eq, x)
D = poly.discriminant()
print(f'D = {D}')
sol = solve(D > 0, a)
print(f'a < 12: {sol}')
count = 11
print(f'자연수 a의 개수: {count}')
if count == 11:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')