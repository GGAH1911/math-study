"""2020 고3 10월 학력평가 가형 10번 — itertools brute-force 검증기 (경우의 수).

문제: A, B, B, C, C, C 가 적힌 6장의 카드 중 5장을 택해 왼쪽부터 일렬로 나열할 때,
      C가 적힌 카드가 왼쪽에서 두 번째 위치에 놓이도록 나열하는 경우의 수?
      (같은 문자가 적힌 카드끼리는 구별하지 않는다.)  답: 30 (보기 ④)

직접 풀이(brute-force): permutations로 5장 나열을 전부 생성하되, 같은 문자 카드는
구별하지 않으므로 set으로 중복 제거. 그중 2번째 자리가 'C'인 것만 센다.
"""
from itertools import permutations

cards = ['A', 'B', 'B', 'C', 'C', 'C']
seen = set()
for p in permutations(cards, 5):          # 6장 중 5장 택해 일렬 나열(위치 기반 전체)
    if p[1] == 'C':                        # 왼쪽에서 두 번째가 C
        seen.add(p)                        # 같은 문자 구별 X → set 으로 중복 제거
result = len(seen)

print('VERIFY_PASS' if result == 30 else f'VERIFY_FAIL ({result})')
