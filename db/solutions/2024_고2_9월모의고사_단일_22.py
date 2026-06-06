from sympy import symbols, solve, Eq, powsimp
x = symbols('x', real=True)
# 원래 방정식: 3^(2x-1) = 27
eq = Eq(3**(2*x - 1), 27)
sol = solve(eq, x)
if sol and sol[0] == 2:
    verify = 3**(2*2 - 1)
    if verify == 27:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')