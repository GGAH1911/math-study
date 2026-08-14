# -*- coding: utf-8 -*-
"""
원문제(객관식 4번): 두 사건 A, B가 서로 배반이고 P(A)=1/6, P(B)=2/3일 때
P(A^C ∩ B)의 값은? (A^C은 A의 여사건)  → 정답 ⑤ 2/3

파라미터화한 수학 구조:
    P(A^C ∩ B) = P(B) - P(A∩B)   ... 일반 공식, 배반이면 P(A∩B) = 0
  - pa  = P(A)  : 문제 데이터(원문제도 P(A)는 답 계산에 불필요하게 주어짐),
                   보기 구성(오답 P(A))과 확률공간 일관성(pa+pb-pab <= 1)에 관여
  - pb  = P(B)  : 답(값)을 직접 좌우하는 손잡이
  - pab = P(A∩B): 0이면 '서로 배반'(원문제), 0보다 크면 일반적인 겹침 문제.
                   답(값)을 직접 좌우하는 손잡이

★결합 구조(실측 확인): 배반(pab=0)이면 답 = P(B)라서 pa는 답에 무관하고,
  객관식 답은 '값의 순위'라서 pb를 흔들어도 값이 항상 최댓값(⑤)에 머문다.
  즉 개별 파라미터를 하나씩 흔드는 방식으로는 답을 못 움직인다
  (무효 공간까지 허용하면 순위만 흔들리는데, 규칙 6대로 유효성 검증을 하면
   그마저도 예외가 된다). 따라서 규칙 5에 따라 성립하는 조합 VARIANTS 로
   재생성 능력을 증명한다 — V1 은 pb 를, V2·V3 는 pab 를 바꿔 답을 바꾼다.
"""
from sympy import Rational, simplify

CANDIDATE = 5  # 원문제 정답: 보기 ⑤ (값 2/3) — 절대 변경 금지

PARAMS = dict(pa=Rational(1, 6), pb=Rational(2, 3), pab=Rational(0))


def _validate(prm):
    """확률공간 성립 조건. 어기면 예외(규칙 6: None 반환 금지)."""
    pa, pb, pab = prm['pa'], prm['pb'], prm['pab']
    if not (Rational(0) <= pab <= min(pa, pb)):
        raise ValueError(f'성립 불가: 0 <= P(A∩B) <= min(P(A),P(B)) 필요 '
                         f'(pa={pa}, pb={pb}, pab={pab})')
    if pa + pb - pab > 1:
        raise ValueError(f'성립 불가: P(A∪B) = pa+pb-pab > 1 '
                         f'(pa={pa}, pb={pb}, pab={pab})')


def value(prm):
    """수학적 답: P(A^C ∩ B) = P(B) - P(A∩B) (sympy 로 실제 계산)"""
    return prm['pb'] - prm['pab']


def choices(prm):
    """보기 5개 — 값과 데이터에서 유도(고정 튜플 금지).

    오답 후보: P(A), P(B^C), P(B)-P(A), (P(B)-P(A))/2  ← 원문제 보기의 구성.
    정답 value 를 반드시 포함하고, 중복·부족분은 데이터에서 파생된 값으로 보충.
    """
    pa, pb, pab = prm['pa'], prm['pb'], prm['pab']
    v = value(prm)
    cand = [pa, 1 - pb, pb - pa, (pb - pa) / 2, v]
    out = []
    for x in cand:
        if all(simplify(x - y) != 0 for y in out):
            out.append(x)
    if all(simplify(v - y) != 0 for y in out):
        out.append(v)
    k = 1
    while len(out) < 5:                       # 중복으로 줄어든 만큼 보충
        x = v + Rational(k, 12)
        if all(simplify(x - y) != 0 for y in out):
            out.append(x)
        k += 1
    return sorted(out, key=float)             # 원문제 보기도 오름차순 배열


def solve(prm):
    """조건 → 답(보기 번호 1~5)"""
    _validate(prm)
    v = value(prm)
    for i, c in enumerate(choices(prm)):
        if simplify(c - v) == 0:
            return i + 1
    raise ValueError(f'답 {v} 이 보기에 없음: {choices(prm)}')


def statement(prm):
    """그 파라미터로 만들어지는 문제 문장(한국어)"""
    _validate(prm)
    pa, pb, pab = prm['pa'], prm['pb'], prm['pab']
    if pab == 0:
        body = (f'두 사건 A, B에 대하여 P(A) = {pa}, P(B) = {pb}이고, '
                f'A, B는 서로 배반이다.')
    else:
        body = (f'두 사건 A, B에 대하여 P(A) = {pa}, P(B) = {pb}이고 '
                f'P(A∩B) = {pab}일 때,')
    q = 'P(A^C ∩ B)의 값은? (단, A^C은 A의 여사건이다.) [3점]'
    marks = ['①', '②', '③', '④', '⑤']
    line = '   '.join(f'{m} {c}' for m, c in zip(marks, choices(prm)))
    return f'{body}\n{q}\n{line}'


# 규칙 4: 유도한 보기가 원문제 보기와 일치하는지 고정
assert choices(PARAMS) == [Rational(1, 6), Rational(1, 4), Rational(1, 3),
                           Rational(1, 2), Rational(2, 3)]

# 규칙 5: 성립하는 조합 3개. V1 은 pb 를, V2·V3 는 pab 를 바꿔 원문제와 다른 답을 낸다.
VARIANTS = [
    dict(pa=Rational(1, 3), pb=Rational(1, 2), pab=Rational(0)),      # 배반, 답 1/2 → ④
    dict(pa=Rational(1, 3), pb=Rational(2, 3), pab=Rational(1, 3)),    # 겹침, 답 1/3 → ②
    dict(pa=Rational(1, 6), pb=Rational(1, 2), pab=Rational(1, 6)),    # 겹침, 답 1/3 → ②
]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')

if __name__ == '__main__':
    print(statement(PARAMS))
    for i, ov in enumerate(VARIANTS, 1):
        prm = {**PARAMS, **ov}
        print(f'-- 변형 {i}: P(A)={prm["pa"]}, P(B)={prm["pb"]}, P(A∩B)={prm["pab"]} '
              f'→ 답 {solve(prm)} (값 {value(prm)})')
