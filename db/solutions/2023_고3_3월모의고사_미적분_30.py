import sympy as sp
from sympy import limit, oo, Symbol, Piecewise, Abs

x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

# Define f(x)
def f(x_val):
    if abs(x_val) < 1:
        return -x_val
    elif abs(x_val) == 1:
        return 0
    else:
        return x_val

# Check key points
test_points = {-8: 8, -6: 6, -4: 4, -2: 2, -1: 0, 0: 0, 1: 0, 3: 0, 5: 0, 7: 0, 9: 0}
range_values = set()

for x_test in [-9.5, -8, -7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, 
                1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]:
    abs_x = abs(x_test)
    for k in range(1, 6):
        if 2*k - 2 <= abs_x < 2*k:
            g_val = (2*k - 1) * f(x_test / (2*k - 1))
            if 0 < g_val < 10:
                range_values.add(round(g_val, 6))
            break

# Check integer values 1-9
missing = []
for t in range(1, 10):
    found = False
    for test_x in [i*0.01 for i in range(-1000, 1000)]:
        abs_x = abs(test_x)
        for k in range(1, 6):
            if 2*k - 2 <= abs_x < 2*k:
                g_val = (2*k - 1) * f(test_x / (2*k - 1))
                if abs(g_val - t) < 0.001 and 0 < t < 10:
                    found = True
                break
        if found: break
    if not found:
        missing.append(t)

if set(missing) == {1, 3, 5, 7, 9} and sum(missing) == 25:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')