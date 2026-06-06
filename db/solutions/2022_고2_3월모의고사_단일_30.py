from sympy import symbols, solve, expand, simplify

alpha, beta, k = 5, 8, 37

# f(x) = 2(x-alpha)(x-beta) + 1
def f(x):
    return 2*(x - alpha)*(x - beta) + 1

# g(x) = x^2 - 2(beta-3)x + (beta^2 - 6*beta + 10)
def g(x):
    return x**2 - 2*(beta - 3)*x + (beta**2 - 6*beta + 10)

x = symbols('x')

# Verify A = {alpha, beta}
f_eq1 = solve(f(x) - 1, x)
g_eq1 = solve(g(x) - 1, x)
union_1 = sorted(list(set(f_eq1 + g_eq1)))
if sorted([alpha, beta]) == union_1:
    print('A condition verified')

# Verify B = {alpha, beta+3}
fg_eq = solve(f(x) - g(x), x)
if sorted(fg_eq) == sorted([alpha, beta + 3]):
    print('B condition verified')

# Verify k=37 roots and sum
f_roots_37 = solve(f(x) - 37, x)
g_roots_37 = solve(g(x) - 37, x)
all_roots_37 = sorted(list(set(f_roots_37 + g_roots_37)))
root_sum = sum(all_roots_37)

if len(all_roots_37) == 3 and root_sum == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')