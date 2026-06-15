"""2019 고3 4월모의고사 나형 23번 — 파라미터 솔버 (수동 작성).
문제: p: -5≤x≤10, q: -6≤x≤a. p가 q이기 위한 충분조건이 되게 하는 a의 최솟값. (답 10)
구조: p ⇒ q ⟺ {p} ⊆ {q} ⟺ [-5,10] ⊆ [-6,a] ⟺ a ≥ 10. 최소 a = 10.
재생산: 구간 끝점 파라미터화.
"""


def solve(p_lo, p_hi, q_lo):
    # [p_lo,p_hi] ⊆ [q_lo, a] 필요충분: q_lo ≤ p_lo 이고 a ≥ p_hi. a 최소 = p_hi.
    assert q_lo <= p_lo
    return p_hi


CANDIDATE = 10
assert solve(-5, 10, -6) == CANDIDATE
print('VERIFY_PASS')
