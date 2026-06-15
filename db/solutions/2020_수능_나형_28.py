CANDIDATE = 7

from sympy import symbols, integrate, simplify

x, t = symbols('x t', real=True)

# f(x) = (3/2)x + 1
def f_val(expr):
    return (3*expr/2 + 1)

# Verify condition (가)
lhs_a = integrate(f_val(t), (t, 1, x))
rhs_a = (x - 1)/2 * (f_val(x) + f_val(1))
diff_a = simplify(lhs_a - rhs_a)
assert diff_a == 0, f"Condition (가) failed: {diff_a}"

# Verify condition (나)
lhs_b = integrate(f_val(x), (x, 0, 2))
rhs_b = 5 * integrate(x * f_val(x), (x, -1, 1))
assert lhs_b == rhs_b, f"Condition (나) failed: {lhs_b} vs {rhs_b}"

# Verify f(0) = 1
assert f_val(0) == 1, "Initial condition f(0)=1 failed"

# Compute f(4)
result = f_val(4)
assert result == CANDIDATE, f"f(4) = {result} != {CANDIDATE}"

print("VERIFY_PASS")