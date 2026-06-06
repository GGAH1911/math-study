"""2026 고3 5월 확통 29 (원순열, brute-force)
1~7을 원형 7의자에 배열(회전동일). (가) 6의 양 이웃 합=9. (나) 7과 이웃하지 않은
4의자 수의 곱이 12의 배수. 회전 제거 위해 값 1을 0번 자리에 고정 → 6!=720 전수."""
from itertools import permutations
from math import prod

CANDIDATE = 68


def solve(n=7, nbr_sum=9, prod_mult=12, anchor_a=6, anchor_b=7):
    cnt = 0
    rest = [x for x in range(1, n + 1) if x != 1]
    for perm in permutations(rest):
        arr = (1,) + perm                                 # 0번 자리=1 (회전 고정)
        pa = arr.index(anchor_a)
        if arr[(pa - 1) % n] + arr[(pa + 1) % n] != nbr_sum:   # (가)
            continue
        pb = arr.index(anchor_b)
        adj = {pb, (pb - 1) % n, (pb + 1) % n}            # 7과 그 양 이웃
        others = [arr[i] for i in range(n) if i not in adj]    # 이웃하지 않은 4의자
        if prod(others) % prod_mult != 0:                 # (나)
            continue
        cnt += 1
    return cnt


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
