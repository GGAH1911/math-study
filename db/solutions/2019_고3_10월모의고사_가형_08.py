import sympy as sp
from sympy import Rational, sqrt, simplify

CANDIDATE = 1  # 원문제 정답: 보기 ①

# ---- 파라미터 ----
# num/den              : cosα = cosβ 의 절댓값(기약분수, 0 < num/den < 1).
#                         0<α<β<2π 에서 cosα=cosβ 를 만족하는 두 해는
#                         α=arccos(c) ∈ (0,π), β=2π-α ∈ (π,2π) 뿐이며,
#                         이때 sinα=+sqrt(1-c²)(>0), sinβ=-sinα 로 고정된다.
# c_positive            : cosα=cosβ 의 부호. True→+num/den, False→-num/den.
#                         부호가 바뀌면 sin(β-α)=-2c·sinα 의 부호가 통째로 뒤집힌다
#                         → 라이브(정답 보기 번호가 ①↔⑤로 바뀜).
# ask_beta_minus_alpha  : True→sin(β-α), False→sin(α-β)=-sin(β-α) 를 물음.
#                         순서를 바꾸면 값의 부호가 뒤집힌다 → 라이브(①↔⑤).
PARAMS = dict(num=1, den=3, c_positive=True, ask_beta_minus_alpha=True)


def _core(prm):
    """(sin(질문한 차각), |sin(β-α)|) 를 정확한 부호로 계산한다."""
    num, den = prm['num'], prm['den']
    if not (0 < num < den):
        raise ValueError('0 < num/den < 1 이어야 cosα=cosβ=c 가 (0,2π) 안에서 '
                          'α≠β 인 두 해를 갖는다')
    mag = Rational(num, den)
    c = mag if prm['c_positive'] else -mag

    # α = arccos(c) ∈ (0, π) 인 principal value → sinα = +sqrt(1-c²)
    sin_alpha = sqrt(1 - c**2)
    # β = 2π - α : (0,2π) 안에서 cosβ=c 를 만족하는 α 이외의 유일한 해 → sinβ = -sinα
    sin_beta = -sin_alpha

    diff = simplify(sin_beta * c - c * sin_alpha)  # sin(β-α) = sinβcosα - cosβsinα
    if not prm['ask_beta_minus_alpha']:
        diff = -diff                                # sin(α-β) = -sin(β-α)

    abs_v = simplify(2 * mag * sin_alpha)            # |sin(β-α)| = 2c·sinα (항상 양수)
    return diff, abs_v


def value(prm):
    diff, _ = _core(prm)
    return diff


def choices(prm):
    """값에서 유도한 5지선다: ∓|v|, ∓|v|/√2, 0 (오름차순)."""
    _, a = _core(prm)
    return [-a, -a / sqrt(2), sp.Integer(0), a / sqrt(2), a]


def solve(prm):
    v = value(prm)
    for i, ch in enumerate(choices(prm), start=1):
        if simplify(v - ch) == 0:
            return i
    raise ValueError('계산된 값이 보기 목록 어디에도 없음')


def statement(prm):
    num, den = prm['num'], prm['den']
    sign = '' if prm['c_positive'] else '-'
    target = 'sin(β-α)' if prm['ask_beta_minus_alpha'] else 'sin(α-β)'
    return (f"0 < α < β < 2π 이고 cosα = cosβ = {sign}{num}/{den} 일 때, "
            f"{target} 의 값은?")


# 원문제 보기(①~⑤) 고정 재현 확인
_expected_choices = [-4 * sqrt(2) / 9, -Rational(4, 9), sp.Integer(0), Rational(4, 9), 4 * sqrt(2) / 9]
_got_choices = choices(PARAMS)
assert all(simplify(a - b) == 0 for a, b in zip(_got_choices, _expected_choices)), \
    f'보기 불일치: {_got_choices}'

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
