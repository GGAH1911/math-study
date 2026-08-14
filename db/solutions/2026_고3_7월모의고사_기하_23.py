import sympy as sp

a = sp.Matrix([3, 1])
b = sp.Matrix([-2, 1])
s = a + b
total = sum(s)

if total == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
