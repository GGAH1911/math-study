from fractions import Fraction

# ── 문제 구조 ──────────────────────────────────────────────────────
# 두 사건 A, B가 서로 독립이고 P(A)=a, P(A∪B)=u 가 주어질 때 P(B)를 구하는 문제.
#   독립조건 : P(A∩B) = a·P(B)
#   덧셈정리 : u = a + P(B) - a·P(B) = a + P(B)(1-a)
#   ⇒ P(B) = (u - a) / (1 - a)                       ... 실제 정답(value)
#
# 보기 ①~⑤(원문제: 2/9, 1/3, 4/9, 5/9, 2/3)는 정답 하나와, 이 문제 유형에서
# 자주 나오는 오답 계산 결과 4가지를 함께 늘어놓은 것이다. a, u 만으로 역산하면
# 정확히 원문제 보기 5개가 재현된다:
#   1-u        : 여사건(합사건의 여집합)과 착각
#   a+u-1      : 교집합 공식 P(A∩B)=P(A)+P(B)-P(A∪B) 을 P(B) 자리에 잘못 대입
#   2a-u       : 교집합을 P(A)로 착각(P(A∩B)≈P(A))하고 덧셈정리를 거꾸로 적용
#   a          : 구하라는 P(B) 대신 주어진 P(A)를 그대로 답으로 착각
#
# ★파라미터화 포인트: P(A), P(A∪B) 두 확률(분자/분모 4개)이 문제를 결정한다.
#   이 값들이 바뀌면 정답 값뿐 아니라 5개 보기의 상대적 크기 순서까지 바뀌므로
#   "정답이 몇 번째 보기인가"(solve 의 반환값)도 함께 바뀐다.

PARAMS = dict(
    P_A_num=2, P_A_den=3,      # P(A) = 2/3
    P_AuB_num=7, P_AuB_den=9,  # P(A∪B) = 7/9
)


def _inputs(prm):
    a = Fraction(prm['P_A_num'], prm['P_A_den'])
    u = Fraction(prm['P_AuB_num'], prm['P_AuB_den'])
    if not (0 < a < 1):
        raise ValueError('P(A)는 (0,1) 구간의 확률이어야 함')
    if not (a <= u <= 1):
        raise ValueError('P(A∪B)는 P(A) 이상 1 이하이어야 함(합사건은 원사건을 포함)')
    return a, u


def value(prm):
    """실제 수학적 답: 독립조건 + 덧셈정리로 구한 P(B)."""
    a, u = _inputs(prm)
    pb = (u - a) / (1 - a)
    if not (0 < pb < 1):
        raise ValueError('P(B)가 유효한 확률(0,1) 범위를 벗어남 — 성립하지 않는 조합')
    return pb


def choices(prm):
    """정답 + 전형적 오답 4가지를 a, u 로부터 유도해 오름차순으로 나열한 보기."""
    a, u = _inputs(prm)
    v = value(prm)
    exprs = [1 - u, v, a + u - 1, 2 * a - u, a]
    uniq = sorted(set(exprs))
    if len(uniq) != 5:
        raise ValueError('보기 5개가 서로 구별되지 않음 — 유효한 문제가 아님')
    return uniq


# 원문제 보기(①2/9 ②1/3 ③4/9 ④5/9 ⑤2/3)가 그대로 재현되는지 고정
_ORIG_CHOICES = [Fraction(2, 9), Fraction(1, 3), Fraction(4, 9), Fraction(5, 9), Fraction(2, 3)]
assert choices(PARAMS) == _ORIG_CHOICES, '원문제 보기 재현 실패'


def solve(prm):
    """정답이 보기 중 몇 번째(1-based)인지를 돌려준다 — 객관식 정답 번호."""
    v = value(prm)
    ch = choices(prm)
    return ch.index(v) + 1


def statement(prm):
    a, u = _inputs(prm)
    return (
        '두 사건 A, B가 서로 독립이고\n'
        f'  P(A)={a}, P(A∪B)={u}\n'
        '일 때, P(B)의 값은?'
    )


CANDIDATE = 2  # 원문제 정답: ② (P(B)=1/3)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
