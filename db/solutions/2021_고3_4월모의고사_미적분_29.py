import sympy as sp
from sympy import sqrt, cos, sin, tan, pi, simplify, N

alpha = sp.Symbol('alpha', real=True, positive=True)
beta = sp.Symbol('beta', real=True, positive=True)

# Given: cos²α = (7 + √21)/14
cos_sq_alpha = (7 + sqrt(21)) / 14

# Verify tan α
sin_sq_alpha = 1 - cos_sq_alpha
tan_sq_alpha = sin_sq_alpha / cos_sq_alpha
tan_alpha = sqrt(tan_sq_alpha)
tan_alpha_simplified = (sqrt(7) - sqrt(3)) / 2

# Check if our tan α is correct
diff = simplify(tan_alpha - tan_alpha_simplified)
if abs(N(diff)) < 1e-10:
    print(f"tan α verification: correct")
else:
    print(f"tan α verification: VERIFY_FAIL")

# Calculate tan 2α
tan_2alpha = 2 * tan_alpha_simplified / (1 - tan_sq_alpha)
tan_2alpha_simplified = 2*sqrt(3) / 3
tan_2alpha_check = simplify(tan_2alpha - tan_2alpha_simplified)

if abs(N(tan_2alpha_check)) < 1e-10:
    print(f"tan 2α verification: correct")
else:
    print(f"tan 2α verification: VERIFY_FAIL")

# β = 60° - 2α in radians
beta_val = pi/3 - 2*sp.asin(sqrt(sin_sq_alpha))

# tan β = (√3 - tan 2α) / (1 + √3 tan 2α)
tan_beta = (sqrt(3) - tan_2alpha_simplified) / (1 + sqrt(3) * tan_2alpha_simplified)
tan_beta_simplified = sqrt(3) / 9

tan_beta_check = simplify(tan_beta - tan_beta_simplified)
if abs(N(tan_beta_check)) < 1e-10:
    print(f"tan β verification: correct")
else:
    print(f"tan β verification: VERIFY_FAIL")

# Final answer: 54√3 × tan β
result = 54 * sqrt(3) * tan_beta_simplified
result_simplified = simplify(result)

print(f"54√3 × tan β = {result_simplified}")
if result_simplified == 18:
    print("VERIFY_PASS")
else:
    print(f"Result: {N(result_simplified)}")
    print("VERIFY_FAIL")