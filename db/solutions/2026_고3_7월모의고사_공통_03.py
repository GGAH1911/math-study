from sympy import symbols, Eq, solve, Sum, Rational

# Let S = sum_{k=1}^5 a_k be unknown; equation: sum k + 3S = 27
k_sum = sum(range(1,6))
S = symbols('S')
eq = Eq(k_sum + 3*S, 27)
sol = solve(eq, S)[0]

# Verify: reconstruct a sequence satisfying sum(k+3a_k)=27 with sum a_k = sol
# e.g. distribute S among a_1..a_5 arbitrarily, check consistency
import sympy
a = [sol/5]*5  # simplest choice
lhs = sum(k + 3*a[k-1] for k in range(1,6))

if sol == 4 and sympy.simplify(lhs - 27) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')