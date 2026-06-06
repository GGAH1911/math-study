from fractions import Fraction

# 합의 분포
p_sum = {2: Fraction(1,9), 3: Fraction(2,9), 4: Fraction(3,9), 5: Fraction(2,9), 6: Fraction(1,9)}

# P(S2 > S1) 계산
prob_s2_greater = Fraction(0)
for s1_val, p_s1 in p_sum.items():
    for s2_val, p_s2 in p_sum.items():
        if s2_val > s1_val:
            prob_s2_greater += p_s1 * p_s2

# P(S2=5 and S2>S1) 계산
prob_s2_5_and_greater = Fraction(0)
for s1_val, p_s1 in p_sum.items():
    if s1_val < 5:
        prob_s2_5_and_greater += p_s1 * p_sum[5]

# 조건부 확률
prob_cond = prob_s2_5_and_greater / prob_s2_greater

print(f'P(S2>S1) = {prob_s2_greater}')
print(f'P(S2=5|S2>S1) = {prob_cond}')

# p=31, q=12 검증
p, q = 31, 12
if prob_cond == Fraction(q, p) and Fraction(p, q) == prob_s2_greater:
    print('VERIFY_PASS')
else:
    # 다시 검증: q=12, p=31 (순서 변경)
    if prob_cond == Fraction(q, p):
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: {prob_cond} != {Fraction(q,p)}')