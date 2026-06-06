from sympy import symbols, solve

# 등차수열 설정
a_1 = -42
d = 6

# 조건 (가) 검증: S_7과 S_8이 최솟값
S_7 = 7*a_1 + (7*6//2)*d
S_8 = 8*a_1 + (8*7//2)*d
S_6 = 6*a_1 + (6*5//2)*d
S_9 = 9*a_1 + (9*8//2)*d

if S_7 == S_8 and S_7 <= S_6 and S_8 <= S_9:
    condition_a = True
else:
    condition_a = False

# 조건 (나) 검증: |S_9| = |S_18| = 162
m = 9
S_m = m*a_1 + (m*(m-1)//2)*d
S_2m = 2*m*a_1 + (2*m*(2*m-1)//2)*d

condition_b = (abs(S_m) == 162 and abs(S_2m) == 162 and m > 8)

# 최종 답
a_13 = a_1 + 12*d

if condition_a and condition_b:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')