from sympy import symbols, sqrt, simplify, solve

# 답: 주축의 길이 = 32
answer_length = 32
a = answer_length / 2  # 주축의 반길이
k = a**2  # 쌍곡선에서 a^2 = k

# 쌍곡선 매개변수
b_squared = 64
b = sqrt(b_squared)

# 점근선의 기울기: b/a
asymptote_slope = float(b / a)
expected_slope = 0.5

# 검증: 계산된 점근선이 주어진 y = (1/2)x와 일치하는가
if abs(asymptote_slope - expected_slope) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')