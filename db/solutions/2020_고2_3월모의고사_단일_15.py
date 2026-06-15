from math import comb
# A에서 6개 선(AB·4cevian·AC), 횡단선 4개(BC+3평행). 삼각형 개수? (④=60)
# 삼각형 = A선 2개(C(6,2)) × 횡단선 1개(4) [A선 3개=공점, 횡단선 2개=평행 → 불가]
CANDIDATE = 60
print('VERIFY_PASS' if comb(6, 2)*4 == CANDIDATE else 'VERIFY_FAIL')
