import sympy as sp
from sympy import symbols, log, solve, sqrt

a_val = sp.Rational(25, 4)
t = sp.Rational(3, 2)

# 점 A 검증
x1, y1 = t, -t + 4
assert y1 == sp.Rational(5, 2), f"y1={y1}"
assert abs(float(a_val**(x1-1) - y1)) < 1e-9, f"A: a^(x-1)={a_val**(x1-1)}, y={y1}"

# 점 B 검증  
x2, y2 = t + 2, -(t + 2) + 4
assert y2 == sp.Rational(1, 2), f"y2={y2}"
log_val = log(x2 - 1, a_val)
assert abs(float(log_val - y2)) < 1e-9, f"B: log_a(x-1)={log_val}, y={y2}"

# AB 거리 검증
AB = sqrt((x2-x1)**2 + (y2-y1)**2)
assert AB == 2*sqrt(2), f"AB={AB}, expected 2*sqrt(2)"

# 삼각형 넓이
x_A, y_A = x1, y1
x_B, y_B = x2, y2
x_C, y_C = 0, 1/a_val

area = abs((x_B - x_A)*(y_C - y_A) - (x_C - x_A)*(y_B - y_A))/2
assert area == sp.Rational(96, 25), f"area={area}, expected 96/25"

result = 50 * area
assert result == 192, f"50*S={result}"

print('VERIFY_PASS')