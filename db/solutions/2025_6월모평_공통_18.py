import sympy as sp
a = 2
result = sum(a*k**2 - 10*k for k in range(1, 10))
if result == 120:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')