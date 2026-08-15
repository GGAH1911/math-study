"""
[문제] 수열 {a_n}은 a_1 = 1이고, 모든 자연수 n에 대하여
  a_{n+1} = (a_n)^2 + 1   (a_n이 짝수인 경우)
  a_{n+1} = 3*a_n - 1     (a_n이 홀수인 경우)
를 만족시킨다. a_4의 값은?  ① 10 ② 11 ③ 12 ④ 13 ⑤ 14   [정답 ⑤]

★파라미터화 구조
  이 문제의 수학적 뼈대는 "조건부(홀/짝) 점화식을 몇 단계 반복해 얻은 값이 무엇인가"이다.
  구조를 그대로 유지한 채 다음을 파라미터로 뽑았다:
    - a1        : 수열의 첫째항
    - n_steps   : a_1 에서 몇 번 점화식을 적용해 목표항(a_{1+n_steps})을 얻는지
    - odd_mult  : 홀수일 때 곱해지는 계수 (원문제 3)
    - odd_sub   : 홀수일 때 빼는 상수 (원문제 1)
    - even_add  : 짝수일 때 제곱에 더하는 상수 (원문제 1)

  객관식 보기는 "정답이 속한 5의 배수 구간의 다섯 정수" (예: 14 -> 10~14)로 자동 생성한다.
  즉 reference = value - (value mod 5), choices = [reference, ..., reference+4].
  원문제에서 14 = 2*5+4 이므로 reference=10, choices=[10,11,12,13,14], 정답은 그 중 5번째
  (14가 속한 자리, value mod 5 = 4 -> 인덱스 5) — 실제 보기·정답 번호와 정확히 일치한다.
"""
import sympy as sp

CANDIDATE = 5  # ★원문제 정답(보기 번호) — 절대 변경 금지

# 문제를 정하는 값들: 초기항, 반복 횟수, 홀/짝 점화식의 계수들
PARAMS = dict(
    a1=1,        # 첫째항
    n_steps=3,   # a_1 -> a_{1+n_steps} 까지 점화식 적용 횟수 (a_4 = 3번 적용)
    odd_mult=3,  # 홀수 분기: odd_mult * a_n - odd_sub
    odd_sub=1,
    even_add=1,  # 짝수 분기: a_n**2 + even_add
)


def value(prm):
    """조건부 점화식을 n_steps번 sympy로 실제 전개해 목표항의 값을 구한다."""
    a = sp.Integer(prm['a1'])
    for _ in range(prm['n_steps']):
        expr = sp.Piecewise(
            (a**2 + prm['even_add'], sp.Eq(sp.Mod(a, 2), 0)),   # 짝수인 경우
            (prm['odd_mult'] * a - prm['odd_sub'], True),        # 홀수인 경우
        )
        a = sp.nsimplify(expr)
        if not sp.Integer(a).is_integer:
            raise ValueError('수열 항이 정수가 아니게 되었다')
    return sp.Integer(a)


def choices(prm):
    """정답 값이 속한 '5의 배수 구간'의 연속된 다섯 정수를 보기로 생성한다."""
    v = value(prm)
    ref = v - sp.Mod(v, 5)
    return [int(ref + i) for i in range(5)]


def solve(prm):
    """정답 값이 보기 목록에서 몇 번째(1-based)인지 반환한다."""
    v = value(prm)
    idx = int(sp.Mod(v, 5)) + 1
    return idx


def statement(prm):
    return (
        f"수열 {{a_n}}은 a_1 = {prm['a1']}이고, 모든 자연수 n에 대하여\n"
        f"  a_(n+1) = (a_n)^2 + {prm['even_add']}   (a_n이 짝수인 경우)\n"
        f"  a_(n+1) = {prm['odd_mult']}*a_n - {prm['odd_sub']}   (a_n이 홀수인 경우)\n"
        f"를 만족시킨다. a_{1 + prm['n_steps']}의 값은?\n"
        + " ".join(f"{i+1}) {c}" for i, c in enumerate(choices(prm)))
    )


# 원문제 보기(①10 ②11 ③12 ④13 ⑤14)와 정확히 일치하는지 고정
assert choices(PARAMS) == [10, 11, 12, 13, 14]
assert value(PARAMS) == 14

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
