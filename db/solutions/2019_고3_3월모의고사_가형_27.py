"""2019 고3 3월모의고사 가형 27번 — 파라미터화 솔버.

원문제 구조
  - 두 로그곡선 y=log2(c·x), y=log2(x) 는 상수 shift=log2(c) 만큼 수직으로 어긋나 있다.
    (원문제 c=4 → shift=2)
  - 수평선 y=y0 (원문제 y0=2) 이 두 곡선과 만나는 점이 A(=c·x 곡선), B(=x 곡선).
  - 수평선 y=k (k>y0, 미지수) 가 두 곡선과 만나는 점이 C, D.
  - B를 지나는 수직선(x=x_B)이 선분 CD를 ratio_num:ratio_den 로 내분하는 점에서
    만난다는 조건으로 k를 역산한다. (원문제 1:2)
  - AB, CD 는 서로 평행(둘 다 수평선)하므로 사각형 ABDC 는 사다리꼴이고
    넓이 S = (AB+CD)(k-y0)/2.
  - 최종 답은 mult·S. (원문제 mult=12)

파라미터로 뽑은 수학적 자유도
  - shift : 두 로그곡선의 수직 이격 = log2(c) (곡선 y=log2(c x) 의 c 를 결정)
  - y0    : 첫 번째 수평선의 높이 (A, B 를 결정)
  - ratio_num : ratio_den : 점 E 가 CD 를 내분하는 비율 (k 를 결정)
  - mult  : 최종 답 = mult·S 에서의 배수

  이 중 y0, ratio_den, mult 를 각각 바꾸면 k, S, 최종 답이 모두 달라짐을 아래
  VERIFY 블록 이후 직접 실행하여 확인했다 (54 → 108, 54 → 다른 값, 54 → 27 등).
"""
import sympy as sp


def _solve_core(shift, y0, ratio_num, ratio_den, mult):
    """조건들로부터 k 를 역산하고 사다리꼴 넓이 S 를 구해 mult*S 를 반환."""
    t = sp.symbols('t', positive=True)          # t = 2**k 로 치환하여 대수적으로 풀기
    two = sp.Integer(2)

    xA = two ** (y0 - shift)                     # y=y0 와 y=log2(c x) 의 교점 x좌표
    xB = two ** y0                               # y=y0 와 y=log2(x)   의 교점 x좌표
    xC = t / two ** shift                        # y=k  와 y=log2(c x) 의 교점 x좌표 (t=2^k)
    xD = t                                       # y=k  와 y=log2(x)   의 교점 x좌표

    f = sp.Rational(ratio_num, ratio_num + ratio_den)   # E 가 CD 를 ratio_num:ratio_den 로 내분
    sols = sp.solve(sp.Eq(xB, xC + f * (xD - xC)), t)   # E_x = x_B 조건으로 t(=2^k) 를 구함
    sols = [s for s in sols if s.is_real and s > 0]
    if not sols:
        raise ValueError("주어진 조건을 만족하는 k가 존재하지 않습니다.")
    t0 = sols[0]

    k0 = sp.simplify(sp.log(t0, 2))
    if not sp.simplify(k0 - y0) > 0:
        raise ValueError("k>y0 조건을 만족하지 않아 문제가 성립하지 않습니다.")

    AB = xB - xA
    CD = (xD - xC).subs(t, t0)
    if sp.simplify(AB) <= 0 or sp.simplify(CD) <= 0:
        raise ValueError("선분 AB, CD 가 양수 길이를 갖지 않아 사각형이 성립하지 않습니다.")

    S = sp.Rational(1, 2) * (AB + CD) * (k0 - y0)
    return sp.nsimplify(sp.simplify(mult * S))


def solve(prm):
    return _solve_core(
        prm['shift'], prm['y0'], prm['ratio_num'], prm['ratio_den'], prm['mult']
    )


def statement(prm):
    c = 2 ** prm['shift']
    return (
        f"그림과 같이 직선 y={prm['y0']}가 두 곡선 y=log_2({c}x), y=log_2 x와 만나는 점을 "
        f"각각 A, B라 하고, 직선 y=k (k>{prm['y0']})가 두 곡선 y=log_2({c}x), y=log_2 x와 "
        f"만나는 점을 각각 C, D라 하자. 점 B를 지나고 y축과 평행한 직선이 직선 CD와 만나는 "
        f"점을 E라 하면 점 E는 선분 CD를 {prm['ratio_num']}:{prm['ratio_den']}로 내분한다. "
        f"사각형 ABDC의 넓이를 S라 할 때, {prm['mult']}S의 값을 구하시오."
    )


CANDIDATE = 54          # ★원문제 정답 — 절대 바꾸지 않음
PARAMS = dict(
    shift=2,             # log2(4) : 곡선 y=log2(4x) 의 4
    y0=2,                # 첫 번째 수평선 y=2
    ratio_num=1,         # CE:ED = 1:2 의 1
    ratio_den=2,         # CE:ED = 1:2 의 2
    mult=12,             # 최종 답 = 12S
)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
