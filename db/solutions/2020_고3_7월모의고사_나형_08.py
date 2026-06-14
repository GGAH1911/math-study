from sympy import symbols, diff, solve, simplify

x, a = symbols('x a')
f = x**3 + 6*x**2 + 9*x + a

# 도함수
f_prime = diff(f, x)
critical_points = solve(f_prime, x)

# a = -2일 때
a_val = -2
f_with_a = x**3 + 6*x**2 + 9*x + a_val

# x = -1에서의 함수값
f_at_minus1 = f_with_a.subs(x, -1)

# 극솟값이 -6인지 확인
if f_at_minus1 == -6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')