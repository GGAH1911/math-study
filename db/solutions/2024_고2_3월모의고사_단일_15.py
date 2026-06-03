import sympy as sp

z = sp.Symbol('z')
valid_k = []

for k in [-4, 2, 4, -1, 1, 0, -2, 3]:  # 충분한 후보 검사
    c_lin = k**2 - 3*k - 4
    c_con = k**2 + 2*k - 8
    roots = sp.solve(z**2 + c_lin*z + c_con, z)
    for r in roots:
        # 조건 (가): conjugate(z) == -z  <==>  실수부 == 0
        real_part = sp.re(r)
        if real_part == 0:
            valid_k.append(k)
            break

product = 1
for v in valid_k:
    product *= v

if set(valid_k) == {-4, 2, 4} and product == -32:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', valid_k, product)
