from sympy import symbols, solve, Eq
a = symbols('a', positive=True, real=True)
eq = Eq(3*a**2 - a*a - 32, 0)
solutions = solve(eq, a)
print(f'Solutions: {solutions}')
if 4 in solutions:
    val = 4
    result = 3*val**2 - val*val - 32
    print(f'Verification: 3({val})² - {val}·{val} - 32 = {result}')
    print('VERIFY_PASS' if result == 0 else 'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')