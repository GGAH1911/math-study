import math

a_val = 5
b_val = 7
k_val = -39

# 1. k < -1
cond1 = k_val < -1

# 2. 1 < a < b
cond2 = 1 < a_val < b_val

# 3. A(a,b) on curve x^2 - xy + y^2 + k = 0
cond3 = (a_val**2 - a_val*b_val + b_val**2 + k_val == 0)

# 4. B(b,a) on curve
cond4 = (b_val**2 - b_val*a_val + a_val**2 + k_val == 0)

# 5. AB = 2*sqrt(2)
AB = math.sqrt((b_val - a_val)**2 + (a_val - b_val)**2)
cond5 = abs(AB - 2*math.sqrt(2)) < 1e-10

# 6. tan(theta) = 4/3
# dy/dx = (y - 2x)/(2y - x)
mA = (b_val - 2*a_val) / (2*b_val - a_val)
mB = (a_val - 2*b_val) / (2*a_val - b_val)
tan_theta = abs((mA - mB) / (1 + mA * mB))
cond6 = abs(tan_theta - 4/3) < 1e-10

# 7. k + a + b = -27
cond7 = (k_val + a_val + b_val == -27)

if all([cond1, cond2, cond3, cond4, cond5, cond6, cond7]):
    print('VERIFY_PASS')
else:
    failed = [i+1 for i, c in enumerate([cond1,cond2,cond3,cond4,cond5,cond6,cond7]) if not c]
    print(f'VERIFY_FAIL: conditions {failed} failed')
