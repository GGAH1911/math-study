"""2019 고3 3월모의고사 가형 29번 — 파라미터 솔버 (수동 작성).
문제: 0,1,2,3 적힌 공에서 복원추출 3회, 차례로 a,b,c. bc/a 가 정수가 되는
      모든 순서쌍 (a,b,c) 의 개수. (답 40)
구조: a=0 이면 bc/a 정의 안 됨 → 제외(a∈{1,2,3}). 나머지는 a | bc 열거.
      a=1:16, a=2(bc 짝수):12, a=3(3|bc):12 → 40.
재생산: 공 숫자집합(digits) 파라미터화 → 같은 유형 무한 생성.
"""
from itertools import product


def count(digits):
    return sum(1 for a, b, c in product(digits, repeat=3)
               if a != 0 and (b * c) % a == 0)


CANDIDATE = 40
assert count(range(4)) == CANDIDATE, count(range(4))
print('VERIFY_PASS')
