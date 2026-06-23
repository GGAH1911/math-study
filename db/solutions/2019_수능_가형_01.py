import sympy as sp
a = sp.Matrix([1, -2])
b = sp.Matrix([-1, 4])
result = a + 2*b
total = sum(result)
print('VERIFY_PASS' if total == 5 else 'VERIFY_FAIL')