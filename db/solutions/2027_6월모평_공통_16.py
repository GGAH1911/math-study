import math
t_val = 6.0
for _ in range(15):
    f = t_val**3 - 6*t_val**2 - 1
    df = 3*t_val**2 - 12*t_val
    t_val = t_val - f / df
x_val = math.log(t_val) / math.log(3)
lhs = 3**x_val - 6
rhs = (1/9)**x_val
if abs(lhs - rhs) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')