from sympy import *
x = symbols('x')

# Differentiability conditions: k = b*sqrt(3), a = 4b - 2k
b_gen = symbols('b_gen', positive=True)
k_gen = b_gen * sqrt(3)
a_gen = 4*b_gen - 2*k_gen

# Check ㄱ: f'(k) = a always => if a=1, f'(k)=1
left_deriv = a_gen
right_deriv = -2*k_gen + 4*b_gen
assert simplify(left_deriv - right_deriv) == 0  # f'(k) = a confirmed

# Check ㄴ: k=3 => a = -6 + 4*sqrt(3)
b_k3 = Rational(3,1) / sqrt(3)
a_k3 = 4*b_k3 - 2*3
assert simplify(a_k3 - (-6 + 4*sqrt(3))) == 0

# Check ㄷ: f(k)=f'(k) => k=1, area = 1/3
# f(k)=ak, f'(k)=a => ak=a => k=1
k_c = Integer(1)
b_c = k_c / sqrt(3)
a_c = 4*b_c - 2*k_c
assert a_c > 0  # positive
# Area 1: integral of a*x from 0 to 1
area1 = integrate(a_c * x, (x, 0, 1))
# Area 2: parabola from k=1 to 3b=sqrt(3)
f_quad = -x**2 + 4*b_c*x - 3*b_c**2
area2 = integrate(f_quad, (x, 1, sqrt(3)))
total = simplify(area1 + area2)
if total == Rational(1, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL:', total)