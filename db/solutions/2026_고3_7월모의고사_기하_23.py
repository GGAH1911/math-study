"""2026 고3 7월 기하 23 — 두 평면벡터의 합의 모든 성분의 합 (객관식).

파라미터화: 두 벡터의 성분과 보기 값 목록이 문제를 결정한다.
solve 는 합벡터의 성분 합을 실제로 계산한 뒤 보기와 대조해 **보기 번호**를 돌려준다.
"""
import sympy as sp

CANDIDATE = 1

PARAMS = dict(
    ax=3, ay=1,          # 벡터 a 의 성분
    bx=-2, by=1,         # 벡터 b 의 성분
    choices=[3, 4, 5, 6, 7],   # ①~⑤ 보기 값
)


def solve(prm):
    a = sp.Matrix([sp.Integer(prm['ax']), sp.Integer(prm['ay'])])
    b = sp.Matrix([sp.Integer(prm['bx']), sp.Integer(prm['by'])])
    s = a + b                       # 합벡터: 성분끼리 더한다
    total = sp.simplify(sum(s))     # 모든 성분의 합
    for i, c in enumerate(prm['choices'], start=1):
        if sp.simplify(total - sp.nsimplify(c)) == 0:
            return i                # 보기 번호
    return None                     # 보기에 없음 = 문제로 성립하지 않음


def value(prm):
    """보기 번호가 아닌 '성분의 합' 실제 값 (유사문제 만들 때 보기 구성용)."""
    return int(prm['ax'] + prm['bx'] + prm['ay'] + prm['by'])


def statement(prm):
    return (f"두 벡터 a=({prm['ax']},{prm['ay']}), b=({prm['bx']},{prm['by']}) 에 대하여 "
            f"a+b 의 모든 성분의 합은? "
            + ' '.join(f'{n} {c}' for n, c in zip('①②③④⑤', prm['choices'])))


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
