from sympy import symbols, solve, simplify

d, r = symbols('d r', integer=True, positive=True)

# a_6 = 9 => a_1 = 9 - 5*d
a1 = 9 - 5*d

# b_6 = 9 => b_1 = 9 / r^5
b1 = 9 / (r**5)

# Condition (a): a_7 = b_7
# a1 + 6*d = b1 * r^6
eq1 = a1 + 6*d - b1 * r**6

# Solve for d in terms of r
d_expr = solve(eq1, d)[0]
print(f'd = {d_expr}')

# d should be 9(r-1) = 9r - 9
assert simplify(d_expr - 9*(r-1)) == 0, 'Incorrect d expression'

# Condition (b): 94 < a_11 < 109
# a_11 = a1 + 10*d = 9 - 5*d + 10*d = 9 + 5*d
a11 = 9 + 5*d_expr
a11_simplified = simplify(a11)
print(f'a_11 = {a11_simplified}')

# a_11 = 45*r - 36
assert simplify(a11_simplified - (45*r - 36)) == 0, 'Incorrect a_11'

# Find r: 94 < 45*r - 36 < 109
# 130 < 45*r < 145
# 2.888 < r < 3.222
r_val = 3  # Only natural number in range

# Verify condition (b)
a11_val = 45*r_val - 36
print(f'a_11 = {a11_val}')
assert 94 < a11_val < 109, f'Condition (b) failed: {a11_val}'

# Calculate a_7 and b_8
d_val = 9*(r_val - 1)
a1_val = 9 - 5*d_val
b1_val = 9 / (r_val**5)

a7 = a1_val + 6*d_val
b8 = b1_val * (r_val**7)

print(f'a_1 = {a1_val}, d = {d_val}')
print(f'b_1 = {b1_val}, r = {r_val}')
print(f'a_6 = {a1_val + 5*d_val}')
print(f'b_6 = {b1_val * (r_val**5)}')
print(f'a_7 = {a7}')
print(f'b_7 = {b1_val * (r_val**6)}')
print(f'a_7 + b_8 = {a7 + b8}')

if a7 + b8 == 108:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')