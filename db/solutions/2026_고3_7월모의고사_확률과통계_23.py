"""2026 고3 7월모의고사 확률과통계 23번 — 독립사건의 교사건 확률 (파라미터 솔버)

구조: 두 사건 A, B 가 서로 독립  ⇒  P(A∩B) = P(A)·P(B).
파라미터(문제가 준 값): P(A), P(B) 의 분자·분모와 5지선다 보기 값.
정답 번호는 solve 가 계산값을 보기와 대조해 정한다(하드코딩 아님).
"""
from sympy import Rational

CANDIDATE = 5                      # 정답 보기 번호 (정답표 answer: "5")

PARAMS = dict(
    pa_num=2, pa_den=3,            # P(A) = 2/3
    pb_num=3, pb_den=4,            # P(B) = 3/4
    choices=[Rational(1, 4), Rational(5, 16), Rational(3, 8),
             Rational(7, 16), Rational(1, 2)],   # ①~⑤ 보기 값
)


def target_value(prm):
    """조건 → 구하는 값 P(A∩B). 독립이므로 곱셈정리가 곧 P(A)P(B)."""
    pa = Rational(prm['pa_num'], prm['pa_den'])
    pb = Rational(prm['pb_num'], prm['pb_den'])
    return pa * pb


def solve(prm):
    """계산값을 보기와 대조해 정답 번호(1~5)를 돌려준다. 보기에 없으면 0."""
    val = target_value(prm)
    for i, c in enumerate(prm['choices'], start=1):
        if Rational(c) == val:
            return i
    return 0


def statement(prm):
    """새 문제 문장 (searchable_text 형식)."""
    pa = Rational(prm['pa_num'], prm['pa_den'])
    pb = Rational(prm['pb_num'], prm['pb_den'])
    def tex(r):
        r = Rational(r)
        return str(r.p) if r.q == 1 else r'\frac{%d}{%d}' % (r.p, r.q)
    opts = ''.join('%s%s' % (m, tex(c))
                   for m, c in zip('①②③④⑤', prm['choices']))
    return ('두 사건 A, B는 서로 독립이고\n'
            'P(A)=%s,  P(B)=%s\n'
            '일 때, P(A∩B)의 값은? [2점]\n%s' % (tex(pa), tex(pb), opts))


def make_variant(pa_num, pa_den, pb_num, pb_den, distractors):
    """유사문제 생성기: 두 확률과 오답 4개(값)를 주면 PARAMS 를 만들어 준다.
    정답 값은 자동 계산해 오답들과 함께 오름차순으로 배열한다."""
    prm = dict(pa_num=pa_num, pa_den=pa_den, pb_num=pb_num, pb_den=pb_den, choices=[])
    val = target_value(prm)
    wrong = sorted({Rational(x) for x in distractors} - {val})[:4]
    prm['choices'] = sorted(wrong + [val])
    return prm


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
