"""2019 고3 10월모의고사 가형 22번 — 파라미터 솔버 (수동).
₇H₃ = 중복조합 = C(7+3-1,3)=C(9,3)=84. (답 84)"""
from math import comb
def H(n,r): return comb(n+r-1,r)
assert H(7,3)==84
print('VERIFY_PASS')
