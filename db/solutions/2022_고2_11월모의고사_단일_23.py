from sympy import symbols, solve, simplify

# 등비수열 정의
a1, r = symbols('a1 r', real=True, positive=True)

# 주어진 조건
eq1 = a1 * r - 2
eq2 = a1 * r**5 - 9

# 방정식 풀기
solutions = solve([eq1, eq2], [a1, r])

# 모든 해에 대해 검증
for sol in solutions:
    a1_val, r_val = sol
    a2 = a1_val * r_val
    a6 = a1_val * r_val**5
    a3_times_a5 = (a1_val * r_val**2) * (a1_val * r_val**4)
    
    # 조건 만족 확인
    if abs(float(a2) - 2) < 1e-10 and abs(float(a6) - 9) < 1e-10:
        answer_candidate = simplify(a3_times_a5)
        if abs(float(answer_candidate) - 18) < 1e-10:
            print('VERIFY_PASS')
            exit()

print('VERIFY_FAIL')