from sympy import symbols, diff, solve

CANDIDATE = '7'

# 문제에서 주어진 조건
# 함수: f(x) = x^4 + kx + 10
# x = 1에서 극값을 가짐
# 구하는 것: f(1)의 값

x, k = symbols('x k', real=True)

# 함수 정의
f = x**4 + k*x + 10

# 1계 도함수
f_prime = diff(f, x)  # f'(x) = 4x^3 + k

# 극값 조건: f'(1) = 0
f_prime_at_1 = f_prime.subs(x, 1)  # 4 + k = 0

# k 구하기
k_solutions = solve(f_prime_at_1, k)
k_value = k_solutions[0]  # k = -4

# 2계 도함수로 극값 확인
f_double_prime = diff(f_prime, x)  # f''(x) = 12x^2
f_double_prime_at_1 = f_double_prime.subs(x, 1)  # 12

# x = 1에서 극값인지 확인 (f''(1) = 12 > 0이므로 극소값)
is_extreme = f_double_prime_at_1 > 0

# f(1) 계산 (k 값 대입)
f_1_value = f.subs([(x, 1), (k, k_value)])

# 검증
try:
    candidate_value = int(CANDIDATE)
    computed_value = int(f_1_value)
    
    # 극값 조건과 함수 값 모두 확인
    if is_extreme and candidate_value == computed_value:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
except:
    print("VERIFY_FAIL")