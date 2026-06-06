from sympy import symbols, diff, integrate, simplify

x = symbols('x')
f_prime = 6*x**2 - 2*x - 1

# 부정적분
f_general = integrate(f_prime, x)
# f_general = 2*x**3 - x**2 - x + C

# 초기조건을 이용해 C 결정
C = 3  # f(1) = 3에서 결정
f = f_general + C

# 조건 검증
check_f1 = f.subs(x, 1)
assert check_f1 == 3, f'f(1) = {check_f1}, expected 3'

# 미분 검증
f_prime_check = diff(f, x)
assert simplify(f_prime_check - f_prime) == 0, 'f\'(x) not matching'

# 답 계산
answer = f.subs(x, 2)
assert answer == 13, f'f(2) = {answer}, expected 13'

print('VERIFY_PASS')