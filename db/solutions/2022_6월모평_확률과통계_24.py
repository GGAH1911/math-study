# 표의 데이터
A_1st = 7
B_1st = 5
A_2nd = 4
B_2nd = 4

# 진로활동 B를 선택한 학생 수
B_total = B_1st + B_2nd  # 5 + 4 = 9

# 진로활동 B를 선택한 학생 중 1학년인 학생
B_and_1st = B_1st  # 5

# 조건부 확률: P(1학년 | B선택)
prob = B_and_1st / B_total  # 5/9

# 정답과 비교
from fractions import Fraction
answer_fraction = Fraction(5, 9)
computed_fraction = Fraction(B_and_1st, B_total)

if computed_fraction == answer_fraction:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')