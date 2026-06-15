import numpy as np
from scipy.optimize import fsolve
import sympy as sp

CANDIDATE = 86

# 조건 검증
z_sym = sp.Symbol('z', real=True)
r_vals = [7, 8, 9]
dot_products = []

for r in r_vals:
    # |OP|^2 = r^2 조건
    eq = 3*z_sym**2 + 11*sp.sqrt(2)*z_sym + (60.5 - r**2)
    sols = sp.solve(eq, z_sym)
    
    for z_val in sols:
        if z_val.is_real or (isinstance(z_val, sp.Expr)):
            # |OP|^2 계산
            op_squared = 60.5 + 11*sp.sqrt(2)*z_val + 3*z_val**2
            op_squared_simplified = sp.simplify(op_squared)
            
            # OP·AP = |OP|^2 - 22
            dot_product = sp.simplify(op_squared_simplified - 22)
            if dot_product not in dot_products:
                dot_products.append(dot_product)

dot_products = sorted([float(d) if isinstance(d, (int, float)) else float(d.evalf()) for d in dot_products if d is not None])
M = max(dot_products) if dot_products else None
m = min(dot_products) if dot_products else None

if M is not None and m is not None:
    result = M + m
    if abs(result - CANDIDATE) < 0.01:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')