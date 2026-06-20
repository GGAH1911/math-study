import sympy as sp
a1 = sp.Symbol('a1')
eq = (a1 - 6) * (a1 - 18) - 64
sols = sp.solve(eq, a1)
valid_sols = [s for s in sols if s - 21 > 0]
a1_val = valid_sols[0]
a2_val = a1_val - 3
a3_val = a1_val - 6
a7_val = a1_val - 18
a8_val = a1_val - 21
if a3_val * a7_val == 64 and a8_val > 0 and a2_val == 19:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')