"""2022 고3 4월 기하 23 (평면벡터, 객관식)
한 변 s=1인 정육각형 ABCDEF. |AD+2DE|=? 좌표:
A(-s/2,s√3/2) B(-s,0) C(-s/2,-s√3/2) D(s/2,-s√3/2) E(s,0) F(s/2,s√3/2).
AD=(s,-s√3), DE=(s/2,s√3/2) → AD+2DE=(2s,0) → |·|=2s=2=보기③."""
import sympy as sp

CANDIDATE = 3
choices = {1: sp.Integer(1), 2: sp.sqrt(3), 3: sp.Integer(2), 4: sp.Integer(3), 5: 2 * sp.sqrt(3)}


def solve(s=1):
    s = sp.Integer(s)
    h = s * sp.sqrt(3) / 2
    A, B, C = (-s / 2, h), (-s, 0), (-s / 2, -h)
    D, E, F = (s / 2, -h), (s, 0), (s / 2, h)
    AD = (D[0] - A[0], D[1] - A[1])
    DE = (E[0] - D[0], E[1] - D[1])
    v = (AD[0] + 2 * DE[0], AD[1] + 2 * DE[1])
    val = sp.simplify(sp.sqrt(v[0] ** 2 + v[1] ** 2))
    for num, cval in choices.items():
        if sp.simplify(val - cval) == 0:
            return num
    return -1


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
