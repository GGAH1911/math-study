from sympy import symbols, solve, simplify
a = symbols('a', real=True, positive=True)
f_a = a**2 - 3*a + 3
g_a = 2*a**2 - 4*a

# Case 1: 0 < a < 2
case1_sum = f_a + (4*a - 2*a**2)
case1_cond = -a**2 + a + 3 - 3

# Case 2: a >= 2
case2_sum = f_a + g_a
case2_cond = 3*a**2 - 7*a + 3 - 3

# Verify boundary points
a_min, a_max = 1, simplify(7/3)
sum_result = a_min + a_max

# Check a=1
val_1 = (-1 + 1 + 3)
# Check a=7/3
val_73 = 3*(49/9) - 7*(7/3) + 3

if abs(val_1 - 3) < 1e-9 and abs(val_73 - 3) < 1e-9 and abs(sum_result - 10/3) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')