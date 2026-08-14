import sympy as sp

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 쌍곡선  x^2/A2 - y^2/B2 = 1  (A2=a^2, B2=b^2), 초점 A(-c,0), B(c,0), c^2=A2+B2.
# 제1사분면 위의 점 P가 ∠APB=π/2 를 만족 ⇔ PA·PB=0 ⇔ x^2+y^2=c^2
#   (원점을 중심으로 반지름 c인 원 위에 있음, AB가 지름이므로 원주각 정리).
# 원과 쌍곡선을 연립하면 닫힌 식으로
#   x0^2 = A2*(B2+c^2)/c^2 ,  y0 = B2/c
# 가 나온다 (A2, B2 > 0 이면 항상 x0 > sqrt(A2) 이므로 쌍곡선의 오른쪽 가지 위 점으로 유효).
# 직선 AP에 원점에서 내린 거리 = 원점 중심이고 AP에 접하는 원의 반지름.
#   거리 d = |y0*c| / sqrt(y0^2 + (x0+c)^2)
#
# 원문제: A2=4, B2=12 → c=4, x0=√7, y0=3, d=√7-1

CANDIDATE = sp.sqrt(7) - 1   # ★원문제 정답, 절대 변경 금지

PARAMS = dict(A2=4, B2=12)   # 쌍곡선 x^2/A2 - y^2/B2 = 1 의 계수 (둘 다 답을 바꾸는 살아있는 파라미터)


def value(prm):
    """쌍곡선 계수(A2, B2)로부터 원점-직선AP 거리(=구하는 반지름)를 sympy로 실제 계산."""
    A2 = sp.nsimplify(prm['A2'])
    B2 = sp.nsimplify(prm['B2'])
    if A2 <= 0 or B2 <= 0:
        raise ValueError('A2, B2 는 양수여야 한다 (쌍곡선이 성립하지 않음)')

    c2 = A2 + B2
    c = sp.sqrt(c2)

    # 원(x^2+y^2=c^2)과 쌍곡선의 제1사분면 교점 P=(x0, y0)  — 닫힌 식으로 유도
    x0_sq = A2 * (B2 + c2) / c2
    x0 = sp.sqrt(x0_sq)
    y0 = B2 / c

    # A=(-c,0), P=(x0,y0) 를 지나는 직선까지 원점에서의 거리
    dist = sp.Abs(y0 * c) / sp.sqrt(y0**2 + (x0 + c)**2)
    return sp.nsimplify(sp.simplify(dist))


def solve(prm):
    return value(prm)


def statement(prm):
    A2 = prm['A2']
    B2 = prm['B2']
    return (
        f"좌표평면 위에 두 점 A(-c, 0), B(c, 0)과 쌍곡선 "
        f"x^2/{A2} - y^2/{B2} = 1 (c^2 = {A2}+{B2}) 이 있다. "
        f"쌍곡선 위에 있고 제1사분면에 있는 점 P에 대하여 ∠APB = π/2 일 때, "
        f"원점을 중심으로 하고 직선 AP에 접하는 원의 반지름의 길이는?"
    )


if __name__ == '__main__':
    print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
