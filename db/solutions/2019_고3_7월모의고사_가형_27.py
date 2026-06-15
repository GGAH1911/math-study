"""2019 고3 7월모의고사 가형 27번 — 파라미터 솔버 (수동).
8개 레인 중 3명이 서로 다른 번호 선택, 세 번호 중 어느 둘도 연속 아님.
비연속 3개 택 = C(8-3+1,3)=C(6,3)=20, 학생 구분 ×3! = 120. (답 120)"""
from itertools import combinations
from math import factorial
def solve(lanes=8, k=3):
    cnt = sum(1 for c in combinations(range(1,lanes+1),k)
              if all(b-a>1 for a,b in zip(sorted(c),sorted(c)[1:])))
    return cnt * factorial(k)
assert solve() == 120
print('VERIFY_PASS')
