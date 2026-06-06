import sympy as sp
a = 1
b = 3
f = lambda x: a*x - 3*a
g = lambda x: x**2 + 2*x + b

f2 = f(2)
f3 = f(3)
result1 = g(f2) == 2
result2 = g(f3) == 3

if result1 and result2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')