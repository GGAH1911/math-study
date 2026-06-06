# 원래 조건들로부터 유도한 값이 조건을 만족하는지 검증
S_2_to_20 = 160  # sum of a_2 to a_20
T_1_to_19 = 170  # sum of b_1 to b_19

# 조건 1: 2*sum(a_{k+1} for k=1..19) - sum(b_k for k=1..19) = 150
# sum(a_{k+1} for k=1..19) = sum(a_j for j=2..20) = S_2_to_20
cond1 = 2 * S_2_to_20 - T_1_to_19

# 조건 2: sum(a_{k+1} for k=1..19) + sum(b_k for k=1..19) = 330
cond2 = S_2_to_20 + T_1_to_19

# 최종 답: sum(a_k for k=1..20) = a_1 + sum(a_k for k=2..20)
answer = 3 + S_2_to_20

if cond1 == 150 and cond2 == 330 and answer == 163:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')