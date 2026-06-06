# 주어진 조건을 검증
# S_a = 70, S_b = 40일 때
S_a = 70
S_b = 40

# 첫 번째 조건 검증: sum(a_k - b_k + 2) = 50
cond1 = (S_a - S_b) + 10*2
print(f'첫 번째 조건: {cond1} (기대값: 50)')

# 두 번째 조건 검증: sum(a_k - 2*b_k) = -10
cond2 = S_a - 2*S_b
print(f'두 번째 조건: {cond2} (기대값: -10)')

# 최종 답 검증
ans = S_a + S_b
print(f'최종 답: {ans}')

if cond1 == 50 and cond2 == -10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')