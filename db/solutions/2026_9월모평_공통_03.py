from sympy import symbols, Eq, solve

# 조건: sum_{k=1}^6 (2*a_k - 1) = 30
# 이를 전개하면: 2*sum(a_k) - 6 = 30
# sum(a_k) = S 라고 하면
# 2*S - 6 = 30
# S = 18

S = symbols('S')
eq = Eq(2*S - 6, 30)
sol = solve(eq, S)

if sol and sol[0] == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')