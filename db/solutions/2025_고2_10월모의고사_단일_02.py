# 미분의 정의를 역대입하여 검증
# 주어진 조건: lim_{h->0} [f(1+h) - f(1)]/(3h) = 2
# 구한 답: f'(1) = 6

# 미분의 정의에서 f'(1) = lim_{h->0} [f(1+h) - f(1)]/h 이므로
# lim_{h->0} [f(1+h) - f(1)]/(3h) = (1/3) * lim_{h->0} [f(1+h) - f(1)]/h = (1/3) * f'(1)

derivative_at_1 = 6  # 우리가 구한 답

# 주어진 극한값
given_limit = 2

# 검증: (1/3) * f'(1) = given_limit인지 확인
result = (1/3) * derivative_at_1

if abs(result - given_limit) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')