"""2019 고3 10월모의고사 가형 28번 — 파라미터 솔버 (수동).
T자 도형(정사각형 4칸) 채우기. ◇정사각형 1개 + 직각이등변삼각형 6개(1○·1☆·4◎, ◎구별X, 뒤집기X).
면적: 사각형1 + 삼각형6×½=3 = 4 ✓. ◇가 1칸 채우고 나머지 3칸은 각각 대각선으로 2삼각분할.
경우의 수 = (◇ 위치 4) × (3칸 대각선 방향 2³=8) × (6 삼각슬롯에 ○·☆·◎⁴ 배치 6!/4!=30) = 960.
삼각슬롯은 회전대칭 없어 조각당 배치 유일(뒤집기 금지) → 라벨링만 셈."""
from math import factorial
def solve(ncells=4, split_cells=3, circ=1, star=1, double=4):
    pos = ncells                                  # ◇ 들어갈 칸
    diag = 2**split_cells                          # 분할 칸당 대각선 2방향
    slots = 2*split_cells                          # 삼각 슬롯 수 = 6
    label = factorial(slots)//(factorial(circ)*factorial(star)*factorial(double))
    return pos * diag * label
assert solve()==960, solve()
print('VERIFY_PASS')
