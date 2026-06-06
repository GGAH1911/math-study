from itertools import combinations
from math import gcd

# 1부터 12까지의 공 중 3개를 선택
all_cases = list(combinations(range(1, 13), 3))

# 각 경우에서 a, b, c를 정렬
cases_abc = [(min(x), sorted(x)[1], max(x)) for x in all_cases]

# b - a >= 5인 경우
case_condition = [abc for abc in cases_abc if abc[1] - abc[0] >= 5]
count_condition = len(case_condition)

# b - a >= 5이고 c - a >= 10인 경우
case_both = [abc for abc in cases_abc if abc[1] - abc[0] >= 5 and abc[2] - abc[0] >= 10]
count_both = len(case_both)

# 조건부 확률
prob_numerator = count_both
prob_denominator = count_condition

# 기약분수로 만들기
g = gcd(prob_numerator, prob_denominator)
q = prob_numerator // g
p = prob_denominator // g

# 검증
if q == 2 and p == 7 and p + q == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')