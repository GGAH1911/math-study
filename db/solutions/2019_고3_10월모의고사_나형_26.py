from itertools import combinations
from sympy import symbols, expand

CANDIDATE = 15  # ★원문제 정답, 절대 바꾸지 않음

# 문제의 수학 구조
#  - 주머니에 5가지 색의 공이 각각 정해진 개수만큼 들어있다.
#  - 그중 DRAW개를 꺼내는데, 꺼낸 공의 색이 정확히 K가지여야 한다.
#  - 답을 바꾸는 파라미터: 각 색깔 공의 개수(white/black/blue/red/yellow),
#    총 뽑는 개수(draw), 원하는 색의 가짓수(k)
PARAMS = dict(
    white=4,   # 흰 공 개수
    black=2,   # 검은 공 개수
    blue=2,    # 파란 공 개수
    red=1,     # 빨간 공 개수
    yellow=1,  # 노란 공 개수
    draw=5,    # 꺼내는 공의 총 개수
    k=3,       # 꺼낸 공에 나타나야 하는 색의 가짓수
)


def _balls(prm):
    # 색 이름 -> 개수. 순서는 문장 서술 순서로도 사용.
    return {
        '흰': prm['white'],
        '검은': prm['black'],
        '파란': prm['blue'],
        '빨간': prm['red'],
        '노란': prm['yellow'],
    }


def solve(prm):
    balls = _balls(prm)
    draw = prm['draw']
    k = prm['k']
    colors = list(balls.keys())

    if not (1 <= k <= len(colors)):
        raise ValueError("색의 가짓수 k가 유효 범위를 벗어남")

    x = symbols('x')
    total = 0

    # 5가지 색 중 정확히 k가지를 선택
    for selected_colors in combinations(colors, k):
        # 선택된 각 색은 최소 1개, 최대 보유 개수만큼 뽑을 수 있다.
        # 각 색의 생성함수: x + x^2 + ... + x^(보유개수)
        poly = 1
        for c in selected_colors:
            n = balls[c]
            if n < 1:
                raise ValueError("공의 개수는 1개 이상이어야 함")
            gf = sum(x ** i for i in range(1, n + 1))
            poly = expand(poly * gf)

        # 총 draw개를 뽑는 경우의 수 = x^draw의 계수
        coeff = poly.coeff(x, draw)
        total += coeff

    if total == 0:
        raise ValueError("성립하는 경우가 없는 파라미터 조합")

    return int(total)


def statement(prm):
    balls = _balls(prm)
    total_balls = sum(balls.values())
    parts = ", ".join(f"{name} 공 {n}개" for name, n in balls.items())
    return (
        f"{parts}, 총 {total_balls}개의 공이 들어있는 주머니가 있다. "
        f"이 주머니에서 {prm['draw']}개의 공을 꺼낼 때, 꺼낸 공의 색이 "
        f"{prm['k']}종류인 경우의 수를 구하시오. "
        f"(단, 같은 색의 공은 구별하지 않는다.)"
    )


print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else f'VERIFY_FAIL: calculated {solve(PARAMS)}, got {CANDIDATE}')
