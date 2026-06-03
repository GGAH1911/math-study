from sympy import symbols, solve, simplify

# 등비수열의 첫항과 공비
a1, r = symbols('a1 r', real=True)

# 조건 1: a_2 = 1
cond1 = a1 * r - 1

# a_3 = a1 * r^2, a_5 = a1 * r^4
# 조건 2: a_5 = 2 * (a_3)^2
cond2 = a1 * r**4 - 2 * (a1 * r**2)**2

# 연립방정식 풀이
solutions = solve([cond1, cond2], [a1, r])

# r != 0이므로 유효한 해 찾기
for sol in solutions:
    if sol[1] != 0:  # r != 0
        a1_val, r_val = sol
        a6 = a1_val * r_val**5
        if a6 == 16:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')