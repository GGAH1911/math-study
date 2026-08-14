"""2019 고3 4월모의고사 가형 25번 — 파라미터 솔버.

문제: 곡선 y = a*x^3 + b*ln(x) 의 변곡점에서의 접선의 기울기를 구하시오.
(원문제: a=1/3, b=2 → 답 3)

수학 구조:
  y'  = 3a x^2 + b/x
  y'' = 6a x   - b/x^2
  변곡점 후보: y''=0 → x^3 = b/(6a) → x = (b/(6a))^(1/3)  (x>0 도메인, a,b>0 이면 실근 하나)
  실제 변곡점이려면 그 후보 좌우에서 y'' 의 부호가 바뀌어야 함(검증).
  구하는 접선의 기울기 = y'(변곡점 x좌표).

파라미터화 지점: 3차항 계수 a, 로그항 계수 b — 둘 다 답(기울기 값)에 직접 영향을 준다.
"""
import sympy as sp


def solve(prm):
    a = sp.nsimplify(prm['a'])
    b = sp.nsimplify(prm['b'])
    if a == 0:
        raise ValueError('a=0이면 3차항이 사라져 변곡점 구조 자체가 성립하지 않음')
    if b == 0:
        raise ValueError('b=0이면 로그항이 사라져 정의역/변곡점 구조가 원문제와 달라짐')

    x = sp.symbols('x', positive=True)
    y = a * x ** 3 + b * sp.ln(x)
    y2 = sp.diff(y, x, 2)

    roots = [r for r in sp.solve(sp.Eq(y2, 0), x) if r.is_real]
    if not roots:
        raise ValueError('변곡점 후보(실근)가 존재하지 않음')
    xinf = roots[0]
    if not (xinf.is_positive):
        raise ValueError('변곡점 후보가 정의역(x>0) 밖에 있음')

    # 좌우 부호가 실제로 바뀌는지 확인해야 진짜 변곡점이다.
    eps = xinf * sp.Rational(1, 10)
    left_sign = sp.sign(y2.subs(x, xinf - eps))
    right_sign = sp.sign(y2.subs(x, xinf + eps))
    if left_sign == right_sign or left_sign == 0 or right_sign == 0:
        raise ValueError('이차미분 부호가 바뀌지 않아 변곡점이 아님')

    slope = sp.diff(y, x).subs(x, xinf)
    return sp.nsimplify(sp.simplify(slope))


def statement(prm):
    a = sp.nsimplify(prm['a'])
    b = sp.nsimplify(prm['b'])
    b_sign = '+' if b >= 0 else '-'
    return (
        f"곡선 y={sp.sstr(a)}x^3 {b_sign} {sp.sstr(abs(b))}\\ln x 의 "
        f"변곡점에서의 접선의 기울기를 구하시오."
    )


CANDIDATE = 3
PARAMS = dict(a=sp.Rational(1, 3), b=2)

assert solve(PARAMS) == CANDIDATE, solve(PARAMS)
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
