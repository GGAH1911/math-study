CANDIDATE = 34
import sympy as sp

x, k = sp.symbols('x k')
a = CANDIDATE

f = -x**4 - 2*x**3 - x**2
g = 3*x**2 + a

# Condition 1: 12x+k >= f(x) for all x  =>  phi(x) = -x^2(x+1)^2 - 12x has max at x=-2
phi = f - 12*x  # k >= phi(x) => k >= max phi
phi_func = sp.Lambda(x, phi)
crit = sp.solve(sp.diff(phi, x), x)
max_phi = max(float(phi_func(c)) for c in crit if sp.im(c) == 0)
k_min = int(round(max_phi))
assert abs(max_phi - k_min) < 1e-9, f'k_min not integer: {max_phi}'

# Condition 2: 12x+k <= g(x) for all x  =>  3x^2-12x+(a-k)>=0 always  =>  disc<=0
# disc = 144 - 12*(a-k) <= 0  =>  k <= a-12
k_max = a - 12

# Count natural numbers in [k_min, k_max]
if k_max < k_min:
    count = 0
else:
    count = k_max - k_min + 1

if count == 3 and k_min == 20 and k_max == 22:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: k_min={k_min}, k_max={k_max}, count={count}')
