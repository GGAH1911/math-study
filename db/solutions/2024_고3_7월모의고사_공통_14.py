import sympy as sp

a = 2
x = sp.Symbol('x')

# g(x) derived
def g(val):
    return val**3 - val**2 - 6*val + 2

# f(x) original
def f(val):
    if val <= 0:
        return -2*(val+1)**2 + 4
    else:
        return a*(val - 5)

# p(x) = g(x) - f(x) for x<=0  =>  x^3+x^2-2x = x(x+2)(x-1)
p = x**3 + x**2 - 2*x
p_roots = sp.solve(p, x)  # [0, -2, 1]
p_roots_le0 = sorted([int(r) for r in p_roots if r <= 0])  # [-2, 0]

# q(x) = g(x) - a*(x-5) for x>0  =>  x^3-x^2-8x+12 = (x-2)^2*(x+3)
q = x**3 - x**2 - 8*x + 12
q_roots = sp.solve(q, x)  # [-3, 2]
q_roots_gt0 = sorted([int(r) for r in q_roots if r > 0])  # [2]

all_k = p_roots_le0 + q_roots_gt0  # [-2, 0, 2]

# Check f(k)=g(k) for each k
check_eq = all(abs(f(k) - g(k)) < 1e-9 for k in all_k)

# Check exactly {-2, 0, 2}
check_roots = (sorted(all_k) == [-2, 0, 2])

# g(2a) = g(4)
g2a = g(2 * a)
check_val = (g2a == 26)

if check_eq and check_roots and check_val:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
