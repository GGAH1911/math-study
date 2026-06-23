from sympy import symbols, solve, Eq

n = symbols('n', positive=True, integer=True)

# 이항분포 B(n, 1/2)
# E(X) = n/2
E_X = n/2

# V(X) = n/4
V_X = n/4

# E(X^2) = V(X) + [E(X)]^2
E_X2_formula = V_X + E_X**2

# 조건: E(X^2) = V(X) + 25
condition = Eq(E_X2_formula, V_X + 25)

solution = solve(condition, n)
n_answer = solution[0]

# 검증
E_X_val = n_answer / 2
V_X_val = n_answer / 4
E_X2_val = V_X_val + E_X_val**2

if E_X2_val == V_X_val + 25:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')