from sympy import *
x = symbols('x', real=True)
f = exp(x**3 + 2*x - 2)
f_prime = diff(f, x)

# f(x_0) = e 를 만족하는 x_0 찾기
eq = x**3 + 2*x - 3
x0_solutions = solve(eq, x)
x0 = 1

# 검증: f(1) = e 인지 확인
f_at_1 = f.subs(x, 1)
if not simplify(f_at_1 - E) == 0:
    print('VERIFY_FAIL')
    exit()

# f'(1) 계산
f_prime_at_1 = f_prime.subs(x, 1)
expected = 5*E

if simplify(f_prime_at_1 - expected) == 0:
    g_prime_e = 1 / f_prime_at_1
    if simplify(g_prime_e - 1/(5*E)) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')