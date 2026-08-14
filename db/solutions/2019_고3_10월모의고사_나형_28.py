"""2019 고3 10월모의고사 나형 28번 — 파라미터화 솔버.

수학 구조:
  - 점심 식사에서 한식(K)을 선택할 확률 pK (양식 W 확률은 1-pK).
  - 점심에 양식을 선택한 학생 중 저녁에도 양식을 선택할 조건부확률 WW.
  - 점심에 한식을 선택한 학생 중 저녁에도 한식을 선택할 조건부확률 KK
    (따라서 점심 한식 → 저녁 양식 조건부확률은 1-KK).
  - 구하는 값: P(점심K | 저녁W) = q/p (기약분수) 일 때 p+q.
    베이즈 정리: P(K∩저녁W) = pK·(1-KK), P(저녁W) = (1-pK)·WW + pK·(1-KK).

pK, WW, KK 세 값이 모두 답을 바꾸는 실질 파라미터이다 (아래 검증 참고).
"""
from sympy import Rational

CANDIDATE = 47  # ★원문제 정답 (절대 변경 금지)

PARAMS = dict(
    pK=Rational(6, 10),   # 점심에 한식을 고를 확률 = 60%
    WW=Rational(25, 100),  # 점심W → 저녁W 조건부확률 = 25%
    KK=Rational(30, 100),  # 점심K → 저녁K 조건부확률 = 30%
)


def solve(prm):
    pK = prm["pK"]
    WW = prm["WW"]
    KK = prm["KK"]

    if not (0 < pK < 1 and 0 < WW < 1 and 0 < KK < 1):
        raise ValueError("확률 파라미터는 0과 1 사이여야 합니다.")

    pW = 1 - pK  # 점심에 양식을 고를 확률
    KW = 1 - KK  # 점심K → 저녁W 조건부확률
    WY = WW      # 점심W → 저녁W 조건부확률 (그대로)

    # 전체확률: 저녁에 양식을 선택할 확률
    p_dinner_W = pW * WY + pK * KW
    if p_dinner_W == 0:
        raise ValueError("저녁에 양식을 선택할 확률이 0이라 조건부확률을 정의할 수 없습니다.")

    # 베이즈 정리: P(점심K | 저녁W)
    p_K_given_dinnerW = Rational(pK * KW, p_dinner_W)

    p, q = p_K_given_dinnerW.q, p_K_given_dinnerW.p  # 확률 = q/p (기약분수)
    if q <= 0 or p <= 0:
        raise ValueError("p, q가 자연수가 아닙니다.")

    return p + q


def statement(prm):
    pK = prm["pK"]
    WW = prm["WW"]
    KK = prm["KK"]
    pct = lambda r: int(r * 100)
    return (
        "식문화 체험의 날에 어느 고등학교 전체 학생을 대상으로 점심과 저녁 식사를 "
        "제공하였다. 모든 학생들은 매 식사 때마다 양식과 한식 중 하나를 반드시 "
        f"선택하였고, 전체 학생의 {pct(pK)}%가 점심에 한식을 선택하였다.\n\n"
        f"점심에 양식을 선택한 학생의 {pct(WW)}%는 저녁에도 양식을 선택하였고, "
        f"점심에 한식을 선택한 학생의 {pct(KK)}%는 저녁에도 한식을 선택하였다.\n\n"
        "이 고등학교 학생 중에서 임의로 선택한 한 명이 저녁에 양식을 선택한 "
        "학생일 때, 이 학생이 점심에 한식을 선택했을 확률은 \\frac{q}{p}이다. "
        "p+q의 값을 구하시오. (단, p와 q는 서로소인 자연수이다.)"
    )


if __name__ == "__main__":
    assert solve(PARAMS) == CANDIDATE

    # 원문제와 다른 파라미터 조합으로 답이 실제로 달라지는지 확인
    variant1 = dict(pK=Rational(1, 2), WW=Rational(1, 4), KK=Rational(3, 10))
    variant2 = dict(pK=Rational(7, 10), WW=Rational(1, 5), KK=Rational(2, 5))
    r1 = solve(variant1)
    r2 = solve(variant2)
    assert r1 != CANDIDATE and r2 != CANDIDATE and r1 != r2

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
