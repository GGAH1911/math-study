from sympy import *

CHOICES = {
    1: Rational(1, 4),
    2: sqrt(2) / 4,
    3: Rational(1, 2),
    4: sqrt(2) / 2,
    5: 1
}

CANDIDATE = 3

t = symbols('t', real=True, positive=True)

# 문제 조건
# P(t, t*sin(t))를 중심으로 하고 y축에 접하는 원
# 반지름 = t (P의 x좌표)
# 원의 방정식: (x - t)^2 + (y - t*sin(t))^2 = t^2
#
# 선분 OP의 방정식: y = x*sin(t) (O는 원점)
#
# 원의 방정식에 선분 OP를 대입:
# (x - t)^2 + (x*sin(t) - t*sin(t))^2 = t^2
# (x - t)^2 + sin^2(t)*(x - t)^2 = t^2
# (x - t)^2 * (1 + sin^2(t)) = t^2
#
# (x - t)^2 = t^2 / (1 + sin^2(t))
# x - t = ± t / sqrt(1 + sin^2(t))
#
# Q는 원점 근처에 있으므로 음의 해를 취함:
# f(t) = t - t/sqrt(1 + sin^2(t))
#      = t * (1 - 1/sqrt(1 + sin^2(t)))

f_t = t * (1 - 1 / sqrt(1 + sin(t)**2))

# 극한값 계산: lim_{t→0+} f(t)/t^3
limit_value = limit(f_t / t**3, t, 0, '+')

# CANDIDATE에 해당하는 값
expected_value = CHOICES[CANDIDATE]

# 검증
if simplify(limit_value - expected_value) == 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")