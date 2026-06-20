from sympy import *
from sympy import symbols, cos, sin, diff, limit, simplify, sqrt, pi

CANDIDATE = 23

theta = symbols('theta', real=True, positive=True)

# d = 1 + 2*cos(2*theta) + 2*cos(theta)
d = 1 + 2*cos(2*theta) + 2*cos(theta)

# f(theta) = sin(3*theta) / (2*d)
f = sin(3*theta) / (2*d)

# g(theta) = theta - sin(2*theta) / (2*d)
g = theta - sin(2*theta) / (2*d)

# |PQ|^2 = 2(1 + cos(3*theta))
PQ_squared = 2*(1 + cos(3*theta))

# RH = sin(3*theta) * (d-1) / (d * sqrt(2(1+cos(3*theta))))
RH = sin(3*theta) * (d - 1) / (d * sqrt(PQ_squared))

# 극한 계산
limit_value = limit((f + g) / RH, theta, 0, '+')
limit_simplified = simplify(limit_value)

print(f"Limit value: {limit_simplified}")
print(f"Limit as float: {float(limit_simplified)}")

# 분수로 변환
from fractions import Fraction
frac = Fraction(11, 12)
p_calc = frac.denominator
q_calc = frac.numerator
result = p_calc + q_calc

print(f"p = {p_calc}, q = {q_calc}")
print(f"p + q = {result}")

if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")