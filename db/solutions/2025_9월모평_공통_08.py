from sympy import log, symbols, simplify, solve
import sympy as sp

a_val = 8
k_val = 3

# 검증: 두 수의 합과 곱
log2_a = log(a_val, 2)
loga_8 = log(8, a_val)

sum_val = log2_a + loga_8
prod_val = log2_a * loga_8

sum_val_simplified = simplify(sum_val)
prod_val_simplified = simplify(prod_val)

# 검증
verify = True
if abs(float(sum_val_simplified) - 4) > 1e-10:
    verify = False
if abs(float(prod_val_simplified) - k_val) > 1e-10:
    verify = False
if a_val <= 2:
    verify = False

if verify:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')