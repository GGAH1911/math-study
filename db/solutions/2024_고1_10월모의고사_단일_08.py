import sympy as sp
import numpy as np

# z 정의
a, b = 2, 2*sp.sqrt(2)
z = a + b*sp.I
z_conj = a - b*sp.I

# 조건 확인: z - 3*z_conj = z^2
lhs = z - 3*z_conj
rhs = z**2

print('z - 3z_bar =', lhs)
print('z^2 =', rhs)
print('Equal:', sp.simplify(lhs - rhs) == 0)

# z^2의 절댓값
z_squared_abs = sp.Abs(z**2)
print('|z^2| =', z_squared_abs)
print('|z^2|^2 =', (sp.Abs(z))**2 * (sp.Abs(z))**2)
print('|z^2| (numeric) =', float(z_squared_abs))

if float(z_squared_abs) == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')