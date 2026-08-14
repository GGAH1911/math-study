"""2019 고3 3월모의고사 가형 26번 — 파라미터화 솔버.

문제: 0 \\le x \\le \\pi 일 때, 2 이상의 자연수 n에 대하여
      두 곡선 y=\\sin x, y=\\sin(nx) 의 교점 개수를 a_n 이라 하자.
      a_{n1} + a_{n2} 의 값을 구하시오.

수학 구조:
  sin(nx) = sin(x)  ⟺  nx = x + 2kπ  또는  nx = π - x + 2kπ
    (n-1)x = 2kπ      → x = 2kπ/(n-1)
    (n+1)x = (2k+1)π  → x = (2k+1)π/(n+1)
  x ∈ [0, π] 범위, 즉 t := x/π ∈ [0, 1] 인 유리수 해의 개수(중복 제거)가 a_n.

파라미터로 뽑은 것: 두 지수 n1, n2 (원문제는 n1=3, n2=5).
  n1, n2 를 바꾸면 각 a_n 값이 달라지고 따라서 합 a_n1+a_n2 도 달라진다
  (아래 VARIANTS 로 실제 다른 답이 나옴을 확인).
"""
import sympy as sp


def a(n):
    # y=sin x 와 y=sin(nx) 가 [0, π]에서 만나는 점의 개수
    if n < 2:
        raise ValueError('n은 2 이상의 자연수여야 합니다.')
    sols = set()                       # x/π 값(유리수)으로 저장, 중복 자동 제거
    k = 0                               # nx = x + 2kπ  →  x/π = 2k/(n-1)
    while sp.Rational(2 * k, n - 1) <= 1:
        sols.add(sp.Rational(2 * k, n - 1))
        k += 1
    k = 0                               # nx = π - x + 2kπ  →  x/π = (2k+1)/(n+1)
    while sp.Rational(2 * k + 1, n + 1) <= 1:
        sols.add(sp.Rational(2 * k + 1, n + 1))
        k += 1
    return len(sols)


def solve(prm):
    n1, n2 = prm['n1'], prm['n2']
    return a(n1) + a(n2)


def statement(prm):
    n1, n2 = prm['n1'], prm['n2']
    return (
        r'0 \le x \le \pi 일 때, 2 이상의 자연수 n에 대하여 '
        r'두 곡선 y=\sin x 와 y=\sin(nx) 의 교점의 개수를 a_n이라 하자. '
        f'a_{{{n1}}}+a_{{{n2}}}의 값을 구하시오.'
    )


CANDIDATE = 9                      # ★원문제 정답, 절대 변경 금지
PARAMS = dict(n1=3, n2=5)          # 원문제: a_3 + a_5

assert solve(PARAMS) == CANDIDATE, solve(PARAMS)

# 파라미터가 답을 실제로 바꾸는지 확인 (원문제와 다른 답이 나오는 조합들)
VARIANTS = [
    dict(n1=2, n2=5),   # a_2+a_5 = 3+5 = 8  (n1 변경 → 답 변화)
    dict(n1=3, n2=6),   # a_3+a_6 = 4+7 = 11 (n2 변경 → 답 변화)
    dict(n1=4, n2=5),   # a_4+a_5 = 5+5 = 10
]
for v in VARIANTS:
    assert solve(v) != CANDIDATE, (v, solve(v))

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
