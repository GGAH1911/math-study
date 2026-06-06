from sympy import symbols, expand, solve

# Let S = sum of a_k, Q = sum of a_k^2
S = symbols('S')
Q = 20  # given: sum(a_k^2) = 20

# Expand (a_k + 1)^2
# sum((a_k + 1)^2) = sum(a_k^2 + 2*a_k + 1)
#                 = sum(a_k^2) + 2*sum(a_k) + 10
#                 = Q + 2*S + 10

# Given: sum((a_k + 1)^2) = 50
eq = Q + 2*S + 10 - 50
solution = solve(eq, S)
print(f'sum(a_k) = {solution[0]}')

# Verify: if S = 10, then sum((a_k+1)^2) should equal 50
verify_sum = Q + 2*10 + 10
print(f'Verification: sum((a_k+1)^2) = {verify_sum}')
if verify_sum == 50:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')