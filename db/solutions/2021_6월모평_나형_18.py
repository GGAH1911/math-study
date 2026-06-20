from sympy import symbols, Eq, solve

a1, k = symbols('a1 k')
d = 2

# S_n = n*a1 + n*(n-1)  (d=2이므로 d/2=1)
S_k_expr = k*a1 + k*(k-1)
S_k2_expr = (k+2)*a1 + (k+2)*(k+1)

solutions = solve([Eq(S_k_expr, -16), Eq(S_k2_expr, -12)], [a1, k])

found = False
for sol in solutions:
    if isinstance(sol, dict):
        a_val = sol[a1]
        k_val = sol[k]
    else:
        a_val, k_val = sol[0], sol[1]
    # k는 자연수여야 함
    if not (k_val.is_integer and k_val > 0):
        continue
    # a_{2k} = a1 + (2k-1)*d
    a_2k = a_val + (2*k_val - 1)*d
    # 원래 조건 검증
    s_k = k_val*a_val + k_val*(k_val - 1)
    s_k2 = (k_val+2)*a_val + (k_val+2)*(k_val+1)
    if s_k == -16 and s_k2 == -12 and a_2k == 7:
        found = True

print('VERIFY_PASS' if found else 'VERIFY_FAIL')
