from sympy import symbols, solve, Rational

a, r = symbols('a r', positive=True)

# 등비수열 일반항
def term(n): return a * r**(n-1)

# 조건 방정식
eq1 = term(3)**2 - term(6)  # a3^2 = a6
eq2 = term(2) - term(1) - 2  # a2 - a1 = 2

sols = solve([eq1, eq2], [a, r])

if sols:
    sol = sols[0] if isinstance(sols, list) else [(v) for v in sols.values()]
    a_val, r_val = sol[0], sol[1]
    a5 = a_val * r_val**4
    # 검증
    cond1 = (a_val * r_val**2)**2 == a_val * r_val**5
    cond2 = a_val * r_val - a_val == 2
    if a5 == 32 and cond1 and cond2:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
