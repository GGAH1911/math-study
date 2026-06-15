import numpy as np
from scipy.integrate import quad
import sympy as sp

CANDIDATE = 26

# Define symbolic variable
x = sp.Symbol('x', real=True)
t = sp.Symbol('t', real=True)

# Define g(x) = pi * e^x * sin(pi*x)
pi = sp.pi
e_const = sp.E
g = lambda x_val: sp.pi * sp.exp(x_val) * sp.sin(sp.pi * x_val)

# Verify condition (가): g(x+1) - g(x) = -π(e+1)e^x sin(πx)
lhs_ga = g(x+1) - g(x)
rhs_ga = -sp.pi * (e_const + 1) * sp.exp(x) * sp.sin(sp.pi * x)
verify_ga = sp.simplify(lhs_ga - rhs_ga)

# Define f_p(x) = π(e+1)/2 * sin(πx) + π²e/2 * cos(πx)
f_p = (sp.pi * (e_const + 1) / 2) * sp.sin(sp.pi * x) + (sp.pi**2 * e_const / 2) * sp.cos(sp.pi * x)

# Verify the functional equation: f_p(x+1) - f_p(x) = -π(e+1)sin(πx) - π²e cos(πx)
f_p_diff = f_p.subs(x, x+1) - f_p
rhs_funct = -sp.pi*(e_const+1)*sp.sin(sp.pi*x) - sp.pi**2*e_const*sp.cos(sp.pi*x)
verify_funct = sp.simplify(f_p_diff - rhs_funct)

# Compute integral_0^1 f_p(x) dx
int_fp_01 = sp.integrate(f_p, (x, 0, 1))
int_fp_01_simplified = sp.simplify(int_fp_01)

# From given condition: integral_0^1 f(x) dx = 10/9 * e + 4
# So integral_0^1 phi(x) dx = 10/9 * e + 4 - (e+1) = e/9 + 3
int_phi_01 = sp.Rational(10,9) * e_const + 4 - int_fp_01_simplified
int_phi_01_simplified = sp.simplify(int_phi_01)

# integral_1^10 f_p(x) dx
int_fp_110 = sp.integrate(f_p, (x, 1, 10))
int_fp_110_simplified = sp.simplify(int_fp_110)

# integral_1^10 phi(x) dx = 9 * integral_0^1 phi(x) dx
int_phi_110 = 9 * int_phi_01_simplified
int_phi_110_simplified = sp.simplify(int_phi_110)

# Final answer
final_answer = int_phi_110_simplified + int_fp_110_simplified
final_answer_simplified = sp.simplify(final_answer)

# Verify
if final_answer_simplified == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {CANDIDATE}, got {final_answer_simplified}')