from sympy import ln, exp, diff, symbols, simplify

CANDIDATE = 13

x = symbols('x', positive=True, real=True)
f = ln(x) + 10
f_prime = diff(f, x)

# 조건 1: f'(x) = 1/x 확인
condition1 = simplify(f_prime - 1/x) == 0

# 조건 2: f(1) = 10 확인
condition2 = f.subs(x, 1) == 10

# 조건 3: f(e^3) = 13 확인
f_at_e3 = f.subs(x, exp(3))
condition3 = simplify(f_at_e3) == CANDIDATE

if condition1 and condition2 and condition3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')