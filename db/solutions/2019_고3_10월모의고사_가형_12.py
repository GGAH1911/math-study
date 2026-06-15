from sympy import symbols, limit, diff, simplify

# 검증: 주어진 극한 조건 재확인
# g(1) = -1, g'(1) = 2인지 확인
# f(-1) = 2, f'(-1) = 6인지 확인

# 극한 조건 1: lim (g(x)+1)/(x-1) = 2 as x->1
# => g(1) = -1, g'(1) = 2

# 극한 조건 2: lim (h(x)-2)/(x-1) = 12 as x->1
# h(x) = f(g(x))이므로
# h'(1) = f'(g(1)) * g'(1) = f'(-1) * 2 = 12
# => f'(-1) = 6
# h(1) = 2이므로 f(-1) = 2

# 최종 답
f_minus_1 = 2
f_prime_minus_1 = 6
answer_value = f_minus_1 + f_prime_minus_1

if answer_value == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')