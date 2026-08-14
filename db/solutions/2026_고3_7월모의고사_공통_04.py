# 구간별 함수 f(x) = p·x + a (x < b) / x² - a·x + c (x ≥ b) 가 실수 전체에서 연속이 되도록
# 하는 상수 a 를 구하고, 보기 값 목록에서 그 값의 번호를 답한다.
#
# ★파라미터화 솔버(scripts/CLAUDE.md 규격): PARAMS 를 바꾸면 같은 유형의 새 문제와
#   검증된 답이 그대로 나온다. 원문제는 PARAMS 기본값으로 재현된다.
#   연속 조건: p·b + a = b² - a·b + c  →  a(1 + b) = b² - p·b + c
CANDIDATE = 5
import sympy as sp

PARAMS = dict(
    p=2,            # 왼쪽 조각 p·x + a 의 x 계수
    b=1,            # 두 조각이 갈리는 지점 (x < b / x ≥ b)
    c=11,           # 오른쪽 조각 x² - a·x + c 의 상수항
    ch_start=1,     # 보기 ①의 값
    ch_step=1,      # 보기 사이 간격 → 보기 목록 = ①1 ②2 ③3 ④4 ⑤5
    n_choices=5,
)


def choices_of(prm):
    """보기 값 목록 (①..⑤)."""
    return [sp.nsimplify(prm['ch_start'] + i * prm['ch_step']) for i in range(int(prm['n_choices']))]


def solve(prm):
    x, a = sp.symbols('x a')
    left = prm['p'] * x + a                     # x < b 조각
    right = x**2 - a * x + prm['c']             # x ≥ b 조각
    b = sp.nsimplify(prm['b'])
    # x = b 에서만 연속이 문제되므로 좌극한 = 함숫값
    cond = sp.Eq(sp.limit(left, x, b, '-'), right.subs(x, b))
    sols = sp.solve(cond, a)
    if not sols:
        raise ValueError('연속이 되게 하는 a 가 없다')
    a_val = sp.nsimplify(sols[0])
    ch = choices_of(prm)
    for i, v in enumerate(ch, start=1):         # 보기와 대조해 번호를 정한다
        if sp.simplify(v - a_val) == 0:
            return i
    raise ValueError(f'보기 {ch} 에 정답 값 {a_val} 이 없다')


def statement(prm):
    ch = choices_of(prm)
    body = (f"함수 f(x) = {prm['p']}x + a (x < {prm['b']}), "
            f"x^2 - ax + {prm['c']} (x >= {prm['b']}) 가 실수 전체의 집합에서 연속일 때, "
            f"상수 a 의 값은?")
    return body + '  보기: ' + ' '.join(f'{i}) {v}' for i, v in enumerate(ch, start=1))


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
