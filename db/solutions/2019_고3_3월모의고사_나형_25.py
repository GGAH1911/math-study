"""2019 고3 3월모의고사 나형 25번 — 파라미터 솔버 (수동 작성).
문제: 첫째항 4, a_{n+2}=a_{n+1}+a_n. a_4=34 일 때 a_2. (답 15)
구조: a_3=a_2+a_1, a_4=a_3+a_2=2a_2+a_1 → a_2=(a_4-a_1)/2=(34-4)/2=15.
재생산: (a_1, a_4) 파라미터화 (피보나치형 점화식).
"""
import sympy as sp


def solve(a1, a4):
    a2 = sp.symbols('a2')
    a3 = a2 + a1
    return sp.solve(sp.Eq(a3 + a2, a4), a2)[0]   # a4 = a3 + a2


CANDIDATE = 15
assert solve(4, 34) == CANDIDATE, solve(4, 34)
print('VERIFY_PASS')
