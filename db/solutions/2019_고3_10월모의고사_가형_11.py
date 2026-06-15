import sympy as sp
p = sp.Symbol('p', positive=True)
x1 = 3
y1_sq = 12*p
OP_sq = 9 + y1_sq
PF_sq = (3-p)**2 + y1_sq
eq = sp.Eq(OP_sq, PF_sq)
p_val = sp.solve(eq, p)
p_val = [x for x in p_val if x > 0][0]
PF_length = sp.sqrt((3-p_val)**2 + 12*p_val)
result = float(PF_length)
if abs(result - 9.0) < 1e-9 and float(p_val) == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')