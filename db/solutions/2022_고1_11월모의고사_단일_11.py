import sympy as sp
x = sp.Symbol('x')
k = -1
f = x**3 + (k+1)*x**2 + (4*k-3)*x + k + 7
roots = sp.solve(f, x)
roots_num = sorted([float(r) for r in roots])
alpha = roots_num[0]  # -3
beta = roots_num[2]   # 2 (or take any two non-1 roots)
non_one = [r for r in roots_num if abs(r - 1.0) > 1e-9]
result = abs(non_one[0] - non_one[1])
all_distinct = len(set(roots_num)) == 3
check1 = abs(float(f.subs(x, 1))) < 1e-9
check2 = all(abs(float(f.subs(x, r))) < 1e-9 for r in roots_num)
if all_distinct and check1 and check2 and abs(result - 5.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')