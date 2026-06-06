from sympy import symbols, solve, pi, sqrt, simplify

# Variables
r, c, d = symbols('r c d', positive=True, real=True)

# Condition 1: c + d = 6√2
eq1 = c + d - 6*sqrt(2)

# Condition 2: Area of quadrilateral AO₂O₃B = 34
# Using the formula: Area = (3r² - r(c+d) - cd)/8 = 34
# So: 3r² - 6√2·r - cd = 272
eq2 = 3*r**2 - 6*sqrt(2)*r - (c*d) - 272

# Let p = (6r² - 12√2·r + c² + d²)/4
# With c² + d² = 72 - 2cd
# After substitution: p = (6r² - 12√2·r + 72 - 2cd)/4

# From eq2: cd = 3r² - 6√2·r - 272
cd_expr = 3*r**2 - 6*sqrt(2)*r - 272

# Calculate p
p_formula = (6*r**2 - 12*sqrt(2)*r + 72 - 2*cd_expr) / 4
p_result = simplify(p_formula)

# Check: should equal 154
if p_result == 154:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')