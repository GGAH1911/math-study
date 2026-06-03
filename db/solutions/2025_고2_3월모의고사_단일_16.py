from itertools import combinations

# 5개 동아리: 제육 0,1,2 / 음악 3,4
gyeuk = [0, 1, 2]  # 제육 동아리
music = [3, 4]     # 음악 동아리

# 각 명이 선택 가능한 3개 조합
valid_selections = []
for r_gyeuk in range(1, 4):  # 제육 1~3개
    for r_music in range(1, 3):  # 음악 1~2개
        if r_gyeuk + r_music == 3:
            for g_comb in combinations(gyeuk, r_gyeuk):
                for m_comb in combinations(music, r_music):
                    valid_selections.append(frozenset(g_comb + m_comb))

count = 0
for sa in valid_selections:
    for sb in valid_selections:
        # 조건 (가): 서로 다른 3개 선택
        if sa == sb:
            continue
        # 조건 (나): A가 선택하고 B가 선택하지 않은 동아리 최소 1개
        if len(sa - sb) >= 1:
            count += 1

if count == 72:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')