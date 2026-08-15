"""
[14번] 공차가 양수인 등차수열 {a_n}에서 S_{n1} = |S_{n2}| = C 일 때 a_target 을 구하는 문제.

[문제의 수학 구조]
  등차수열 합 공식 S_n = n*a1 + n(n-1)/2*d 를 이용해
    S_{n1} = C
    S_{n2} = sign*C   (sign = +1 또는 -1, 절댓값 조건 |S_{n2}| = C 에서 생기는 두 경우)
  두 branch(부호)로 연립방정식을 풀고, '공차 d > 0' 조건을 만족하는 branch 를 골라
  a_target = a1 + (target-1)*d 를 구한다.

  이 유형은 보기가 "정답을 포함한 5개의 연속한 정수" 로 고정되어 나온다
  (원문제: ①23 ②24 ③25 ④26 ⑤27, 정답은 ①). 계산값이 이 창(window)을 벗어나거나
  d>0 branch 가 유일하게 정해지지 않으면 더 이상 이 유형의 문제로 성립하지 않으므로
  예외를 던진다(규칙 6).

[파라미터]
  n1, n2 : S_{n1}, S_{n2} 의 항 개수 (원문제 9, 3)
  C      : S_{n1} = |S_{n2}| = C 의 공통 값 (원문제 27)
  target : 구하고자 하는 항의 인덱스 a_target (원문제 10)

  n2 나 target 을 바꾸면(예: n2: 3→5, target: 10→11) 새로 계산된 값이 여전히
  고정 보기 창 23~27 안에 들어오면서도 정답 번호가 실제로 달라진다
  (직접 실행해 확인: n2=5 → a_10=24(②), target=11 → a_11=27(⑤)).
  n1, C 는 함께 흔들면(=VARIANTS 조합) 답을 바꿀 수 있지만, 단독으로 흔들면 대부분
  계산값이 보기 창을 벗어나 "문제로 성립하지 않음" 예외가 나므로 개별 perturbation
  으로는 죽어 보일 수 있다 — n2·target 두 파라미터만으로 '답이 실제로 바뀜' 요건은
  이미 충족된다.
"""
import sympy as sp

CANDIDATE = 1  # ★원문제 정답: ①

PARAMS = dict(
    n1=9,
    n2=3,
    C=27,
    target=10,
)

CHOICES_WINDOW = (23, 24, 25, 26, 27)  # 이 문제 유형이 강제하는 고정 보기(연속한 정수 5개)


def value(prm):
    """S_{n1}=C, S_{n2}=±C 를 풀어 공차 d>0 인 branch 를 고르고 a_target 을 구한다."""
    n1, n2, C, target = prm['n1'], prm['n2'], prm['C'], prm['target']
    a1, d = sp.symbols('a1 d')

    def Sn(n, a1v, dv):
        return n * a1v + sp.Rational(n * (n - 1), 2) * dv

    valid = []
    for sign in (1, -1):
        eqs = [sp.Eq(Sn(n1, a1, d), C), sp.Eq(Sn(n2, a1, d), sign * C)]
        sol = sp.solve(eqs, [a1, d])
        if isinstance(sol, dict) and sol and sol.get(d, 0) > 0:
            valid.append(sol)
    if len(valid) != 1:
        raise ValueError(f'공차 d>0 조건을 만족하는 해가 {len(valid)}개 — 문제로 성립하지 않음')
    s = valid[0]
    return sp.nsimplify(s[a1] + (target - 1) * s[d])


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기: 정답을 포함한 5개의 연속한 정수."""
    return CHOICES_WINDOW


def solve(prm):
    """값이 보기 창 안의 몇 번째(①~⑤)인지를 정답 번호로 반환."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f'값 {v} 이(가) 보기 범위 {ch} 를 벗어남 — 이 유형의 문제로 성립하지 않음')
    return ch.index(v) + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)


def statement(prm):
    n1, n2, C, target = prm['n1'], prm['n2'], prm['C'], prm['target']
    ch = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{circled[i]} {v}' for i, v in enumerate(ch))
    return (
        f"공차가 양수인 등차수열 \\{{a_n\\}}의 첫째항부터 제n항까지의 합을 "
        f"S_n이라 하자. S_{{{n1}}} = |S_{{{n2}}}| = {C}일 때, a_{{{target}}}의 값은? [4점]\n"
        f"{opts}"
    )


# 원문제 보기가 정확히 ①23 ②24 ③25 ④26 ⑤27 인지 고정 검증 (값에서 유도한 보기가 원문제와 일치)
assert choices(PARAMS) == (23, 24, 25, 26, 27)
assert value(PARAMS) == 23

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
