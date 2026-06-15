from fractions import Fraction

# 2020 6월모평 가형 17 (= 나형 19 와 동일 문제): 카드 1~8, 사건 A_k 독립. p×q×r?  (보기 ④=3/4)
CANDIDATE = Fraction(3, 4)
p = Fraction(4, 8)                       # (가) P(A_k)=k/8, k=4
def PAmn(m, n):
    return Fraction(m * (n - 1), 56)     # (나) P(A_m∩A_n)=m(n-1)/56
q = PAmn(3, 5)                           # m=3,n=5
r = sum(1 for m in range(1, 9) for n in range(m + 1, 9)
        if PAmn(m, n) == Fraction(m, 8) * Fraction(n, 8))   # (다) 독립쌍 개수 = 7
print('VERIFY_PASS' if p * q * r == CANDIDATE else 'VERIFY_FAIL')
