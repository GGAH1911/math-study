from itertools import product
import fractions

# 각 시행에서 나올 숫자와 확률
prob = {1: fractions.Fraction(1,4), 2: fractions.Fraction(1,4), 3: fractions.Fraction(1,6), 4: fractions.Fraction(1,6), 5: fractions.Fraction(1,6)}

# 3번 시행의 모든 경우의 수
total_prob_mean2 = fractions.Fraction(0)

for triple in product([1,2,3,4,5], repeat=3):
    if sum(triple) == 6:  # 평균이 2
        prob_triple = prob[triple[0]] * prob[triple[1]] * prob[triple[2]]
        total_prob_mean2 += prob_triple

# q/p 형태로 기약분수 확인
print(f'P(X_mean = 2) = {total_prob_mean2}')
print(f'분자(q) = {total_prob_mean2.numerator}')
print(f'분모(p) = {total_prob_mean2.denominator}')
print(f'p + q = {total_prob_mean2.denominator + total_prob_mean2.numerator}')

if total_prob_mean2 == fractions.Fraction(7, 64):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')