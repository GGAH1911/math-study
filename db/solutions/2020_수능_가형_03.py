from sympy import symbols, solve, sqrt
a = symbols('a', real=True)
PA_sq = 4 + a**2 + 1
PB_sq = 9 + (a-2)**2
eq = PA_sq - PB_sq
sol = solve(eq, a)
print(f'VERIFY_PASS' if sol[0] == 2 else 'VERIFY_FAIL')