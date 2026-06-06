from itertools import product

# 주사위 두 번 던지는 모든 경우
all_cases = list(product(range(1, 7), repeat=2))
print(f'전체 경우의 수: {len(all_cases)}')

# 첫 번째 < 두 번째인 경우
favorable = [case for case in all_cases if case[0] < case[1]]
print(f'유리한 경우의 수: {len(favorable)}')

# 확률
prob = len(favorable) / len(all_cases)
print(f'확률: {prob}')
print(f'분수: {len(favorable)}/{len(all_cases)}')

# 답이 5/12인지 확인
from fractions import Fraction
result_fraction = Fraction(len(favorable), len(all_cases))
expected_fraction = Fraction(5, 12)

if result_fraction == expected_fraction:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')