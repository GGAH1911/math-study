from sympy import symbols, solve, Eq, simplify

a1 = symbols('a1', positive=True, real=True)

# 등비수열: a_n = a1 * (-2)^(n-1)
# 각 항 계산
terms = [a1 * ((-2)**(k-1)) for k in range(1, 10)]

# |a_k| + a_k 계산
sum_expr = sum(abs(t) + t for t in terms)

# 방정식 풀기
eq = Eq(sum_expr, 66)
solution = solve(eq, a1)

if solution:
    a1_val = solution[0]
    # 검증
    check = sum_expr.subs(a1, a1_val)
    if check == 66:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')