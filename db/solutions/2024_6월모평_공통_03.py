from sympy import symbols, summation

# 검증: 주어진 조건 만족 여부 확인
# S = sum of a_k라 하면, 원래 조건은 2S + 30 = 60이어야 함

S_answer = 15

# 조건 검증
left_side = 2 * S_answer + 30
expected = 60

if left_side == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')