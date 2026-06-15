from sympy import *
theta = symbols('theta', real=True, positive=True)

# 극한값 계산
S = sqrt(2)/2 * theta**3
T = Rational(1,2) * theta**3
ratio = (S - T) / theta**3
limit_val = limit(ratio, theta, 0)
print(f'극한값: {limit_val}')
print(f'수치값: {float(limit_val)}')
print(f'(sqrt(2)-1)/2 = {float((sqrt(2)-1)/2)}')
if abs(limit_val - (sqrt(2)-1)/2) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')