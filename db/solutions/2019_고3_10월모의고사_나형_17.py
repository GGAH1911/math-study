import sympy as sp
from sympy import symbols, solve, summation

n, k = symbols('n k', integer=True)

# Define S_n
S = lambda n_val: -n_val**2 + 60*n_val - 490

# Verify conditions
assert S(10) == 10, f"S_10 should be 10, got {S(10)}"
assert S(50) == 10, f"S_50 should be 10, got {S(50)}"
assert S(30) == 410, f"S_30 should be 410, got {S(30)}"

# Find m where S_m > S_50
# -m^2 + 60m - 490 > 10
# m^2 - 60m + 500 < 0
m = symbols('m', integer=True, real=True)
eq = m**2 - 60*m + 500
roots = solve(eq, m)
print(f"Roots: {roots}")
assert roots == [10, 50], f"Roots should be [10, 50], got {roots}"

# So 10 < m < 50, with m < 50 natural number
# m in {11, 12, ..., 49}
p = 11
q = 49
assert all(S(m_val) > S(50) for m_val in range(p, q+1)), "All m in [p,q] should satisfy S_m > S_50"
assert not all(S(m_val) > S(50) for m_val in range(p-1, q+2)), "Boundary check failed"

# Calculate a_k
def a(k_val):
    if k_val == 1:
        return S(1)
    else:
        return S(k_val) - S(k_val - 1)

# Verify a_k = 61 - 2k for k >= 2
for k_val in range(2, 10):
    assert a(k_val) == 61 - 2*k_val, f"a_{k_val} mismatch"

# Calculate sum
total = sum(a(k_val) for k_val in range(p, q+1))
print(f"Sum from k={p} to k={q}: {total}")
assert total == 39, f"Expected 39, got {total}"

print("VERIFY_PASS")