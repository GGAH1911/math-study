from sympy import symbols, solve, simplify, Sum, oo, Rational

a1, r = symbols('a1 r', real=True)

# 첫 번째 조건: sum(a_{2n-1} - a_{2n}) = 3
# a_{2n-1} - a_{2n} = a1*r^{2n-2} - a1*r^{2n-1} = a1*r^{2n-2}(1-r)
# sum = a1(1-r) * 1/(1-r^2) = a1/(1+r) = 3
cond1 = a1/(1+r) - 3

# 두 번째 조건: sum(a_n^2) = 6
# a_n^2 = a1^2 * r^{2(n-1)}
# sum = a1^2 * 1/(1-r^2) = 6
cond2 = a1**2/(1-r**2) - 6

# 연립방정식 풀기
sol = solve([cond1, cond2], [a1, r])

# 유효한 해 찾기 (|r| < 1)
valid_sols = []
for s in sol:
    a1_val, r_val = s
    if abs(r_val) < 1:
        valid_sols.append(s)

if len(valid_sols) > 0:
    a1_val, r_val = valid_sols[0]
    
    # 원래 조건 검증
    cond1_check = a1_val / (1 + r_val)
    cond2_check = a1_val**2 / (1 - r_val**2)
    
    # 무한급수 합 계산
    series_sum = a1_val / (1 - r_val)
    
    # 검증
    if abs(cond1_check - 3) < 1e-10 and abs(cond2_check - 6) < 1e-10:
        if abs(series_sum - 2) < 1e-10:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')