"""2019 고3 10월모의고사 가형 26번 — 파라미터화 솔버.

[문제 구조]
어느 모집단에서 표본 n명을 뽑아 그 중 m명이 특정 성질을 가졌을 때,
모비율 p 에 대한 신뢰도 95% 신뢰구간은
    p̂ - z·sqrt(p̂q̂/n)  ≤  p  ≤  p̂ + z·sqrt(p̂q̂/n)   (p̂ = m/n, q̂ = 1-p̂)
로 주어진다. 문제는 이 신뢰구간의 하한 lo, 상한 hi 와 z(=1.96, P(|Z|≤z)=0.95)
값을 준 뒤 m+n 을 묻는다.

수학적으로 이 문제를 결정하는 파라미터는 (lo, hi, z) 세 값이다.
    p̂     = (lo+hi)/2               ← 신뢰구간 중심
    margin = (hi-lo)/2               ← 신뢰구간 반폭
    margin = z·sqrt(p̂(1-p̂)/n)       ← 이 식을 n에 대해 풀면 n, 이어서 m=p̂·n
lo, hi, z 중 어느 것을 바꿔도(단, n, m 이 자연수가 되도록 잘 잡아야 함) m+n 값이
달라지므로 이 셋을 PARAMS 로 노출한다.
"""
import sympy as sp

CANDIDATE = 440  # ★원문제 정답. 절대 바꾸지 않음

PARAMS = dict(
    lo=sp.Rational(706, 10000),   # 신뢰구간 하한 0.0706
    hi=sp.Rational(1294, 10000),  # 신뢰구간 상한 0.1294
    z=sp.Rational(196, 100),      # P(|Z|≤z)=0.95 를 만족하는 z=1.96
)


def solve(prm):
    lo = sp.Rational(prm['lo'])
    hi = sp.Rational(prm['hi'])
    z = sp.Rational(prm['z'])

    if lo <= 0 or hi <= lo or hi >= 1:
        raise ValueError("신뢰구간이 0<lo<hi<1 을 만족해야 합니다.")

    n = sp.symbols('n', positive=True)

    phat = (lo + hi) / sp.Integer(2)      # 신뢰구간 중심 = 표본비율 m/n
    margin = (hi - lo) / sp.Integer(2)    # 신뢰구간 반폭
    qhat = 1 - phat

    # margin = z*sqrt(phat*qhat/n) 을 양변 제곱하여 n에 대한 방정식으로 만들고 sympy로 푼다.
    eq = sp.Eq(margin ** 2, z ** 2 * phat * qhat / n)
    n_sols = sp.solve(eq, n)
    if not n_sols:
        raise ValueError("n을 구할 수 없습니다.")
    n_val = sp.nsimplify(n_sols[0])

    if not n_val.is_rational or n_val <= 0 or n_val.q != 1:
        raise ValueError("n이 자연수가 아닙니다 (문제로 성립하지 않음).")
    n_val = sp.Integer(n_val)

    m_val = phat * n_val
    if not m_val.is_rational or m_val <= 0 or sp.nsimplify(m_val).q != 1:
        raise ValueError("m이 자연수가 아닙니다 (문제로 성립하지 않음).")
    m_val = sp.Integer(m_val)

    return int(m_val + n_val)


def statement(prm):
    lo = sp.Rational(prm['lo'])
    hi = sp.Rational(prm['hi'])
    z = sp.Rational(prm['z'])
    lo_s = sp.nsimplify(lo)
    hi_s = sp.nsimplify(hi)
    z_s = sp.nsimplify(z)
    return (
        "어느 영화를 관람한 사람 중에서 n명을 임의추출하여 조사한 결과, "
        "이 영화를 재관람한 사람은 m명이었다. 이 결과를 이용하여, 이 영화를 관람한 "
        "사람 전체 중 이 영화를 재관람한 사람의 비율 p에 대한 신뢰도 95%의 신뢰구간을 "
        f"구하면 {sp.N(lo_s, 6)} \\le p \\le {sp.N(hi_s, 6)} 이다. m+n의 값을 구하시오.\n"
        f"(단, Z가 표준정규분포를 따르는 확률변수일 때, P(|Z| \\le {sp.N(z_s, 3)})=0.95 로 계산한다.)"
    )


# --- 파라미터 민감도 확인용 변형들 --------------------------------------
# lo, hi, z 세 값은 n, m 이 자연수가 되도록 서로 묶여 있으므로(신뢰구간 문제의 본질),
# (표본비율 p̂, 표본크기 n, z값)을 먼저 자연수로 정하고 그로부터 lo=p̂-margin,
# hi=p̂+margin 을 역산하면 항상 자기모순 없는 새 문제가 만들어진다.
# 아래 두 변형은 원문제(phat=0.1, n=400, z=1.96 → 440)와 값을 각각 하나씩만
# 바꿔서, lo/hi(=p̂,n)와 z 각각이 답을 실제로 바꾸는 파라미터임을 보여준다.
def _make(phat, n, z):
    phat = sp.Rational(phat)
    n = sp.Integer(n)
    z = sp.Rational(z)
    margin = z * sp.sqrt(phat * (1 - phat) / n)
    return dict(lo=phat - margin, hi=phat + margin, z=z)


VARIANTS = [
    PARAMS,                                   # phat=1/10, n=400,  z=1.96 → 440 (원문제)
    _make(sp.Rational(1, 10), 100, sp.Rational(196, 100)),   # n만 400→100   → 110
    _make(sp.Rational(1, 5), 100, sp.Rational(1645, 1000)),  # phat,z까지 변경 → 120
]

if __name__ == '__main__':
    results = [solve(v) for v in VARIANTS]
    assert results[0] == CANDIDATE
    assert len(set(results)) >= 3, f"변형들이 서로 다른 답을 내야 합니다: {results}"

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
