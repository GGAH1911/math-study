import sympy as sp
a = sp.Symbol('a', real=True)
x = sp.Symbol('x', real=True)

# 경우 1: a = 11/3
a1 = sp.Rational(11, 3)
P1 = 1 - a1 + 7 - a1
P0_1 = 7 - a1
val1 = sp.sqrt(P1) + sp.sqrt(-P1) - sp.sqrt(P0_1 - 4)
val1_simplified = sp.simplify(val1)

P_minus4_1 = 16 + 4*a1 + 7 - a1

# 경우 2: a = 5
a2 = 5
P1_2 = 8 - 2*a2
P0_2 = 7 - a2
val2 = sp.sqrt(P1_2) + sp.sqrt(-P1_2) - sp.sqrt(P0_2 - 4)
val2_simplified = sp.simplify(val2)

P_minus4_2 = 16 + 4*a2 + 7 - a2

total = P_minus4_1 + P_minus4_2

if total == 72:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')