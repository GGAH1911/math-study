# -*- coding: utf-8 -*-
"""
[원문제 구조]
  실수 전체집합의 두 부분집합 A={a,b,c,d,e}, B={a+k,...,e+k} (a,b,c,d,e 는
  A-B 로 드러나는 세 원소 p,q,r 과, B와 겹치는 두 원소 d,e 로 이루어진다).
  (가) S(A)=37   (나) A-B={2,4,9}   (다) S(A∪B)=92   → k=8

  [풀이 구조]
  A-B={p,q,r} 이므로 A={p,q,r,d,e} 이고 d,e ∈ B. k≠0 이면 B의 원소 중
  {p,q,r} 과 값이 같을 수 있는 후보는 {p+k,q+k,r+k} 뿐이므로 d,e 는 이 셋 중
  두 개(x+k,y+k)이고 나머지 하나(z)가 "A-B 에서 살아남는" 원소가 된다.
  S(A)=p+q+r+d+e=S_A 를 풀면 각 (x,y,z) 배정마다 k 후보가 하나씩 나오고,
  그중 실제로 A-B={p,q,r} 과 S(A∪B)=S_union 을 모두 만족하는 배정만 참값이다.

  ★답을 바꾸는 파라미터: A-B의 세 원소 p,q,r 과 목표합 S_A, S_union 이다.
    이들은 서로 독립적으로 흔들어도 (조합에 따라) 항등식을 실제로 풀어서 k가
    달라짐을 아래 solve()가 직접 sympy 로 계산해 보여준다.

  ★보기(選択肢)는 "정답을 가운데 둔 6~10" 처럼 파라미터로 다시 만들 때마다
    재중심화하면 정답의 보기 번호가 항상 3번으로 고정되어 버려(대칭 구조라서)
    파라미터가 전부 "장식"으로 오판된다. 그래서 원문제와 동일한 고정 보기창
    CHOICES_WINDOW=(6,7,8,9,10) 을 그대로 두고, 계산된 k가 이 창 안에 실제로
    들어오는 위치(번호)를 답으로 삼는다 — 창을 벗어나면 이 유형으로 성립하지
    않는 것이므로 예외를 던진다(규칙 6).
"""

import sympy as sp

CANDIDATE = 3  # ★원문제 정답: ③ (k=8, 보기 6~10 중 세 번째)

PARAMS = dict(
    p=2,        # A-B = {p, q, r} 의 첫 원소
    q=4,        # A-B = {p, q, r} 의 둘째 원소
    r=9,        # A-B = {p, q, r} 의 셋째 원소
    S_A=37,     # 조건 (가): S(A)
    S_union=92,  # 조건 (다): S(A∪B)
)

# 이 문제 유형이 강제하는 고정 보기: 6부터 10까지의 연속한 정수.
CHOICES_WINDOW = (6, 7, 8, 9, 10)


def value(prm):
    """조건 (가)(나)(다)를 모두 만족하는 상수 k를 sympy 로 실제로 구한다."""
    p, q, r = sp.nsimplify(prm['p']), sp.nsimplify(prm['q']), sp.nsimplify(prm['r'])
    S_A = sp.nsimplify(prm['S_A'])
    S_union = sp.nsimplify(prm['S_union'])
    base = [p, q, r]
    if len({p, q, r}) != 3:
        raise ValueError('p, q, r 은 서로 달라야 A-B가 세 원소 집합이 된다')

    k = sp.symbols('k')
    found = []
    for i in range(3):
        z = base[i]
        x, y = [base[j] for j in range(3) if j != i]
        d_expr, e_expr = x + k, y + k
        # 조건 (가): S(A) = p+q+r+d+e = S_A
        sols = sp.solve(sp.Eq(p + q + r + d_expr + e_expr, S_A), k)
        for kv in sols:
            if kv == 0:
                continue  # k=0 이면 A=B가 되어 문제가 성립하지 않는다
            dv, ev = x + kv, y + kv
            A = {p, q, r, dv, ev}
            if len(A) != 5:
                continue
            B = {p + kv, q + kv, r + kv, dv + kv, ev + kv}
            # 조건 (나): A - B = {p, q, r} 이 실제로 성립하는지 집합으로 직접 확인
            if A - B != {p, q, r}:
                continue
            # 조건 (다): S(A∪B) = S_union
            if sp.simplify(sum(A | B) - S_union) != 0:
                continue
            found.append(sp.nsimplify(kv))

    found = sorted(set(found), key=lambda v: sp.N(v))
    if not found:
        raise ValueError('조건 (가)(나)(다)를 모두 만족하는 k가 존재하지 않는다')
    if len(found) > 1:
        raise ValueError(f'k가 유일하게 정해지지 않는다: {found}')
    return found[0]


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기: 6부터 10까지의 연속 정수."""
    return CHOICES_WINDOW


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"k={v} 가 보기 범위 {ch}를 벗어남 — 문제로 성립하지 않음")
    return ch.index(v) + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)


def statement(prm):
    p, q, r, S_A, S_union = prm['p'], prm['q'], prm['r'], prm['S_A'], prm['S_union']
    return (
        "집합 X의 모든 원소의 합을 S(X)라 할 때, 실수 전체의 집합의 두 부분집합\n"
        "A = {a, b, c, d, e}, B = {a+k, b+k, c+k, d+k, e+k}\n"
        "에 대하여 다음 조건을 만족시키는 상수 k의 값은?\n"
        f"(가) S(A)={S_A}\n"
        f"(나) A-B={{{p}, {q}, {r}}}\n"
        f"(다) S(A∪B)={S_union}\n"
        "① 6 ② 7 ③ 8 ④ 9 ⑤ 10"
    )


# 원문제 보기가 정확히 ①6 ②7 ③8 ④9 ⑤10 인지 고정 검증
assert choices(PARAMS) == (6, 7, 8, 9, 10)
# 원문제 값(k=8)이 정확히 재현되는지 고정 검증
assert value(PARAMS) == 8

# p, q, r, S_A, S_union 은 "조건 (가)(나)(다)를 동시에 만족시키는 k가 유일하게
# 존재해야 한다"는 조건으로 서로 묶여 있다(규칙 5). p 하나만 +1 하면 S_A, S_union
# 이 예전 값 그대로라 해가 아예 사라진다. 대신 실제로 성립하는 (p,q,r,S_A,S_union)
# 조합을 여러 개 제시해 "답이 실제로 달라짐"을 증명한다 — 서로 다른 k(6,7,9,10)가
# 나오므로 보기 번호(1,2,4,5)도 원문제(3번)와 실제로 달라진다.
VARIANTS = [
    dict(p=1, q=2, r=3, S_A=23, S_union=59),   # k=6  → ①
    dict(p=1, q=2, r=3, S_A=25, S_union=66),   # k=7  → ②
    dict(p=2, q=3, r=7, S_A=40, S_union=97),   # k=9  → ④
    dict(p=1, q=5, r=6, S_A=43, S_union=105),  # k=10 → ⑤
]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
