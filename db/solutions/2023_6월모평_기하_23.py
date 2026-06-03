from sympy import symbols, solve, simplify

# Symbolic vectors a and b (represented as basis)
# Two vectors: u = a + 2b, v = 3a + kb
# For parallelism: v = lambda * u
# 3a + kb = lambda(a + 2b) = lambda*a + 2*lambda*b
# Comparing coefficients:
# a: 3 = lambda
# b: k = 2*lambda

lambda_val = 3
k = 2 * lambda_val

print(f"k = {k}")

# Verification: Check if 3a + 6b = 3(a + 2b)
# 3a + 6b = 3a + 6b ✓

if k == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')