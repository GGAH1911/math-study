from sympy import *
a = Rational(4, 3)
b = Integer(3)
x = symbols('x', real=True)
f = 3*sin(pi*x/a) + b
# 원래 조건 1: f(2) = 0
check1 = simplify(f.subs(x, 2)) == 0
# 원래 조건 2: [0,2a]에서 영점 = {2}만
# sin(pi*x/a)=-1 → x = 3a/2 + 2n*a
zeros_in_domain = []
for n_val in range(-10, 10):
    x_val = Rational(3,2)*a + 2*n_val*a
    if 0 <= x_val <= 2*a:
        zeros_in_domain.append(x_val)
check2 = (len(zeros_in_domain) == 1 and zeros_in_domain[0] == 2)
if check1 and check2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')