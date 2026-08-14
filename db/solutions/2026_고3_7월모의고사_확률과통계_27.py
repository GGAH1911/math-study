"""2026 고3 7월모의고사 확률과통계 27번 — 파라미터화 솔버.

원문제: 남학생 4명, 여학생 3명이 원탁에 둘러앉을 때(회전하여 일치하면 같은 것),
        '자신과 이웃한 두 학생이 모두 남학생'인 여학생의 수가 정확히 1이 되는 경우의 수.

수학 구조: n = 남+여 명을 원형으로 배열(회전 동일시 → 특정 1명을 한 자리에 고정하고
           나머지 (n-1)! 개의 줄배열을 전수 확인). 각 여학생마다 좌우 이웃이 모두
           남학생인지 판정하여, 그런 여학생의 수가 target 과 같은 배열만 센다.
           males / females / target 을 바꾸면 곧바로 같은 유형의 새 문제가 된다.
"""
from itertools import permutations

CANDIDATE = 2

PARAMS = dict(
    males=4,        # 남학생 수
    females=3,      # 여학생 수
    target=1,       # 이웃한 두 학생이 모두 남학생인 여학생의 수(조건값)
    choices=[396, 432, 468, 504, 540],   # 보기 ①~⑤ (정답 번호는 solve 가 결정)
)


def count_seatings(males: int, females: int, target: int) -> int:
    """원탁(회전 동일시) 배열 중, 양쪽 이웃이 모두 남학생인 여학생이 정확히 target 명인 경우의 수."""
    n = males + females
    if n < 3 or males < 0 or females < 0 or target < 0 or target > females:
        return 0
    # 라벨: 0..males-1 = 남학생, males..n-1 = 여학생 (전원 서로 다른 사람)
    # 회전 동일시 → 0번 학생을 자리 0에 고정하고 나머지 (n-1)! 줄배열을 전수 조사
    rest = list(range(1, n))
    total = 0
    for perm in permutations(rest):
        seat = (0,) + perm
        c = 0
        for i in range(n):
            if seat[i] >= males:                       # 여학생 자리
                if seat[i - 1] < males and seat[(i + 1) % n] < males:
                    c += 1
        if c == target:
            total += 1
    return total


def solve(prm):
    value = count_seatings(prm['males'], prm['females'], prm['target'])
    choices = prm.get('choices') or []
    # 객관식: 계산값과 보기를 대조해 번호를 결정한다(번호는 파라미터가 아니다)
    if value in choices:
        return choices.index(value) + 1
    return value


def statement(prm):
    return (f"남학생 {prm['males']}명, 여학생 {prm['females']}명이 있다. "
            f"이 {prm['males'] + prm['females']}명의 학생이 일정한 간격을 두고 원 모양의 탁자에 "
            f"모두 둘러앉을 때, 자신과 이웃한 두 학생이 모두 남학생인 여학생의 수가 "
            f"{prm['target']}이 되도록 하는 경우의 수는? (단, 회전하여 일치하는 것은 같은 것으로 본다.)")


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
