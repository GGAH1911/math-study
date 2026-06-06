import sympy as sp
from sympy import sin, cos, tan, limit, symbols, pi

theta = symbols('theta', positive=True, real=True)

# f(theta) = 2*tan(theta) - theta/2
f_theta = 2*tan(theta) - theta/2

# g(theta) = theta
g_theta = theta

# Calculate the limit
ratio = f_theta / g_theta
lim_result = limit(ratio, theta, 0, '+')

print(f'lim(f/g) = {lim_result}')
print(f'40 * lim(f/g) = {40 * lim_result}')

# Verify the answer
answer = 40 * lim_result
if answer == 60:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')