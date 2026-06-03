from math import comb

# 주머니 A: 흰공 2, 검은공 4
prob_white_A = comb(2, 2) / comb(6, 2)
prob_dice_A = 2 / 6  # 5, 6

# 주머니 B: 흰공 3, 검은공 3
prob_white_B = comb(3, 2) / comb(6, 2)
prob_dice_B = 4 / 6  # 1, 2, 3, 4

# P(5이상 AND 흰공 2개)
p_a_and_white = prob_dice_A * prob_white_A

# P(5미만 AND 흰공 2개)
p_b_and_white = prob_dice_B * prob_white_B

# P(흰공 2개)
p_white = p_a_and_white + p_b_and_white

# P(5이상 | 흰공 2개)
conditional_prob = p_a_and_white / p_white

# 답: 1/7
expected = 1 / 7

if abs(conditional_prob - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')