import sympy as sp
from sympy import log, symbols, solve, simplify

CANDIDATE = 36

q = symbols('q', positive=True, real=True)

# 등비수열 조건: 3, a, b
a = 3 * q
b = 3 * q**2

# 로그 방정식: log_a(3b) + log_3(b) = 5
# log_a(3b) 계산
log_a_3b = log(3*b, a)
log_a_3b_simplified = simplify(log_a_3b)

# log_3(b) 계산
log_3_b = log(b, 3)

# 전체 방정식
equation = log_a_3b + log_3_b - 5

# q 풀기
solution_q = solve(equation, q)

# 구한 q 값으로 a, b 계산
if solution_q:
    q_val = solution_q[0]
    a_val = 3 * q_val
    b_val = 3 * q_val**2
    sum_ab = a_val + b_val
    
    # 검증: 로그 조건식이 5를 만족하는지 확인
    log_a_check = float(log(3*b_val, a_val))
    log_3_check = float(log(b_val, 3))
    total = log_a_check + log_3_check
    
    if abs(sum_ab - CANDIDATE) < 0.0001 and abs(total - 5) < 0.0001:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')