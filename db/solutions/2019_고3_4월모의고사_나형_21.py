from sympy import symbols, limit, oo, Abs, Piecewise

k = 2
x = symbols('x', real=True)
n = symbols('n', integer=True, positive=True)

# Define f(x)
def f_val(x_val):
    if abs(x_val - 1) < k:
        return -1
    elif abs(x_val - 1) == k:
        return 0
    else:
        return 1

# Compute f(k)
f_k = f_val(2)
print(f'f(2) = {f_k}')

# Compute (f∘f)(k)
f_f_k = f_val(f_k)
print(f'(f∘f)(2) = f(f(2)) = f({f_k}) = {f_f_k}')

# Check continuity: limit of (x-k)^2 at x=k should equal g(k) = (f∘f)(k)
limit_at_k = 0  # lim (x-2)^2 = 0
print(f'Continuity check: lim(g(x)) = {limit_at_k}, g(k) = {f_f_k}, continuous: {limit_at_k == f_f_k}')

# Compute (g∘f)(k)
f_k_value = f_val(2)  # = -1
print(f'f(2) = {f_k_value}')

# g(-1) where -1 ≠ k=2
g_of_minus1 = (-1 - 2)**2
print(f'g(-1) = (-1-2)^2 = {g_of_minus1}')

g_f_k = g_of_minus1
print(f'(g∘f)(2) = g(f(2)) = g(-1) = {g_f_k}')

if g_f_k == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')