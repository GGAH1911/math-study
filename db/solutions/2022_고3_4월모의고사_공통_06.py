from sympy import Rational

# 주어진 조건: sin(θ) + cos(θ) = 1/2에서
# (sin(θ) + cos(θ))^2 = 1/4
# 1 + 2sin(θ)cos(θ) = 1/4
# sin(θ)cos(θ) = -3/8

sin_theta_cos_theta = Rational(-3, 8)

# (2sin(θ) + cos(θ))(sin(θ) + 2cos(θ))
# = 2sin^2(θ) + 5sin(θ)cos(θ) + 2cos^2(θ)
# = 2(sin^2(θ) + cos^2(θ)) + 5sin(θ)cos(θ)
# = 2(1) + 5sin(θ)cos(θ)

result = 2 * 1 + 5 * sin_theta_cos_theta
expected = Rational(1, 8)

if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')