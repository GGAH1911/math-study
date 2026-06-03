import sympy as sp
a = 10
ex = 1/2 + 2*a/5
ex2 = 1/2 + 2*a**2/5
var = ex2 - ex**2
sigma = sp.sqrt(var)
result = ex2 + ex
print('VERIFY_PASS' if abs(sigma - ex) < 1e-10 and abs(result - 45) < 1e-10 else 'VERIFY_FAIL')