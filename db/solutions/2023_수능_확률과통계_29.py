"""2023 수능 확통 29 (조건부확률, brute-force)
6장 카드(앞 i, 뒤 0), 주사위 3번. 눈 k → k번째 카드 뒤집기.
3번 후 짝수 위치(짝수번 뒤집힘)는 i 보이고 홀수번은 0. 보이는 합이 짝수(A)일 때
1의 눈이 정확히 1번(B) 확률 q/p, p+q. 216개 주사위열 전수열거."""
from itertools import product
from fractions import Fraction

CANDIDATE = 49


def solve(rolls=3, cards=6, faces=6, target_face=1, target_count=1):
    total = favor = 0
    for seq in product(range(1, faces + 1), repeat=rolls):
        visible = sum(i for i in range(1, cards + 1) if seq.count(i) % 2 == 0)
        if visible % 2 == 0:                              # 사건 A: 보이는 합 짝수
            total += 1
            if seq.count(target_face) == target_count:    # 사건 B: target_face 정확히 target_count번
                favor += 1
    pr = Fraction(favor, total)                           # q/p (기약)
    return pr.numerator + pr.denominator                  # p+q


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
