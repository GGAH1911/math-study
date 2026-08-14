# 2026 고3 7월 확통 30 — 수직선 위 점 P의 랜덤워크(주사위 독립시행) 조건부확률.
#   주사위 눈 k: up_faces 개면 +1, down_faces 개면 -1, 나머지는 이동 없음.
#   trials 번 시행하여 n번째 시행 후 좌표를 a_n 이라 할 때
#   a_1 = first_pos 이고 a_trials = final_pos 인 조건 아래
#   max{a_m | 1<=m<=trials} = target_max 일 조건부확률 q/p 의 p+q.
# 구조: (위치, 지금까지의 최댓값) 상태 DP 로 정확한 유리수 확률을 세어 조건부확률을 만든다.
CANDIDATE = 725

import sympy as sp
from collections import defaultdict

PARAMS = dict(
    trials=7,        # 시행 횟수 (a_1 ... a_trials)
    sides=6,         # 주사위 면 수
    up_faces=1,      # 양의 방향(+1)으로 가는 눈의 개수 (k=1)
    down_faces=1,    # 음의 방향(-1)으로 가는 눈의 개수 (k=2)
    first_pos=0,     # 조건 a_1 의 값
    final_pos=1,     # 조건 a_trials 의 값
    target_max=2,    # 원소 중 가장 큰 값
)


def _weights(prm):
    sides = int(prm['sides']); up = int(prm['up_faces']); down = int(prm['down_faces'])
    stay = sides - up - down
    if sides <= 0 or up < 0 or down < 0 or stay < 0:
        return None
    return {1: sp.Rational(up, sides), -1: sp.Rational(down, sides), 0: sp.Rational(stay, sides)}


def solve(prm):
    """조건 → p+q. (조건부확률 P(max=target_max | a_1=first_pos, a_trials=final_pos) = q/p)"""
    W = _weights(prm)
    if W is None:
        return None
    N = int(prm['trials'])
    first = int(prm['first_pos']); final = int(prm['final_pos']); tmax = int(prm['target_max'])
    if N < 1 or first not in W or W[first] == 0:
        return None

    # 상태 = (현재 좌표, a_1..a_n 중 최댓값) → 확률(정확한 유리수)
    cur = defaultdict(lambda: sp.Integer(0))
    cur[(first, first)] = W[first]
    for _ in range(N - 1):
        nxt = defaultdict(lambda: sp.Integer(0))
        for (pos, mx), w in cur.items():
            for step, ws in W.items():
                if ws == 0:
                    continue
                np_ = pos + step
                nxt[(np_, max(mx, np_))] += w * ws
        cur = nxt

    den = sum((w for (pos, mx), w in cur.items() if pos == final), sp.Integer(0))
    num = sum((w for (pos, mx), w in cur.items() if pos == final and mx == tmax), sp.Integer(0))
    if den == 0:
        return None
    prob = sp.simplify(sp.Rational(num, den))
    q, p = sp.fraction(sp.nsimplify(prob))
    return int(p + q)


def statement(prm):
    """새로 만든 문제의 문장."""
    sides = int(prm['sides']); up = int(prm['up_faces']); down = int(prm['down_faces'])
    up_k = f"1 이상 {up} 이하" if up > 1 else "1"
    dn_lo, dn_hi = up + 1, up + down
    down_k = f"{dn_lo} 이상 {dn_hi} 이하" if down > 1 else f"{dn_lo}"
    return (
        f"수직선의 원점에 점 P가 있다. 각 면에 1부터 {sides}까지의 수가 하나씩 적힌 주사위를 "
        f"한 번 던져 나온 눈의 수를 k라 할 때, k가 {up_k}이면 점 P를 양의 방향으로 1만큼, "
        f"k가 {down_k}이면 점 P를 음의 방향으로 1만큼 이동시키고, 그 밖의 경우 이동시키지 않는다. "
        f"이 시행을 {int(prm['trials'])}번 반복할 때, n번째 시행 후 점 P의 좌표를 a_n이라 하자. "
        f"a_1={int(prm['first_pos'])}이고 a_{{{int(prm['trials'])}}}={int(prm['final_pos'])}일 때, "
        f"집합 {{a_m | m은 {int(prm['trials'])} 이하의 자연수}}의 원소 중 가장 큰 값이 "
        f"{int(prm['target_max'])}일 확률은 q/p이다. p+q의 값을 구하시오. (p, q는 서로소인 자연수)"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
