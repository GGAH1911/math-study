from sympy import pi, Rational, simplify

# 주어진 조건
theta = Rational(3, 4) * pi  # 중심각
L_given = Rational(2, 3) * pi  # 호의 길이

# 구한 답
r = Rational(8, 9)

# 검증: 호의 길이 공식 L = r * theta
L_calculated = r * theta

# 주어진 호의 길이와 계산된 호의 길이 비교
if simplify(L_calculated - L_given) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')