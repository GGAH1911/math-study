import numpy as np
from scipy.optimize import brentq
from fractions import Fraction
import math

CANDIDATE = '17'

# Step 1: Verify conditions lead to (a, b) = (3/2, -3π)
# From condition (가): f(0) = sin(b) = 0 => b = nπ
# From condition (가): f(2π) = sin(2πa + b) = 2πa + b
#                     => sin(θ) = θ only when θ = 0
#                     => 2πa + b = 0 => b = -2πa
# With 1 ≤ a ≤ 2: (a,b) ∈ {(1,-2π), (3/2,-3π), (2,-4π)}
# Condition (나) determines a = 3/2, b = -3π

a = 3.0/2.0  # Rational(3, 2)
b = -3.0 * np.pi

# Verify condition (가)
assert abs(np.sin(b)) < 1e-10, "f(0) = sin(b) must equal 0"
assert abs(2*np.pi*a + b) < 1e-10, "2πa + b must equal 0"

# Step 2: Find extrema in (0, 4π)
# f'(x) = a·cos(ax + b + sin x)·(a + cos x)
# Extrema occur when cos(ax + b + sin x) = 0 (since a + cos x > 0)
# i.e., ax + b + sin x = π/2 + mπ
# Maxima occur when ax + b + sin x = π/2 + 2kπ

# h(x) = ax + b + sin x = (3/2)x - 3π + sin x
# h is strictly increasing: h'(x) = 3/2 + cos x > 0
# h(0) = -3π, h(4π) = 6π - 3π = 3π

def h(x):
    return a * x + b + np.sin(x)

# Find all x ∈ (0, 4π) where h(x) = π/2 + 2kπ
# Range check: -3π < π/2 + 2kπ < 3π => k ∈ {-1, 0, 1}

extrema_x_list = []

for k in [-1, 0, 1]:
    target_h = np.pi/2 + 2*k*np.pi
    
    def equation(x):
        return h(x) - target_h
    
    try:
        # Find root using Brent's method
        x_solution = brentq(equation, 0.0001, 4*np.pi - 0.0001)
        extrema_x_list.append(x_solution)
    except:
        pass

extrema_x_list.sort()
n = len(extrema_x_list)
alpha_1 = extrema_x_list[0]

# Verify n = 3 and α₁ ≈ π
assert n == 3, f"Expected 3 extrema, found {n}"
assert abs(alpha_1 - np.pi) < 1e-6, f"Expected α₁ ≈ π, got {alpha_1}"

# Step 3: Calculate n·α₁ - ab
ab_product = a * b  # = (3/2) × (-3π) = -9π/2
n_times_alpha1_minus_ab = n * alpha_1 - ab_product

# Express as (q/p)π
result_divided_by_pi = n_times_alpha1_minus_ab / np.pi

# Convert to simplest fraction form
frac_result = Fraction(result_divided_by_pi).limit_denominator(10000)
p_value = frac_result.denominator
q_value = frac_result.numerator

# Verify p and q are coprime
assert math.gcd(p_value, q_value) == 1, f"p={p_value} and q={q_value} must be coprime"

# Calculate answer
computed_answer = p_value + q_value

# Verification against CANDIDATE
if str(computed_answer) == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")