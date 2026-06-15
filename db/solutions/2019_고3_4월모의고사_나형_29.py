"""2019 고3 4월모의고사 나형 29번 — 파라미터 솔버 (수동 작성).
문제: 자연수 a,b,c 가 (가) 모두 짝수 (나) a×b×c=10^5 일 때 순서쌍 (a,b,c) 개수. (답 126)
구조: 10^5=2^5·5^5. a,b,c=2^{xi}5^{yi}. 짝수 ⇒ xi≥1. Σxi=5(각≥1)→C(4,2)=6, Σyi=5(각≥0)→C(7,2)=21.
      6×21=126.
검증: 닫힌식(별-막대) 과 전수(약수 3중) 두 경로 일치로 자가검증.
재생산: N(=곱) 파라미터화.
"""
import sympy as sp
from math import comb


def count_formula(N):
    f = sp.factorint(N)
    if 2 not in f:
        return 0                                   # 짝수 3개면 곱은 2^≥3 필요
    total = 1
    for p, e in f.items():
        total *= comb(e - 1, 2) if p == 2 else comb(e + 2, 2)  # 2: 각≥1, 그외: 각≥0, 3분배
    return total


def count_brute(N):
    divs = [d for d in range(1, N + 1) if N % d == 0]
    c = 0
    for a in divs:
        if a % 2 or N % a:
            continue
        Na = N // a
        for b in divs:
            if b % 2 or Na % b:
                continue
            if (Na // b) % 2 == 0:
                c += 1
    return c


N = 10 ** 5
CANDIDATE = 126
assert count_formula(N) == CANDIDATE == count_brute(N), (count_formula(N), count_brute(N))
print('VERIFY_PASS')
