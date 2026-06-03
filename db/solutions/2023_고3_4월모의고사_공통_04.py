from sympy import symbols, diff, solve

x, a_sym = symbols('x a')
f = 2*x**3 - 6*x + a_sym

# 극값 조건: f'(1) = 0 (이미 확인함), f(1) = 2
f_at_1 = f.subs(x, 1)
eq = f_at_1 - 2
a_value = solve(eq, a_sym)[0]

if a_value == 6:
    # 역대입 검증: a=6일 때 f(1) = 2인지 확인
    f_final = 2*x**3 - 6*x + 6
    result = f_final.subs(x, 1)
    if result == 2:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')