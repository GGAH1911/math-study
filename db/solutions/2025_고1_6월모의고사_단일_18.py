from sympy import symbols, Abs, solve

x, a = symbols('x a', real=True)

# 자연수가 정확히 2개인지 확인
test_values = [-6, -5, 6, 7]
total_sum = 0

for a_val in test_values:
    # 두 조건을 만족하는 자연수 찾기
    solutions = []
    for nat_x in range(1, 10):
        cond1 = abs(a_val * nat_x - 1) < 21
        cond2 = 2 * nat_x + 3 > 5
        if cond1 and cond2:
            solutions.append(nat_x)
    
    if len(solutions) == 2:
        total_sum += a_val

if total_sum == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')