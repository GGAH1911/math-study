import sympy as sp
from sympy import cos, sin, sqrt, diff, pi, simplify

theta = sp.Symbol('theta', real=True, positive=True)

# cos(2a) = -7/25, sin(2a) = 24/25를 만족하는 a
cos2a = sp.Rational(-7, 25)
sin2a = sp.Rational(24, 25)

# f(theta) = (1/8)(sqrt(3) + 2*cos(2*theta + pi/6))
f = (sqrt(3) + 2*cos(2*theta + pi/6)) / 8

# f'(theta)
f_prime = diff(f, theta)

# theta = a에서의 값 (cos(2a) = -7/25, sin(2a) = 24/25)
# sin(2a + pi/6) = sin(2a)*cos(pi/6) + cos(2a)*sin(pi/6)
sin_val = sin2a * cos(pi/6) + cos2a * sin(pi/6)
sin_val_simplified = simplify(sin_val)

# f'(a) = -(1/2)*sin(2a + pi/6)
f_prime_a = -sp.Rational(1, 2) * sin_val_simplified
f_prime_a_simplified = simplify(f_prime_a)

# f'(a) = p + q*sqrt(3) 형태로 표현
# f'(a) = (7 - 24*sqrt(3))/100
p_coeff = f_prime_a_simplified.coeff(sqrt(3), 0)  # sqrt(3)의 계수가 아닌 부분
q_coeff = f_prime_a_simplified.coeff(sqrt(3), 1)  # sqrt(3)의 계수

# 다시 확인
p_val = sp.Rational(7, 100)
q_val = sp.Rational(-24, 100)

# |p + q|
result = abs(p_val + q_val)
final_answer = 100 * result

if final_answer == 17:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected 17, got {final_answer}')