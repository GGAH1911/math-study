import sympy as sp
d = 4
a1 = -6 * d
sum_check = sum([1 / ((k-7)*d * (k-6)*d) for k in range(1, 6)])
expected = 5/96
print('VERIFY_PASS' if abs(sum_check - expected) < 1e-10 else 'VERIFY_FAIL')
abs_a6 = abs(a1 + 5*d)
a8 = a1 + 7*d
print('VERIFY_PASS' if abs_a6 == a8 else 'VERIFY_FAIL')
ans = sum([a1 + (k-1)*d for k in range(1, 16)])
print('VERIFY_PASS' if ans == 60 else 'VERIFY_FAIL')