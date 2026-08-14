import sympy as sp
from sympy import Rational

CANDIDATE = 59  # ★원문제 정답 — 절대 바꾸지 않는다

# 문제의 수학 구조:
#   X ~ B(n, p)              이항분포, 성공확률 p
#   Y = a*X + b               선형변환
#   V(Y) = a^2 * n * p * (1-p) = V_target  →  n 결정
#   E(Y) = a * n * p + b       구하는 값
#
# 원문제(B(n, 1/3), Y=2X-1, V(Y)=80)는 p=1/3, a=2, b=-1, V_target=80 인 특수한 경우.
PARAMS = dict(
    p=Rational(1, 3),   # 이항분포 성공확률
    a=2,                 # 선형변환 계수 (Y = aX + b)
    b=-1,                # 선형변환 상수항
    V_target=80,         # 주어진 V(Y) 값
)


def solve(prm):
    p = prm['p']
    a = prm['a']
    b = prm['b']
    V_target = prm['V_target']

    n = sp.symbols('n')
    V_X = n * p * (1 - p)      # V(X) = np(1-p)
    V_Y = a ** 2 * V_X          # V(aX+b) = a^2 V(X)

    n_sols = sp.solve(sp.Eq(V_Y, V_target), n)
    if not n_sols:
        raise ValueError('주어진 조건을 만족하는 n이 없습니다.')
    n_val = n_sols[0]

    E_X = n_val * p             # E(X) = np
    E_Y = a * E_X + b           # E(aX+b) = aE(X)+b

    if not E_Y.is_number or E_Y.has(sp.zoo, sp.nan, sp.oo):
        raise ValueError('유효한 답이 아닙니다.')
    return sp.nsimplify(E_Y)


def statement(prm):
    p = prm['p']
    a = prm['a']
    b = prm['b']
    V_target = prm['V_target']

    p_str = sp.nsimplify(p)
    expr_str = f"{a}X" + (f"+{b}" if b >= 0 else f"{b}")

    return (
        f"이항분포 B(n, {p_str})을 따르는 확률변수 X에 대하여 "
        f"V({expr_str})={V_target}일 때, E({expr_str})의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
