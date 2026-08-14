"""2019 고3 10월모의고사 가형 28번 — 파라미터 솔버.

[문제 구조]
  도형은 단위정사각형 여러 칸으로 이루어져 있다. 조각은 두 종류:
    · ◇ 정사각형 조각 1개 — 도형의 칸 중 한 곳을 통째로 채운다.
    · 직각이등변삼각형 조각 여러 개 — 나머지 칸을 하나씩 대각선으로 2등분해 채운다.
      각 삼각형에는 ○·☆·◎ 표시가 있고 (circ·star·double 개), ◎끼리는 서로 구별하지 않는다.

  경우의 수 = (◇를 놓을 수 있는 자리 수 pos)
            × (대각선 분할된 칸마다 절단 방향 2가지 → 2**split_cells)
            × (2*split_cells개 삼각슬롯에 ○·☆·◎ 표시를 배치하는 다중순열
               (2*split_cells)! / (circ! star! double!))

  삼각형 총 개수 circ+star+double 은 항상 짝수여야 하고(대각선 분할 칸 수의 2배),
  split_cells = (circ+star+double)/2 로 자동 결정된다 — circ·star·double 중 하나만
  바뀌어도 전체 삼각형 수·분할 칸 수·대각선 경우의 수가 함께 바뀐다(묶인 구조이지만
  홀수 합이 아닌 한 항상 유효한 새 문제가 되므로 자유 파라미터로 둘 수 있다).

[파라미터]
  pos    : ◇ 정사각형 조각을 놓을 수 있는 자리(칸)의 수                — 원문제 4
  circ   : ○ 조각 개수                                                — 원문제 1
  star   : ☆ 조각 개수                                                — 원문제 1
  double : ◎ 조각 개수 (서로 구별하지 않음)                            — 원문제 4
"""
from sympy import factorial, Integer

CANDIDATE = 960  # ★원문제 정답 — 절대 바꾸지 않음

PARAMS = dict(
    pos=4,
    circ=1,
    star=1,
    double=4,
)


def solve(prm):
    pos = Integer(prm['pos'])
    circ = Integer(prm['circ'])
    star = Integer(prm['star'])
    double = Integer(prm['double'])
    if pos <= 0 or circ < 0 or star < 0 or double < 0:
        raise ValueError('자리 수·조각 개수는 음이 아닌 정수여야 한다')
    total_tri = circ + star + double           # 직각이등변삼각형 총 개수
    if total_tri <= 0 or total_tri % 2 != 0:
        raise ValueError('삼각형 총 개수가 짝수가 아니면 칸을 대각선으로 나눌 수 없다')
    split_cells = total_tri // 2                # 대각선으로 나뉘는 칸 수
    diag = 2 ** split_cells                      # 칸마다 대각선 방향 2가지
    label = factorial(total_tri) // (factorial(circ) * factorial(star) * factorial(double))
    return int(pos * diag * label)


def statement(prm):
    circ, star, double = prm['circ'], prm['star'], prm['double']
    total = circ + star + double
    return (
        f"빗변의 길이가 \\sqrt{{2}}인 직각이등변삼각형 모양의 조각 {total}개와 "
        f"한 변의 길이가 1인 정사각형 모양의 조각 1개가 있다. 직각이등변삼각형 모양의 조각 중 "
        f"○, ☆, ◎가 그려진 조각은 각각 {circ}개, {star}개, {double}개가 있고, "
        f"정사각형 모양의 조각에는 ◇가 그려져 있다. "
        f"이 조각을 모두 사용하여, 정사각형 조각을 놓을 수 있는 자리가 {prm['pos']}곳 있고 "
        f"나머지 칸은 각각 대각선으로 삼각형 2개씩 나뉘는 도형을 빈틈없이 채우려고 한다. "
        f"이 도형을 빈틈없이 채우는 경우의 수를 구하시오. "
        f"(단, ◎가 그려진 조각은 서로 구별하지 않고, 각 조각은 뒤집지 않는다.)"
    )


if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
