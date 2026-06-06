from sympy import symbols, Eq, solve

# Define variables
a = symbols('a1:11')  # a1, a2, ..., a10
A = sum(a[i] for i in range(7))  # sum a_1 to a_7

# Condition 1: sum(a_1 to a_10) - sum(a_1 to a_7)/2 = 56
cond1 = Eq(sum(a[:10]) - A/2, 56)

# Condition 2: 2*sum(a_1 to a_10) - sum(a_1 to a_8) = 100
cond2 = Eq(2*sum(a[:10]) - sum(a[:8]), 100)

# We need to verify that a_8 = 12 is consistent
# Let's verify by substitution
a_8_value = 12

# From our derivation:
# cond1: (1/2)*A + a_8 + B = 56
# cond2: A + a_8 + 2*B = 100
# where B = a_9 + a_10

# Subtract: (1/2)*A + B = 44
# So: A + 2*B = 88
# And: (1/2)*A + a_8 + B = 56
# Thus: a_8 = 56 - 44 = 12

B, A_var = symbols('B A_var', real=True)
eq1_simplified = Eq(A_var/2 + a_8_value + B, 56)
eq2_simplified = Eq(A_var + a_8_value + 2*B, 100)

# Solve for A_var and B
sol = solve([eq1_simplified, eq2_simplified], [A_var, B])
if sol:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')