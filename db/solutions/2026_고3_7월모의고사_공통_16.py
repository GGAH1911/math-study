# a_1 = a1, a_{n+1} = a_n/(den_mul*n + den_add) + add  →  a_target
# 원문제: a_1=2, a_{n+1}=a_n/n+4, a_3=?  (점화식을 target-1 번 그대로 돌린다)
CANDIDATE = 7
import sympy as sp

PARAMS = dict(
    a1=2,          # 첫째항 a_1
    den_mul=1,     # 분모 계수: 분모 = den_mul*n + den_add
    den_add=0,
    add=4,         # 점화식에 더하는 상수
    target=3,      # 구하는 항의 번호
)


def solve(prm):
    """조건(첫째항·점화식·구할 항 번호) → 답. a_{n+1} = a_n/(den_mul*n+den_add) + add."""
    a = sp.Rational(prm['a1'])
    n = 1
    while n < int(prm['target']):
        den = sp.Integer(prm['den_mul']) * n + sp.Integer(prm['den_add'])
        if den == 0:
            return sp.zoo
        a = sp.simplify(a / den + sp.Rational(prm['add']))
        n += 1
    return a


def statement(prm):
    """새 문제 문장."""
    d = []
    if prm['den_mul'] != 1 or prm['den_add'] != 0:
        if prm['den_mul'] != 0:
            d.append(('' if prm['den_mul'] == 1 else str(prm['den_mul'])) + 'n')
        if prm['den_add'] != 0:
            d.append(('+' if prm['den_add'] > 0 else '-') + str(abs(prm['den_add'])))
        den = ''.join(d).lstrip('+')
    else:
        den = 'n'
    return (f"수열 {{a_n}}은 a_1={prm['a1']}이고, 모든 자연수 n에 대하여 "
            f"a_{{n+1}}=\\frac{{a_n}}{{{den}}}+{prm['add']} 를 만족시킨다. "
            f"a_{{{prm['target']}}}의 값을 구하시오.")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
