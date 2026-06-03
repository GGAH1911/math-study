import sympy as sp
from sympy import symbols, Eq, solve

# 검증: a = 5, b = 14
a = 5
b = 14

# 조건 1: 점근선이 y = 5
# y = 3^x + a 에서 x → -∞일 때 y → a
asymptote = a
if asymptote == 5:
    condition1 = True
else:
    condition1 = False

# 조건 2: 점 (2, b)를 지남
# y = 3^x + a에 x=2, y=b를 대입
y_at_x2 = 3**2 + a
if y_at_x2 == b:
    condition2 = True
else:
    condition2 = False

if condition1 and condition2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')