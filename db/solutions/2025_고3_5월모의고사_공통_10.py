import sympy as sp

# 주어진 조건: a_n = 4n-2, b_n = 4n+2
# 원래 문제의 조건 검증
def verify_sum_formula(n_val):
    total = 0
    for k in range(1, n_val + 1):
        a_k = 4*k - 2
        b_k = 4*k + 2
        total += 1 / (a_k * b_k)
    
    expected = n_val / (8*n_val + 4)
    return abs(total - expected) < 1e-10

# n=1,2,3,4,5에서 검증
for n in range(1, 6):
    if not verify_sum_formula(n):
        print('VERIFY_FAIL')
        exit()

# 최종 답 검증: sum(a_k + b_k) for k=1 to 5
total_sum = 0
for k in range(1, 6):
    a_k = 4*k - 2
    b_k = 4*k + 2
    total_sum += a_k + b_k

if total_sum == 120:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')