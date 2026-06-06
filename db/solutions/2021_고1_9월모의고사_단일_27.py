from sympy import symbols, solve, simplify

x, n = symbols('x n', integer=True, real=True)

# 두 조건을 만족하는 정수 개수 계산
target_n_values = [4, 5, 6, 7, 8]
valid_count = 0

for n_val in target_n_values:
    # x의 범위: 3 <= x <= 7
    x_range = [3, 4, 5, 6, 7]
    
    # 두 번째 부등식 만족 여부 확인
    satisfied = []
    for x_val in x_range:
        # x^2 - 2(n-1)x + n^2 - 2n >= 0
        result = x_val**2 - 2*(n_val-1)*x_val + n_val**2 - 2*n_val
        if result >= 0:
            satisfied.append(x_val)
    
    if len(satisfied) == 4:
        valid_count += 1

if valid_count == 5:
    answer_sum = sum(target_n_values)
    print(f'VERIFY_PASS') if answer_sum == 30 else print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')