"""2019 고3 4월모의고사 가형 28번 — 파라미터화 솔버.

문제 구조:
  - 영화관 좌석이 A열(앞), B열(뒤) 두 열로 이루어져 있고 각 열에 ncols 개의 좌석이
    같은 열(column)끼리 마주보게 배열되어 있다.
  - A열에는 front_group 명(할아버지·할머니)이 서로 이웃하여 앉는다. "이웃"을
    front_group>2 로 일반화하면 '연속한 좌석 블록을 이룬다'는 뜻이 된다
    (front_group=2 일 때는 원문제의 단순 인접 조건과 동일).
  - B열에는 back_group 명(아버지·어머니·아이)이 앉되, 그중 마지막 한 명(아이)은
    나머지 back_group-1 명(부모) 중 적어도 한 명과 이웃(열 번호 차 1)해야 한다.
  - avoid_front_seat 이 참이면, 아이가 앉은 열(column)의 A열 좌석(=아이 바로 앞자리)이
    비어 있어야 하므로 아이의 column 은 A열 착석자들의 column 집합에 속하면 안 된다.

  이 네 값(ncols, front_group, back_group, avoid_front_seat)이 문제의 수학 구조를
  결정하는 파라미터다. 실제 경우의 수는 sympy 로 조합적 카운팅을 수행해 구한다
  (숫자를 박아 넣지 않고, front_group! · back_group! 순열을 직접 나열/검사한다).
"""
from itertools import permutations
import sympy as sp


def solve(prm):
    ncols = prm['ncols']
    front_group = prm['front_group']
    back_group = prm['back_group']
    avoid_front_seat = prm['avoid_front_seat']

    if front_group < 2 or back_group < 2:
        raise ValueError('front_group, back_group 은 2 이상이어야 이웃 조건이 의미를 가진다')
    if front_group > ncols or back_group > ncols:
        raise ValueError('한 열의 인원이 좌석 수(ncols)를 초과할 수 없다')

    cols = list(range(1, ncols + 1))
    total = sp.Integer(0)

    # A열: front_group 명이 '연속한 블록'(서로 이웃)을 이루며 앉는 모든 경우.
    #  front_group=2 일 때는 |gf-gm|==1 과 동일한 조건이 된다(연속 블록 = 두 자리 인접).
    for front_cols in permutations(cols, front_group):
        if max(front_cols) - min(front_cols) != front_group - 1:
            continue  # 연속 블록이 아니면 '이웃'이 아님
        occupied_front = set(front_cols)

        # B열: back_group 명 중 마지막 한 명(아이)이 나머지(부모)와 이웃해야 함
        for back_cols in permutations(cols, back_group):
            child_col = back_cols[-1]
            parents_cols = back_cols[:-1]
            if not any(abs(child_col - p) == 1 for p in parents_cols):
                continue
            if avoid_front_seat and child_col in occupied_front:
                continue
            total += 1

    return int(total)


def statement(prm):
    return (
        f"할아버지, 할머니, 아버지, 어머니, 아이로 구성된 {prm['front_group'] + prm['back_group']}명의 가족이 "
        f"영화를 보려고 한다. 영화관의 좌석은 A, B 두 개의 열로 이루어져 있고, 각 열에는 {prm['ncols']}개의 좌석이 "
        f"있다. A열에는 할아버지와 할머니를 포함한 {prm['front_group']}명이 이웃하여 앉고, B열에는 아버지, 어머니를 "
        f"포함한 {prm['back_group']}명이 앉되 아이는 부모 중 한 명과 이웃하고, "
        + ("아이의 바로 앞에 있는 좌석은 비어 있도록 한다. " if prm['avoid_front_seat'] else "")
        + "이때, 모두 좌석에 앉는 경우의 수를 구하시오. (단, 2명이 같은 열의 바로 옆에 앉을 때만 이웃한 것으로 "
        "본다. 또한 한 좌석에는 한 명만 앉고, 다른 관람객은 없다.)"
    )


CANDIDATE = 192

# 원문제: 좌석 5개인 두 열, A열 2명(조부모) 인접, B열 3명(부모2+아이) 중 아이가
# 부모와 이웃 + 아이 앞자리(A열) 공석 조건.
PARAMS = dict(
    ncols=5,
    front_group=2,
    back_group=3,
    avoid_front_seat=True,
)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
