from math import comb

# 흰 공 분배: 각 주머니에 최소 1개
# w_A + w_B + w_C + w_D = 5, 모두 >= 1
# 치환: w'_i = w_i - 1 >= 0
# w'_A + w'_B + w'_C + w'_D = 1
white_cases = comb(1 + 4 - 1, 4 - 1)
print(f'White distribution cases: {white_cases}')  # Should be 4

# 각 흰 공 분배에 따른 w_A + w_B + w_C
white_sum_cases = {}
for i in range(4):
    if i < 3:
        white_sum = 4  # A, B, C 중 하나에 추가
    else:
        white_sum = 3  # D에 추가
    white_sum_cases[i] = white_sum

# 검은 공 분배
total = 0
for case, ws in white_sum_cases.items():
    b_d = ws  # 조건 (나)
    black_for_abc = 10 - b_d
    # b_A + b_B + b_C = black_for_abc, 모두 >= 0
    black_cases = comb(black_for_abc + 3 - 1, 3 - 1)
    if ws == 3:
        total += 1 * black_cases
    else:  # ws == 4
        total += 1 * black_cases

print(f'Case w_sum=3: 1 × {comb(9, 2)} = {1 * comb(9, 2)}')
print(f'Case w_sum=4: 3 × {comb(8, 2)} = {3 * comb(8, 2)}')
print(f'Total: {1 * comb(9, 2) + 3 * comb(8, 2)}')

if total == 120:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')