from fractions import Fraction

# 2020 6월모평 나형 19 (그림=8칸 일렬, 계산엔 무관): p×q×r?  (보기 ④=3/4)
# 카드 1~8 을 8칸에 임의 배치. A_k = k번째 칸의 수 <= k.
CANDIDATE = Fraction(3, 4)
# (가) P(A_k) = k/8 → k=4 대입 = p
p = Fraction(4, 8)
# (나) P(A_m∩A_n) = m(n-1)/56 → m=3,n=5 대입 = q
def PAmn(m, n):
    return Fraction(m * (n - 1), 56)
q = PAmn(3, 5)
# (다) 독립: P(A_m∩A_n)=P(A_m)P(A_n) ⟺ m(n-1)/56 = (m/8)(n/8). 만족하는 (m,n) 개수 = r
r = sum(1 for m in range(1, 9) for n in range(m + 1, 9)
        if PAmn(m, n) == Fraction(m, 8) * Fraction(n, 8))
val = p * q * r
print('VERIFY_PASS' if val == CANDIDATE else 'VERIFY_FAIL')
