from sympy import Matrix, Rational, Mod, nsimplify

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 좌표공간의 세 점 A,B,C 의 무게중심 G=(Gx,Gy,Gz) 에서 Gy=a, Gz=b 를 구해
# a+b 를 묻는 문제. x좌표의 합은 0(=Gx)으로 고정해 "G(0,a,b)" 형태를
# 유지하고, y·z좌표는 "무게중심 값(Gy,Gz)" 자체를 자유 파라미터로 삼아
# 세 점의 좌표를 역산한다 — 세 점의 y(또는 z)좌표 하나만 직접 흔들면
# 합이 3의 배수가 아니게 되어(나눗셈 분모 조건 위반) 답이 정수가 아닌
# 채로 깨지기 쉬우므로, 정수해가 항상 보장되는 "무게중심 값" 을 파라미터로
# 승격했다(오프셋 2,3,-5 는 항상 합이 0이 되도록 고정해 두어 Gy,Gz 값만
# 그대로 무게중심에 반영된다).
#
# 보기는 원문제(① 6 ② 7 ③ 8 ④ 9 ⑤ 10)처럼 "정답을 포함하는 연속된 정수
# 5개" 블록으로 구성한다. 그 블록 안에서 정답이 몇 번째(①~⑤)에 오는지는
# 정답 값의 (값-1) mod 5 나머지로 정해지므로, Gy·Gz 를 바꾸면 정답 숫자뿐
# 아니라 정답 "보기 번호"(=solve 의 반환값) 자체도 함께 바뀐다.
PARAMS = dict(
    Gy=4,               # 무게중심의 y좌표 (= 문제의 a)
    Gz=2,               # 무게중심의 z좌표 (= 문제의 b)
    Ax=2, Bx=-5, Cx=3,  # x좌표 (합이 0이 되도록 고정 → Gx = 0)
)

CANDIDATE = 1  # 원문제 정답: ①


def _points(prm):
    """Gy, Gz 로부터 원문제와 같은 형태의 세 점 좌표를 역산한다."""
    Gy, Gz = prm['Gy'], prm['Gz']
    Ax, Bx, Cx = prm['Ax'], prm['Bx'], prm['Cx']
    if Ax + Bx + Cx != 0:
        raise ValueError('x좌표의 합이 0이 아니면 G=(0, a, b) 형태가 성립하지 않는다')
    A = (Ax, Gy + 2, Gz - 5)
    B = (Bx, Gy + 3, Gz + 2)
    C = (Cx, Gy - 5, Gz + 3)
    return A, B, C


def value(prm):
    """세 점의 무게중심 G 에서 y,z 성분의 합 a+b (sympy 로 실제 계산)."""
    A, B, C = _points(prm)
    G = Rational(1, 3) * (Matrix(A) + Matrix(B) + Matrix(C))
    if G[0] != 0:
        raise ValueError(f'Gx != 0: {G[0]}')
    a, b = G[1], G[2]
    v = nsimplify(a + b)
    if not v.is_integer:
        raise ValueError(f'a+b 가 정수가 아니다: {v}')
    return v


def choices(prm):
    """정답을 포함하는 '연속 정수 5개' 블록. 블록 안 위치는 정답값의
    (값-1) mod 5 로 정해져 원문제의 '①에 정답' 배치를 그대로 재현한다."""
    v = value(prm)
    offset = Mod(v - 1, 5)
    start = v - offset
    return [start + i for i in range(5)]


def solve(prm):
    """조건 → 보기 번호(①=1 ... ⑤=5)."""
    v = value(prm)
    ch = choices(prm)
    return ch.index(v) + 1


# 유도한 보기가 원문제 보기(① 6 ② 7 ③ 8 ④ 9 ⑤ 10)와 같은지 고정
assert choices(PARAMS) == [6, 7, 8, 9, 10], choices(PARAMS)


def statement(prm):
    A, B, C = _points(prm)
    ch = choices(prm)
    labels = '①②③④⑤'
    opts = ' '.join(f'{labels[i]} {c}' for i, c in enumerate(ch))
    return (
        f'좌표공간의 세 점 A{A}, B{B}, C{C}를 꼭짓점으로 하는 '
        f'삼각형 ABC의 무게중심이 G(0, a, b)일 때, a+b의 값은?\n{opts}'
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
