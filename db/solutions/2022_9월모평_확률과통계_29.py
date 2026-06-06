from fractions import Fraction

# V(Y) = 39/5 확인
V_X = Fraction(31, 5)
V_Y = V_X + Fraction(8, 5)
assert V_Y == Fraction(39, 5), f'V(Y) 계산 오류: {V_Y}'

# 최종 답
answer = 10 * V_Y
assert answer == 78, f'10 × V(Y) 계산 오류: {answer}'

print('VERIFY_PASS')