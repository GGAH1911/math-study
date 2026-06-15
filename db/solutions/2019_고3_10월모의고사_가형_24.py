from sympy import symbols, solve

CANDIDATE = 59

n = symbols('n', positive=True, integer=True)

# X ~ B(n, 1/3)
p = 1/3
E_X = n * p
V_X = n * p * (1 - p)

# Y = 2X - 1
E_Y = 2 * E_X - 1
V_Y = 4 * V_X

# 주어진 조건: V(2X-1) = 80
eq = V_Y - 80
n_val = solve(eq, n)[0]

# n = 90일 때 E(2X-1) 계산
E_Y_value = E_Y.subs(n, n_val)

if abs(E_Y_value - CANDIDATE) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')