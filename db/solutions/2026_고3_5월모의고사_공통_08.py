from sympy import symbols, solve, Rational

a1, r = symbols('a1 r', real=True)

# 조건 1: a_1 * a_5 = 36
eq1 = a1 * (a1 * r**4) - 36

# 조건 2: a_3 + 2*a_4 = 2
eq2 = (a1 * r**2) + 2 * (a1 * r**3) - 2

# 조건 3: 첫째항이 음수
# a1 < 0

solutions = solve([eq1, eq2], [a1, r])
valid_solutions = [(sol_a1, sol_r) for sol_a1, sol_r in solutions if sol_a1 < 0]

for sol_a1, sol_r in valid_solutions:
    a2 = sol_a1 * sol_r
    
    # 검증
    a1_val = sol_a1
    a5_val = a1_val * sol_r**4
    a3_val = a1_val * sol_r**2
    a4_val = a1_val * sol_r**3
    
    check1 = a1_val * a5_val
    check2 = a3_val + 2 * a4_val
    
    if abs(check1 - 36) < 1e-10 and abs(check2 - 2) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')