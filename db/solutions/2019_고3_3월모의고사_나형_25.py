"""2019 고3 3월모의고사 나형 25번 — 파라미터화 솔버.

문제 구조:
  수열 {a_n} 이 점화식 a_{n+2} = a_{n+1} + a_n (피보나치형) 을 만족하고,
  첫째항 a_1 이 주어진 상태에서 a_4 의 값이 주어질 때 a_2 를 구한다.

  a_3 = a_2 + a_1
  a_4 = a_3 + a_2 = 2*a_2 + a_1
  → a_2 = (a_4 - a_1) / 2

파라미터로 뽑은 수학 구조:
  - a1  : 수열의 첫째항 (점화식의 초기값)
  - a4  : 목표로 주어지는 a_4 값
  둘 다 답 a_2 = (a4 - a1) / 2 를 직접 바꾼다.
  (a1, a4)의 홀짝이 같아야 a_2 가 정수가 되므로, 조건이 깨지면 예외를 던진다.
"""
import sympy as sp

CANDIDATE = 15  # 원문제 정답 (절대 변경 금지)

PARAMS = dict(
    a1=4,   # 첫째항
    a4=34,  # a_4 의 값
)


def solve(prm):
    a1 = sp.Integer(prm['a1'])
    a4_target = sp.Integer(prm['a4'])

    # 점화식 a_{n+2} = a_{n+1} + a_n 을 그대로 심볼로 전개한다.
    a2 = sp.symbols('a2')
    a3_expr = a2 + a1          # a_3 = a_2 + a_1
    a4_expr = a3_expr + a2     # a_4 = a_3 + a_2

    sols = sp.solve(sp.Eq(a4_expr, a4_target), a2)
    if not sols:
        raise ValueError("해가 존재하지 않습니다.")
    a2_val = sols[0]

    # 수열이 자연수(또는 정수) 항으로 성립해야 문제로서 유효하다.
    if not a2_val.is_integer:
        raise ValueError(f"a2가 정수가 아닙니다: a1={a1}, a4={a4_target} 조합은 유효하지 않습니다.")

    return int(a2_val)


def statement(prm):
    return (
        f"첫째항이 {prm['a1']}인 수열 {{a_n}}이 모든 자연수 n에 대하여\n"
        f"  a_(n+2) = a_(n+1) + a_n\n"
        f"을 만족시킨다. a_4 = {prm['a4']}일 때 a_2의 값을 구하시오."
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    print('answer =', solve(PARAMS))

    # 파라미터를 바꾸면 답이 실제로 달라지는지 확인
    variant1 = dict(a1=6, a4=42)   # a2 = (42-6)/2 = 18  (원문제와 다른 답)
    variant2 = dict(a1=4, a4=50)   # a2 = (50-4)/2 = 23  (원문제와 다른 답)
    print('variant1 ->', solve(variant1))
    print('variant2 ->', solve(variant2))

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
