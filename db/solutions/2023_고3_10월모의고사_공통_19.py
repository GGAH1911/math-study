import sympy as sp
from scipy.integrate import quad

t = sp.Symbol('t')
v1 = 12*t - 12
v2 = 3*t**2 + 2*t - 12

# Position functions
x_P = sp.integrate(v1, (t, 0, t))
x_Q = sp.integrate(v2, (t, 0, t))

# Find k where x_P(k) = x_Q(k)
eq = sp.Eq(x_P, x_Q)
k_solutions = [sol for sol in sp.solve(eq, t) if sol > 0]
k = k_solutions[0]

print(f'k = {k}')

# Check when v1 changes sign
v1_zero = sp.solve(v1, t)[0]
print(f'v1 zero at t = {v1_zero}')

# Calculate distance
x_P_func = lambda tau: float(6*tau**2 - 12*tau)
x_P_at_1 = x_P_func(1)
x_P_at_k = x_P_func(float(k))
x_P_at_0 = 0

dist_0_to_1 = abs(x_P_at_1 - x_P_at_0)
dist_1_to_k = abs(x_P_at_k - x_P_at_1)
total_dist = dist_0_to_1 + dist_1_to_k

print(f'Distance [0,1]: {dist_0_to_1}')
print(f'Distance [1,k]: {dist_1_to_k}')
print(f'Total distance: {total_dist}')

if total_dist == 102:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')