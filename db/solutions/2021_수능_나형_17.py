from sympy import symbols, limit, diff, Function, Eq, solve

x = symbols('x')
a0, a1, b0, b1 = symbols('a0 a1 b0 b1', real=True)

# f(x) = a0 + a1*x + ..., g(x) = b0 + b1*x + ...
# 조건: f(0) + g(0) = 0 → a0 + b0 = 0
# 조건: f(0) = -3 → a0 = -3
# 따라서 b0 = 3

a0_val = -3
b0_val = 3

# 첫 번째 조건: f'(0) + g'(0) = 3
eq1 = Eq(a1 + b1, 3)

# 두 번째 조건: f'(0) / g(0) = 2
eq2 = Eq(a1 / b0_val, 2)

sol = solve([eq1, eq2], [a1, b1])
a1_val = sol[a1]
b1_val = sol[b1]

# h'(0) = f'(0)*g(0) + f(0)*g'(0)
h_prime_0 = a1_val * b0_val + a0_val * b1_val

# 검증
if h_prime_0 == 27:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {h_prime_0}')