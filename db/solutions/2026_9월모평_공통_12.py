import sympy as sp

a_val = sp.Rational(1,4)  # exponent: a = 2^(1/4)
t_val = sp.Integer(4)

a = 2**sp.Rational(1,4)
t = sp.Integer(4)

A = (t, a**t)
B = (2*t, a**(2*t))
C = (2*t, sp.Integer(0))

AB2 = (B[0]-A[0])**2 + (B[1]-A[1])**2
AC2 = (C[0]-A[0])**2 + (C[1]-A[1])**2

cond1 = sp.simplify(AB2 - AC2) == 0

base = B[1] - C[1]  # |BC|
height = C[0] - A[0]  # horizontal distance
area = sp.Rational(1,2) * base * height
cond2 = sp.simplify(area - 8) == 0

result = a * t
expected = 2**sp.Rational(9,4)
cond3 = sp.simplify(result - expected) == 0

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: AB2==AC2={cond1}, area==8={cond2}, result==2^(9/4)={cond3}')
