import sympy as sp
x, a, b = sp.symbols('x a b', real=True, integer=True)

# a=1, P=[1,3]
quad_a1 = x**2 - 4*x + 1 + 2
roots_a1 = sp.solve(quad_a1, x)
assert roots_a1 == [1, 3], f'a=1 roots: {roots_a1}'
P_a1_in_Q = []
for b_val in range(1, 10):
    Q_contains = (b_val - 4 <= 1 and 3 <= b_val + 4 and b_val not in [1, 2, 3])
    if Q_contains:
        P_a1_in_Q.append(b_val)
assert set(P_a1_in_Q) == {4, 5}, f'a=1: {P_a1_in_Q}'

# a=2, P={2}
quad_a2 = x**2 - 4*x + 2 + 2
roots_a2 = sp.solve(quad_a2, x)
assert roots_a2 == [2], f'a=2 roots: {roots_a2}'
P_a2_in_Q = []
for b_val in range(1, 10):
    Q_contains = (b_val - 4 <= 2 <= b_val + 4 and b_val != 2)
    if Q_contains:
        P_a2_in_Q.append(b_val)
assert set(P_a2_in_Q) == {1, 3, 4, 5, 6}, f'a=2: {P_a2_in_Q}'

total = len(P_a1_in_Q) + len(P_a2_in_Q)
assert total == 7, f'Total: {total}'
print('VERIFY_PASS')