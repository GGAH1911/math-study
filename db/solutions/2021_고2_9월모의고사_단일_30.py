import sympy as sp
import numpy as np
from sympy import sqrt, symbols, simplify

# Define symbolic variable
x = symbols('x', real=True)

# Parameters
a, b = 3, -3
k_val = (11 + 3*sqrt(17))/8

# Left piece: f(x) = 3x^2 - 9x + 6
f_left = 3*x**2 - 9*x + 6

# Right piece: f(x) = -x^2 + 2x + 8
f_right = -x**2 + 2*x + 8

# Check roots: f(1) = 0, f(2) = 0, f(4) = 0
f1_left = f_left.subs(x, 1)
f2_left = f_left.subs(x, 2)
f4_right = f_right.subs(x, 4)

# Check continuity at k
f_k_left = f_left.subs(x, k_val)
f_k_right = f_right.subs(x, k_val)

# Verify all conditions
if f1_left == 0 and f2_left == 0 and f4_right == 0:
    if simplify(f_k_left - f_k_right) == 0:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")