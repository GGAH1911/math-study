from sympy import symbols, Sum, Rational, simplify

# Given conditions (numeric)
sum_ak = 4          # sum_{k=1}^{10} a_k = 4
sum_ak_plus2_sq = 67  # sum_{k=1}^{10} (a_k+2)^2 = 67

# Expand sum_{k=1}^{10} (a_k+2)^2
# = sum a_k^2 + 4*sum a_k + 4*10
# => sum_ak2 = sum_ak_plus2_sq - 4*sum_ak - 40
sum_ak2 = sum_ak_plus2_sq - 4 * sum_ak - 40

# Verify expansion is consistent
check = sum_ak2 + 4 * sum_ak + 40

if sum_ak2 == 11 and check == sum_ak_plus2_sq:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
