# 구간별 함수 정의
def f(x):
    if 0 < x < 1:
        return 1.0
    elif 1 <= x < 3:
        return 0.5 * x + 0.5
    elif 3 <= x < 4:
        return x - 2.0
    return None

# 극한값 계산
lim_1_plus = 0.5 * 1 + 0.5  # x->1+, f(x) = (1/2)x + 1/2
lim_3_minus = 0.5 * 3 + 0.5  # x->3-, f(x) = (1/2)x + 1/2

result = lim_1_plus - lim_3_minus

assert lim_1_plus == 1.0, f'lim_1_plus = {lim_1_plus}, expected 1.0'
assert lim_3_minus == 2.0, f'lim_3_minus = {lim_3_minus}, expected 2.0'
assert result == -1.0, f'result = {result}, expected -1.0'

print('VERIFY_PASS')