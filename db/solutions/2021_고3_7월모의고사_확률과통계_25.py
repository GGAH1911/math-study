from fractions import Fraction

# 확률분포 정의
a = Fraction(1, 3)
prob_dist = {
    -1: a,
    0: Fraction(1, 2) * a,
    1: Fraction(3, 2) * a
}

# 확률의 합 검증
prob_sum = sum(prob_dist.values())
assert prob_sum == 1, f'확률의 합이 1이 아님: {prob_sum}'

# 기댓값 계산
E_X = sum(x * prob for x, prob in prob_dist.items())

# 답이 1/6인지 확인
if E_X == Fraction(1, 6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')