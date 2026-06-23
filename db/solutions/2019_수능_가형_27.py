from fractions import Fraction as F
# 파라미터화: 주사위 N면, 사건 A=홀수, B=m의 약수의 눈. A⊥B 인 m의 합.
N = 6
A = {x for x in range(1, N+1) if x % 2 == 1}   # 홀수
CANDIDATE = 8
PA = F(len(A), N)
good = []
for m in range(1, N+1):
    B = {d for d in range(1, N+1) if m % d == 0}   # m의 약수 중 N 이하
    if F(len(A & B), N) == PA * F(len(B), N):       # 독립: P(A∩B)=P(A)P(B)
        good.append(m)
print('VERIFY_PASS' if sum(good) == CANDIDATE else 'VERIFY_FAIL')
