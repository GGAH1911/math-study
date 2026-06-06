from fractions import Fraction
from itertools import product

# 5번 시행에서 모든 경우의 수
count_multiple_of_6 = 0
total_cases = 0

for draws in product([1,2,3], repeat=5):
    # 5개 수의 곱
    prod = 1
    for num in draws:
        prod *= num
    
    total_cases += 1
    if prod % 6 == 0:
        count_multiple_of_6 += 1

# 확률
prob = Fraction(count_multiple_of_6, total_cases)
q_val = prob.numerator
p_val = prob.denominator

# 검증
if prob == Fraction(20, 27) and p_val + q_val == 47:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: prob={prob}, p+q={p_val + q_val}')