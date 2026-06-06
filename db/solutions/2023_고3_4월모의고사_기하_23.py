"""2023 고3 4월 기하 23 (평면벡터, 객관식)
정사각형 ABCD(변 s=2), M=AD중점, N=CD중점. |BM+DN|=√2=보기③.
좌표 A(0,s) D(s,s) B(0,0) C(s,0); M=(s/2,s) N=(s,s/2)."""
import sympy as sp

CANDIDATE = 3
choices = {1: sp.sqrt(2) / 2, 2: sp.Integer(1), 3: sp.sqrt(2), 4: sp.Integer(2), 5: 2 * sp.sqrt(2)}


def solve(s=2):
    s = sp.Integer(s)                            # 심볼릭 유지(√2가 부동소수로 안 떨어지게)
    A, B, C, D = (0, s), (0, 0), (s, 0), (s, s)
    M = ((A[0] + D[0]) / 2, (A[1] + D[1]) / 2)   # AD 중점
    N = ((C[0] + D[0]) / 2, (C[1] + D[1]) / 2)   # CD 중점
    BM = (M[0] - B[0], M[1] - B[1])
    DN = (N[0] - D[0], N[1] - D[1])
    v = (BM[0] + DN[0], BM[1] + DN[1])
    val = sp.sqrt(v[0] ** 2 + v[1] ** 2)
    for num, cval in choices.items():
        if sp.simplify(val - cval) == 0:
            return num
    return -1


if __name__ == '__main__':
    print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')
