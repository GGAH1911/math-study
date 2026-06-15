import sympy as sp
a = sp.Matrix([3, 1])
b = sp.Matrix([-2, 4])
result = a + sp.Rational(1, 2) * b
total = sum(result)
print('VERIFY_PASS' if total == 5 else 'VERIFY_FAIL')