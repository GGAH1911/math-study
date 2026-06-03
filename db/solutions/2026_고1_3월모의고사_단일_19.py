from sympy import *
g = symbols('g', positive=True)
Bx_prime = 8*g**2 / (g**2 + 16)
By_prime = 32*g / (g**2 + 16)
sol = solve(Eq(Bx_prime, 1), g)
g_val = [v for v in sol if v > 0][0]
CG = sqrt(16 + g_val**2)
CG_simplified = simplify(CG)
expected = 8*sqrt(14)/7
match = simplify(CG_simplified - expected) == 0
By_val = float(By_prime.subs(g, g_val))
if match and 0 <= By_val <= 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')