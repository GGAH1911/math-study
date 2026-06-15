from itertools import combinations

CANDIDATE = 15

# 공의 개수
balls = {
    'white': 4,
    'black': 2,
    'blue': 2,
    'red': 1,
    'yellow': 1
}

colors = list(balls.keys())
count = 0

# 5가지 색 중 정확히 3가지를 선택
for selected_colors in combinations(colors, 3):
    max_counts = {c: balls[c] for c in selected_colors}
    
    # 선택된 3가지 색 각각에서 최소 1개, 최대 available개를 뽑아 합이 5
    for count_0 in range(1, max_counts[selected_colors[0]] + 1):
        for count_1 in range(1, max_counts[selected_colors[1]] + 1):
            for count_2 in range(1, max_counts[selected_colors[2]] + 1):
                if count_0 + count_1 + count_2 == 5:
                    count += 1

if count == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: calculated {count}, got {CANDIDATE}')