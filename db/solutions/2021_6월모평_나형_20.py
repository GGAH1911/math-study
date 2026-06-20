from itertools import combinations

balls = [
    ('W', 1), ('W', 2), ('W', 3), ('W', 4),
    ('B', 3), ('B', 4), ('B', 5), ('B', 6)
]

all_draws = list(combinations(range(8), 4))

same_number_exists = []
for draw in all_draws:
    numbers_white = set()
    numbers_black = set()
    for idx in draw:
        color, num = balls[idx]
        if color == 'W':
            numbers_white.add(num)
        else:
            numbers_black.add(num)
    if numbers_white & numbers_black:
        same_number_exists.append(draw)

exactly_2_black = 0
for draw in same_number_exists:
    black_count = sum(1 for idx in draw if balls[idx][0] == 'B')
    if black_count == 2:
        exactly_2_black += 1

probability = exactly_2_black / len(same_number_exists)
expected = 17/29

if abs(probability - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')