"""2024 고3 3월 확통 26 (격자 최단경로, 객관식)
아래·위 격자가 유일점 J=(3,3)에서만 연결(모든 A→B 경로가 J 통과).
P 지나고 Q 안 지나는 경우 = (P지나 B) - (P,Q 모두 지나 B) = 180 - 81 = 99 = 보기④.
A(0,0) P(2,1) J(3,3) Q(4,5) B(6,6)."""
from math import comb

CANDIDATE = 4
choices = {1: 72, 2: 81, 3: 90, 4: 99, 5: 108}


def _paths(ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    return comb(dx + dy, dx) if dx >= 0 and dy >= 0 else 0


def solve(px=2, py=1, jx=3, jy=3, qx=4, qy=5, bx=6, by=6):
    aP = _paths(0, 0, px, py)
    Pj = _paths(px, py, jx, jy)
    thru_P = aP * Pj * _paths(jx, jy, bx, by)            # P 지나 B (J 강제통과)
    thru_PQ = aP * Pj * _paths(jx, jy, qx, qy) * _paths(qx, qy, bx, by)  # P,Q 모두
    val = thru_P - thru_PQ
    for num, cval in choices.items():
        if cval == val:
            return num
    return -1


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
