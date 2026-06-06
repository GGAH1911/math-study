from sympy import symbols, diff, solve, simplify

# 원래 함수
x, a, b = symbols('x a b')
f = x**3 - 6*x**2 + a*x + b

# 조건 1: x=1에서 극대
f_prime = diff(f, x)
eq1 = f_prime.subs(x, 1)  # f'(1) = 0
a_val = solve(eq1, a)[0]  # a = 9

# 조건 2: 극솟값이 5
f_with_a = f.subs(a, a_val)  # a=9 대입
f_prime_with_a = diff(f_with_a, x)
critical_points = solve(f_prime_with_a, x)  # x = 1, 3

# x=3에서 극소값
f_at_3 = f_with_a.subs(x, 3)
eq2 = f_at_3 - 5  # f(3) = 5
b_val = solve(eq2, b)[0]  # b = 5

# 최종 함수
f_final = f.subs([(a, a_val), (b, b_val)])

# 검증
f_prime_final = diff(f_final, x)
f_double_prime = diff(f_prime_final, x)

verify_1 = f_prime_final.subs(x, 1) == 0  # f'(1) = 0
verify_2 = f_double_prime.subs(x, 1) < 0  # f''(1) < 0 (극대)
verify_3 = f_final.subs(x, 3) == 5  # f(3) = 5 (극솟값)
verify_4 = f_double_prime.subs(x, 3) > 0  # f''(3) > 0 (극소)

if verify_1 and verify_2 and verify_3 and verify_4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')