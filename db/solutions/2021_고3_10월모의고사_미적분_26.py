from sympy import *
import numpy as np
sqrt3 = sqrt(3)
pi_val = pi

rho = 4*sqrt3 - 6
rho_sq = expand(rho**2)
one_minus_rho_sq = expand(1 - rho_sq)

print('ρ =', rho, '≈', float(rho))
print('ρ² =', rho_sq, '≈', float(rho_sq))
print('1 - ρ² =', one_minus_rho_sq, '≈', float(one_minus_rho_sq))

S_1 = pi_val * one_minus_rho_sq / 2
limit_result = S_1 / one_minus_rho_sq
limit_simplified = simplify(limit_result)

print('S_1 =', S_1)
print('lim S_n =', limit_simplified)
print('lim S_n ≈', float(limit_simplified))
print('π/2 ≈', float(pi_val/2))

if simplify(limit_simplified - pi_val/2) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')