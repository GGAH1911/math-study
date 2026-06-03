from sympy import *
x = symbols('x')
a = 3
f = x*(x-a)*(x-a-1)
# Verify OQ
OQ = sqrt((a+2)**2 + (2*(a+2))**2)
assert OQ == 5*sqrt(5), f'OQ={OQ}'
# Verify roots
assert f.subs(x,0)==0 and f.subs(x,a)==0 and f.subs(x,a+1)==0
# Verify intersections with y=2x
pts = sorted(solve(f-2*x, x))
assert pts == [0,2,5], f'intersections={pts}'
# Area A
A = integrate(2*x,(x,0,2)) + integrate(f,(x,2,3))
# Area B (f<0 on (3,4))
B = -integrate(f,(x,3,4))
result = A - B
if result == Rational(16,3):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: A-B={result}')