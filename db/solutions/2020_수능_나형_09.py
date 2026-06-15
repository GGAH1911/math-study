from sympy import Rational, nsimplify

# 표의 값 (이미지 그대로)
male_culture, male_eco = 40, 60      # 남학생: 문화체험, 생태연구
female_culture, female_eco = 50, 50  # 여학생: 문화체험, 생태연구

total_eco = male_eco + female_eco            # 생태연구 선택 전체 = 110
P = Rational(female_eco, total_eco)          # 생태연구 중 여학생 = 50/110

CANDIDATE = Rational(5, 11)

# 합계 검증
assert male_culture + male_eco == 100
assert female_culture + female_eco == 100
assert male_culture + female_culture == 90
assert total_eco == 110
assert (male_culture+male_eco+female_culture+female_eco) == 200

if P == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')