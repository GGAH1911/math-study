import sympy as sp

# f(m) = 2^(m(m+1)), g(m) = 2^(2(m+1))
m = sp.Symbol('m')
f_m = 2**(m * (m + 1))
g_m = 2**(2 * (m + 1))

# Evaluate at m=3 and m=7
f_3 = f_m.subs(m, 3)  # 2^12
g_7 = g_m.subs(m, 7)  # 2^16

ratio = g_7 / f_3
ratio_simplified = sp.simplify(ratio)

if ratio_simplified == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')