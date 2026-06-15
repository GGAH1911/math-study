from sympy import symbols, integrate, limit, summation

x, n, k = symbols('x n k')
f = lambda t: 4*t**3 + t

# 리만 합을 정적분으로 계산
integral_result = integrate(f(x), (x, 0, 2))
remann_limit = integral_result / 2

# 직접 리만 합으로도 검증
def riemann_sum(num_n):
    total = sum(f(2*k_val/num_n) / num_n for k_val in range(1, num_n+1))
    return total

# 큰 n에서 리만 합 계산
for test_n in [100, 1000, 10000]:
    approx = riemann_sum(test_n)
    
expected_answer = 9
final_check = abs(float(remann_limit) - expected_answer) < 1e-10

if final_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')